# 多 Agent 和多 Gateway 架构分析

> 日期：2026-02-28
> 来源：Steven 分享的文章 + 官方文档
> 目标：提高单台宿主机的效率和可靠性

---

## 一、架构概述

### 文章描述的架构

```
┌─────────────────────────────────────────┐
│           宿主机（同一台服务器）           │
├─────────────────────────────────────────┤
│                                         │
│  ┌────────────────────┐                 │
│  │   主 Gateway       │                 │
│  │   (Port: 18789)    │                 │
│  └────────┬───────────┘                 │
│           │                             │
│     ┌─────┴─────┬─────────┬────────┐   │
│     ▼           ▼         ▼        ▼   │
│  Agent 1    Agent 2   Agent 3  Agent 4 │
│  (内容)     (热点)    (股票)   (其他)   │
│                                         │
│  ┌────────────────────┐                 │
│  │   医生 Gateway     │                 │
│  │   (Port: 19789)    │                 │
│  │   专职：修复主群    │                 │
│  └────────────────────┘                 │
└─────────────────────────────────────────┘
```

### 核心价值

1. **隔离性**：每个 agent 独立 workspace，互不污染
2. **容错性**：主 gateway 挂了，医生 gateway 可以修复
3. **高效性**：多 agent 并行，充分利用单机资源

---

## 二、本机现状分析

### 当前配置

```json
{
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "loopback"
  },
  "agents": {
    "list": [
      { "id": "main" },
      { 
        "id": "helper",
        "workspace": "/Users/caidengyong/.openclaw/workspace-helper",
        "agentDir": "/Users/caidengyong/.openclaw/agents/helper/agent"
      }
    ]
  }
}
```

### 问题

- ✅ 已有两个 agent（main + helper）
- ❌ **但都在同一个 gateway 下**（端口 18789）
- ❌ 如果 gateway 挂了，两个 agent 一起躺平

### 结论

**当前是"多 agent 单 gateway"架构，缺医生 gateway**

---

## 三、官方文档确认

### 多 Gateway 要求（必须满足）

| 配置项 | 主 Gateway | 医生 Gateway |
|--------|-----------|-------------|
| `gateway.port` | 18789 | 19789（+1000 避免冲突）|
| `OPENCLAW_CONFIG_PATH` | `~/.openclaw/openclaw.json` | `~/.openclaw-rescue/openclaw.json` |
| `OPENCLAW_STATE_DIR` | `~/.openclaw/` | `~/.openclaw-rescue/` |
| `agents.defaults.workspace` | `~/.openclaw/workspace` | `~/.openclaw/workspace-rescue` |

### 推荐方式：使用 Profile

```bash
# 主 gateway（已有）
openclaw --profile main gateway --port 18789

# 医生 gateway（新建）
openclaw --profile rescue gateway --port 19789
```

### 端口分配规则

- Base port = `gateway.port`
- Browser control = base + 2
- CDP ports = base + 9 ~ base + 108
- **建议间隔 ≥ 20**，我们用 1000（18789 → 19789）完全安全

---

## 四、实施方案

### 方案 A：快速实施（推荐）

#### Step 1：创建医生 Gateway

```bash
# 使用 --profile rescue 自动隔离配置
openclaw --profile rescue onboard

# 按提示配置：
# - 使用同一个 LLM provider（zai/glm-5）
# - 不需要配置 channels（医生不接消息）
# - 设置端口为 19789
```

#### Step 2：安装医生服务

```bash
openclaw --profile rescue gateway install
```

#### Step 3：配置医生能力

医生 gateway 需要的能力：
- ✅ 读取主 gateway 的日志（`~/.openclaw/logs/`）
- ✅ 执行 `openclaw doctor` 命令
- ✅ 执行 `openclaw gateway restart`（主 gateway）
- ✅ 访问主 gateway 的配置文件（只读）

#### Step 4：测试修复流程

```bash
# 1. 启动两个 gateway
openclaw --profile main status      # 应该 running
openclaw --profile rescue status    # 应该 running

# 2. 模拟主 gateway 故障
# （手动破坏配置或停止服务）

# 3. 用医生 gateway 修复
openclaw --profile rescue doctor --target main

# 4. 验证主 gateway 恢复
openclaw --profile main status
```

---

### 方案 B：手动实施（更可控）

#### Step 1：创建独立配置文件

```bash
# 复制主配置
cp ~/.openclaw/openclaw.json ~/.openclaw-rescue/openclaw.json

# 编辑医生配置
nano ~/.openclaw-rescue/openclaw.json
```

修改以下字段：
```json
{
  "gateway": {
    "port": 19789  // 改为 19789
  },
  "agents": {
    "defaults": {
      "workspace": "/Users/caidengyong/.openclaw/workspace-rescue"  // 改为独立 workspace
    },
    "list": [
      {
        "id": "rescue",
        "name": "Gateway 医生",
        "role": "修复主 gateway 故障"
      }
    ]
  },
  "channels": {}  // 清空，医生不接消息
}
```

#### Step 2：创建独立 state 目录

```bash
mkdir -p ~/.openclaw-rescue
```

#### Step 3：启动医生 gateway

```bash
OPENCLAW_CONFIG_PATH=~/.openclaw-rescue/openclaw.json \
OPENCLAW_STATE_DIR=~/.openclaw-rescue \
openclaw gateway --port 19789
```

#### Step 4：安装服务

```bash
OPENCLAW_CONFIG_PATH=~/.openclaw-rescue/openclaw.json \
openclaw gateway install
```

---

## 五、医生 Gateway 能力设计

### 职责范围

1. **监控主 gateway 健康状态**
   - 定期 ping 主 gateway API
   - 检查主 gateway 日志中的错误

2. **自动修复常见问题**
   - `doctor fix` 修复配置错误
   - `gateway restart` 重启服务
   - 回滚到上一次正常配置

3. **升级护航**
   - 升级前备份配置
   - 升级后验证健康
   - 失败则自动回滚

### 限制（安全边界）

- ❌ 不能修改主 gateway 的 channels 配置
- ❌ 不能访问主 gateway 的 credentials
- ❌ 不能发送消息到外部（Discord/Telegram/飞书）
- ✅ 只能读取日志和执行修复命令

### 实现方式

**方法 1：Cron 定时任务**

```bash
# 在医生 gateway 中配置 cron
openclaw --profile rescue cron add \
  --name "health-check" \
  --schedule "*/5 * * * *" \
  --command "curl -f http://127.0.0.1:18789/health || openclaw --profile main doctor fix"
```

**方法 2：Agent 自主监控**

在医生 gateway 的 agent 中配置：
```markdown
# AGENTS.md（医生 workspace）

## 职责

你是 Gateway 医生，唯一职责是监控和修复主 gateway。

## 监控任务

每 5 分钟检查一次主 gateway：
1. 访问 http://127.0.0.1:18789/health
2. 如果失败，读取日志找出问题
3. 执行 `openclaw --profile main doctor fix`
4. 如果仍失败，通知 Steven（通过 Discord）
```

---

## 六、后续行动步骤

### 立即行动（今天）

1. ✅ **已完成**：阅读官方文档，确认多 gateway 可行性
2. ⏭️ **下一步**：使用方案 A 创建医生 gateway

```bash
# 执行这个命令开始
openclaw --profile rescue onboard
```

### 短期计划（本周）

1. 测试医生 gateway 的修复能力
2. 配置自动监控（cron 或 agent）
3. 记录常见问题和修复脚本

### 长期优化（未来）

1. **多 agent 扩展**：根据业务需要，在主 gateway 下添加更多专用 agent
   - 内容创作 agent
   - 数据分析 agent
   - 自动化运维 agent
2. **监控面板**：创建可视化面板显示所有 gateway/agent 状态
3. **灾备方案**：如果宿主机挂了怎么办？（跨机器部署）

---

## 七、风险评估

### 潜在问题

1. **端口冲突**
   - 解决：使用 19789（+1000），官方建议 ≥ 20 即可

2. **资源消耗**
   - 两个 gateway = 双倍内存？
   - 实际：医生 gateway 极简配置，不接消息，消耗很小

3. **权限问题**
   - 医生需要访问主的日志和配置
   - 解决：macOS 上同用户运行，权限自然继承

### 回退方案

如果医生 gateway 有问题：
```bash
# 停止医生
openclaw --profile rescue gateway stop

# 删除配置
rm -rf ~/.openclaw-rescue

# 回到单 gateway 模式
```

---

## 八、总结

### 核心洞察

1. **多 agent 单 gateway** 是当前状态，已有隔离（workspace），但缺容错
2. **医生 gateway** 是官方推荐的 rescue profile 应用
3. **实施成本低**：一条命令 `openclaw --profile rescue onboard` 即可开始

### 推荐路径

```
Day 1: 创建医生 gateway → 测试修复能力
Day 2-3: 配置自动监控 → 模拟故障演练
Week 2+: 扩展多 agent → 业务分仓隔离
```

### 下一步命令

```bash
# 开始创建医生 gateway
openclaw --profile rescue onboard
```

执行后会交互式引导配置，按提示操作即可。

---

## 附录：参考资料

- 官方文档：https://docs.openclaw.ai/gateway/multiple-gateways
- Gateway Runbook：https://docs.openclaw.ai/gateway
- 故障排除：https://docs.openclaw.ai/gateway/troubleshooting

---

*生成时间：2026-02-28*
*位置：~/.openclaw/workspace/docs/topics/gateway/multi-gateway-analysis.md*
