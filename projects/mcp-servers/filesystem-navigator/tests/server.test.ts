import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { FileSystemServer } from '../src/server.js';
import * as fs from 'fs/promises';
import * as path from 'path';
import * as os from 'os';

describe('FileSystemServer', () => {
  let server: Server;
  let fsServer: FileSystemServer;
  let tempDir: string;

  beforeEach(async () => {
    // Create a temporary directory for testing
    tempDir = await fs.mkdtemp(path.join(os.tmpdir(), 'fs-navigator-test-'));
    
    // Set up test environment
    process.env.FS_ROOT_PATH = tempDir;
    process.env.FS_MAX_DEPTH = '5';
    process.env.FS_MAX_FILE_SIZE = '1048576'; // 1MB
    
    server = new Server(
      { name: 'test-server', version: '1.0.0' },
      { capabilities: { tools: {}, resources: {} } }
    );
    
    fsServer = new FileSystemServer(server);
    await fsServer.initialize();

    // Create test files and directories
    await fs.mkdir(path.join(tempDir, 'src'));
    await fs.mkdir(path.join(tempDir, 'tests'));
    await fs.writeFile(path.join(tempDir, 'package.json'), '{"name": "test"}');
    await fs.writeFile(path.join(tempDir, 'src', 'index.ts'), 'console.log("hello");');
    await fs.writeFile(path.join(tempDir, 'tests', 'test.spec.ts'), 'describe("test", () => {});');
  });

  afterEach(async () => {
    // Clean up temporary directory
    await fs.rm(tempDir, { recursive: true, force: true });
  });

  describe('search_files tool', () => {
    it('should find TypeScript files', async () => {
      const result = await server.request(
        {
          method: 'tools/call',
          params: {
            name: 'search_files',
            arguments: {
              pattern: '*.ts',
              directory: '.',
            },
          },
        },
        { meta: {} }
      );

      expect(result.content).toBeDefined();
      expect(result.content[0].type).toBe('text');
      
      const response = JSON.parse(result.content[0].text);
      expect(response.files).toHaveLength(2);
      expect(response.files.some((f: any) => f.name === 'index.ts')).toBe(true);
      expect(response.files.some((f: any) => f.name === 'test.spec.ts')).toBe(true);
    });

    it('should respect maxResults parameter', async () => {
      const result = await server.request(
        {
          method: 'tools/call',
          params: {
            name: 'search_files',
            arguments: {
              pattern: '*.ts',
              directory: '.',
              maxResults: 1,
            },
          },
        },
        { meta: {} }
      );

      const response = JSON.parse(result.content[0].text);
      expect(response.returned).toBe(1);
      expect(response.totalFound).toBe(2);
    });
  });

  describe('read_directory tool', () => {
    it('should list directory contents', async () => {
      const result = await server.request(
        {
          method: 'tools/call',
          params: {
            name: 'read_directory',
            arguments: {
              path: '.',
            },
          },
        },
        { meta: {} }
      );

      const response = JSON.parse(result.content[0].text);
      expect(response.contents).toHaveLength(3); // src, tests, package.json
      
      const names = response.contents.map((item: any) => item.name);
      expect(names).toContain('src');
      expect(names).toContain('tests');
      expect(names).toContain('package.json');
    });

    it('should handle recursive listing', async () => {
      const result = await server.request(
        {
          method: 'tools/call',
          params: {
            name: 'read_directory',
            arguments: {
              path: '.',
              recursive: true,
              maxDepth: 2,
            },
          },
        },
        { meta: {} }
      );

      const response = JSON.parse(result.content[0].text);
      expect(response.contents.length).toBeGreaterThan(3);
      
      const paths = response.contents.map((item: any) => item.path);
      expect(paths.some((p: string) => p.includes('src/index.ts'))).toBe(true);
    });
  });

  describe('get_file_info tool', () => {
    it('should return file information', async () => {
      const result = await server.request(
        {
          method: 'tools/call',
          params: {
            name: 'get_file_info',
            arguments: {
              path: 'package.json',
            },
          },
        },
        { meta: {} }
      );

      const info = JSON.parse(result.content[0].text);
      expect(info.name).toBe('package.json');
      expect(info.isFile).toBe(true);
      expect(info.isDirectory).toBe(false);
      expect(info.size).toBeGreaterThan(0);
      expect(info.mimeType).toBe('application/json');
    });

    it('should return directory information', async () => {
      const result = await server.request(
        {
          method: 'tools/call',
          params: {
            name: 'get_file_info',
            arguments: {
              path: 'src',
            },
          },
        },
        { meta: {} }
      );

      const info = JSON.parse(result.content[0].text);
      expect(info.name).toBe('src');
      expect(info.isFile).toBe(false);
      expect(info.isDirectory).toBe(true);
    });
  });

  describe('read_file_content tool', () => {
    it('should read file content', async () => {
      const result = await server.request(
        {
          method: 'tools/call',
          params: {
            name: 'read_file_content',
            arguments: {
              path: 'package.json',
            },
          },
        },
        { meta: {} }
      );

      expect(result.content[0].text).toBe('{"name": "test"}');
    });

    it('should handle encoding parameter', async () => {
      const result = await server.request(
        {
          method: 'tools/call',
          params: {
            name: 'read_file_content',
            arguments: {
              path: 'src/index.ts',
              encoding: 'utf8',
            },
          },
        },
        { meta: {} }
      );

      expect(result.content[0].text).toBe('console.log("hello");');
    });
  });

  describe('security', () => {
    it('should prevent path traversal', async () => {
      const result = await server.request(
        {
          method: 'tools/call',
          params: {
            name: 'get_file_info',
            arguments: {
              path: '../../../etc/passwd',
            },
          },
        },
        { meta: {} }
      );

      expect(result.content[0].text).toContain('Access denied');
    });

    it('should respect file size limits', async () => {
      // Create a large file
      const largePath = path.join(tempDir, 'large.txt');
      await fs.writeFile(largePath, 'x'.repeat(2 * 1024 * 1024)); // 2MB

      const result = await server.request(
        {
          method: 'tools/call',
          params: {
            name: 'read_file_content',
            arguments: {
              path: 'large.txt',
            },
          },
        },
        { meta: {} }
      );

      expect(result.content[0].text).toContain('exceeds maximum allowed size');
    });
  });
});