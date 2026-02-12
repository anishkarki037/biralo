"""Memory system for persistent agent memory."""

from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

from biralo.utils.helpers import ensure_dir, today_date
from biralo.agent.memory_db import MemoryDatabase


class MemoryStore:
    """
    Memory system for the agent.
    
    Supports daily notes (memory/YYYY-MM-DD.md) and long-term memory (MEMORY.md).
    All memories are also stored in SQLite for efficient querying, tagging, and consolidation.
    """
    
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.memory_dir = ensure_dir(workspace / "memory")
        self.memory_file = self.memory_dir / "MEMORY.md"
        
        # Initialize SQLite backend
        self.db = MemoryDatabase(workspace)
    
    def get_today_file(self) -> Path:
        """Get path to today's memory file."""
        return self.memory_dir / f"{today_date()}.md"
    
    def read_today(self) -> str:
        """Read today's memory notes."""
        today_file = self.get_today_file()
        if today_file.exists():
            return today_file.read_text(encoding="utf-8")
        return ""
    
    def append_today(self, content: str) -> None:
        """Append content to today's memory notes."""
        today_file = self.get_today_file()
        today = today_date()
        
        if today_file.exists():
            existing = today_file.read_text(encoding="utf-8")
            content = existing + "\n" + content
        else:
            # Add header for new day
            header = f"# {today}\n\n"
            content = header + content
        
        today_file.write_text(content, encoding="utf-8")
        
        # Also save to database
        self.db.save_daily_note(today, content)
        # Add as memory for search and indexing
        self.db.add_memory(
            content=content,
            category="daily-note",
            importance=2,
            source="daily-notes",
            tags=[today]
        )
    
    def read_long_term(self) -> str:
        """Read long-term memory (MEMORY.md)."""
        if self.memory_file.exists():
            return self.memory_file.read_text(encoding="utf-8")
        return ""
    
    def write_long_term(self, content: str) -> None:
        """Write to long-term memory (MEMORY.md)."""
        self.memory_file.write_text(content, encoding="utf-8")
        # Also store in database
        self.db.save_long_term_memory("default", content)
    
    def get_recent_memories(self, days: int = 7) -> str:
        """
        Get memories from the last N days.
        
        Args:
            days: Number of days to look back.
        
        Returns:
            Combined memory content.
        """
        from datetime import timedelta
        
        memories = []
        today = datetime.now().date()
        
        for i in range(days):
            date = today - timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            file_path = self.memory_dir / f"{date_str}.md"
            
            if file_path.exists():
                content = file_path.read_text(encoding="utf-8")
                memories.append(content)
        
        return "\n\n---\n\n".join(memories)
    
    def list_memory_files(self) -> list[Path]:
        """List all memory files sorted by date (newest first)."""
        if not self.memory_dir.exists():
            return []
        
        files = list(self.memory_dir.glob("????-??-??.md"))
        return sorted(files, reverse=True)
    
    def get_memory_context(self) -> str:
        """
        Get memory context for the agent.
        
        Returns:
            Formatted memory context including long-term and recent memories.
        """
        parts = []
        
        # Long-term memory
        long_term = self.read_long_term()
        if long_term:
            parts.append("## Long-term Memory\n" + long_term)
        
        # Today's notes
        today = self.read_today()
        if today:
            parts.append("## Today's Notes\n" + today)
        
        return "\n\n".join(parts) if parts else ""

    # ============ SQLite Backend Methods ============
    
    def add_memory(
        self,
        content: str,
        category: str = "general",
        importance: int = 1,
        tags: Optional[List[str]] = None,
        source: Optional[str] = None,
    ) -> int:
        """
        Add a new memory to the database.
        
        Args:
            content: Memory content
            category: Memory category (user-info, project, learning, etc.)
            importance: Importance level 1-5 (5 is highest)
            tags: Optional list of tags for organization
            source: Optional source (conversation, daily-note, etc.)
        
        Returns:
            Memory ID
        """
        return self.db.add_memory(content, category, importance, tags, source)
    
    def search_memories(
        self,
        query: str,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        min_importance: int = 1,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Search memories using full-text search.
        
        Args:
            query: Search query (supports FTS5 syntax)
            category: Optional category filter
            tags: Optional tag filters (AND logic)
            min_importance: Minimum importance level (1-5)
            limit: Maximum results to return
        
        Returns:
            List of matching memories with metadata
        """
        return self.db.search_memories(query, category, tags, min_importance, limit)
    
    def get_memories_by_category(
        self,
        category: str,
        days_back: Optional[int] = None,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """
        Get memories by category.
        
        Args:
            category: Category to filter by
            days_back: Only include memories from last N days
            limit: Maximum results
        
        Returns:
            List of memories
        """
        return self.db.get_memories_by_category(category, days_back, limit)
    
    def get_memories_by_tag(
        self,
        tag: str,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """Get memories by tag."""
        return self.db.get_memories_by_tag(tag, limit)
    
    def update_memory(
        self,
        memory_id: int,
        content: Optional[str] = None,
        category: Optional[str] = None,
        importance: Optional[int] = None,
        tags: Optional[List[str]] = None,
    ) -> bool:
        """Update a memory."""
        return self.db.update_memory(memory_id, content, category, importance, tags)
    
    def delete_memory(self, memory_id: int) -> bool:
        """Delete a memory."""
        return self.db.delete_memory(memory_id)
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get memory statistics.
        
        Returns:
            Dictionary with stats on total memories, by category, by importance, etc.
        """
        return self.db.get_memory_stats()
    
    def get_consolidation_candidates(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get candidate memories for consolidation into long-term memory.
        
        Returns memories that are high-importance or frequently accessed.
        """
        return self.db.get_consolidation_candidates(days)
    
    def mark_consolidated(self, memory_id: int, note: str = "") -> None:
        """Mark a memory as consolidated."""
        self.db.mark_consolidated(memory_id, note)
    
    def export_memories_to_markdown(self) -> str:
        """Export all memories to markdown format."""
        return self.db.export_to_markdown()
