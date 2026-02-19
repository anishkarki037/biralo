"""Memory summary tool for getting top/important memories."""

from pathlib import Path
from typing import Optional

from biralo.agent.tools.base import Tool


class MemorySummaryTool(Tool):
    """
    Tool for getting a summary of important memories.
    
    Use this tool when:
    - Getting the most important memories for context
    - Finding frequently accessed information
    - Understanding key stored information quickly
    """
    
    name = "memory_summary"
    description = """
    Get a summary of the most important memories.
    
    Use this tool when:
    - Getting context on important memories
    - Finding frequently accessed information
    - Understanding key stored information
    
    Returns memories sorted by importance and access count.
    This is useful for quick context retrieval.
    """
    
    def __init__(self, workspace: Path):
        from biralo.agent.memory import MemoryStore
        from biralo.agent.memory_consolidation import MemoryConsolidationService
        self.workspace = workspace
        self.memory = MemoryStore(workspace)
        self.consolidation = MemoryConsolidationService(workspace)
    
    @property
    def parameters(self) -> dict:
        """Return tool parameters schema."""
        return {
            "type": "object",
            "properties": {
                "limit": {
                    "type": "integer",
                    "description": "Number of top memories to return",
                    "default": 5
                },
                "include_consolidated": {
                    "type": "boolean",
                    "description": "Include memories that are already consolidated",
                    "default": False
                }
            },
            "required": []
        }
    
    async def execute(self, limit: int = 5, include_consolidated: bool = False) -> str:
        """Execute memory summary query."""
        if include_consolidated:
            # Get all memories sorted by importance
            from biralo.agent.memory_db import MemoryDatabase
            db = MemoryDatabase(self.workspace)
            cursor = db.conn.cursor()
            cursor.execute("""
                SELECT id, content, importance, access_count, created_at, category
                FROM memories
                ORDER BY importance DESC, access_count DESC
                LIMIT ?
            """, (limit,))
            memories = [dict(row) for row in cursor.fetchall()]
        else:
            summary = self.consolidation.get_memory_summary(limit=limit)
            memories = [
                {
                    'content': m['content'],
                    'importance': m['importance'],
                    'access_count': m['access_count'],
                    'created_at': m['created_at'],
                    'category': 'unknown'
                }
                for m in summary['top_memories']
            ]
        
        if not memories:
            return "No memories found."
        
        lines = [f"# Memory Summary (Top {len(memories)})\n\n"]
        
        for i, mem in enumerate(memories, 1):
            stars = "⭐" * mem['importance']
            lines.append(f"{i}. {stars} {mem['content'][:100]}...")
            if len(mem['content']) > 100:
                lines.append("\n")
            lines.append(f"   *Accessed {mem['access_count']} times | {mem['created_at'][:10]}*\n\n")
        
        lines.append("\n---\n")
        lines.append("Use `memory_query` tool for more detailed filtering.")
        
        return "".join(lines)
