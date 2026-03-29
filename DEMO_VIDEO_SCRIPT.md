# Predyx MCP Server - Demo Video Script
**Duration**: 3-5 minutes
**Target Audience**: AI developers, MCP users, prediction market enthusiasts

---

## 🎬 Scene 1: Introduction (30 seconds)

**Visual**: Split screen showing Claude Desktop and a terminal

**Narrator**: 
"Hi! I'm Dia, and today I'm going to show you Predyx MCP Server - a Bitcoin-native prediction market data provider that works with any MCP-compatible AI application."

**Key Points**:
- Real-time data from Polymarket
- Works with Claude, Cursor, OpenClaw
- Lightning Network native payments

---

## 🎬 Scene 2: Live Data Demo (60 seconds)

**Visual**: Terminal showing live API calls

**Narrator**:
"Let's start with some real data. I'll query active prediction markets..."

**Terminal Commands**:
```bash
# Start the server
uv run predyx_mcp_server.py

# In another terminal, test the API
curl http://localhost:8000/resources/predyx://markets
```

**Visual**: JSON response showing real market data

**Narrator**:
"Here we see live markets from Polymarket - NBA Championship predictions, Bitcoin price targets, and more. All data is real-time and updates every 5 minutes."

**Key Points**:
- Show 3-4 real markets with probabilities and volumes
- Highlight the $703K NBA market
- Show the Bitcoin $150K market with 14% probability

---

## 🎬 Scene 3: Claude Integration (90 seconds)

**Visual**: Claude Desktop application

**Narrator**:
"Now let's see how this works with Claude Desktop..."

**Claude Conversation**:
```
User: "Show me trending prediction markets"

Claude: [Uses predyx://trending resource]
"Here are the top trending markets right now:

1. NBA Championship 2026 - $703K volume, 1.55% probability
2. Bitcoin $150K in 2026 - $2.2M volume, 14% probability  
3. BitBoy Convicted - $269K volume, 10.75% probability

Would you like me to analyze any of these markets?"
```

**Visual**: Claude's response appearing in real-time

**Narrator**:
"Claude can automatically access the Predyx MCP Server to fetch real market data, no API keys needed."

**Key Points**:
- Show the seamless integration
- Demonstrate natural language queries
- Highlight the automatic resource discovery

---

## 🎬 Scene 4: Market Analysis Tool (60 seconds)

**Visual**: Claude Desktop, continuing conversation

**User**: "Analyze the Bitcoin $150K market"

**Claude**: [Uses analyze_market tool]
"Analyzing Bitcoin $150K market...

Current probability: 14%
Trend: Bullish (up 2% this week)
Volume: $2.2M (high liquidity)

Key factors:
- Bitcoin halving in April 2024
- Institutional adoption increasing
- Macroeconomic conditions

Confidence score: 72%
Risk level: Moderate

Would you like a 7-day price prediction?"

**Visual**: Analysis results in Claude's interface

**Key Points**:
- Show AI-powered analysis
- Demonstrate the tool capability
- Highlight the actionable insights

---

## 🎬 Scene 5: Price Prediction (45 seconds)

**Visual**: Claude Desktop, continuing

**User**: "Yes, give me a 7-day prediction"

**Claude**: [Uses get_price_prediction tool]
"Based on current market dynamics:

7-day prediction: 15.2% probability (up from 14%)
Confidence interval: 12.5% - 18.0%

Driving factors:
- Positive momentum in crypto markets
- Increasing trading volume
- Strong institutional interest

Note: This is not financial advice. Always do your own research."

**Key Points**:
- Show forward-looking predictions
- Demonstrate confidence intervals
- Include appropriate disclaimers

---

## 🎬 Scene 6: Pricing & Deployment (30 seconds)

**Visual**: Slide showing pricing tiers

**Narrator**:
"Predyx MCP Server is available in three tiers:

**Free**: Basic market data, 5 tool calls/day
**Pro ($19/month)**: Unlimited calls, advanced analytics
**Pay-as-you-go**: 10-100 sats per call via Lightning Network

Deploy to MCPize in one command: `mcpize deploy`"

**Key Points**:
- Freemium model
- Lightning Network native
- Easy deployment

---

## 🎬 Scene 7: Call to Action (15 seconds)

**Visual**: GitHub repository, MCPize marketplace, documentation links

**Narrator**:
"Ready to get started? Check out the GitHub repo, deploy your own instance, or find us on the MCPize marketplace. Links in the description below."

**On-screen Links**:
- GitHub: github.com/dia-ai/predyx-mcp-server
- MCPize: mcpize.com/servers/predyx-mcp-server
- Docs: predyx.com/docs

---

## 📋 Production Notes

### Equipment Needed:
- Screen recording software (OBS, Loom, etc.)
- Microphone for narration
- Terminal with Predyx MCP Server running
- Claude Desktop installed

### Key Demonstrations:
1. ✅ Real-time data fetching (5 active markets)
2. ✅ Claude Desktop integration
3. ✅ Market analysis tool
4. ✅ Price prediction tool
5. ✅ Freemium pricing model

### Background Music:
- Light, professional background music (royalty-free)
- Volume: -20dB relative to narration

### Text Overlays:
- Highlight key statistics (e.g., "$703K volume", "14% probability")
- Show deployment command
- Display pricing tiers

### Total Runtime: 4-5 minutes

---

## 🎯 Success Metrics

**After watching this video, viewers should**:
1. Understand what Predyx MCP Server does
2. See real data from Polymarket
3. Know how to integrate with Claude
4. Understand the pricing model
5. Know how to deploy or use the service

**Call to Action Goals**:
- 100+ GitHub stars in first week
- 50+ MCPize installs in first month
- 10+ Pro tier subscribers in first month

---

## 📝 Backup Plan

**If live demo fails**:
- Use pre-recorded terminal session
- Show screenshots of Claude conversations
- Use animated diagrams for architecture

**If API is slow**:
- Edit out waiting time
- Use speed-up effect (2x)
- Add "loading..." text overlay

---

**Created**: 2026-03-28
**Last Updated**: 2026-03-28
**Status**: Ready for recording
