// Twitter Bookmarks 抓取脚本
// 在浏览器控制台中运行

(async function() {
  const bookmarks = [];
  const maxBookmarks = 50;
  
  // 滚动加载更多内容
  async function scrollToLoad() {
    const scrollHeight = document.documentElement.scrollHeight;
    window.scrollTo(0, scrollHeight);
    await new Promise(resolve => setTimeout(resolve, 2000)); // 等待加载
  }
  
  // 提取单条 tweet 信息
  function extractTweet(article) {
    try {
      const authorLink = article.querySelector('a[href^="/"]');
      const authorName = article.querySelector('[data-testid="User-Name"]')?.textContent || '';
      const authorHandle = authorLink?.href.split('/').pop() || '';
      
      const tweetText = article.querySelector('[data-testid="tweetText"]')?.textContent || '';
      const tweetLink = article.querySelector('a[href*="/status/"]')?.href || '';
      const timeElement = article.querySelector('time');
      const date = timeElement?.getAttribute('datetime') || '';
      
      // 检测是否是敏感内容（成人内容相关关键词）
      const sensitiveKeywords = ['nsfw', '18+', 'adult', 'porn', 'nude', '性感', '福利'];
      const isSensitive = sensitiveKeywords.some(keyword => 
        tweetText.toLowerCase().includes(keyword.toLowerCase())
      );
      
      return {
        authorName: authorName.split('Verified')[0].trim(),
        authorHandle: '@' + authorHandle,
        content: tweetText,
        url: tweetLink,
        date: date,
        isSensitive: isSensitive
      };
    } catch (error) {
      return null;
    }
  }
  
  // 主抓取逻辑
  let attempts = 0;
  const maxAttempts = 10;
  
  while (bookmarks.length < maxBookmarks && attempts < maxAttempts) {
    const articles = document.querySelectorAll('article[data-testid="tweet"]');
    
    for (const article of articles) {
      const tweet = extractTweet(article);
      if (tweet && !tweet.isSensitive && !bookmarks.find(b => b.url === tweet.url)) {
        bookmarks.push(tweet);
        if (bookmarks.length >= maxBookmarks) break;
      }
    }
    
    if (bookmarks.length < maxBookmarks) {
      await scrollToLoad();
      attempts++;
    }
  }
  
  console.log('抓取完成！');
  console.log(`共抓取 ${bookmarks.length} 条收藏（已过滤敏感内容）`);
  console.log(JSON.stringify(bookmarks, null, 2));
  
  // 下载为 JSON 文件
  const blob = new Blob([JSON.stringify(bookmarks, null, 2)], {type: 'application/json'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'twitter-bookmarks-raw.json';
  a.click();
  URL.revokeObjectURL(url);
  
  return bookmarks;
})();
