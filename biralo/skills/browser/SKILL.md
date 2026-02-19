---
name: browser
description: Open URLs and search queries in the user's default browser. Use for playing YouTube videos, searching Google, or opening any website.
metadata: {"biralo":{"emoji":"🌐","requires":{"bins":["python"]}}}
---

# Browser Tool

Open URLs and search queries in the user's default browser. Uses yt-dlp for reliable YouTube video search.

## When to Use

Use this skill when:
- User wants to play something on YouTube
- User wants to search Google
- User wants to open a GitHub repository
- User wants to open any URL

## Tool Usage

The browser tool has the following parameters:
- `action`: The action to perform (open, youtube, play, google, github)
- `url`: URL to open (for 'open' action)
- `query`: Search query (for youtube, play, google, github actions)

### Actions

#### Play on YouTube (Searches and plays best match)
```json
{"action": "play", "query": "never gonna give you up"}
```

1. Uses yt-dlp to search YouTube
2. Finds the most relevant video
3. Opens it directly on YouTube
4. Returns the video title and URL

#### YouTube Search (Shows results)
```json
{"action": "youtube", "query": "python tutorial"}
```

Opens YouTube search results page. User can browse and select.

#### Open URL
```json
{"action": "open", "url": "https://example.com"}
```

#### Google Search
```json
{"action": "google", "query": "python tutorials"}
```

#### GitHub
```json
{"action": "github", "query": "microsoft/vscode"}
```

Opens a specific repository if format is `user/repo`, otherwise searches GitHub.

## Examples

### Play Music on YouTube
```
User: Play soda pop on YouTube
Agent: {"action": "play", "query": "soda pop"}

Response:
Playing: "Soda Pop" Official Lyric Video | KPop Demon Hunters | Sony Animation
URL: https://www.youtube.com/watch?v=983bBbJx0Mk
```

### Browse YouTube Results
```
User: Search for Python tutorials on YouTube
Agent: {"action": "youtube", "query": "Python tutorials"}
```

### Search for Documentation
```
User: Search for Python async documentation
Agent: {"action": "google", "query": "Python async documentation"}
```

### Open a GitHub Repo
```
User: Open the React repository
Agent: {"action": "github", "query": "facebook/react"}
```

## How It Works

The `play` action:
1. Runs `yt-dlp "ytsearch1:{query}"` to find the first video result
2. Extracts the video ID and title
3. Opens `https://www.youtube.com/watch?v={videoId}` in the default browser
4. Returns the video title and URL

## Requirements

- **yt-dlp**: Required for YouTube search. Install with `pip install yt-dlp`
- **Python webbrowser**: Built-in, no installation needed

## Benefits

- **Reliable search**: Uses yt-dlp which handles YouTube's complexity
- **User's default browser**: Opens in Chrome, Firefox, Edge, etc.
- **Direct video links**: Opens actual YouTube video URLs
- **Informative**: Shows what video was found
- **Cross-platform**: Works on Windows, macOS, Linux
