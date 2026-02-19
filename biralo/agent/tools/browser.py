"""Simple browser tool using Python's webbrowser module."""

import asyncio
import webbrowser
import urllib.parse
import subprocess
import shutil
from typing import Any

from ..tools.base import Tool


class BrowserTool(Tool):
    """Tool for opening URLs in the user's default browser."""

    @property
    def name(self) -> str:
        return "browser"

    @property
    def description(self) -> str:
        return """Open URLs in the user's default browser.
        
Actions:
- open: Open any URL in the browser
- youtube: Search on YouTube (opens search results)
- play: Search YouTube and play the most relevant video (uses yt-dlp)
- google: Search on Google
- github: Open a GitHub repository or search

Examples:
- {"action": "play", "query": "never gonna give you up"}  # Finds and plays best match
- {"action": "youtube", "query": "python tutorial"}  # Shows search results
- {"action": "open", "url": "https://example.com"}
- {"action": "google", "query": "python tutorials"}
"""

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "action": {
                "type": "string",
                "description": "Action to perform",
                "enum": ["open", "youtube", "play", "google", "github"]
            },
            "url": {
                "type": "string",
                "description": "URL to open (for 'open' action)",
                "default": ""
            },
            "query": {
                "type": "string",
                "description": "Search query (for youtube, play, google, github actions)",
                "default": ""
            }
        }

    async def _search_youtube_ytdlp(self, query: str) -> tuple[str, str] | None:
        """Search YouTube using yt-dlp and return (video_id, title)."""
        try:
            # Run yt-dlp to search for the first result
            # Using python -m yt_dlp since yt-dlp might not be in PATH
            cmd = [
                "python", "-m", "yt_dlp",
                f"ytsearch1:{query}",
                "--print", "%(id)s|||%(title)s",
                "--no-download",
                "--quiet",
                "--no-warnings",
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0 and stdout:
                result = stdout.decode().strip()
                if "|||" in result:
                    video_id, title = result.split("|||", 1)
                    return video_id.strip(), title.strip()
        except Exception:
            pass
        
        return None

    async def execute(self, action: str, url: str = "", query: str = "") -> str:
        """Execute a browser action."""
        try:
            if action == "open":
                if not url:
                    return "Error: URL is required for 'open' action"
                webbrowser.open(url)
                return f"Opened {url} in default browser"
            
            elif action == "youtube":
                if not query:
                    return "Error: Query is required for 'youtube' action"
                # Open YouTube search results
                search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
                webbrowser.open(search_url)
                return f"Opened YouTube search for '{query}' in default browser"
            
            elif action == "play":
                if not query:
                    return "Error: Query is required for 'play' action"
                
                # Try to find video using yt-dlp
                result = await self._search_youtube_ytdlp(query)
                
                if result:
                    video_id, title = result
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    webbrowser.open(video_url)
                    return f"Playing: {title}\nURL: {video_url}"
                else:
                    # Fallback to search results if yt-dlp fails
                    search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
                    webbrowser.open(search_url)
                    return f"Could not find video directly. Opened YouTube search for '{query}'"
            
            elif action == "google":
                if not query:
                    return "Error: Query is required for 'google' action"
                search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
                webbrowser.open(search_url)
                return f"Opened Google search for '{query}' in default browser"
            
            elif action == "github":
                if not query:
                    return "Error: Query is required for 'github' action"
                # Check if it looks like a repo (user/repo format)
                if "/" in query and " " not in query:
                    # Direct repo link
                    repo_url = f"https://github.com/{query}"
                    webbrowser.open(repo_url)
                    return f"Opened GitHub repository '{query}' in default browser"
                else:
                    # Search GitHub
                    search_url = f"https://github.com/search?q={urllib.parse.quote(query)}"
                    webbrowser.open(search_url)
                    return f"Opened GitHub search for '{query}' in default browser"
            
            else:
                return f"Error: Unknown action '{action}'"
                
        except Exception as e:
            return f"Error: {str(e)}"
