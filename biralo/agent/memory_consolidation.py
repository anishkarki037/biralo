"""Automatic memory consolidation service."""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pathlib import Path

from biralo.agent.memory_db import MemoryDatabase


class MemoryConsolidationService:
    """
    Automatically consolidate daily memories into long-term memory.
    
    This service:
    - Identifies important memories from recent days
    - Groups related memories by topic
    - Suggests consolidation to long-term memory
    - Removes redundant memories
    """
    
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.db = MemoryDatabase(workspace)
    
    def get_consolidation_report(self, days: int = 7) -> Dict[str, Any]:
        """
        Generate a consolidation report.
        
        Args:
            days: Number of days to analyze
        
        Returns:
            Report with consolidation candidates and suggestions
        """
        candidates = self.db.get_consolidation_candidates(days)
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "days_analyzed": days,
            "total_candidates": len(candidates),
            "by_category": {},
            "suggestions": [],
        }
        
        # Group by category
        for mem in candidates:
            category = mem['category']
            if category not in report["by_category"]:
                report["by_category"][category] = []
            report["by_category"][category].append({
                "id": mem['id'],
                "content": mem['content'][:100] + "..." if len(mem['content']) > 100 else mem['content'],
                "importance": mem['importance'],
                "access_count": mem['access_count'],
                "created_at": mem['created_at'],
            })
        
        # Generate suggestions
        report["suggestions"] = self._generate_suggestions(candidates)
        
        return report
    
    def _generate_suggestions(self, candidates: List[Dict[str, Any]]) -> List[str]:
        """Generate consolidation suggestions."""
        suggestions = []
        
        if not candidates:
            return ["No consolidation candidates found."]
        
        # Group by importance
        by_importance = {}
        for mem in candidates:
            imp = mem['importance']
            if imp not in by_importance:
                by_importance[imp] = 0
            by_importance[imp] += 1
        
        # High importance memories
        high_imp = by_importance.get(5, 0) + by_importance.get(4, 0)
        if high_imp > 0:
            suggestions.append(
                f"Consider consolidating {high_imp} high-importance memories "
                f"into a dedicated long-term section."
            )
        
        # Frequently accessed
        frequently_accessed = sum(1 for m in candidates if m['access_count'] >= 3)
        if frequently_accessed > 0:
            suggestions.append(
                f"{frequently_accessed} memories are frequently accessed - "
                f"these are likely important for context."
            )
        
        # Duplicate detection
        duplicates = self._find_similar_memories(candidates)
        if duplicates:
            suggestions.append(
                f"Found {len(duplicates)} groups of similar memories - "
                f"consider merging related memories."
            )
        
        return suggestions
    
    def _find_similar_memories(self, memories: List[Dict[str, Any]]) -> List[List[int]]:
        """Find potentially similar/duplicate memories."""
        similar_groups = []
        checked = set()
        
        for i, mem1 in enumerate(memories):
            if i in checked:
                continue
            
            group = [mem1['id']]
            content1 = mem1['content'].lower()
            
            for j, mem2 in enumerate(memories[i + 1:], i + 1):
                if j in checked:
                    continue
                
                content2 = mem2['content'].lower()
                
                # Simple similarity check (word overlap)
                words1 = set(content1.split())
                words2 = set(content2.split())
                
                if words1 and words2:
                    overlap = len(words1 & words2) / len(words1 | words2)
                    if overlap > 0.5:  # 50% similarity threshold
                        group.append(mem2['id'])
                        checked.add(j)
            
            if len(group) > 1:
                similar_groups.append(group)
                checked.add(i)
        
        return similar_groups
    
    def consolidate_memories(
        self,
        memory_ids: List[int],
        section: str,
        consolidation_note: str = ""
    ) -> None:
        """
        Consolidate a group of memories into long-term memory.
        
        Args:
            memory_ids: IDs of memories to consolidate
            section: Section in long-term memory to consolidate into
            consolidation_note: Note about consolidation
        """
        # Get memories content
        cursor = self.db.conn.cursor()
        memories_content = []
        
        for mem_id in memory_ids:
            cursor.execute("SELECT content, created_at FROM memories WHERE id = ?", (mem_id,))
            row = cursor.fetchone()
            if row:
                memories_content.append(f"- {row['content']} *(from {row['created_at']})*")
        
        # Build consolidated content
        consolidated = "\n".join(memories_content)
        
        # Get existing section or create new
        long_term = self.db.get_long_term_memory(section)
        
        if section in long_term:
            # Append to existing section
            new_content = long_term[section] + "\n\n" + consolidated
        else:
            # Create new section
            new_content = f"## {section}\n\n{consolidated}"
        
        self.db.save_long_term_memory(section, new_content)
        
        # Mark memories as consolidated
        for mem_id in memory_ids:
            self.db.mark_consolidated(mem_id, consolidation_note)
    
    def auto_consolidate(self, days: int = 7, threshold: int = 4) -> Dict[str, Any]:
        """
        Automatically consolidate high-importance memories.
        
        Args:
            days: Number of days to look back
            threshold: Importance threshold (1-5)
        
        Returns:
            Summary of auto-consolidation
        """
        cursor = self.db.conn.cursor()
        
        # Find high-importance memories from the period
        cutoff = datetime.now() - timedelta(days=days)
        cursor.execute("""
            SELECT * FROM memories
            WHERE importance >= ? AND is_consolidated = 0 AND created_at >= ?
            ORDER BY importance DESC, category
        """, (threshold, cutoff.isoformat()))
        
        memories = [dict(row) for row in cursor.fetchall()]
        
        summary = {
            "consolidation_timestamp": datetime.now().isoformat(),
            "memories_consolidated": 0,
            "by_category": {},
        }
        
        # Group by category and consolidate
        current_category = None
        category_memories = []
        
        for mem in memories:
            if current_category is None:
                current_category = mem['category']
            
            if mem['category'] != current_category:
                # Consolidate previous category
                if category_memories:
                    section = current_category.replace("-", " ").title()
                    mem_ids = [m['id'] for m in category_memories]
                    self.consolidate_memories(
                        mem_ids,
                        section,
                        "Auto-consolidated by consolidation service"
                    )
                    
                    summary["by_category"][current_category] = len(category_memories)
                    summary["memories_consolidated"] += len(category_memories)
                
                current_category = mem['category']
                category_memories = []
            
            category_memories.append(mem)
        
        # Consolidate last category
        if category_memories:
            section = current_category.replace("-", " ").title()
            mem_ids = [m['id'] for m in category_memories]
            self.consolidate_memories(
                mem_ids,
                section,
                "Auto-consolidated by consolidation service"
            )
            
            summary["by_category"][current_category] = len(category_memories)
            summary["memories_consolidated"] += len(category_memories)
        
        return summary
    
    def cleanup_old_memories(self, days: int = 90) -> Dict[str, Any]:
        """
        Archive or clean up old memories.
        
        Args:
            days: Only keep memories newer than this
        
        Returns:
            Summary of cleanup
        """
        cursor = self.db.conn.cursor()
        
        cutoff = datetime.now() - timedelta(days=days)
        
        # Count old memories
        cursor.execute("""
            SELECT COUNT(*) as count FROM memories
            WHERE created_at < ? AND is_consolidated = 0
        """, (cutoff.isoformat(),))
        
        count_to_remove = cursor.fetchone()['count']
        
        # For now, just mark them as consolidated (archive)
        cursor.execute("""
            UPDATE memories
            SET is_consolidated = 1, consolidation_note = ?
            WHERE created_at < ? AND is_consolidated = 0
        """, ("Archived by cleanup service", cutoff.isoformat()))
        
        self.db.conn.commit()
        
        return {
            "cleanup_timestamp": datetime.now().isoformat(),
            "memories_archived": count_to_remove,
            "cutoff_date": cutoff.isoformat(),
            "reason": f"Older than {days} days",
        }
    
    def get_memory_summary(self, limit: int = 5) -> Dict[str, Any]:
        """
        Get a summary of important memories for context.
        
        Args:
            limit: Number of top memories to include
        
        Returns:
            Summary of top memories by importance and access
        """
        cursor = self.db.conn.cursor()
        
        # Top memories by importance
        cursor.execute("""
            SELECT id, content, importance, access_count, created_at
            FROM memories
            WHERE is_consolidated = 0
            ORDER BY importance DESC, access_count DESC
            LIMIT ?
        """, (limit,))
        
        top_memories = [dict(row) for row in cursor.fetchall()]
        
        return {
            "summary_timestamp": datetime.now().isoformat(),
            "total_active_memories": len(top_memories),
            "top_memories": [
                {
                    "content": m['content'][:80] + "..." if len(m['content']) > 80 else m['content'],
                    "importance": m['importance'],
                    "access_count": m['access_count'],
                    "created_at": m['created_at'],
                }
                for m in top_memories
            ],
        }
