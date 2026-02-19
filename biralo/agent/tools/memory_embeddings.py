"""Memory embedding management tool."""

from pathlib import Path
from typing import Optional

from biralo.agent.tools.base import Tool


class MemoryEmbeddingsTool(Tool):
    """
    Tool for managing memory embeddings.
    
    Use this tool when:
    - Generating embeddings for existing memories
    - Checking embedding status
    - Indexing memories for semantic search
    """
    
    name = "memory_embeddings"
    description = """
    Manage memory embeddings for semantic search.
    
    Use this tool when:
    - Generating embeddings for existing memories
    - Indexing memories for semantic search
    - Checking embedding status
    
    This tool uses sentence-transformers to generate embeddings
    that enable concept-based (semantic) search across memories.
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
                "action": {
                    "type": "string",
                    "enum": ["status", "generate", "generate_all"],
                    "description": "Action to perform",
                    "default": "status"
                },
                "batch_size": {
                    "type": "integer",
                    "description": "Batch size for embedding generation",
                    "default": 50
                }
            },
            "required": ["action"]
        }
    
    async def execute(self, action: str = "status", batch_size: int = 50) -> str:
        """Execute embedding management."""
        if action == "status":
            return await self._get_status()
        elif action == "generate":
            return await self._generate_one()
        elif action == "generate_all":
            return await self._generate_all(batch_size)
        else:
            return f"Unknown action: {action}"
    
    async def _get_status(self) -> str:
        """Get embedding status."""
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT COUNT(*) as total FROM memories")
        total = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as embedded FROM memories WHERE embedding IS NOT NULL")
        embedded = cursor.fetchone()['embedded']
        
        lines = ["# Embedding Status\n\n"]
        lines.append(f"**Total Memories**: {total}\n")
        lines.append(f"**With Embeddings**: {embedded}\n")
        lines.append(f"**Without Embeddings**: {total - embedded}\n")
        
        if total > 0:
            pct = (embedded / total) * 100
            lines.append(f"\n**Coverage**: {pct:.1f}%\n")
        
        if total - embedded > 0:
            lines.append(f"\nRun `memory_embeddings(action='generate_all')` to generate embeddings for all memories.\n")
        
        return "".join(lines)
    
    async def _generate_one(self) -> str:
        """Generate embedding for one memory without embedding."""
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT id, content FROM memories WHERE embedding IS NULL LIMIT 1")
        mem = cursor.fetchone()
        
        if not mem:
            return "All memories already have embeddings!"
        
        try:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer('all-MiniLM-L6-v2')
            embedding = model.encode([mem['content']])[0].tolist()
            self.db.save_embedding(mem['id'], embedding)
            return f"Generated embedding for memory ID {mem['id']}:\n\n{mem['content'][:100]}..."
        except ImportError:
            return "sentence-transformers not installed. Install with: pip install sentence-transformers"
        except Exception as e:
            return f"Error generating embedding: {e}"
    
    async def _generate_all(self, batch_size: int) -> str:
        """Generate embeddings for all memories."""
        try:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer('all-MiniLM-L6-v2')
        except ImportError:
            return "sentence-transformers not installed. Install with: pip install sentence-transformers"
        
        count = self.db.generate_embeddings_for_memories(batch_size)
        
        lines = [f"# Embedding Generation Complete\n\n"]
        lines.append(f"**Generated**: {count} embeddings\n")
        
        # Check remaining
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT COUNT(*) as remaining FROM memories WHERE embedding IS NULL")
        remaining = cursor.fetchone()['remaining']
        
        if remaining > 0:
            lines.append(f"\n**Remaining**: {remaining} memories\n")
            lines.append(f"Run again to generate more, or increase batch_size.\n")
        else:
            lines.append("\nAll memories now have embeddings! Semantic search is ready.\n")
        
        return "".join(lines)
