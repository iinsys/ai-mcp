#!/usr/bin/env node
/**
 * Test Client for FileSystem Navigator MCP Server
 * 
 * This script demonstrates how to test the filesystem navigator MCP server
 * using Node.js and the MCP SDK.
 */

import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

async function testFilesystemNavigator() {
    console.log('🚀 Starting FileSystem Navigator MCP Server Test...\n');
    
    // Spawn the MCP server process
    const serverProcess = spawn(process.execPath, ['../dist/index.js'], {
        cwd: __dirname,
        env: {
            ...process.env,
            FS_ROOT_PATH: __dirname,
            FS_MAX_DEPTH: '5',
            FS_MAX_FILE_SIZE: '1048576',
            LOG_LEVEL: 'INFO'
        },
        stdio: ['pipe', 'pipe', 'inherit']
    });
    
    // Create transport and client
    const transport = new StdioClientTransport({
        command: process.execPath,
        args: ['../dist/index.js'],
        env: {
            FS_ROOT_PATH: __dirname,
            FS_MAX_DEPTH: '5',
            FS_MAX_FILE_SIZE: '1048576',
            LOG_LEVEL: 'INFO'
        }
    });
    
    const client = new Client({
        name: 'test-client',
        version: '1.0.0'
    }, {
        capabilities: {}
    });
    
    try {
        // Connect to the server
        await client.connect(transport);
        console.log('✅ Connected to MCP server!\n');
        
        // List available tools
        console.log('📋 Listing available tools...');
        const tools = await client.listTools();
        console.log(`Found ${tools.tools.length} tools:`);
        tools.tools.forEach(tool => {
            console.log(`  - ${tool.name}: ${tool.description}`);
        });
        console.log();
        
        // List available resources
        console.log('📚 Listing available resources...');
        const resources = await client.listResources();
        console.log(`Found ${resources.resources.length} resources:`);
        resources.resources.forEach(resource => {
            console.log(`  - ${resource.name}: ${resource.description}`);
        });
        console.log();
        
        // Test 1: Search for TypeScript files
        console.log('🔍 Test 1: Searching for TypeScript files...');
        try {
            const result = await client.callTool({
                name: 'search_files',
                arguments: {
                    pattern: '**/*.ts',
                    directory: '.',
                    maxResults: 5
                }
            });
            console.log('✅ Search result:', result.content[0].text);
        } catch (error) {
            console.log('❌ Search error:', error.message);
        }
        console.log();
        
        // Test 2: Read directory contents
        console.log('📁 Test 2: Reading directory contents...');
        try {
            const result = await client.callTool({
                name: 'read_directory',
                arguments: {
                    path: '.',
                    includeHidden: false
                }
            });
            console.log('✅ Directory contents:', result.content[0].text);
        } catch (error) {
            console.log('❌ Directory read error:', error.message);
        }
        console.log();
        
        // Test 3: Get file information
        console.log('📄 Test 3: Getting file information...');
        try {
            const result = await client.callTool({
                name: 'get_file_info',
                arguments: {
                    path: 'README.md'
                }
            });
            console.log('✅ File info:', result.content[0].text);
        } catch (error) {
            console.log('❌ File info error:', error.message);
        }
        console.log();
        
        // Test 4: Read file content
        console.log('📖 Test 4: Reading file content...');
        try {
            const result = await client.callTool({
                name: 'read_file_content',
                arguments: {
                    path: 'README.md',
                    encoding: 'utf8'
                }
            });
            console.log('✅ File content preview:', result.content[0].text.substring(0, 200) + '...');
        } catch (error) {
            console.log('❌ File read error:', error.message);
        }
        console.log();
        
        // Test 5: Test security - path traversal attempt
        console.log('🔒 Test 5: Testing security (path traversal)...');
        try {
            const result = await client.callTool({
                name: 'get_file_info',
                arguments: {
                    path: '../../../etc/passwd'
                }
            });
            console.log('✅ Security test result:', result.content[0].text);
        } catch (error) {
            console.log('❌ Security test error:', error.message);
        }
        console.log();
        
        // Test 6: Access file via resource URI
        console.log('🔗 Test 6: Accessing file via resource URI...');
        try {
            const result = await client.readResource({
                uri: 'file://README.md'
            });
            console.log('✅ Resource content preview:', result.contents[0].text.substring(0, 200) + '...');
        } catch (error) {
            console.log('❌ Resource access error:', error.message);
        }
        console.log();
        
        console.log('✅ All tests completed successfully!');
        
    } catch (error) {
        console.error('❌ Test failed:', error);
    } finally {
        // Clean up
        client.close();
        serverProcess.kill();
    }
}

// Run the test
testFilesystemNavigator().catch(console.error);
