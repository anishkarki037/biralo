"""Migration utilities for importing markdown memories into SQLite."""

import re
from pathlib import Path
from datetime import datetime
from typing import Tuple

from biralo.agent.memory_db import MemoryDatabase


class MemoryMigration:
    """Migrate existing markdown memories to SQLite."""
    
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.memory_dir = workspace / "memory"
        self.db = MemoryDatabase(workspace)
    
    def migrate_daily_notes(self) -> int:
        """
        Migrate daily note markdown files to SQLite.
        
        Returns:
            Number of files migrated
        """
        if not self.memory_dir.exists():
            return 0
        
        count = 0
        # Find all YYYY-MM-DD.md files
        for file_path in self.memory_dir.glob("????-??-??.md"):
            try:
                # Extract date from filename
                date_str = file_path.stem
                content = file_path.read_text(encoding="utf-8")
                
                # Save to database
                self.db.save_daily_note(date_str, content)
                
                # Also add as memory for search
                self.db.add_memory(
                    content=content,
                    category="daily-note",
                    importance=2,
                    source="migrated-daily-note",
                    tags=[date_str, "daily-note"]
                )
                
                count += 1
            except Exception as e:
                print(f"Error migrating {file_path}: {e}")
        
        return count
    
    def migrate_long_term_memory(self) -> bool:
        """
        Migrate MEMORY.md to SQLite.
        
        Returns:
            True if successful
        """
        memory_file = self.memory_dir / "MEMORY.md"
        if not memory_file.exists():
            return False
        
        try:
            content = memory_file.read_text(encoding="utf-8")
            self.db.save_long_term_memory("default", content)
            
            # Extract sections and create memories
            self._extract_and_save_sections(content)
            
            return True
        except Exception as e:
            print(f"Error migrating MEMORY.md: {e}")
            return False
    
    def _extract_and_save_sections(self, content: str) -> None:
        """Extract sections from markdown and save as individual memories."""
        # Split by ## headers
        sections = re.split(r'^## (.+)$', content, flags=re.MULTILINE)
        
        for i in range(1, len(sections), 2):
            if i + 1 < len(sections):
                section_title = sections[i].strip()
                section_content = sections[i + 1].strip()
                
                if section_content and len(section_content) > 10:
                    # Map section titles to categories
                    category_map = {
                        "user information": "user-info",
                        "preferences": "preferences",
                        "project context": "project",
                        "important notes": "important",
                    }
                    
                    category = category_map.get(
                        section_title.lower(),
                        "long-term"
                    )
                    
                    self.db.add_memory(
                        content=f"## {section_title}\n\n{section_content}",
                        category=category,
                        importance=4,
                        source="migrated-long-term",
                        tags=["long-term", section_title.lower()]
                    )
    
    def run_full_migration(self) -> dict:
        """
        Run complete migration from markdown to SQLite.
        
        Returns:
            Dictionary with migration results
        """
        results = {
            "daily_notes_migrated": 0,
            "long_term_migrated": False,
            "total_memories_in_db": 0,
        }
        
        print("Starting memory migration...")
        
        # Migrate daily notes
        results["daily_notes_migrated"] = self.migrate_daily_notes()
        print(f"✓ Migrated {results['daily_notes_migrated']} daily note files")
        
        # Migrate long-term memory
        results["long_term_migrated"] = self.migrate_long_term_memory()
        print(f"✓ Migrated MEMORY.md: {results['long_term_migrated']}")
        
        # Get final stats
        stats = self.db.get_memory_stats()
        results["total_memories_in_db"] = stats.get("total_memories", 0)
        print(f"✓ Total memories in database: {results['total_memories_in_db']}")
        
        return results
    
    def verify_migration(self) -> dict:
        """
        Verify migration was successful.
        
        Returns:
            Verification results
        """
        stats = self.db.get_memory_stats()
        
        return {
            "total_memories": stats.get("total_memories", 0),
            "categories": stats.get("by_category", {}),
            "importance_distribution": stats.get("by_importance", {}),
            "total_tags": stats.get("total_tags", 0),
            "top_tags": stats.get("top_tags", {}),
        }
