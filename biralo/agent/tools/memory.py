"""Memory tool for the agent to save and retrieve memories."""

from pathlib import Path
from typing import Optional, Dict, Any

from biralo.agent.tools.base import Tool


class MemoryTool(Tool):
    """
    Tool for saving and retrieving memories.
    
    Use this tool when:
    - User asks to remember something
    - Important information should be saved for future reference
    - User preferences or context should be stored
    - Learning new information that should be recalled later
    """
    
    name = "memory"
    description = """
    Save or retrieve information from memory.
    
    Use this tool when:
    - User asks you to remember something
    - Important information should be saved for future reference
    - User preferences or context should be stored
    - Learning new information that should be recalled later
    
    Actions:
    - save: Save information to memory
    - search: Search for previously saved information
    - list: List recent memories by category
    """
    
    def __init__(self, workspace: Path):
        from biralo.agent.memory import MemoryStore
        self.workspace = workspace
        self.memory = MemoryStore(workspace)
    
    @property
    def parameters(self) -> dict:
        """Return tool parameters schema."""
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["save", "search", "list", "longterm"],
                    "description": "Action to perform"
                },
                "content": {
                    "type": "string", 
                    "description": "Content to save to memory"
                },
                "query": {
                    "type": "string",
                    "description": "Search query"
                },
                "category": {
                    "type": "string",
                    "description": "Category for the memory"
                },
                "importance": {
                    "type": "integer",
                    "description": "Importance level 1-5",
                    "default": 2
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Tags for the memory"
                },
                "days": {
                    "type": "integer",
                    "description": "Days to look back for list action",
                    "default": 7
                }
            },
            "required": ["action"]
        }
    
    async def execute(self, action: str, content: Optional[str] = None, query: Optional[str] = None, 
                     category: Optional[str] = None, importance: int = 2, 
                     tags: Optional[list] = None, days: int = 7) -> str:
        """
        Execute memory operations.
        
        Args:
            action: save, search, or list
            content: Content to save (for save action)
            query: Search query (for search action)
            category: Category for memory (for save action)
            importance: Importance level 1-5 (for save action)
            tags: Tags for memory (for save action)
            days: Number of days to look back (for list action)
        """
        from biralo.agent.memory import MemoryStore
        
        if action == "save":
            if not content:
                return "Error: content is required for save action"
            
            self.memory.append_today(content)
            
            return f"Saved to memory:\n\n{content[:200]}{'...' if len(content) > 200 else ''}"
        
        elif action == "search":
            if not query:
                return "Error: query is required for search action"
            
            memories = self.memory.db.search_memories(
                query=query,
                category=category,
                min_importance=1,
                limit=10
            )
            
            if not memories:
                return f"No memories found for '{query}'"
            
            results = []
            for m in memories[:5]:
                results.append(f"- [{m['category']}] {m['content'][:100]}...")
            
            return f"Found {len(memories)} memories:\n\n" + "\n".join(results)
        
        elif action == "list":
            from biralo.agent.memory_db import MemoryDatabase
            
            db = MemoryDatabase(self.workspace)
            
            if category:
                memories = db.get_memories_by_category(category, days_back=days)
            else:
                memories = db.get_recent_memories(days=days)
            
            if not memories:
                return "No memories found"
            
            results = []
            for m in memories[:10]:
                results.append(f"- [{m['category']}] {m['content'][:100]}...")
            
            return f"Recent memories:\n\n" + "\n".join(results)
        
        elif action == "longterm":
            # Read long-term memory
            content = self.memory.read_long_term()
            if content:
                return f"Long-term memory:\n\n{content}"
            else:
                return "No long-term memory stored"
        
        else:
            return f"Unknown action: {action}"
