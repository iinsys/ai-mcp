import { FileSystemServer } from '../src/server';
import * as fs from 'fs/promises';
import * as path from 'path';
import * as os from 'os';
import { it } from 'node:test';
import { it } from 'node:test';
import { describe } from 'node:test';
import { it } from 'node:test';
import { it } from 'node:test';
import { describe } from 'node:test';
import { it } from 'node:test';
import { it } from 'node:test';
import { describe } from 'node:test';
import { it } from 'node:test';
import { it } from 'node:test';
import { describe } from 'node:test';
import { it } from 'node:test';
import { it } from 'node:test';
import { describe } from 'node:test';
import { afterEach } from 'node:test';
import { beforeEach } from 'node:test';
import { describe } from 'node:test';

// Mock server class for testing
class MockServer {
  private toolHandlers = new Map<string, Function>();
  private resourceHandlers = new Map<string, Function>();

  setRequestHandler(schema: any, handler: Function) {
    if (schema.shape?.method?.value === 'tools/list') {
      this.toolHandlers.set('tools/list', handler);
    } else if (schema.shape?.method?.value === 'tools/call') {
      this.toolHandlers.set('tools/call', handler);
    } else if (schema.shape?.method?.value === 'resources/list') {
      this.resourceHandlers.set('resources/list', handler);
    } else if (schema.shape?.method?.value === 'resources/read') {
      this.resourceHandlers.set('resources/read', handler);
    }
  }

  async callTool(name: string, args: any) {
    const handler = this.toolHandlers.get('tools/call');
    if (!handler) {
      throw new Error('No tool handler found');
    }
    return await handler({
      method: 'tools/call',
      params: { name, arguments: args },
    });
  }

  async listTools() {
    const handler = this.toolHandlers.get('tools/list');
    if (!handler) {
      throw new Error('No tools/list handler found');
    }
    return await handler({ method: 'tools/list', params: {} });
  }
}

// Type definitions for test responses
interface ToolCallResponse {
  content: Array<{
    type: string;
    text: string;
  }>;
}

describe('FileSystemServer', () => {
  let server: MockServer;
  let fsServer: FileSystemServer;
  let tempDir: string;

  beforeEach(async () => {
    // Create a temporary directory for testing
    tempDir = await fs.mkdtemp(path.join(os.tmpdir(), 'fs-navigator-test-'));

    // Set up test environment
    process.env.FS_ROOT_PATH = tempDir;
    process.env.FS_MAX_DEPTH = '5';
    process.env.FS_MAX_FILE_SIZE = '1048576'; // 1MB

    server = new MockServer();
    fsServer = new FileSystemServer(server as any);
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
      const result = await server.callTool('search_files', {
        pattern: '**/*.ts',  // Use recursive pattern to find files in subdirectories
        directory: '.',
      }) as ToolCallResponse;

      expect(result.content).toBeDefined();
      expect(result.content[0].type).toBe('text');

      // Check if it's an error first
      if (result.content[0].text.startsWith('Error:')) {
        throw new Error(`Tool returned error: ${result.content[0].text}`);
      }

      const response = JSON.parse(result.content[0].text);
      expect(response.files).toHaveLength(2);
      expect(response.files.some((f: any) => f.name === 'index.ts')).toBe(true);
      expect(response.files.some((f: any) => f.name === 'test.spec.ts')).toBe(true);
    });

    it('should respect maxResults parameter', async () => {
      const result = await server.callTool('search_files', {
        pattern: '**/*.ts',  // Use recursive pattern
        directory: '.',
        maxResults: 1,
      }) as ToolCallResponse;

      // Check if it's an error first
      if (result.content[0].text.startsWith('Error:')) {
        throw new Error(`Tool returned error: ${result.content[0].text}`);
      }

      const response = JSON.parse(result.content[0].text);
      expect(response.returned).toBe(1);
      expect(response.totalFound).toBe(2);
    });
  });

  describe('read_directory tool', () => {
    it('should list directory contents', async () => {
      const result = await server.callTool('read_directory', {
        path: '.',
      }) as ToolCallResponse;

      const response = JSON.parse(result.content[0].text);
      expect(response.contents).toHaveLength(3); // src, tests, package.json

      const names = response.contents.map((item: any) => item.name);
      expect(names).toContain('src');
      expect(names).toContain('tests');
      expect(names).toContain('package.json');
    });

    it('should handle recursive listing', async () => {
      const result = await server.callTool('read_directory', {
        path: '.',
        recursive: true,
        maxDepth: 2,
      }) as ToolCallResponse;

      const response = JSON.parse(result.content[0].text);
      expect(response.contents.length).toBeGreaterThan(3);

      const paths = response.contents.map((item: any) => item.path);
      expect(paths.some((p: string) => p.includes('src/index.ts'))).toBe(true);
    });
  });

  describe('get_file_info tool', () => {
    it('should return file information', async () => {
      const result = await server.callTool('get_file_info', {
        path: 'package.json',
      }) as ToolCallResponse;

      const info = JSON.parse(result.content[0].text);
      expect(info.name).toBe('package.json');
      expect(info.isFile).toBe(true);
      expect(info.isDirectory).toBe(false);
      expect(info.size).toBeGreaterThan(0);
      expect(info.mimeType).toBe('application/json');
    });

    it('should return directory information', async () => {
      const result = await server.callTool('get_file_info', {
        path: 'src',
      }) as ToolCallResponse;

      const info = JSON.parse(result.content[0].text);
      expect(info.name).toBe('src');
      expect(info.isFile).toBe(false);
      expect(info.isDirectory).toBe(true);
    });
  });

  describe('read_file_content tool', () => {
    it('should read file content', async () => {
      const result = await server.callTool('read_file_content', {
        path: 'package.json',
      }) as ToolCallResponse;

      expect(result.content[0].text).toBe('{"name": "test"}');
    });

    it('should handle encoding parameter', async () => {
      const result = await server.callTool('read_file_content', {
        path: 'src/index.ts',
        encoding: 'utf8',
      }) as ToolCallResponse;

      expect(result.content[0].text).toBe('console.log("hello");');
    });
  });

  describe('security', () => {
    it('should prevent path traversal', async () => {
      const result = await server.callTool('get_file_info', {
        path: '../../../etc/passwd',
      }) as ToolCallResponse;

      expect(result.content[0].text).toContain('Access denied');
    });

    it('should respect file size limits', async () => {
      // Create a large file
      const largePath = path.join(tempDir, 'large.txt');
      await fs.writeFile(largePath, 'x'.repeat(2 * 1024 * 1024)); // 2MB

      const result = await server.callTool('read_file_content', {
        path: 'large.txt',
      }) as ToolCallResponse;

      expect(result.content[0].text).toContain('exceeds maximum allowed size');
    });
  });
});