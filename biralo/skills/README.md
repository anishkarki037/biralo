# biralo Skills

This directory contains built-in skills that extend biralo's capabilities.

## Skill Format

Each skill is a directory containing a `SKILL.md` file with:
- YAML frontmatter (name, description, metadata)
- Markdown instructions for the agent

## Attribution

These skills are adapted from [OpenClaw](https://github.com/openclaw/openclaw)'s skill system.
The skill format and metadata structure follow OpenClaw's conventions to maintain compatibility.

## Available Skills

| Skill | Description |
|-------|-------------|
| `browser` | Automate web browser interactions for scraping and testing |
| `cron` | Schedule reminders and recurring tasks |
| `github` | Interact with GitHub using the `gh` CLI |
| `memory` | Save and retrieve memories |
| `research-and-act` | Research topics and take action based on findings |
| `self-awareness` | Self-reflection, goal tracking, autonomous learning |
| `skill-creator` | Create new skills |
| `summarize` | Summarize URLs, files, and YouTube videos |
| `tmux` | Remote-control tmux sessions |
| `weather` | Get weather info using wttr.in and Open-Meteo |