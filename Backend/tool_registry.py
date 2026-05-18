"""
Dynamic Tool Registry System
Centralized system for tool discovery, registration, and execution
Replaces hardcoded logic with flexible tool definitions
"""
import logging
import json
from typing import Dict, List, Callable, Any, Optional
from enum import Enum
import inspect

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ToolCategory(str, Enum):
    """Tool categories for organization and discovery"""
    APPLICATION = "application"        # Open apps, software
    BROWSER = "browser"                # Browser control, navigation
    FILE_SYSTEM = "file_system"        # File/folder operations
    KEYBOARD = "keyboard"              # Keyboard input
    MOUSE = "mouse"                    # Mouse operations
    SYSTEM = "system"                  # System operations
    INFORMATION = "information"        # Information retrieval
    MEDIA = "media"                    # Media operations
    CODING = "coding"                  # Code editing, commands
    COMMUNICATION = "communication"    # Email, messaging


class ToolParameter:
    """Definition of a tool parameter"""
    
    def __init__(self, name: str, param_type: str, required: bool = False, 
                 description: str = "", default: Any = None):
        self.name = name
        self.param_type = param_type
        self.required = required
        self.description = description
        self.default = default
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "type": self.param_type,
            "required": self.required,
            "description": self.description,
            "default": self.default
        }


class Tool:
    """
    Represents an available tool the AI can use
    Tools are self-contained units of functionality with clear inputs/outputs
    """
    
    def __init__(
        self,
        name: str,
        category: ToolCategory,
        function: Callable,
        description: str,
        parameters: List[ToolParameter] = None,
        examples: List[Dict] = None,
        dependencies: List[str] = None,
        enabled: bool = True
    ):
        self.name = name
        self.category = category
        self.function = function
        self.description = description
        self.parameters = parameters or []
        self.examples = examples or []
        self.dependencies = dependencies or []
        self.enabled = enabled
        self.execution_count = 0
        self.success_count = 0
        self.error_count = 0
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool with given parameters
        
        Returns:
            {
                "success": bool,
                "result": Any,
                "error": Optional[str],
                "metadata": Dict
            }
        """
        try:
            self.execution_count += 1
            
            # Validate parameters
            missing_params = []
            for param in self.parameters:
                if param.required and param.name not in kwargs:
                    missing_params.append(param.name)
            
            if missing_params:
                return {
                    "success": False,
                    "result": None,
                    "error": f"Missing required parameters: {', '.join(missing_params)}"
                }
            
            # Execute function
            result = await self.function(**kwargs) if inspect.iscoroutinefunction(self.function) else self.function(**kwargs)
            
            self.success_count += 1
            
            return {
                "success": True,
                "result": result,
                "error": None,
                "tool": self.name,
                "category": self.category.value
            }
            
        except Exception as e:
            self.error_count += 1
            error_msg = f"Tool execution error: {str(e)}"
            logger.error(error_msg)
            
            return {
                "success": False,
                "result": None,
                "error": error_msg,
                "tool": self.name,
                "exception_type": type(e).__name__
            }
    
    def get_stats(self) -> Dict:
        """Get execution statistics for this tool"""
        success_rate = (self.success_count / self.execution_count * 100) if self.execution_count > 0 else 0
        return {
            "name": self.name,
            "executions": self.execution_count,
            "successes": self.success_count,
            "errors": self.error_count,
            "success_rate": f"{success_rate:.1f}%"
        }
    
    def to_dict(self) -> Dict:
        """Convert tool to dictionary for LLM context"""
        return {
            "name": self.name,
            "category": self.category.value,
            "description": self.description,
            "parameters": [p.to_dict() for p in self.parameters],
            "examples": self.examples,
            "enabled": self.enabled
        }


class ToolRegistry:
    """
    Central registry for all available tools
    Manages tool discovery, registration, and execution
    """
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self.categories: Dict[ToolCategory, List[str]] = {cat: [] for cat in ToolCategory}
        self.tool_aliases: Dict[str, str] = {}  # Aliases for tools
        logger.info("🔧 ToolRegistry initialized")
    
    def register(self, tool: Tool) -> None:
        """Register a tool in the registry"""
        if tool.name in self.tools:
            logger.warning(f"⚠️ Tool '{tool.name}' already registered, overwriting")
        
        self.tools[tool.name] = tool
        self.categories[tool.category].append(tool.name)
        logger.info(f"✅ Registered tool: {tool.name} ({tool.category.value})")
    
    def add_alias(self, alias: str, tool_name: str) -> None:
        """Add an alias for a tool (e.g., 'navigate' -> 'open_website')"""
        if tool_name not in self.tools:
            logger.warning(f"⚠️ Tool '{tool_name}' not found, cannot create alias")
            return
        
        self.tool_aliases[alias] = tool_name
        logger.info(f"✅ Added alias '{alias}' -> '{tool_name}'")
    
    def get_tool(self, tool_name: str) -> Optional[Tool]:
        """Get a tool by name (with alias resolution)"""
        # Resolve alias if needed
        if tool_name in self.tool_aliases:
            tool_name = self.tool_aliases[tool_name]
        
        return self.tools.get(tool_name)
    
    def get_tools_by_category(self, category: ToolCategory) -> List[Tool]:
        """Get all tools in a category"""
        tool_names = self.categories[category]
        return [self.tools[name] for name in tool_names if self.tools[name].enabled]
    
    def get_all_tools(self, enabled_only: bool = True) -> List[Tool]:
        """Get all registered tools"""
        tools = list(self.tools.values())
        if enabled_only:
            tools = [t for t in tools if t.enabled]
        return tools
    
    def search_tools(self, query: str) -> List[Tool]:
        """Search for tools by name or description"""
        query = query.lower()
        results = []
        
        for tool in self.tools.values():
            if not tool.enabled:
                continue
            
            if (query in tool.name.lower() or 
                query in tool.description.lower()):
                results.append(tool)
        
        return results
    
    async def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Execute a tool and return results"""
        tool = self.get_tool(tool_name)
        
        if not tool:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found"
            }
        
        if not tool.enabled:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' is disabled"
            }
        
        logger.info(f"🔨 Executing tool: {tool_name} with params: {kwargs}")
        return await tool.execute(**kwargs)
    
    def get_tools_for_llm(self) -> str:
        """
        Get formatted tool descriptions for LLM context
        Used to inform the AI what tools are available
        """
        tools_by_category = {}
        
        for tool in self.get_all_tools():
            cat = tool.category.value
            if cat not in tools_by_category:
                tools_by_category[cat] = []
            tools_by_category[cat].append(tool.to_dict())
        
        return json.dumps(tools_by_category, indent=2)
    
    def get_statistics(self) -> Dict:
        """Get statistics about tool usage"""
        return {
            "total_tools": len(self.tools),
            "enabled_tools": len([t for t in self.tools.values() if t.enabled]),
            "total_executions": sum(t.execution_count for t in self.tools.values()),
            "total_successes": sum(t.success_count for t in self.tools.values()),
            "total_errors": sum(t.error_count for t in self.tools.values()),
            "tools_stats": [t.get_stats() for t in self.tools.values()]
        }


# Global registry instance
_registry: Optional[ToolRegistry] = None


def get_tool_registry() -> ToolRegistry:
    """Get or create the global tool registry"""
    global _registry
    if _registry is None:
        _registry = ToolRegistry()
    return _registry


def register_tool(name: str, category: ToolCategory, function: Callable,
                 description: str, parameters: List[ToolParameter] = None,
                 examples: List[Dict] = None) -> None:
    """
    Convenience function to register a tool
    
    Usage:
        @register_tool("click_button", ToolCategory.MOUSE, description="Click a button")
        def click_button(text: str):
            ...
    """
    tool = Tool(
        name=name,
        category=category,
        function=function,
        description=description,
        parameters=parameters or [],
        examples=examples or []
    )
    get_tool_registry().register(tool)
