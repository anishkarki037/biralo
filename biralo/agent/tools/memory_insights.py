"""Memory insights tool for the agent."""

from pathlib import Path
from typing import Optional, Dict, Any

from biralo.agent.tools.base import Tool


class MemoryInsightsTool(Tool):
    """
    Tool for getting memory consolidation insights and recommendations.
    
    Use this tool when:
    - Identifying important memories that should be consolidated
    - Finding frequently accessed information
    - Getting suggestions for memory organization
    - Understanding memory patterns
    """
    
    name = "memory_insights"
    description = """
    Get insights and recommendations about memories.
    
    Use this tool when:
    - Identifying important memories for consolidation
    - Finding frequently accessed information
    - Getting suggestions for memory organization
    - Understanding memory patterns over time
    
    Returns:
    - Consolidation candidates (high importance, frequently accessed)
    - Suggestions for memory organization
    - Memory summary by importance
    - Duplicate/similar memory detection
    """
    
    def __init__(self, workspace: Path):
        from biralo.agent.memory import MemoryStore
        from biralo.agent.memory_db import MemoryDatabase
        from biralo.agent.memory_consolidation import MemoryConsolidationService
        self.workspace = workspace
        self.memory = MemoryStore(workspace)
        self.db = MemoryDatabase(workspace)
        self.consolidation = MemoryConsolidationService(workspace)
    
    @property
    def parameters(self) -> dict:
        """Return tool parameters schema."""
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["report", "candidates", "summary", "all"],
                    "description": "Type of insights to retrieve",
                    "default": "report"
                },
                "days": {
                    "type": "integer",
                    "description": "Number of days to look back",
                    "default": 7
                }
            },
            "required": ["action"]
        }
    
    async def execute(self, action: str = "report", days: int = 7) -> str:
        """Execute memory insights query."""
        if action == "report":
            return await self._get_report(days)
        elif action == "candidates":
            return await self._get_candidates(days)
        elif action == "summary":
            return await self._get_summary()
        elif action == "all":
            return await self._get_all(days)
        else:
            return f"Unknown action: {action}"
    
    async def _get_report(self, days: int) -> str:
        """Get comprehensive consolidation report."""
        report = self.consolidation.get_consolidation_report(days)
        
        lines = [f"# Memory Consolidation Report ({days} days)\n"]
        lines.append(f"Generated: {report['generated_at']}\n\n")
        lines.append(f"**Total Candidates**: {report['total_candidates']}\n\n")
        
        lines.append("## Suggestions\n")
        for suggestion in report['suggestions']:
            lines.append(f"- {suggestion}\n")
        
        lines.append("\n## By Category\n")
        for cat, mems in report['by_category'].items():
            lines.append(f"\n### {cat} ({len(mems)} memories)\n")
            for mem in mems[:5]:  # Show top 5 per category
                lines.append(f"- [{mem['importance']}⭐] {mem['content'][:80]}...\n")
        
        return "".join(lines)
    
    async def _get_candidates(self, days: int) -> str:
        """Get consolidation candidates."""
        candidates = self.db.get_consolidation_candidates(days)
        
        if not candidates:
            return "No consolidation candidates found."
        
        lines = [f"# Consolidation Candidates ({days} days)\n\n"]
        lines.append(f"Found {len(candidates)} candidates:\n\n")
        
        for mem in candidates:
            stars = "⭐" * mem['importance']
            lines.append(f"## ID: {mem['id']} {stars}\n")
            lines.append(f"**Category**: {mem['category']}\n")
            lines.append(f"**Access Count**: {mem['access_count']}\n")
            lines.append(f"**Created**: {mem['created_at']}\n")
            lines.append(f"\n{_truncate(mem['content'], 200)}\n")
            lines.append("\n---\n\n")
        
        return "".join(lines)
    
    async def _get_summary(self) -> str:
        """Get memory summary."""
        summary = self.consolidation.get_memory_summary(limit=10)
        
        lines = ["# Memory Summary\n\n"]
        lines.append(f"Generated: {summary['summary_timestamp']}\n\n")
        
        lines.append("## Top Memories\n")
        for mem in summary['top_memories']:
            lines.append(f"- [{mem['importance']}⭐] {mem['content'][:80]}...")
            lines.append(f" (accessed {mem['access_count']} times)\n")
        
        return "".join(lines)
    
    async def _get_all(self, days: int) -> str:
        """Get all insights."""
        report = await self._get_report(days)
        summary = await self._get_summary()
        
        return f"{report}\n\n{summary}"


def _truncate(text: str, length: int) -> str:
    """Truncate text to length."""
    if len(text) <= length:
        return text
    return text[:length] + "..."
