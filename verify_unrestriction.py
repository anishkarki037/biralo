import asyncio
import os
from pathlib import Path
from biralo.agent.tools.shell import ExecTool
from biralo.config.schema import ExecToolConfig

async def test_exec_tool_unrestriction():
    print("Testing ExecTool un-restriction...")
    
    # 1. Test default blocks are still there
    tool = ExecTool()
    result = await tool.execute("rm -rf /")
    print(f"Default block check ('rm -rf /'): {result}")
    assert "blocked" in result.lower()
    
    # 2. Test configurable pattern addition
    custom_deny = [r"\bnanobot\b"]
    tool_custom = ExecTool(deny_patterns=custom_deny)
    result = await tool_custom.execute("echo nanobot")
    print(f"Custom block check ('echo nanobot'): {result}")
    assert "blocked" in result.lower()
    
    # 3. Test that normal commands still work
    result = await tool.execute("echo 'Status: Unrestricted'")
    print(f"Normal command check: {result}")
    assert "Unrestricted" in result
    
    # 4. Test Config Schema
    config = ExecToolConfig(timeout=30, deny_patterns=[".*secret.*"])
    print(f"Config schema check: timeout={config.timeout}, deny_patterns={config.deny_patterns}")
    assert config.timeout == 30
    assert ".*secret.*" in config.deny_patterns

if __name__ == "__main__":
    asyncio.run(test_exec_tool_unrestriction())
    print("\nVerification complete!")
