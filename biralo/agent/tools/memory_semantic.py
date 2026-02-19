"""Semantic memory search tool using embeddings."""

from pathlib import Path
from typing import Optional

from biralo.agent.tools.base import Tool


class MemorySemanticTool(Tool):
    """
    Tool for semantic search across memories using embeddings.
    
    Use this tool when:
    - Finding conceptually related memories (not just keyword matches)
    - Searching with natural language queries
    - Finding similar information expressed differently
    """
    
    name = "memory_semantic"
    description = """
    Search memories using semantic similarity (concept-based search).
    
    Use this tool when:
    - Finding conceptually related memories
    - Using natural language queries
    - Searching for information expressed differently
    - Finding similar topics even without keyword matches
    
    This uses embeddings to find semantically similar content,
    not just keyword matches.
    
    Example: Search for "coding preferences" will find memories 
    about "Python scripting" even without using those exact words.
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
                "query": {
                    "type": "string",
                    "description": "Natural language query to search for"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum results to return",
                    "default": 5
                },
                "min_importance": {
                    "type": "integer",
                    "description": "Minimum importance level (1-5)",
                    "default": 1
                }
            },
            "required": ["query"]
        }
    
    async def execute(self, query: str, limit: int = 5, min_importance: int = 1) -> str:
        """Execute semantic search."""
        results = self.db.search_semantic(
            query=query,
            limit=limit,
            min_importance=min_importance
        )
        
        if not results:
            return f"No semantically similar memories found for '{query}'. Try the regular search tool instead."
        
        lines = [f"# Semantic Search Results: \"{query}\"\n\n"]
        
        if 'similarity' in results[0]:
            lines.append("*(Ranked by semantic similarity)*\n\n")
        
        for i, mem in enumerate(results, 1):
            stars = "⭐" * mem['importance']
            similarity = mem.get('similarity', 0)
            
            lines.append(f"{i}. {stars} [{mem['category']}]")
            if similarity:
                lines.append(f" *(similarity: {similarity:.2f})*")
            lines.append("\n")
            
            lines.append(f"   {mem['content']}\n")
            lines.append(f"   *{mem['created_at'][:10]}*")
            if mem.get('access_count', 0) > 0:
                lines.append(f" | Accessed {mem['access_count']} times")
            lines.append("\n\n")
        
        lines.append("---\n")
        lines.append("Tip: Use `memory_query` for keyword-based search or `memory_search` for full-text search.")
        
        return "".join(lines)
