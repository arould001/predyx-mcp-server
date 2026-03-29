#!/usr/bin/env node

/**
 * Chrome DevTools MCP Helper
 * 用于测试和使用 Chrome DevTools MCP 的简单工具
 */

const { spawn } = require('child_process');
const readline = require('readline');

class ChromeDevToolsMCP {
  constructor(browserUrl = 'http://127.0.0.1:9222') {
    this.browserUrl = browserUrl;
    this.mcp = null;
    this.requestId = 0;
    this.pendingRequests = new Map();
    this.buffer = '';
  }

  async start() {
    return new Promise((resolve, reject) => {
      console.log('Starting Chrome DevTools MCP...');
      
      this.mcp = spawn('npx', ['-y', 'chrome-devtools-mcp@latest', '--browserUrl', this.browserUrl, '--no-usage-statistics'], {
        stdio: ['pipe', 'pipe', 'pipe']
      });

      this.mcp.stdout.on('data', (data) => {
        this.handleData(data.toString());
      });

      this.mcp.stderr.on('data', (data) => {
        // 忽略警告信息
      });

      this.mcp.on('error', (err) => {
        reject(err);
      });

      // 初始化连接
      setTimeout(async () => {
        try {
          const result = await this.sendRequest('initialize', {
            protocolVersion: '2024-11-05',
            capabilities: {},
            clientInfo: {
              name: 'chrome-mcp-helper',
              version: '1.0.0'
            }
          });
          console.log('✅ MCP initialized:', result.serverInfo.title, result.serverInfo.version);
          resolve();
        } catch (err) {
          reject(err);
        }
      }, 1000);
    });
  }

  handleData(data) {
    this.buffer += data;
    const lines = this.buffer.split('\n');
    this.buffer = lines.pop();

    lines.forEach(line => {
      if (line.trim()) {
        try {
          const msg = JSON.parse(line);
          if (msg.id !== undefined && this.pendingRequests.has(msg.id)) {
            const { resolve, reject } = this.pendingRequests.get(msg.id);
            this.pendingRequests.delete(msg.id);
            if (msg.error) {
              reject(new Error(msg.error.message));
            } else {
              resolve(msg.result);
            }
          }
        } catch (e) {
          // 忽略非 JSON 行
        }
      }
    });
  }

  sendRequest(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = ++this.requestId;
      const request = {
        jsonrpc: '2.0',
        id,
        method,
        params
      };

      this.pendingRequests.set(id, { resolve, reject });
      this.mcp.stdin.write(JSON.stringify(request) + '\n');

      // 超时处理
      setTimeout(() => {
        if (this.pendingRequests.has(id)) {
          this.pendingRequests.delete(id);
          reject(new Error('Request timeout'));
        }
      }, 30000);
    });
  }

  async listTools() {
    const result = await this.sendRequest('tools/list');
    return result.tools;
  }

  async callTool(name, args = {}) {
    const result = await this.sendRequest('tools/call', {
      name,
      arguments: args
    });
    return result;
  }

  stop() {
    if (this.mcp) {
      this.mcp.kill();
    }
  }
}

// 测试函数
async function test() {
  const mcp = new ChromeDevToolsMCP();
  
  try {
    await mcp.start();
    
    console.log('\n📋 Listing available tools...');
    const tools = await mcp.listTools();
    console.log(`Found ${tools.length} tools:`);
    tools.slice(0, 10).forEach(tool => {
      console.log(`  - ${tool.name}: ${tool.description.substring(0, 60)}...`);
    });
    if (tools.length > 10) {
      console.log(`  ... and ${tools.length - 10} more`);
    }
    
    // 示例：导航到一个页面
    console.log('\n🌐 Testing navigation...');
    const navResult = await mcp.callTool('devtools_navigate', {
      url: 'https://example.com'
    });
    console.log('✅ Navigation successful');
    
    // 示例：获取页面标题
    console.log('\n📄 Getting page title...');
    const titleResult = await mcp.callTool('evaluate_script', {
      function: '() => document.title'
    });
    console.log('Page title:', titleResult.content[0].text);
    
    // 示例：截图
    console.log('\n📸 Taking screenshot...');
    const screenshotResult = await mcp.callTool('screenshot', {});
    if (screenshotResult.content && screenshotResult.content[0]) {
      console.log('✅ Screenshot taken (base64 length:', screenshotResult.content[0].data.length, ')');
    } else {
      console.log('Screenshot result:', JSON.stringify(screenshotResult, null, 2));
    }
    
    console.log('\n✅ All tests passed!');
    
  } catch (err) {
    console.error('❌ Test failed:', err.message);
  } finally {
    mcp.stop();
  }
}

// 如果直接运行，执行测试
if (require.main === module) {
  test();
}

module.exports = ChromeDevToolsMCP;
