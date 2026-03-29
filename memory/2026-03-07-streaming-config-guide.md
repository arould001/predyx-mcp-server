# OpenClaw 流式输出配置指南

> 踩坑时间：2026-03-07
> 踩坑人：Dia
> 目的：让消息逐步显示，像真人打字一样

---

## 一、正确配置

在 `openclaw.json` 的 `agents.defaults` 中添加：

```json
{
  "agents": {
    "defaults": {
      "blockStreamingDefault": "on",
      "blockStreamingBreak": "text_end",
      "blockStreamingChunk": {
        "minChars": 100,
        "maxChars": 500,
        "breakPreference": "paragraph"
      }
    }
  }
}
```

### 参数说明

| 参数 | 值 | 说明 |
|------|-----|------|
| `blockStreamingDefault` | `"on"` | 全局开启块流式 |
| `blockStreamingBreak` | `"text_end"` | 在文本结束时分割 |
| `blockStreamingChunk.minChars` | `100` | 每块最小 100 字符 |
| `blockStreamingChunk.maxChars` | `500` | 每块最大 500 字符 |
| `blockStreamingChunk.breakPreference` | `"paragraph"` | 优先在段落处分割 |

---

## 二、踩过的坑 ⚠️

### 坑 1：`blockStreamingChunk` 格式错误

**错误写法**（会导致服务挂掉）：
```json
"blockStreamingChunk": 500
```

**正确写法**（必须是对象）：
```json
"blockStreamingChunk": {
  "minChars": 100,
  "maxChars": 500,
  "breakPreference": "paragraph"
}
```

### 坑 2：配置后不重启

改完配置必须重启 gateway：
```bash
openclaw gateway restart
```

---

## 三、Discord 额外配置

Discord 通道还有自己的流式配置：

```json
{
  "channels": {
    "discord": {
      "blockStreaming": true,
      "streaming": "partial"
    }
  }
}
```

| 参数 | 值 | 说明 |
|------|-----|------|
| `blockStreaming` | `true` | Discord 启用块流式 |
| `streaming` | `"partial"` | 预览模式，消息实时更新 |

---

## 四、完整配置示例

```json
{
  "agents": {
    "defaults": {
      "blockStreamingDefault": "on",
      "blockStreamingBreak": "text_end",
      "blockStreamingChunk": {
        "minChars": 100,
        "maxChars": 500,
        "breakPreference": "paragraph"
      }
    }
  },
  "channels": {
    "discord": {
      "blockStreaming": true,
      "streaming": "partial"
    },
    "telegram": {
      "streaming": "off"
    }
  }
}
```

---

## 五、验证方法

1. 发一条长消息给 Agent
2. 观察消息显示方式：
   - ✅ **逐步出现** = 流式生效
   - ❌ **一次性全部出现** = 流式未生效

---

## 六、故障排查

如果配置后服务挂了：

1. 检查 `blockStreamingChunk` 是否是**对象**而不是数字
2. 检查 JSON 格式是否正确（逗号、引号）
3. 查看日志：`tail -50 /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log`

---

**总结一句话**：`blockStreamingChunk` 必须是对象 `{}`，不能是数字！

<!-- compounded: 2026-03-09 -->
