"""Memory statistics tool for the agent."""

from pathlib import Path
from typing import Optional

from biralo.agent.tools.base import Tool


class MemoryStatsTool(Tool):
    """
    Tool for getting memory statistics and analytics.
    
    Use this tool when:
    - You want to understand memory usage patterns
    - Checking how many memories exist
    - Looking at memory distribution by category or importance
    - Getting insights into tag usage
    """
    
    name = "memory_stats"
    description = """
    Get statistics and analytics about stored memories.
    
    Use this tool when:
    - Understanding memory usage patterns
    - Checking memory distribution by category or importance
    - Viewing top tags and access patterns
    - Getting insights into stored information
    
    Returns comprehensive statistics including:
    - Total memories count
    - Memories by category
    - Memories by importance level
    - Top tags
    - Average access count
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
            "properties": {},
            "required": []
        }
    
    async def execute(self) -> str:
        """Execute memory statistics query."""
        stats = self.db.get_memory_stats()
        
        lines = ["# Memory Statistics\n"]
        lines.append(f"**Total Memories**: {stats['total_memories']}\n")
        lines.append(f"**Total Tags**: {stats['total_tags']}\n")
        lines.append(f"**Average Access Count**: {stats['avg_access_count']:.1f}\n")
        
        lines.append("\n## By Category\n")
        for cat, count in stats.get('by_category', {}).items():
            lines.append(f"- {cat}: {count}\n")
        
        lines.append("\n## By Importance\n")
        for imp in sorted(stats.get('by_importance', {}).keys(), reverse=True):
            count = stats['by_importance'][imp]
            stars = "⭐" * imp
            lines.append(f"- {stars} (level {imp}): {count}\n")
        
        lines.append("\n## Top Tags\n")
        for tag, count in stats.get('top_tags', {}).items():
            lines.append(f"- {tag}: {count}\n")
        
        return "".join(lines)
