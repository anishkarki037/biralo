---
name: memory
description: Save and retrieve memories. Use when user asks to remember something, recalls past conversations, or needs to store important information.
---

# Memory Skill

Save and retrieve information using the `memory` tool.

## When to Use

Use `memory` tool when:
- User says "remember this" or "don't forget"
- User asks "what did I tell you earlier"
- Important context should be stored
- User preferences should be recalled later
- Past decisions need to be referenced

## Actions

### Save Memory

```bash
memory(action="save", content="User prefers responses in English", category="user-preference", importance=3)
```

### Search Memory

```bash
memory(action="search", query="user preferences")
```

### List Recent Memories

```bash
memory(action="list", days=7)
```

### Read Long-term Memory

```bash
memory(action="longterm")
```

## Examples

**User: "Remember that I like Python best"**
```bash
memory(action="save", content="User prefers Python programming language", category="user-preference", importance=3)
```

**User: "What did I tell me about my preferences?"**
```bash
memory(action="search", query="preferences")
```

**User: "Don't forget to summarize before responding"**
```bash
memory(action="save", content="User wants summaries before detailed responses", category="user-preference", importance=4)
```

## Categories

Use appropriate categories:
- `user-preference` - User likes, dislikes, preferences
- `user-info` - Facts about the user (name, role, etc.)
- `project` - Project-related information
- `decision` - Important decisions made
- `learning` - Things the agent learned
- `general` - Default category

## Importance Levels

| Level | Description |
|-------|-------------|
| 1 | Minor information |
| 2 | Normal (default) |
| 3 | Important |
| 4 | Very important |
| 5 | Critical |

## Best Practices

1. **Save proactively** - When user asks to remember something
2. **Search before asking** - Check memory first
3. **Use categories** - Makes retrieval easier
4. **Set appropriate importance** - Helps with consolidation
