#!/usr/bin/env node

const ChromeDevToolsMCP = require('./chrome-mcp-helper.js');

async function listAllTools() {
  const mcp = new ChromeDevToolsMCP();
  
  try {
    await mcp.start();
    
    console.log('\n📋 All available tools:\n');
    const tools = await mcp.listTools();
    
    tools.forEach((tool, index) => {
      console.log(`${index + 1}. ${tool.name}`);
      console.log(`   ${tool.description}`);
      if (tool.inputSchema && tool.inputSchema.properties) {
        const params = Object.keys(tool.inputSchema.properties);
        if (params.length > 0) {
          console.log(`   Parameters: ${params.join(', ')}`);
        }
      }
      console.log('');
    });
    
  } catch (err) {
    console.error('❌ Failed:', err.message);
  } finally {
    mcp.stop();
  }
}

listAllTools();
