# SCHEDULED_TASKS.md - 定时任务

> **系统维护任务，定期执行，保持记忆系统健康。**

---

## 任务概览

| 任务 | 频率 | 下次执行 | 状态文件 |
|------|------|---------|---------|
| 知识复利 | 每 3-5 天 | `heartbeat-state.json` → `lastChecks.compounding` |
| 记忆衰减 | 每周 | `heartbeat-state.json` → `lastChecks.decay` |
| 核心记忆晋升 | 每月 | `heartbeat-state.json` → `lastChecks.promotion` |

---

## 任务 1：知识复利（每 3-5 天）

**目的**：提炼日常日志，更新长期记忆

**判断条件**：
```
今天 - lastChecks.compounding >= 3
```

**执行流程**：
1. 读取 `memory/YYYY-MM-DD.md`（最近 7 天）
2. 识别重要内容：
   - 决策（P0/P1）
   - 踩坑和纠正
   - 关键进展
3. 提炼核心洞察
4. 更新 `MEMORY.md` 对应章节
5. 在提炼过的日志末尾添加：`<!-- compounded: YYYY-MM-DD -->`
6. 更新 `heartbeat-state.json`：
   ```json
   {
     "lastChecks": {
       "compounding": "2026-03-29"
     }
   }
   ```

**输出格式**：
```
📚 知识复利完成 [时间]

处理日志：{数量} 个
提炼洞察：{数量} 条
更新章节：{MEMORY.md 章节}
```

---

## 任务 2：记忆衰减（每周）

**目的**：归档长期未访问的 P2 记忆

**判断条件**：
```
今天 - lastChecks.decay >= 7
```

**执行流程**：
1. 扫描 `MEMORY.md` 中的 P2 记忆
2. 识别超过 30 天未访问的内容
3. 标记为 `#archive`
4. 移动到 `## 📦 已归档` 章节
5. 更新 `heartbeat-state.json`：
   ```json
   {
     "lastChecks": {
       "decay": "2026-03-29"
     }
   }
   ```

**输出格式**：
```
📉 记忆衰减完成 [时间]

扫描记忆：{数量} 条
归档记忆：{数量} 条
归档列表：{摘要}
```

---

## 任务 3：核心记忆晋升（每月）

**目的**：识别反复出现的 P1 记忆，考虑晋升为 P0

**判断条件**：
```
今天 - lastChecks.promotion >= 30
```

**执行流程**：
1. 检查 P1 记忆是否有反复出现 3+ 次的主题
2. 如果有 → 记录到 `memory/promotion-candidates.md`
3. 下次对话时提醒 Steven 确认
4. 更新 `heartbeat-state.json`：
   ```json
   {
     "lastChecks": {
       "promotion": "2026-03-29"
     }
   }
   ```

**输出格式**：
```
⬆️ 核心记忆晋升检查完成 [时间]

P1 记忆：{数量} 条
晋升候选：{数量} 条
候选列表：{摘要}

⏳ 待 Steven 确认后晋升
```

---

## 时间判断

- **安静时段**（23:00-08:00）：跳过定时任务
- **活跃时段**：正常执行

---

## 手动触发

Steven 可以通过以下命令手动触发：
- `/compound` - 手动触发知识复利
- `/decay` - 手动触发记忆衰减
- `/promote` - 手动触发核心记忆晋升

---

## 与其他系统的关系

```
定时任务（SCHEDULED_TASKS.md）
  ├── 维护记忆系统健康
  ├── 不依赖心跳触发
  └── 独立的 cron 任务

心跳检查（HEARTBEAT.md）
  └── 只检查状态，不执行定时任务

自由探索（FREE_EXPLORATION.md）
  └── 好奇心驱动的研究，与维护任务无关
```

---

## 更新记录

| 日期 | 变更 |
|------|------|
| 2026-03-29 | 从 HEARTBEAT.md 分离，创建独立文档 |
