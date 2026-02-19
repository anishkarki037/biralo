---
name: research-and-act
description: Research topics using web search and summarize tools, then take action based on findings. Use when user asks to research, investigate, look up, find information about, or analyze a topic and then do something with it.
metadata: {"biralo":{"emoji":"🔍","requires":{"bins":["curl"]}}}
---

# Research and Act

Research topics using web search and summarize tools, then take action based on findings.

## When to Use

Use this skill when the user asks to:
- "Research [topic] and..."
- "Look up [topic] and..."
- "Find information about [topic] and..."
- "Investigate [topic] and..."
- "Analyze [topic] and..."
- "Learn about [topic] and..."

## Research Workflow

### Step 1: Gather Information

1. **Web search**: Use `web_search` tool to find relevant sources
2. **Summarize**: Use `summarize` skill to extract key information from URLs
3. **Iterate**: Follow promising leads, search for deeper information

```bash
# Search for information
web_search query="best practices for python async programming"

# Summarize a relevant article
summarize "https://realpython.com/async-python/" --length medium
```

### Step 2: Synthesize Findings

Combine information from multiple sources:
- Identify common patterns and best practices
- Note conflicting information and resolve it
- Extract actionable insights

### Step 3: Take Action

Based on research findings:
- Implement solutions using appropriate tools
- Apply best practices discovered
- Create summaries or reports for the user

## Example: Research and Implement

User: "Research Python async best practices and create an async task runner"

```
1. web_search query="python async best practices 2024"
2. summarize <top-3-results> --length medium
3. synthesize: identify patterns (await in try/finally, proper task cancellation, connection pooling)
4. write_to_file async_runner.py with best practices
```

## Tips

- Start with broad searches, then narrow down
- Prioritize official documentation and reputable sources
- Use summarize skill to quickly extract info from long articles
- Take notes on key findings for later action
- Verify information across multiple sources when critical
