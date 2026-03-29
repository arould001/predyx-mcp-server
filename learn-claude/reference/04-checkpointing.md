# Checkpointing

> **来源**: https://code.claude.com/docs/en/checkpointing
> **抓取时间**: 2026-03-14

Track, rewind, and summarize Claude's edits and conversation to manage session state.

---

## How Checkpoints Work

Claude Code automatically tracks Claude's file edits as you work, allowing you to quickly undo changes and rewind to previous states if anything gets off track.

### Automatic Tracking

Claude Code tracks all changes made by its file editing tools:
- **Every user prompt creates a new checkpoint**
- **Checkpoints persist across sessions**, so you can access them in resumed conversations
- **Automatically cleaned up** along with sessions after 30 days (configurable)

---

## Rewind and Summarize

Press `Esc` twice (`Esc + Esc`) or use the `/rewind` command to open the rewind menu. A scrollable list shows each of your prompts from the session. Select the point you want to act on, then choose an action:

1. **Restore code and conversation**: revert both code and conversation to that point
2. **Restore conversation**: rewind to that message while keeping current code
3. **Restore code**: revert file changes while keeping the conversation
4. **Summarize from here**: compress the conversation from this point forward into a summary, freeing context window space
5. **Never mind**: return to the message list without making changes

After restoring the conversation or summarizing, the original prompt from the selected message is restored into the input field so you can re-send or edit it.

---

## Restore vs. Summarize

The three restore options revert state: they undo code changes, conversation history, or both. "Summarize from here" works differently:

- **Messages before the selected message stay intact**
- **The selected message and all subsequent messages get replaced with a compact AI-generated summary**
- **No files on disk are changed**
- **The original messages are preserved in the session transcript**, so Claude can reference the details if needed

This is similar to `/compact`, but targeted: instead of summarizing the entire conversation, you keep early context in full detail and only compress the parts that are using up space. You can type optional instructions to guide what the summary focuses on.

**Summarize** keeps you in the same session and compresses context. If you want to branch off and try a different approach while preserving the original session intact, use **fork** instead (`claude --continue --fork-session`).

---

## Common Use Cases

Checkpoints are particularly useful when:
- **Exploring alternatives**: try different implementation approaches without losing your starting point
- **Recovering from mistakes**: quickly undo changes that introduced bugs or broke functionality
- **Iterating on features**: experiment with variations knowing you can revert to working states
- **Freeing context space**: summarize a verbose debugging session from the midpoint forward, keeping your initial instructions intact

---

## Limitations

### Bash Command Changes Not Tracked

Checkpointing does not track files modified by bash commands. For example, if Claude Code runs:

```bash
rm file.txt
mv old.txt new.txt
cp source.txt dest.txt
```

These file modifications **cannot be undone through rewind**. Only direct file edits made through Claude's file editing tools are tracked.

### External Changes Not Tracked

Checkpointing only tracks files that have been edited within the current session. Manual changes you make to files outside of Claude Code and edits from other concurrent sessions are normally not captured, unless they happen to modify the same files as the current session.

### Not a Replacement for Version Control

Checkpoints are designed for quick, session-level recovery. For permanent version history and collaboration:
- **Continue using version control** (ex. Git) for commits, branches, and long-term history
- **Checkpoints complement but don't replace proper version control**

Think of checkpoints as "local undo" and Git as "permanent history".

---

## Key Patterns

### 🔄 Quick Rewind

```
Esc + Esc  →  Select message  →  Restore code and conversation
```

### 📝 Targeted Summarize

```
/rewind  →  Select message  →  Summarize from here  →  Add instructions (optional)
```

### 🌿 Fork Session (Branch Approach)

```bash
claude --continue --fork-session
```

### 💡 When to Use What

| Scenario | Action |
|----------|--------|
| Made a mistake, want to go back | Restore code and conversation |
| Want to keep code, redo conversation | Restore conversation |
| Want to redo code, keep conversation | Restore code |
| Context window full | Summarize from here |
| Try different approach, preserve original | Fork session |

---

## See Also

- Interactive mode - Keyboard shortcuts and session controls
- Built-in commands - Accessing checkpoints using `/rewind`
- CLI reference - Command-line options
