"""Memory query tool for parameterized searches."""

from pathlib import Path
from typing import Optional, List

from biralo.agent.tools.base import Tool


class MemoryQueryTool(Tool):
    """
    Tool for querying memories with various filters.
    
    Use this tool when:
    - Finding memories by category
    - Filtering by importance level
    - Looking for memories from specific time periods
    - Combining multiple filters
    """
    
    name = "memory_query"
    description = """
    Query memories with various filters and parameters.
    
    Use this tool when:
    - Finding memories by category (user-info, project, learning, etc.)
    - Filtering by importance level (1-5)
    - Looking for memories from specific time periods
    - Combining multiple filters
    
    All parameters are optional - leave blank to get default results.
    """
    
    def __init__(self, workspace: Path):
        from biralo.agent.memory import MemoryStore
        from biralo.agent.memory_db import MemoryDatabase
        self.workspace = workspace
        self.memory = MemoryStore(workspace)
        self.db = MemoryDatabase(workspace)
    
    @property
    def parameters(self) -> dict:
        """Return tool parameters schema."""
        return {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Filter by category (e.g., user-info, project, learning)"
                },
                "tag": {
                    "type": "string",
                    "description": "Filter by specific tag"
                },
                "min_importance": {
                    "type": "integer",
                    "description": "Minimum importance level (1-5)",
                    "default": 1
                },
                "days_back": {
                    "type": "integer",
                    "description": "Only show memories from last N days",
                    "default": 30
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum results to return",
                    "default": 20
                }
            },
            "required": []
        }
    
    async def execute(
        self,
        category: Optional[str] = None,
        tag: Optional[str] = None,
        min_importance: int = 1,
        days_back: int = 30,
        limit: int = 20
    ) -> str:
        """Execute memory query."""
        # Build query description
        filters = []
        if category:
            filters.append(f"category={category}")
        if tag:
            filters.append(f"tag={tag}")
        if min_importance > 1:
            filters.append(f"importance≥{min_importance}")
        if days_back < 365:
            filters.append(f"last {days_back} days")
        
        filter_desc = ", ".join(filters) if filters else "all memories"
        
        # Execute query
        if category:
            memories = self.db.get_memories_by_category(
                category=category,
                days_back=days_back,
                limit=limit
            )
        elif tag:
            memories = self.db.get_memories_by_tag(
                tag=tag,
                limit=limit
            )
        else:
            memories = self.db.get_recent_memories(
                days=days_back,
                limit=limit,
                min_importance=min_importance
            )
        
        if not memories:
            return f"No memories found for {filter_desc}."
        
        lines = [f"# Query Results: {filter_desc}\n\n"]
        lines.append(f"Found {len(memories)} memories:\n\n")
        
        for mem in memories:
            stars = "⭐" * mem['importance']
            lines.append(f"## {stars} [{mem['category']}]\n")
            lines.append(f"*{mem['created_at'][:10]}* | Accessed: {mem['access_count']} times\n\n")
            lines.append(f"{_truncate(mem['content'], 150)}\n")
            lines.append("\n---\n\n")
        
        return "".join(lines)


def _truncate(text: str, length: int) -> str:
    """Truncate text to length."""
    if len(text) <= length:
        return text
    return text[:length] + "..."
