---
name: self-awareness
description: Self-reflection, goal tracking, and autonomous learning. Connect reflections to actual task improvement. Use after completing tasks to reflect, before starting new tasks to apply improvements.
metadata: {"biralo":{"emoji":"🧠","always":true}}
---

# Self-Awareness Skill

Enable the agent to reflect on actions, track goals, and **connect reflections to actual task improvement**.

## Key Concept: Improvement Loop

```
Task → Reflect → Record Improvement → Apply to Future Tasks → Improve
```

## When to Use

### After Completing a Task
- "Reflect on what just happened"
- "How could I improve next time?"
- Record what worked and what didn't

### Before Starting New Tasks
- "Apply improvements for [context]"
- Get relevant suggestions from past reflections

### When Setting Goals
- "What should I achieve today?"
- "Break this into steps"

## Actions

### Reflect on Completed Task

```bash
self_aware(action="reflect", task="Fixed memory bug", result="Working now", improvement="Add tests next time", quality="7/10")
```

### Record Improvement Directly

```bash
self_aware(action="record_improvement", task="Debug import error", improvement="Check module exists before importing")
```

### Apply Relevant Improvements (Before New Task!)

```bash
self_aware(action="apply_improvements", context="debugging memory issues")
```

### Show All Improvements

```bash
self_aware(action="show_improvements")
```

### Set a Goal

```bash
self_aware(action="set_goal", goal="Learn about AI agents", milestones="Read papers, Build agent, Test it")
```

### Check Goal Progress

```bash
self_aware(action="check_goals")
```

### Analyze Knowledge Gaps

```bash
self_aware(action="knowledge_gaps", topic="machine learning", known="basics", unknown="transformers, attention")
```

## Example Workflow: Improvement Loop

### 1. Complete Task → Reflect

User: "Fix the memory bug"
```
# After fixing...
self_aware(action="reflect", task="Fixed memory import error", 
           result="Tool loads correctly now",
           improvement="Should add better error messages for missing imports",
           quality="6/10")
```

### 2. Start New Task → Apply Improvements

User: "Fix the cron scheduling issue"
```
# Before starting...
self_aware(action="apply_improvements", context="debugging")
# Output shows: "Add better error messages for missing imports"
# Agent applies: Checks if cron module exists, adds clear error
```

### 3. Improved Result

User: "That was faster!"
```
self_aware(action="reflect", task="Fixed cron scheduling issue",
           result="Quick fix using previous improvement",
           improvement="Improvement system worked!",
           quality="9/10")
```

## Self-Dialogue Patterns

### Before Answering

User: "How do I fix X?"
```
self_aware(action="apply_improvements", context="fixing bugs")
# Get relevant improvements, apply them
```

### After Responding

User: "Thanks"
```
self_aware(action="reflect", context="just helped user",
           result="User satisfied",
           improvement="Could have added example code")
```

## Memory Integration

All reflections and improvements are saved:
- **Daily notes** - Today's reflections
- **improvements.json** - Tracked improvements by relevance
- **Long-term memory** - Key learnings

## Best Practices

1. **Always reflect** - After every significant task
2. **Record improvements** - Not just "do better", record HOW
3. **Apply before starting** - Check relevant improvements first
4. **Be specific** - "Add null check" > "Do better"
5. **Track usage** - See which improvements help most
6. **Celebrate wins** - When improvement system works!

## Triggers

Use self_aware when:
- Task completes → `self_aware(action="reflect", ...)`
- New task starts → `self_aware(action="apply_improvements", context="...")`
- Setting goals → `self_aware(action="set_goal", ...)`
- Feeling stuck → `self_aware(action="knowledge_gaps", ...)`
