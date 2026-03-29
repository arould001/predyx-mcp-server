# Steven 新需求记录（2026-03-29）

## 每日早报关注的 AI 工具

**需求来源**：Steven（2026-03-29 22:30）

**需要持续关注的 AI 工具**：
1. **Claude Code**（Anthropic）
2. **Codex**（OpenAI）
3. **Cursor**（独立公司）
4. **Gemini**（Google）
5. **Google AI**（Google 的其他 AI 产品）
6. **GLM**（智谱 AI）
7. **Minimax**（中国 AI 公司）

**实施方式**：
- 每日早报使用 **Tavily Search** 搜索这些工具的最新动态
- 搜索策略：
  ```bash
  # 每个工具单独搜索（新闻 + 时间范围过滤）
  /Users/caidengyong/.openclaw/workspace/skills/liang-tavily-search/tavily "Claude Code" --topic news --time-range day
  /Users/caidengyong/.openclaw/workspace/skills/liang-tavily-search/tavily "OpenAI Codex" --topic news --time-range day
  /Users/caidengyong/.openclaw/workspace/skills/liang-tavily-search/tavily "Cursor AI" --topic news --time-range day
  /Users/caidengyong/.openclaw/workspace/skills/liang-tavily-search/tavily "Google Gemini" --topic news --time-range day
  /Users/caidengyong/.openclaw/workspace/skills/liang-tavily-search/tavily "Google AI" --topic news --time-range day
  /Users/caidengyong/.openclaw/workspace/skills/liang-tavily-search/tavily "智谱AI GLM" --topic news --time-range day
  /Users/caidengyong/.openclaw/workspace/skills/liang-tavily-search/tavily "Minimax AI" --topic news --time-range day
  ```

**过滤策略**：
- 只关注最近 24 小时（`--time-range day`）
- 只看新闻（`--topic news`）
- 重点关注：
  - 新功能发布
  - 重大更新
  - 行业动态
  - 技术突破

**记录位置**：
- 每日早报：Discord DM
- 记忆系统：`memory/YYYY-MM-DD.md`

**优先级**：P1（Steven 的持续需求）

**开始时间**：2026-03-30 早报开始实施
