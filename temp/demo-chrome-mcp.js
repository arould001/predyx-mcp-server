#!/usr/bin/env node

/**
 * Chrome DevTools MCP 完整演示
 * 展示所有主要功能
 */

const ChromeDevToolsMCP = require('./chrome-mcp-helper.js');
const fs = require('fs');
const path = require('path');

async function demo() {
  const mcp = new ChromeDevToolsMCP();
  
  try {
    await mcp.start();
    
    // 1. 列出所有打开的页面
    console.log('\n📄 Step 1: List open pages');
    const pages = await mcp.callTool('list_pages', {});
    console.log(`Found ${pages.content[0].text.split('\n').length - 1} open pages`);
    console.log(pages.content[0].text.substring(0, 300) + '...\n');
    
    // 2. 创建新页面并导航
    console.log('🌐 Step 2: Create new page and navigate');
    const newPage = await mcp.callTool('new_page', {
      url: 'https://example.com',
      background: false
    });
    console.log('✅ New page created\n');
    
    // 3. 等待页面加载
    console.log('⏳ Step 3: Wait for page to load');
    await new Promise(resolve => setTimeout(resolve, 2000));
    console.log('✅ Page loaded\n');
    
    // 4. 获取页面快照（文本）
    console.log('📸 Step 4: Take text snapshot');
    const snapshot = await mcp.callTool('take_snapshot', {});
    console.log('Snapshot preview:');
    console.log(snapshot.content[0].text.substring(0, 500) + '...\n');
    
    // 5. 执行 JavaScript
    console.log('🔧 Step 5: Execute JavaScript');
    const titleResult = await mcp.callTool('evaluate_script', {
      function: '() => ({ title: document.title, url: window.location.href })'
    });
    console.log('Page info:', titleResult.content[0].text);
    
    const linksResult = await mcp.callTool('evaluate_script', {
      function: '() => Array.from(document.querySelectorAll("a")).slice(0, 5).map(a => a.href)'
    });
    console.log('First 5 links:', linksResult.content[0].text + '\n');
    
    // 6. 截图
    console.log('📸 Step 6: Take screenshot');
    const screenshot = await mcp.callTool('take_screenshot', {
      format: 'png'
    });
    
    if (screenshot.content && screenshot.content[0] && screenshot.content[0].data) {
      const screenshotPath = path.join(__dirname, 'screenshot.png');
      const buffer = Buffer.from(screenshot.content[0].data, 'base64');
      fs.writeFileSync(screenshotPath, buffer);
      console.log(`✅ Screenshot saved to: ${screenshotPath}`);
      console.log(`   Size: ${buffer.length} bytes\n`);
    }
    
    // 7. 查看网络请求
    console.log('🌐 Step 7: List network requests');
    const networkRequests = await mcp.callTool('list_network_requests', {
      pageSize: 5
    });
    console.log('Recent network requests:');
    console.log(networkRequests.content[0].text.substring(0, 400) + '...\n');
    
    // 8. 查看控制台消息
    console.log('💻 Step 8: List console messages');
    const consoleMessages = await mcp.callTool('list_console_messages', {
      pageSize: 5
    });
    console.log('Console messages:');
    console.log(consoleMessages.content[0].text || '(none)\n');
    
    // 9. 关闭页面
    console.log('🚪 Step 9: Close the page');
    const allPages = await mcp.callTool('list_pages', {});
    const pageLines = allPages.content[0].text.split('\n');
    if (pageLines.length > 2) {
      // 获取最后一个页面的 ID
      const lastPageLine = pageLines[pageLines.length - 2];
      const pageIdMatch = lastPageLine.match(/\[(\d+)\]/);
      if (pageIdMatch) {
        await mcp.callTool('close_page', { pageId: pageIdMatch[1] });
        console.log('✅ Page closed\n');
      }
    }
    
    console.log('✅ All demonstrations completed successfully!');
    console.log('\n📊 Summary:');
    console.log('  - Listed pages');
    console.log('  - Created new page');
    console.log('  - Navigated to URL');
    console.log('  - Took text snapshot');
    console.log('  - Executed JavaScript');
    console.log('  - Took screenshot');
    console.log('  - Listed network requests');
    console.log('  - Listed console messages');
    console.log('  - Closed page');
    
  } catch (err) {
    console.error('\n❌ Demo failed:', err.message);
    console.error(err.stack);
  } finally {
    mcp.stop();
  }
}

demo();
