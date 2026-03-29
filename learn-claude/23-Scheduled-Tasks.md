# 23 - Run Prompts on a Schedule 学习笔记

**学习时间**：2026-03-14 16:30
**页面地址**：https://code.claude.com/docs/en/scheduled-tasks

---

## 📖 核心概念

### 是什么
**Scheduled tasks** 让 Claude 自动重复运行 prompt。用于轮询部署、看护 PR、检查长时间构建、或提醒稍后做某事。

### Prerequisites
- **Claude Code v2.1.72+**
- Check: `claude --version`

### Session-Scoped
**Tasks are session-scoped**:
- Live in current Claude Code process
- Gone when you exit

**For durable scheduling** (survives restarts, runs without active terminal):
- See **Desktop scheduled tasks**
- See **GitHub Actions**

---

## 🔄 Schedule a Recurring Prompt with /loop

### Bundled Skill
**`/loop`** is the quickest way to schedule recurring prompt.

**Syntax**: `/loop [interval] <prompt>`

**Example**:
```
/loop 5m check if the deployment finished and tell me what happened
```

**What happens**:
1. Claude parses interval
2. Converts to cron expression
3. Schedules job
4. Confirms cadence and job ID

### Interval Syntax

**Intervals are optional**. Can lead, trail, or omit entirely.

| Form | Example | Parsed Interval |
|------|---------|-----------------|
| **Leading token** | `/loop 30m check the build` | Every 30 minutes |
| **Trailing every clause** | `/loop check the build every 2 hours` | Every 2 hours |
| **No interval** | `/loop check the build` | Defaults to every 10 minutes |

**Supported units**:
- `s` for seconds
- `m` for minutes
- `h` for hours
- `d` for days

**Note**:
- Seconds rounded up to nearest minute (cron has one-minute granularity)
- Intervals that don't divide evenly (7m, 90m) are rounded to nearest clean interval
- Claude tells you what it picked

---

## 🔁 Loop Over Another Command

### Scheduled Prompt Can Be Command/Skill
**Useful for re-running workflow you've already packaged**.

**Example**:
```
/loop 20m /review-pr 1234
```

**Each time job fires**: Claude runs `/review-pr 1234` as if you had typed it.

---

## ⏰ Set a One-Time Reminder

### Natural Language Instead of /loop
**For one-shot reminders**, describe what you want in natural language.

**Claude schedules single-fire task** that deletes itself after running.

**Examples**:
```
remind me at 3pm to push the release branch
```

```
in 45 minutes, check whether the integration tests passed
```

**What happens**:
- Claude pins fire time to specific minute and hour using cron expression
- Confirms when it will fire

---

## 🛠️ Manage Scheduled Tasks

### Natural Language
**Ask Claude in natural language** to list or cancel tasks.

**Examples**:
```
what scheduled tasks do I have?
```

```
cancel the deploy check job
```

### Underlying Tools

| Tool | Purpose |
|------|---------|
| **CronCreate** | Schedule new task. Accepts 5-field cron expression, prompt to run, whether it recurs or fires once. |
| **CronList** | List all scheduled tasks with IDs, schedules, prompts. |
| **CronDelete** | Cancel task by ID. |

**Task ID**: Each scheduled task has **8-character ID** you can pass to `CronDelete`.

**Limit**: A session can hold up to **50 scheduled tasks** at once.

---

## ⚙️ How Scheduled Tasks Run

### Execution Model
**Scheduler checks every second** for due tasks and enqueues them at **low priority**.

**Scheduled prompt fires between your turns**, not while Claude is mid-response.

**If Claude is busy when task comes due**: Prompt waits until current turn ends.

### Timezone
**All times interpreted in your local timezone**.

**Example**: `0 9 * * *` means 9am wherever you're running Claude Code, not UTC.

---

## 🎲 Jitter

### Why Jitter?
**To avoid every session hitting API at same wall-clock moment**.

### Recurring Tasks
- Fire up to **10% of their period late**, capped at 15 minutes
- **Example**: Hourly job might fire anywhere from `:00` to `:06`

### One-Shot Tasks
- Scheduled for top or bottom of hour fire up to **90 seconds early**

### Deterministic Offset
**Offset derived from task ID** → same task always gets same offset.

**If exact timing matters**:
- Pick minute that is not `:00` or `:30`
- **Example**: `3 9 * * *` instead of `0 9 * * *`
- One-shot jitter will not apply

---

## ⏱️ Three-Day Expiry

### Auto-Expiry
**Recurring tasks automatically expire 3 days after creation**.

**What happens**:
1. Task fires one final time
2. Deletes itself

**Purpose**: Bounds how long a forgotten loop can run.

**If you need longer**:
- Cancel and recreate before expiry
- Use **Desktop scheduled tasks** for durable scheduling

---

## 📋 Cron Expression Reference

### Standard 5-Field Format
**CronCreate accepts standard 5-field cron expressions**:
```
minute hour day-of-month month day-of-week
```

### Supported Syntax
**All fields support**:
- Wildcards (`*`)
- Single values (`5`)
- Steps (`*/15`)
- Ranges (`1-5`)
- Comma-separated lists (`1,15,30`)

### Examples

| Example | Meaning |
|---------|---------|
| `*/5 * * * *` | Every 5 minutes |
| `0 * * * *` | Every hour on the hour |
| `7 * * * *` | Every hour at 7 minutes past |
| `0 9 * * *` | Every day at 9am local |
| `0 9 * * 1-5` | Weekdays at 9am local |
| `30 14 15 3 *` | March 15 at 2:30pm local |

### Day-of-Week
- `0` or `7` for Sunday
- `6` for Saturday

**NOT supported**:
- Extended syntax (`L`, `W`, `?`)
- Name aliases (`MON`, `JAN`)

### Day-of-Month AND Day-of-Week
**When both constrained**: Date matches if **either field matches**.

**Follows standard vixie-cron semantics**.

---

## 🚫 Disable Scheduled Tasks

### Environment Variable
**Set `CLAUDE_CODE_DISABLE_CRON=1`** to disable scheduler entirely.

**What happens**:
- Cron tools and `/loop` become unavailable
- Already-scheduled tasks stop firing

**See** [Environment variables](#environment-variables) for full list of disable flags.

---

## ⚠️ Limitations

### Session-Scoped Constraints

#### 1. Tasks Only Fire While Claude Code Running and Idle
**Closing terminal or letting session exit cancels everything**.

#### 2. No Catch-Up for Missed Fires
**If task's scheduled time passes while Claude busy on long-running request**:
- Fires **once** when Claude becomes idle
- **Not** once per missed interval

#### 3. No Persistence Across Restarts
**Restarting Claude Code clears all session-scoped tasks**.

### For Unattended Automation
**Use**:
- **GitHub Actions workflow** with schedule trigger
- **Desktop scheduled tasks** for graphical setup flow

---

## 💡 学习感悟

### 1. **/loop 是最简单的定时任务方式**
**Bundled skill** → 直接使用，无需配置。

**Interval 语法灵活**：
- Leading token: `/loop 30m check`
- Trailing every: `/loop check every 2 hours`
- No interval: Defaults to 10 minutes

**支持单位**: s, m, h, d

### 2. **Session-Scoped 是核心限制**
**Tasks live in current process**:
- ✅ Simple, no setup
- ❌ Gone when exit
- ❌ No persistence across restarts

**For durable scheduling** → Desktop scheduled tasks or GitHub Actions.

### 3. **One-Time Reminders 用自然语言**
**不需要 /loop**:
```
remind me at 3pm to push the release branch
```

**Claude schedules single-fire task** → deletes after running.

### 4. **Underlying Tools 是 CronCreate/List/Delete**
**Natural language → 这些工具**:
- `CronCreate`: Schedule task (5-field cron + prompt)
- `CronList`: List all tasks
- `CronDelete`: Cancel by ID

**Task ID**: 8-character ID
**Limit**: 50 tasks per session

### 5. **Jitter 避免同时冲击 API**
**Recurring tasks**: Up to 10% late (capped at 15 min)
**One-shot tasks**: Up to 90 seconds early (top/bottom of hour)

**Deterministic offset** → same task always same offset.

**Exact timing matters?** Pick non-:00/:30 minute.

### 6. **Three-Day Expiry 防止遗忘 Loop**
**Auto-expire after 3 days**:
- Fires one final time
- Deletes itself

**Need longer?** Cancel and recreate, or use Desktop scheduled tasks.

### 7. **Cron Expression 是标准 5-Field**
**Format**: `minute hour day-of-month month day-of-week`

**支持**:
- Wildcards (`*`)
- Single values (`5`)
- Steps (`*/15`)
- Ranges (`1-5`)
- Comma-separated (`1,15,30`)

**NOT supported**: `L`, `W`, `?`, `MON`, `JAN`

**Day-of-week**: 0 or 7 = Sunday, 6 = Saturday

**Both day-of-month and day-of-week constrained** → either field matches.

### 8. **Low Priority, Fires Between Turns**
**Scheduler checks every second**:
- Enqueues at low priority
- Fires between turns, not mid-response
- If busy → waits until current turn ends

### 9. **Timezone 是本地时区**
**All times in local timezone**, not UTC.

**Example**: `0 9 * * *` = 9am local.

### 10. **Disable via Environment Variable**
**`CLAUDE_CODE_DISABLE_CRON=1`**:
- Disables scheduler entirely
- Cron tools and `/loop` unavailable
- Already-scheduled tasks stop firing

---

## 🎯 实践建议

### 1. **Use /loop for Quick Polling**
```
/loop 5m check if the deployment finished
```

**Simple, session-scoped, good for short-term tasks**.

### 2. **Set One-Time Reminders in Natural Language**
```
remind me at 3pm to push the release branch
```

**Easier than /loop for one-shot**.

### 3. **Loop Over Commands/Skills**
```
/loop 20m /review-pr 1234
```

**Re-run packaged workflows**.

### 4. **Manage Tasks in Natural Language**
```
what scheduled tasks do I have?
cancel the deploy check job
```

**Easier than remembering tool names**.

### 5. **Pick Non-:00/:30 Minutes for Exact Timing**
**Avoid one-shot jitter**:
```
# Instead of 0 9 * * *
3 9 * * *
```

**Jitter won't apply**.

### 6. **Recreate Tasks Before 3-Day Expiry**
**Recurring tasks auto-expire**:
- Cancel and recreate before expiry
- Or use Desktop scheduled tasks

### 7. **Use Desktop/GitHub Actions for Durable Scheduling**
**Session-scoped limitations**:
- No persistence across restarts
- No catch-up for missed fires
- Only runs while session active

**For unattended automation** → Desktop or GitHub Actions.

### 8. **Check Version First**
```bash
claude --version
```

**Requires v2.1.72+**.

### 9. **Disable If Needed**
```bash
export CLAUDE_CODE_DISABLE_CRON=1
```

**Disables scheduler entirely**.

### 10. **Remember 50 Task Limit**
**Per session**: Up to 50 scheduled tasks.

**Check with**:
```
what scheduled tasks do I have?
```

---

## 📚 Use Cases

### 1. Poll Deployment Status
```
/loop 5m check if the deployment finished and tell me what happened
```

### 2. Babysit a PR
```
/loop 20m /review-pr 1234
```

### 3. Check Long-Running Build
```
/loop 10m check if the build finished
```

### 4. One-Time Reminder
```
remind me at 3pm to push the release branch
```

```
in 45 minutes, check whether the integration tests passed
```

### 5. Periodic Status Check
```
/loop 1h check system health
```

---

## 🔄 vs Desktop Scheduled Tasks vs GitHub Actions

| Feature | Session-Scoped (/loop) | Desktop Scheduled Tasks | GitHub Actions |
|---------|------------------------|-------------------------|----------------|
| **Setup** | Simple (natural language) | Graphical setup | YAML config |
| **Persistence** | Session-scoped (gone on exit) | Durable | Durable |
| **Requires Terminal** | Yes | No | No |
| **Catch-Up** | No | Yes | Yes |
| **Best for** | Quick polling, short-term | Recurring personal tasks | Unattended automation |

**Session-scoped** → Quick, simple, good for active session.
**Desktop/GitHub Actions** → Durable, unattended, long-term.

---

## 🏷️ 标签
`#scheduled-tasks` `#cron` `#/loop` `#reminders` `#polling` `#session-scoped` `#jitter` `#expiry` `#desktop-scheduled-tasks` `#github-actions`
