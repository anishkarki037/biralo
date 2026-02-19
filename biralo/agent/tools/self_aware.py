"""Self-awareness tool for agent reflection and goal tracking."""

from pathlib import Path
from typing import Optional, Dict, Any
import json
import re

from biralo.agent.tools.base import Tool


class SelfAwareTool(Tool):
    """
    Tool for self-reflection, goal tracking, and autonomous learning.
    
    Use this tool when:
    - After completing a task (reflect on what happened)
    - Setting goals (define what to achieve)
    - When uncertain about progress
    - For meta-learning (learning how to learn)
    - Before starting new tasks (apply past improvements)
    """
    
    name = "self_aware"
    description = """
    Self-reflection, goal tracking, and autonomous learning.
    
    Use when:
    - After completing a task (reflect on what happened)
    - Setting goals (define what to achieve)
    - When uncertain about progress
    - For meta-learning (learning how to learn)
    - Before starting new tasks (apply past improvements)
    """
    
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.improvements_file = workspace / "improvements.json"
    
    def _load_improvements(self) -> dict:
        """Load improvements from file."""
        if self.improvements_file.exists():
            try:
                return json.loads(self.improvements_file.read_text())
            except:
                return {}
        return {}
    
    def _save_improvements(self, data: dict) -> None:
        """Save improvements to file."""
        self.improvements_file.write_text(json.dumps(data, indent=2))
    
    @property
    def parameters(self) -> dict:
        """Return tool parameters schema."""
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["reflect", "set_goal", "check_goals", "knowledge_gaps", "plan_next", 
                            "apply_improvements", "record_improvement", "show_improvements", "motivate"],
                    "description": "Action to perform"
                },
                "task": {
                    "type": "string",
                    "description": "Task that was completed"
                },
                "result": {
                    "type": "string",
                    "description": "Result of the task"
                },
                "improvement": {
                    "type": "string",
                    "description": "What could be improved"
                },
                "error": {
                    "type": "string",
                    "description": "Error that occurred"
                },
                "solution": {
                    "type": "string",
                    "description": "Solution that worked"
                },
                "goal": {
                    "type": "string",
                    "description": "Goal to set or work toward"
                },
                "milestones": {
                    "type": "string",
                    "description": "Milestones for the goal"
                },
                "topic": {
                    "type": "string",
                    "description": "Topic to analyze"
                },
                "known": {
                    "type": "string",
                    "description": "What is already known"
                },
                "unknown": {
                    "type": "string",
                    "description": "What is unknown"
                },
                "current": {
                    "type": "string",
                    "description": "Current state"
                },
                "next_step": {
                    "type": "string",
                    "description": "Next step to take"
                },
                "context": {
                    "type": "string",
                    "description": "Context for matching improvements"
                },
                "quality": {
                    "type": "string",
                    "description": "Quality rating (e.g., '7/10')"
                }
            },
            "required": ["action"]
        }
    
    async def execute(self, action: str, task: Optional[str] = None, 
                     result: Optional[str] = None, improvement: Optional[str] = None,
                     error: Optional[str] = None, solution: Optional[str] = None,
                     goal: Optional[str] = None, milestones: Optional[str] = None,
                     topic: Optional[str] = None, known: Optional[str] = None,
                     unknown: Optional[str] = None, current: Optional[str] = None,
                     next_step: Optional[str] = None, context: Optional[str] = None,
                     quality: Optional[str] = None) -> str:
        """
        Execute self-awareness actions.
        """
        from biralo.agent.memory import MemoryStore
        memory = MemoryStore(self.workspace)
        
        if action == "reflect":
            if not task:
                return "What task should I reflect on?"
            
            reflection = f"""## Reflection: {task}

**Result:** {result}
**Improvement:** {improvement}
**Quality:** {quality}
"""
            # Save to memory
            memory.append_today(reflection)
            
            # Record improvement if provided
            if improvement:
                await self._record_improvement(task, improvement, quality)
            
            return f"💭 Reflection saved:\n\n{reflection}"
        
        elif action == "record_improvement":
            if not task or not improvement:
                return "Task and improvement are required"
            
            result_text = await self._record_improvement(task, improvement, quality)
            return result_text
        
        elif action == "apply_improvements":
            if not context:
                return "Context is required to find relevant improvements"
            
            improvements = self._get_relevant_improvements(context)
            
            if not improvements:
                return f"No improvements found for context: {context}"
            
            response = f"📋 Improvements for \"{context}\":\n\n"
            for i, imp in enumerate(improvements[:5], 1):
                response += f"{i}. {imp['improvement']}\n"
                response += f"   From: {imp['task'][:50]}...\n"
                response += f"   Times applied: {imp.get('applied', 0)}\n\n"
            
            # Mark as applied
            for imp in improvements:
                imp['applied'] = imp.get('applied', 0) + 1
            
            data = self._load_improvements()
            for imp in improvements:
                for i, stored in enumerate(data.get('improvements', [])):
                    if stored['task'] == imp['task'] and stored['improvement'] == imp['improvement']:
                        data['improvements'][i]['applied'] = imp['applied']
                        break
            self._save_improvements(data)
            
            return response
        
        elif action == "show_improvements":
            data = self._load_improvements()
            imps = data.get('improvements', [])
            
            if not imps:
                return "No improvements recorded yet"
            
            # Sort by applied count
            sorted_imps = sorted(imps, key=lambda x: x.get('applied', 0), reverse=True)
            
            response = f"📊 Top Improvements (sorted by usage):\n\n"
            for i, imp in enumerate(sorted_imps[:10], 1):
                response += f"{i}. {imp['improvement']}\n"
                response += f"   From: {imp['task'][:40]}...\n"
                response += f"   Applied: {imp.get('applied', 0)} times\n\n"
            
            return response
        
        elif action == "set_goal":
            if not goal:
                return "What goal should I set?"
            
            goal_text = f"""## Goal: {goal}

**Milestones:** {milestones}
"""
            memory.append_today(f"### New Goal\n{goal_text}")
            
            return f"🎯 Goal set:\n\n{goal_text}"
        
        elif action == "check_goals":
            recent = memory.read_today()
            
            # Extract goals from today's notes
            goals = re.findall(r'Goal: (.+?)(?:\n|$)', recent)
            
            if goals:
                return f"📋 Active Goals:\n\n" + "\n".join(f"- {g}" for g in goals)
            else:
                return "📋 No goals set yet. Would you like to set one?"
        
        elif action == "knowledge_gaps":
            if not topic:
                return "What topic should I analyze?"
            
            analysis = f"""
🔍 Knowledge Analysis for: {topic}

Known: {known}
Unknown: {unknown}

Suggestions:
- Research the unknown areas
- Start with fundamentals
- Ask clarifying questions
"""
            return analysis
        
        elif action == "plan_next":
            plan = f"""
📍 Current State: {current}

Next Steps:
1. {next_step}
2. Evaluate result
3. Adjust approach

Keep moving forward! 🚀
"""
            return plan
        
        elif action == "motivate":
            quotes = [
                "Every mistake is a learning opportunity.",
                "Progress over perfection.",
                "You're making progress, even if it's not visible yet.",
                "Ask questions when uncertain - that's how we learn.",
                "Small steps lead to big changes."
            ]
            import random
            return f"💪 {random.choice(quotes)}"
        
        else:
            return f"Unknown action: {action}"
    
    async def _record_improvement(self, task: str, improvement: str, quality: Optional[str] = None) -> str:
        """Record an improvement from reflection."""
        data = self._load_improvements()
        
        if 'improvements' not in data:
            data['improvements'] = []
        
        # Check if similar improvement exists
        for imp in data['improvements']:
            if imp['improvement'].lower() == improvement.lower():
                imp['count'] = imp.get('count', 1) + 1
                imp['applied'] = imp.get('applied', 0)
                self._save_improvements(data)
                return f"📝 Updated improvement (count: {imp['count']})"
        
        # Add new improvement
        data['improvements'].append({
            'task': task,
            'improvement': improvement,
            'quality': quality,
            'count': 1,
            'applied': 0
        })
        
        self._save_improvements(data)
        return f"📝 Recorded improvement: {improvement}"
    
    def _get_relevant_improvements(self, context: str) -> list:
        """Get improvements relevant to the current context."""
        data = self._load_improvements()
        imps = data.get('improvements', [])
        
        # Simple keyword matching
        context_lower = context.lower()
        keywords = set(re.findall(r'\w+', context_lower))
        
        scored = []
        for imp in imps:
            task_lower = imp['task'].lower()
            imp_lower = imp['improvement'].lower()
            
            # Score by keyword overlap
            score = 0
            for keyword in keywords:
                if keyword in task_lower or keyword in imp_lower:
                    score += 1
            
            if score > 0:
                scored.append((score, imp))
        
        # Sort by score and apply count
        scored.sort(key=lambda x: (x[0], x[1].get('applied', 0)), reverse=True)
        
        return [imp for _, imp in scored]
