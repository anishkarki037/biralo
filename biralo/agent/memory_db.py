"""SQLite database backend for persistent agent memory."""

import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import json

from biralo.utils.helpers import ensure_dir


class MemoryDatabase:
    """
    SQLite-based memory storage with full-text search, tagging, and categorization.
    
    Features:
    - Structured memory storage with metadata
    - Full-text search across memories
    - Tags and categories for organization
    - Importance levels for prioritization
    - Automatic consolidation suggestions
    - Memory statistics and analytics
    """
    
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.memory_dir = ensure_dir(workspace / "memory")
        self.db_path = self.memory_dir / "memories.db"
        
        # Initialize database connection with check_same_thread disabled for async support
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()
    
    def _init_schema(self) -> None:
        """Initialize database schema."""
        cursor = self.conn.cursor()
        
        # Main memories table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                category TEXT DEFAULT 'general',
                importance INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                accessed_at TIMESTAMP,
                access_count INTEGER DEFAULT 0,
                source TEXT,
                is_consolidated INTEGER DEFAULT 0,
                consolidation_note TEXT
            )
        """)
        
        # Full-text search virtual table
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
                content,
                category,
                content=memories,
                content_rowid=id
            )
        """)
        
        # Tags table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory_tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_id INTEGER NOT NULL,
                tag TEXT NOT NULL,
                FOREIGN KEY (memory_id) REFERENCES memories(id) ON DELETE CASCADE,
                UNIQUE(memory_id, tag)
            )
        """)
        
        # Daily notes table (for efficient daily memory queries)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT UNIQUE NOT NULL,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Long-term memory table (consolidated memories)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS long_term_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                section TEXT NOT NULL UNIQUE,
                content TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_memories_category ON memories(category)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_memories_importance ON memories(importance DESC)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_memories_created_at ON memories(created_at DESC)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_memory_tags_memory_id ON memory_tags(memory_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_memory_tags_tag ON memory_tags(tag)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_daily_notes_date ON daily_notes(date DESC)")
        
        self.conn.commit()
    
    def add_memory(
        self,
        content: str,
        category: str = "general",
        importance: int = 1,
        tags: Optional[List[str]] = None,
        source: Optional[str] = None,
    ) -> int:
        """
        Add a new memory.
        
        Args:
            content: Memory content
            category: Memory category (e.g., 'user-info', 'project', 'learning')
            importance: Importance level (1-5, where 5 is highest)
            tags: Optional list of tags
            source: Optional source (e.g., 'conversation', 'daily-note')
        
        Returns:
            Memory ID
        """
        cursor = self.conn.cursor()
        
        # Clamp importance to 1-5
        importance = max(1, min(5, importance))
        
        # Insert into memories table
        cursor.execute("""
            INSERT INTO memories (content, category, importance, source)
            VALUES (?, ?, ?, ?)
        """, (content, category, importance, source))
        
        memory_id = cursor.lastrowid
        
        # Insert into FTS table
        cursor.execute("""
            INSERT INTO memories_fts (rowid, content, category)
            VALUES (?, ?, ?)
        """, (memory_id, content, category))
        
        # Insert tags
        if tags:
            for tag in tags:
                cursor.execute("""
                    INSERT INTO memory_tags (memory_id, tag)
                    VALUES (?, ?)
                    ON CONFLICT DO NOTHING
                """, (memory_id, tag.lower()))
        
        self.conn.commit()
        return memory_id
    
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
            min_importance: Minimum importance level
            limit: Maximum results to return
        
        Returns:
            List of matching memories
        """
        cursor = self.conn.cursor()
        
        # Handle wildcard - match all memories
        if query == "*":
            sql = "SELECT * FROM memories m WHERE m.importance >= ?"
            params = [min_importance]
        else:
            # Build base query
            sql = """
                SELECT DISTINCT m.* FROM memories m
                WHERE m.id IN (
                    SELECT rowid FROM memories_fts WHERE memories_fts MATCH ?
                )
                AND m.importance >= ?
            """
            params = [query, min_importance]
        
        # Add category filter
        if category:
            sql += " AND m.category = ?"
            params.append(category)
        
        # Add tag filters
        if tags:
            for tag in tags:
                sql += f" AND m.id IN (SELECT memory_id FROM memory_tags WHERE tag = ?)"
                params.append(tag.lower())
        
        sql += " ORDER BY m.importance DESC, m.accessed_at DESC, m.created_at DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(sql, params)
        results = [dict(row) for row in cursor.fetchall()]
        
        # Update access stats
        for row in results:
            self._update_access_stats(row['id'])
        
        return results
    
    def get_memories_by_category(
        self,
        category: str,
        days_back: Optional[int] = None,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """
        Get memories by category with optional date filtering.
        
        Args:
            category: Category to filter by
            days_back: Only include memories from last N days (None = all)
            limit: Maximum results
        
        Returns:
            List of memories
        """
        cursor = self.conn.cursor()
        
        sql = "SELECT * FROM memories WHERE category = ?"
        params = [category]
        
        if days_back:
            cutoff = datetime.now() - timedelta(days=days_back)
            sql += " AND created_at >= ?"
            params.append(cutoff.isoformat())
        
        sql += " ORDER BY importance DESC, created_at DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(sql, params)
        results = [dict(row) for row in cursor.fetchall()]
        
        return results
    
    def get_memories_by_tag(
        self,
        tag: str,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """Get memories by tag."""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            SELECT m.* FROM memories m
            JOIN memory_tags mt ON m.id = mt.memory_id
            WHERE mt.tag = ?
            ORDER BY m.importance DESC, m.created_at DESC
            LIMIT ?
        """, (tag.lower(), limit))
        
        results = [dict(row) for row in cursor.fetchall()]
        return results
    
    def get_recent_memories(
        self,
        days: int = 7,
        limit: int = 50,
        min_importance: int = 1,
    ) -> List[Dict[str, Any]]:
        """Get memories from the last N days."""
        cursor = self.conn.cursor()
        
        cutoff = datetime.now() - timedelta(days=days)
        cursor.execute("""
            SELECT * FROM memories
            WHERE created_at >= ? AND importance >= ?
            ORDER BY importance DESC, created_at DESC
            LIMIT ?
        """, (cutoff.isoformat(), min_importance, limit))
        
        results = [dict(row) for row in cursor.fetchall()]
        return results
    
    def update_memory(
        self,
        memory_id: int,
        content: Optional[str] = None,
        category: Optional[str] = None,
        importance: Optional[int] = None,
        tags: Optional[List[str]] = None,
    ) -> bool:
        """Update a memory."""
        cursor = self.conn.cursor()
        
        updates = {"updated_at": datetime.now().isoformat()}
        params = []
        
        if content is not None:
            updates["content"] = content
        if category is not None:
            updates["category"] = category
        if importance is not None:
            updates["importance"] = max(1, min(5, importance))
        
        # Update main table
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        params = list(updates.values())
        params.append(memory_id)
        
        cursor.execute(f"UPDATE memories SET {set_clause} WHERE id = ?", params)
        
        # Update FTS if content changed
        if content is not None:
            cursor.execute("""
                UPDATE memories_fts SET content = ? WHERE rowid = ?
            """, (content, memory_id))
        
        # Update tags if provided
        if tags is not None:
            cursor.execute("DELETE FROM memory_tags WHERE memory_id = ?", (memory_id,))
            for tag in tags:
                cursor.execute("""
                    INSERT INTO memory_tags (memory_id, tag)
                    VALUES (?, ?)
                """, (memory_id, tag.lower()))
        
        self.conn.commit()
        return cursor.rowcount > 0
    
    def delete_memory(self, memory_id: int) -> bool:
        """Delete a memory."""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def _update_access_stats(self, memory_id: int) -> None:
        """Update access statistics for a memory."""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE memories
            SET accessed_at = ?, access_count = access_count + 1
            WHERE id = ?
        """, (datetime.now().isoformat(), memory_id))
        self.conn.commit()
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as total FROM memories")
        stats = {"total_memories": cursor.fetchone()['total']}
        
        cursor.execute("""
            SELECT category, COUNT(*) as count
            FROM memories
            GROUP BY category
        """)
        stats["by_category"] = {row['category']: row['count'] for row in cursor.fetchall()}
        
        cursor.execute("""
            SELECT importance, COUNT(*) as count
            FROM memories
            GROUP BY importance
        """)
        stats["by_importance"] = {row['importance']: row['count'] for row in cursor.fetchall()}
        
        cursor.execute("SELECT COUNT(*) as total FROM memory_tags")
        stats["total_tags"] = cursor.fetchone()['total']
        
        cursor.execute("""
            SELECT tag, COUNT(*) as count
            FROM memory_tags
            GROUP BY tag
            ORDER BY count DESC
            LIMIT 10
        """)
        stats["top_tags"] = {row['tag']: row['count'] for row in cursor.fetchall()}
        
        cursor.execute("""
            SELECT AVG(CAST(access_count AS FLOAT)) as avg_accesses
            FROM memories
        """)
        stats["avg_access_count"] = cursor.fetchone()['avg_accesses'] or 0
        
        return stats
    
    def save_daily_note(self, date: str, content: str) -> None:
        """Save daily note for a specific date."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO daily_notes (date, content)
            VALUES (?, ?)
            ON CONFLICT(date) DO UPDATE SET content = ?
        """, (date, content, content))
        self.conn.commit()
    
    def get_daily_note(self, date: str) -> Optional[str]:
        """Get daily note for a specific date."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT content FROM daily_notes WHERE date = ?", (date,))
        row = cursor.fetchone()
        return row['content'] if row else None
    
    def save_long_term_memory(self, section: str, content: str) -> None:
        """Save long-term memory section."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO long_term_memory (section, content)
            VALUES (?, ?)
            ON CONFLICT(section) DO UPDATE SET content = ?, updated_at = CURRENT_TIMESTAMP
        """, (section, content, content))
        self.conn.commit()
    
    def get_long_term_memory(self, section: Optional[str] = None) -> Dict[str, str]:
        """Get long-term memory sections."""
        cursor = self.conn.cursor()
        
        if section:
            cursor.execute("""
                SELECT content FROM long_term_memory WHERE section = ?
            """, (section,))
            row = cursor.fetchone()
            return {section: row['content']} if row else {}
        
        cursor.execute("SELECT section, content FROM long_term_memory")
        return {row['section']: row['content'] for row in cursor.fetchall()}
    
    def get_consolidation_candidates(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Get candidate memories for consolidation into long-term memory.
        
        Returns memories that are high-importance, frequently accessed,
        or relate to important topics.
        """
        cursor = self.conn.cursor()
        
        cutoff = datetime.now() - timedelta(days=days)
        cursor.execute("""
            SELECT * FROM memories
            WHERE is_consolidated = 0
            AND (importance >= 4 OR access_count >= 3)
            AND created_at >= ?
            ORDER BY importance DESC, access_count DESC
            LIMIT 20
        """, (cutoff.isoformat(),))
        
        results = [dict(row) for row in cursor.fetchall()]
        return results
    
    def mark_consolidated(self, memory_id: int, note: str = "") -> None:
        """Mark a memory as consolidated."""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE memories
            SET is_consolidated = 1, consolidation_note = ?
            WHERE id = ?
        """, (note, memory_id))
        self.conn.commit()
    
    def export_to_markdown(self) -> str:
        """Export all memories to markdown format."""
        cursor = self.conn.cursor()
        
        lines = ["# Memory Export\n"]
        lines.append(f"Exported at: {datetime.now().isoformat()}\n\n")
        
        # Long-term memory sections
        long_term = self.get_long_term_memory()
        if long_term:
            lines.append("## Long-term Memory\n")
            for section, content in long_term.items():
                lines.append(f"### {section}\n{content}\n\n")
        
        # Memories by category
        cursor.execute("SELECT DISTINCT category FROM memories ORDER BY category")
        for row in cursor.fetchall():
            category = row['category']
            lines.append(f"## {category.title()}\n")
            
            memories = self.get_memories_by_category(category, limit=100)
            for mem in memories:
                importance_stars = "⭐" * mem['importance']
                tags_str = ""
                
                # Get tags
                tag_cursor = self.conn.cursor()
                tag_cursor.execute("""
                    SELECT tag FROM memory_tags WHERE memory_id = ?
                """, (mem['id'],))
                tags = [t['tag'] for t in tag_cursor.fetchall()]
                if tags:
                    tags_str = f" `{', '.join(tags)}`"
                
                lines.append(f"- {importance_stars} {mem['content']}{tags_str}\n")
            
            lines.append("\n")
        
        return "".join(lines)
    
    def close(self) -> None:
        """Close database connection."""
        self.conn.close()
