# NostrRAG 测试计划（无需 NWC）

**创建时间**: 2026-03-27 14:47 PM
**重大发现**: NostrRAG 可以在只读模式下运行，不需要 NWC connection string！

---

## 🎯 核心发现

### 1. NostrRAG 不需要 NWC！
- **关键发现**: NostrRAG 可以在只读模式下运行
- **只需要**:
  - ✅ `NOSTR_RELAYS`（relay 列表）
  - ✅ `LLM_API_KEY`（LLM 的 API key）
  - ✅ `LLM_BASE_URL`（可选）
  - ✅ `LLM_MODEL_NAME`（可选）

### 2. 工作原理
```python
# 简单用法
from agentstr import NostrRAG
from langchain_openai import ChatOpenAI

rag = NostrRAG(
    relays=["wss://relay.damus.io"],
    llm=ChatOpenAI(model_name="gpt-3.5-turbo")
)

# 查询
answer = await rag.query(
    question="What's new with Bitcoin?",
    limit=8
)
```

### 3. 核心方法
- `build_knowledge_base(question, limit)` - 从 Nostr 构建知识库
- `retrieve(question, limit)` - 从知识库检索文档
- `query(question, limit)` - 完整流程（构建 + 检索 + 生成答案）

### 4. 查询类型
- `"hashtags"` - 通过标签查询（默认）
- `"authors"` - 通过作者查询

---

## 📋 测试计划

### 阶段 1: 环境准备（5 分钟）

#### 1.1 安装依赖
```bash
pip install "agentstr-sdk[rag]"
pip install langchain-openai
```

#### 1.2 配置环境变量
创建 `.env` 文件：
```bash
# Nostr Relays
NOSTR_RELAYS=wss://relay.damus.io,wss://nostr.wine,wss://relay.nostr.band

# LLM 配置（使用 OpenAI）
LLM_API_KEY=your_openai_api_key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL_NAME=gpt-3.5-turbo
```

**注意**: 如果没有 OpenAI API key，可以：
- 使用其他 LLM provider（如 Claude、Gemini）
- 使用免费的 LLM API（如 Ollama）

---

### 阶段 2: 基础测试（10 分钟）

#### 2.1 测试 1: Bitcoin 相关查询
```python
import asyncio
from agentstr import NostrRAG
from langchain_openai import ChatOpenAI

async def test_bitcoin_query():
    # 初始化 NostrRAG
    rag = NostrRAG(
        relays=["wss://relay.damus.io"],
        llm=ChatOpenAI(model_name="gpt-3.5-turbo")
    )
    
    # 查询 Bitcoin 相关内容
    question = "What's the latest discussion about Bitcoin price prediction?"
    answer = await rag.query(question, limit=10)
    
    print(f"Question: {question}")
    print(f"Answer: {answer}")
    
    return answer

asyncio.run(test_bitcoin_query())
```

**预期结果**:
- ✅ 从 Nostr 网络获取 Bitcoin 相关帖子
- ✅ 构建临时知识库
- ✅ 生成基于社区讨论的回答

#### 2.2 测试 2: Predyx 市场查询
```python
async def test_predyx_query():
    rag = NostrRAG(
        relays=["wss://relay.damus.io"],
        llm=ChatOpenAI(model_name="gpt-3.5-turbo")
    )
    
    question = "What are people saying about Predyx prediction markets?"
    answer = await rag.query(question, limit=10)
    
    print(f"Question: {question}")
    print(f"Answer: {answer}")

asyncio.run(test_predyx_query())
```

#### 2.3 测试 3: AI 趋势查询
```python
async def test_ai_trends():
    rag = NostrRAG(
        relays=["wss://relay.damus.io"],
        llm=ChatOpenAI(model_name="gpt-3.5-turbo")
    )
    
    question = "What are the latest AI trends discussed on Nostr?"
    answer = await rag.query(question, limit=10)
    
    print(f"Question: {question}")
    print(f"Answer: {answer}")

asyncio.run(test_ai_trends())
```

---

### 阶段 3: 高级测试（15 分钟）

#### 3.1 测试 4: 知识库构建
```python
async def test_knowledge_base():
    rag = NostrRAG(
        relays=["wss://relay.damus.io"],
        llm=ChatOpenAI(model_name="gpt-3.5-turbo")
    )
    
    # 手动构建知识库
    question = "Bitcoin halving 2024"
    events = await rag.build_knowledge_base(question, limit=20)
    
    print(f"Retrieved {len(events)} events")
    
    # 检索相关文档
    docs = await rag.retrieve(question, limit=5)
    
    print(f"Retrieved {len(docs)} documents")
    
    # 生成答案
    answer = await rag.query(question, limit=5)
    
    print(f"Answer: {answer}")

asyncio.run(test_knowledge_base())
```

#### 3.2 测试 5: 作者查询
```python
async def test_author_query():
    rag = NostrRAG(
        relays=["wss://relay.damus.io"],
        llm=ChatOpenAI(model_name="gpt-3.5-turbo")
    )
    
    # 通过作者查询（需要知道作者 pubkey）
    question = "What does this author think about Lightning Network?"
    answer = await rag.query(
        question,
        limit=10,
        query_type="authors"
    )
    
    print(f"Answer: {answer}")

asyncio.run(test_author_query())
```

---

### 阶段 4: 集成测试（20 分钟）

#### 4.1 创建 NostrRAG 测试脚本
创建 `test_nostrrag.py`:
```python
#!/usr/bin/env python3
"""
NostrRAG 测试脚本
测试从 Nostr 网络获取实时信息的能力
"""

import asyncio
import os
from agentstr import NostrRAG
from langchain_openai import ChatOpenAI

class NostrRAGTester:
    def __init__(self):
        # 从环境变量读取配置
        self.relays = os.getenv("NOSTR_RELAYS", "wss://relay.damus.io").split(",")
        self.llm_api_key = os.getenv("LLM_API_KEY")
        self.llm_base_url = os.getenv("LLM_BASE_URL")
        self.llm_model_name = os.getenv("LLM_MODEL_NAME", "gpt-3.5-turbo")
        
        # 初始化 NostrRAG
        self.rag = NostrRAG(
            relays=self.relays,
            llm=ChatOpenAI(
                model_name=self.llm_model_name,
                openai_api_key=self.llm_api_key,
                openai_api_base=self.llm_base_url
            )
        )
    
    async def test_query(self, question: str, limit: int = 10):
        """测试查询功能"""
        print(f"\n🔍 Testing query: {question}")
        print(f"   Limit: {limit}")
        
        try:
            answer = await self.rag.query(question, limit=limit)
            print(f"\n✅ Answer:\n{answer}\n")
            return answer
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            return None
    
    async def test_retrieve(self, question: str, limit: int = 5):
        """测试检索功能"""
        print(f"\n🔍 Testing retrieve: {question}")
        print(f"   Limit: {limit}")
        
        try:
            # 构建知识库
            events = await self.rag.build_knowledge_base(question, limit=limit * 2)
            print(f"\n✅ Retrieved {len(events)} events")
            
            # 检索文档
            docs = await self.rag.retrieve(question, limit=limit)
            print(f"\n✅ Retrieved {len(docs)} documents")
            
            for i, doc in enumerate(docs, 1):
                print(f"\n   Document {i}:")
                print(f"   {doc.page_content[:200]}...")
            
            return docs
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            return None

async def main():
    print("🚀 NostrRAG Testing Script")
    print("=" * 50)
    
    # 初始化测试器
    tester = NostrRAGTester()
    
    # 测试 1: Bitcoin 价格预测
    await tester.test_query(
        "What's the latest discussion about Bitcoin price prediction?",
        limit=10
    )
    
    # 测试 2: Predyx 市场
    await tester.test_query(
        "What are people saying about Predyx prediction markets?",
        limit=10
    )
    
    # 测试 3: AI 趋势
    await tester.test_query(
        "What are the latest AI trends discussed on Nostr?",
        limit=10
    )
    
    # 测试 4: 检索功能
    await tester.test_retrieve(
        "Bitcoin halving 2024",
        limit=5
    )
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")

if __name__ == "__main__":
    asyncio.run(main())
```

#### 4.2 运行测试
```bash
# 设置环境变量
export NOSTR_RELAYS="wss://relay.damus.io,wss://nostr.wine"
export LLM_API_KEY="your_api_key"
export LLM_BASE_URL="https://api.openai.com/v1"
export LLM_MODEL_NAME="gpt-3.5-turbo"

# 运行测试
python test_nostrrag.py
```

---

## 📊 成功标准

### 技术验证
- ✅ NostrRAG 成功连接到 Nostr relays
- ✅ 能够从 Nostr 网络获取帖子
- ✅ 能够构建临时知识库
- ✅ 能够检索相关文档
- ✅ 能够生成基于社区讨论的回答

### 数据质量
- ✅ 返回的内容与查询相关
- ✅ 包含社区讨论观点
- ✅ 可以提取情感倾向（看涨/看跌）

### 集成验证
- ✅ 可以集成到 enhanced_agent.py
- ✅ 可以自动解析返回数据
- ✅ 可以整合到 Agent 服务

---

## 🎯 下一步行动

### 立即可做（无需等待）
1. ✅ 创建 `.env` 文件（配置 LLM API key）
2. ✅ 安装依赖（`pip install "agentstr-sdk[rag]"`）
3. ✅ 创建测试脚本（`test_nostrrag.py`）
4. ✅ 运行基础测试（Bitcoin、Predyx、AI）

### 后续整合
1. 更新 `enhanced_agent.py`（集成 NostrRAG）
2. 更新 `predyx_tracker.py`（使用 NostrRAG 获取数据）
3. 创建完整的 Agent 服务（支持实时信息获取）

---

## 💡 关键洞察

### 1. NWC 不是必需的
- **误解**: 以为 NostrRAG 需要 NWC connection string
- **真相**: NostrRAG 可以在只读模式下运行
- **优势**: 可以立即开始测试，不需要等待 Steven

### 2. LLM API Key 是唯一的硬依赖
- **必需**: 一个 LLM API key（OpenAI、Claude、Gemini 等）
- **免费方案**: Ollama（本地 LLM，完全免费）
- **付费方案**: OpenAI API（$0.002/1K tokens）

### 3. 查询类型灵活
- **hashtags**: 通过标签查询（适合话题搜索）
- **authors**: 通过作者查询（适合跟踪特定用户）

---

## 📝 测试记录模板

### 测试 1: Bitcoin 价格预测
- **时间**: 待测试
- **查询**: "What's the latest discussion about Bitcoin price prediction?"
- **结果**: 待记录
- **质量**: 待评估

### 测试 2: Predyx 市场
- **时间**: 待测试
- **查询**: "What are people saying about Predyx prediction markets?"
- **结果**: 待记录
- **质量**: 待评估

### 测试 3: AI 趋势
- **时间**: 待测试
- **查询**: "What are the latest AI trends discussed on Nostr?"
- **结果**: 待记录
- **质量**: 待评估

---

**最后更新**: 2026-03-27 14:47 PM
**状态**: ✅ 测试计划完成，准备执行
**下次行动**: 安装依赖 + 运行测试
