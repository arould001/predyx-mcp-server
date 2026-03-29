#!/usr/bin/env node

const { spawn } = require('child_process');

// 启动 Chrome DevTools MCP server
const mcp = spawn('npx', ['-y', 'chrome-devtools-mcp@latest', '--browserUrl', 'http://127.0.0.1:9222'], {
  stdio: ['pipe', 'pipe', 'pipe']
});

let buffer = '';

mcp.stdout.on('data', (data) => {
  buffer += data.toString();
  console.log('STDOUT:', data.toString());
  
  // 尝试解析 JSON-RPC 消息
  const lines = buffer.split('\n');
  buffer = lines.pop(); // 保留未完成的行
  
  lines.forEach(line => {
    if (line.trim()) {
      try {
        const msg = JSON.parse(line);
        console.log('Parsed message:', JSON.stringify(msg, null, 2));
      } catch (e) {
        // 不是 JSON，可能是其他输出
      }
    }
  });
});

mcp.stderr.on('data', (data) => {
  console.error('STDERR:', data.toString());
});

mcp.on('close', (code) => {
  console.log(`MCP server exited with code ${code}`);
});

// 发送初始化请求
setTimeout(() => {
  const initRequest = {
    jsonrpc: '2.0',
    id: 1,
    method: 'initialize',
    params: {
      protocolVersion: '2024-11-05',
      capabilities: {},
      clientInfo: {
        name: 'test-client',
        version: '1.0.0'
      }
    }
  };
  
  console.log('Sending initialize request...');
  mcp.stdin.write(JSON.stringify(initRequest) + '\n');
}, 2000);

// 10 秒后退出
setTimeout(() => {
  console.log('Test completed, exiting...');
  mcp.kill();
  process.exit(0);
}, 10000);
