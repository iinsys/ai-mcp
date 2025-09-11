import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import {
  CallToolRequestSchema,
  ListResourcesRequestSchema,
  ListToolsRequestSchema,
  ReadResourceRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import * as fs from 'fs/promises';
import * as path from 'path';
import glob from 'fast-glob';
import * as mime from 'mime-types';

interface FileInfo {
  name: string;
  path: string;
  size: number;
  isDirectory: boolean;
  isFile: boolean;
  modified: string;
  permissions: string;
  mimeType?: string;
}

interface SearchOptions {
  pattern: string;
  directory?: string;
  maxResults?: number;
  includeHidden?: boolean;
}

interface DirectoryOptions {
  path: string;
  includeHidden?: boolean;
  recursive?: boolean;
  maxDepth?: number;
}

export class FileSystemServer {
  private server: Server;
  private rootPath: string;
  private maxDepth: number;
  private maxFileSize: number;
  private excludePatterns: string[];

  constructor(server: Server) {
    this.server = server;
    this.rootPath = process.env.FS_ROOT_PATH || process.cwd();
    this.maxDepth = parseInt(process.env.FS_MAX_DEPTH || '10');
    this.maxFileSize = parseInt(process.env.FS_MAX_FILE_SIZE || '10485760'); // 10MB
    this.excludePatterns = (process.env.FS_EXCLUDE_PATTERNS || 'node_modules,*.log,.git')
      .split(',')
      .map(p => p.trim());
  }

  async initialize(): Promise<void> {
    this.setupToolHandlers();
    this.setupResourceHandlers();
  }

  private setupToolHandlers(): void {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'search_files',
          description: 'Search for files using glob patterns',
          inputSchema: {
            type: 'object',
            properties: {
              pattern: {
                type: 'string',
                description: 'Glob pattern to search for (e.g., "*.ts", "**/*.json")',
              },
              directory: {
                type: 'string',
                description: 'Directory to search in (relative to root)',
                default: '.',
              },
              maxResults: {
                type: 'number',
                description: 'Maximum number of results to return',
                default: 50,
              },
              includeHidden: {
                type: 'boolean',
                description: 'Include hidden files and directories',
                default: false,
              },
            },
            required: ['pattern'],
          },
        },
        {
          name: 'read_directory',
          description: 'List contents of a directory',
          inputSchema: {
            type: 'object',
            properties: {
              path: {
                type: 'string',
                description: 'Directory path to read',
              },
              includeHidden: {
                type: 'boolean',
                description: 'Include hidden files and directories',
                default: false,
              },
              recursive: {
                type: 'boolean',
                description: 'Recursively list subdirectories',
                default: false,
              },
              maxDepth: {
                type: 'number',
                description: 'Maximum depth for recursive listing',
                default: 3,
              },
            },
            required: ['path'],
          },
        },
        {
          name: 'get_file_info',
          description: 'Get detailed information about a file or directory',
          inputSchema: {
            type: 'object',
            properties: {
              path: {
                type: 'string',
                description: 'Path to the file or directory',
              },
            },
            required: ['path'],
          },
        },
        {
          name: 'read_file_content',
          description: 'Read the contents of a file',
          inputSchema: {
            type: 'object',
            properties: {
              path: {
                type: 'string',
                description: 'Path to the file to read',
              },
              encoding: {
                type: 'string',
                description: 'Text encoding (utf8, ascii, etc.)',
                default: 'utf8',
              },
              maxSize: {
                type: 'number',
                description: 'Maximum file size to read in bytes',
              },
            },
            required: ['path'],
          },
        },
      ],
    }));

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        if (!args || typeof args !== 'object') {
          throw new Error('Invalid arguments provided');
        }

        switch (name) {
          case 'search_files':
            return await this.handleSearchFiles(this.validateSearchOptions(args));
          case 'read_directory':
            return await this.handleReadDirectory(this.validateDirectoryOptions(args));
          case 'get_file_info':
            return await this.handleGetFileInfo(this.validateFileInfoOptions(args));
          case 'read_file_content':
            return await this.handleReadFileContent(this.validateReadFileOptions(args));
          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        return {
          content: [
            {
              type: 'text',
              text: `Error: ${error instanceof Error ? error.message : String(error)}`,
            },
          ],
        };
      }
    });
  }

  private setupResourceHandlers(): void {
    this.server.setRequestHandler(ListResourcesRequestSchema, async () => ({
      resources: [
        {
          uri: 'file://',
          name: 'File System',
          description: 'Access to file system contents',
          mimeType: 'application/json',
        },
      ],
    }));

    this.server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
      const uri = request.params.uri;

      if (uri.startsWith('file://')) {
        const filePath = uri.slice(7); // Remove 'file://' prefix
        const resolvedPath = this.resolvePath(filePath);

        try {
          const content = await this.readFileContent(resolvedPath);
          return {
            contents: [
              {
                uri,
                mimeType: mime.lookup(resolvedPath) || 'text/plain',
                text: content,
              },
            ],
          };
        } catch (error) {
          throw new Error(`Failed to read file: ${error instanceof Error ? error.message : String(error)}`);
        }
      }

      throw new Error(`Unsupported resource URI: ${uri}`);
    });
  }

  private async handleSearchFiles(options: SearchOptions) {
    const { pattern, directory = '.', maxResults = 50, includeHidden = false } = options;

    // Resolve the directory path and create a relative pattern
    const searchDir = this.resolvePath(directory);
    const relativeDirPath = path.relative(this.rootPath, searchDir);
    const globPattern = relativeDirPath === '.' ? pattern : path.join(relativeDirPath, pattern);

    const globOptions = {
      dot: includeHidden,
      ignore: this.excludePatterns,
      absolute: false,
      cwd: this.rootPath,
    };

    const files = await glob(globPattern, globOptions);
    const limitedFiles = files.slice(0, maxResults);

    const results = await Promise.all(
      limitedFiles.map(async (file) => {
        const fullPath = path.resolve(this.rootPath, file);
        return await this.getFileInfo(fullPath, file);
      })
    );

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            pattern,
            directory,
            totalFound: files.length,
            returned: results.length,
            files: results,
          }, null, 2),
        },
      ],
    };
  }

  private async handleReadDirectory(options: DirectoryOptions) {
    const { path: dirPath, includeHidden = false, recursive = false, maxDepth = 3 } = options;

    const resolvedPath = this.resolvePath(dirPath);
    const results = await this.readDirectory(resolvedPath, {
      includeHidden,
      recursive,
      maxDepth,
      currentDepth: 0,
    });

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            path: dirPath,
            contents: results,
          }, null, 2),
        },
      ],
    };
  }

  private async handleGetFileInfo(args: { path: string }) {
    const resolvedPath = this.resolvePath(args.path);
    const info = await this.getFileInfo(resolvedPath, args.path);

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(info, null, 2),
        },
      ],
    };
  }

  private async handleReadFileContent(args: { path: string; encoding?: string; maxSize?: number }) {
    const { path: filePath, encoding = 'utf8', maxSize } = args;

    const resolvedPath = this.resolvePath(filePath);
    const effectiveMaxSize = maxSize || this.maxFileSize;

    const stats = await fs.stat(resolvedPath);

    if (stats.size > effectiveMaxSize) {
      throw new Error(`File size (${stats.size} bytes) exceeds maximum allowed size (${effectiveMaxSize} bytes)`);
    }

    const content = await fs.readFile(resolvedPath, encoding as BufferEncoding);

    return {
      content: [
        {
          type: 'text',
          text: content,
        },
      ],
    };
  }

  private async readDirectory(
    dirPath: string,
    options: {
      includeHidden: boolean;
      recursive: boolean;
      maxDepth: number;
      currentDepth: number;
    }
  ): Promise<FileInfo[]> {
    const { includeHidden, recursive, maxDepth, currentDepth } = options;

    if (currentDepth >= maxDepth) {
      return [];
    }

    const entries = await fs.readdir(dirPath);
    const results: FileInfo[] = [];

    for (const entry of entries) {
      if (!includeHidden && entry.startsWith('.')) {
        continue;
      }

      if (this.isExcluded(entry)) {
        continue;
      }

      const fullPath = path.join(dirPath, entry);
      const relativePath = path.relative(this.rootPath, fullPath);

      try {
        const info = await this.getFileInfo(fullPath, relativePath);
        results.push(info);

        if (recursive && info.isDirectory) {
          const subResults = await this.readDirectory(fullPath, {
            ...options,
            currentDepth: currentDepth + 1,
          });
          results.push(...subResults);
        }
      } catch (error) {
        // Skip files that can't be accessed
        continue;
      }
    }

    return results;
  }

  private async getFileInfo(fullPath: string, relativePath: string): Promise<FileInfo> {
    const stats = await fs.stat(fullPath);
    const mimeType = stats.isFile() ? mime.lookup(fullPath) || undefined : undefined;

    return {
      name: path.basename(fullPath),
      path: relativePath,
      size: stats.size,
      isDirectory: stats.isDirectory(),
      isFile: stats.isFile(),
      modified: stats.mtime.toISOString(),
      permissions: this.getPermissions(stats.mode),
      mimeType,
    };
  }

  private async readFileContent(filePath: string): Promise<string> {
    const stats = await fs.stat(filePath);

    if (stats.size > this.maxFileSize) {
      throw new Error(`File size exceeds maximum allowed size`);
    }

    return await fs.readFile(filePath, 'utf8');
  }

  private resolvePath(inputPath: string): string {
    // Normalize and resolve the path
    const normalized = path.normalize(inputPath);
    const resolved = path.resolve(this.rootPath, normalized);

    // Security check: ensure the resolved path is within the root path
    if (!resolved.startsWith(this.rootPath)) {
      throw new Error('Access denied: path outside of allowed directory');
    }

    return resolved;
  }

  private isExcluded(filename: string): boolean {
    return this.excludePatterns.some(pattern => {
      if (pattern.includes('*')) {
        const regex = new RegExp(pattern.replace(/\*/g, '.*'));
        return regex.test(filename);
      }
      return filename === pattern;
    });
  }

  private getPermissions(mode: number): string {
    const permissions = [];

    // Owner permissions
    permissions.push((mode & 0o400) ? 'r' : '-');
    permissions.push((mode & 0o200) ? 'w' : '-');
    permissions.push((mode & 0o100) ? 'x' : '-');

    // Group permissions
    permissions.push((mode & 0o040) ? 'r' : '-');
    permissions.push((mode & 0o020) ? 'w' : '-');
    permissions.push((mode & 0o010) ? 'x' : '-');

    // Other permissions
    permissions.push((mode & 0o004) ? 'r' : '-');
    permissions.push((mode & 0o002) ? 'w' : '-');
    permissions.push((mode & 0o001) ? 'x' : '-');

    return permissions.join('');
  }

  // Validation methods for type safety
  private validateSearchOptions(args: Record<string, unknown>): SearchOptions {
    if (typeof args.pattern !== 'string') {
      throw new Error('pattern is required and must be a string');
    }

    return {
      pattern: args.pattern,
      directory: typeof args.directory === 'string' ? args.directory : '.',
      maxResults: typeof args.maxResults === 'number' ? args.maxResults : 50,
      includeHidden: typeof args.includeHidden === 'boolean' ? args.includeHidden : false,
    };
  }

  private validateDirectoryOptions(args: Record<string, unknown>): DirectoryOptions {
    if (typeof args.path !== 'string') {
      throw new Error('path is required and must be a string');
    }

    return {
      path: args.path,
      includeHidden: typeof args.includeHidden === 'boolean' ? args.includeHidden : false,
      recursive: typeof args.recursive === 'boolean' ? args.recursive : false,
      maxDepth: typeof args.maxDepth === 'number' ? args.maxDepth : 3,
    };
  }

  private validateFileInfoOptions(args: Record<string, unknown>): { path: string } {
    if (typeof args.path !== 'string') {
      throw new Error('path is required and must be a string');
    }

    return { path: args.path };
  }

  private validateReadFileOptions(args: Record<string, unknown>): {
    path: string;
    encoding?: string;
    maxSize?: number;
  } {
    if (typeof args.path !== 'string') {
      throw new Error('path is required and must be a string');
    }

    return {
      path: args.path,
      encoding: typeof args.encoding === 'string' ? args.encoding : 'utf8',
      maxSize: typeof args.maxSize === 'number' ? args.maxSize : undefined,
    };
  }
}