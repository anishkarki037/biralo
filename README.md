# 🐈 Biralo AI Assistant

![Biralo Logo](biralo-logo.png)

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/anishkarki037/biralo/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)

**Biralo** is a powerful, autonomous, and lightweight personal AI assistant framework designed to be an elite technical companion. Unlike traditional chatbots, Biralo is integrated into the host system, capable of background execution, and authorized to evolve by creating its own skills.

## 🌟 Elite Identity & Vision

Biralo is designed with a core set of directives:
1. **Be Fearless**: Proactively uses system tools to complete tasks.
2. **Technical Excellence**: Refined, direct, and authoritative communication style.
3. **Problem Solver**: Focused on outcomes, anticipating pitfalls before they happen.
4. **Autonomous**: Operates independently with background execution and self-reflection.
5. **Self-Expansion**: Authorized to research, install, and integrate new libraries and tools.

---

## 🏗️ Core Architecture (The "Nanobot" System)

Biralo follows a modular, event-driven architecture that allows for extreme flexibility and power.

### 🧠 The Agent
The brain of the system. It handles intent recognition, tool selection, and coordinate execution. It maintains a persistent state and can spawn subagents for parallel task processing.

### 🚌 The Bus
A robust messaging layer that connects all components. It handles event distribution, allowing skills to react to system changes or agent requests seamlessly.

### 📡 Channels
Standardized communication interfaces. Whether you're using a terminal, a mobile app, or an enterprise messaging platform, the experience remains consistent.
- **Messaging**: Telegram, Slack, Discord, QQ, DingTalk.
- **Web**: Lightweight SocketIO-based web interface.
- **Local**: CLI and the CustomTkinter Desktop App.

### 🧩 Skills & Tools
Skills represent what Biralo can *do*. Each skill is a collection of tools that provide specific capabilities.
- **Visual (Vision)**: Screen capture and visual reporting via `mss`.
- **Browser**: Full web automation using Playwright/Selenium.
- **FileSystem**: Deep system search, file manipulation, and management.
- **Memory**: Semantic long-term memory using vector embeddings.
- **Execution**: Secure shell access and background task scheduling (Cron).

---

## 🚀 Installation

### CLI Installation (Recommended for Power Users)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/anishkarki037/biralo/
   cd biralo
   ```

2. **Set up Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -e .
   ```

3. **Initialize Configuration**:
   ```bash
   biralo init
   ```

### Desktop Application (Modern GUI)

1. Navigate to the app directory:
   ```bash
   cd biralo-app
   ```
2. Run the auto-installer:
   ```bash
   python install.py
   ```
3. Launch:
   ```bash
   python main.py
   ```

---

## ⚙️ Configuration Guide

Biralo stores its configuration in `~/.biralo/config.json`. Below is a comprehensive example with advanced settings.

```json
{
  "providers": {
    "openrouter": {
      "apiKey": "sk-or-v1-...",
      "apiBase": "https://openrouter.ai/api/v1"
    }
  },
  "agents": {
    "defaults": {
      "model": "anthropic/claude-3.5-sonnet",
      "temperature": 0.7,
      "max_tokens": 4096
    }
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "BOT_TOKEN",
      "allowFrom": ["YOUR_USER_ID"]
    },
    "web": {
      "port": 8000,
      "host": "0.0.0.0"
    }
  },
  "filesystem": {
    "workspace": "D:/biralo/workspace",
    "allowed_paths": ["C:/Users/User/Documents"]
  }
}
```

### Advanced LLM Configuration
Biralo uses **LiteLLM**, meaning you can use any provider (OpenAI, Anthropic, Google, etc.) by simply adding the corresponding `apiKey` and `model` name.

---

## 🛠️ Built-in Skills & Toolsets

| Skill | Tools Included | Primary Purpose |
|-------|----------------|-----------------|
| **Web** | `web_search`, `read_url` | Internet research and knowledge retrieval. |
| **Browser** | `navigate_to`, `click`, `extract_text` | Complex web automation and interaction. |
| **Files** | `search_files`, `edit_file`, `move_file` | Direct interaction with the host filesystem. |
| **Memory** | `query_memory`, `store_insight` | Persistent long-term context and information retrieval. |
| **Shell** | `run_command`, `get_status` | Executing terminal commands and monitoring results. |
| **Vision** | `take_screenshot`, `analyze_visuals` | Capturing and understanding visual system output. |

---

## 📘 Detailed Usage Examples

### 1. Complex File Operations
*User: "Find all .log files in my downloads, summarize the errors, and send a report to my Telegram."*
*   **Biralo Actions**: Search Files → Read Content → Summarize → Message (via Telegram).

### 2. Autonomous Web Research
*User: "Research the latest version of Next.js and create a boilerplate in a new folder."*
*   **Biralo Actions**: Web Search → Browse Docs → Create Directory → Generate Files.

### 3. Visual Support
*User: "I'm having a bug in my IDE, what do you see?"*
*   **Biralo Actions**: Take Screenshot → Image Analysis → Provide Solution.

---

## 🆘 Troubleshooting

- **API Errors**: Ensure your OpenRouter or provider credits are sufficient and the key is correctly set in `config.json`.
- **Gateway Issues**: If the gateway fails to start, verify that the enabled channel has all required tokens and the ports are not in use.
- **Dependency Issues**: Run `pip install -r requirements.txt` to ensure all sub-dependencies are satisfied.
- **Permission Denied**: Run the application/terminal with appropriate permissions if accessing restricted system paths.

---

## 🗺️ Roadmap

- [ ] **Voice Interface**: Native TTS and STT integration.
- [ ] **Plugin Ecosystem**: A marketplace for sharing community-created skills.
- [ ] **Subagent Orchestration**: Enhanced delegation for large-scale projects.
- [ ] **Deep IDE Integration**: Direct plugins for VS Code and Cursor.

## 🤝 Contributing

We are looking for elite developers to join the Biralo journey!
1. Fork: [https://github.com/anishkarki037/biralo/](https://github.com/anishkarki037/biralo/)
2. Create Feature Branch
3. Submit PR

## 📄 License

Biralo is open-source software licensed under the **MIT License**.

---

*“Elite problems require elite solutions. Welcome to the future of AI assistance.”* 🐈
