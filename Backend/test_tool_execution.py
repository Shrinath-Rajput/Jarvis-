#!/usr/bin/env python3
"""
Test script to verify tool execution is working
Run this to diagnose tool execution issues
"""
import asyncio
import logging
import sys
sys.path.insert(0, '.')

from tool_implementations import (
    launch_application,
    open_website,
    search_google,
    type_text
)
from tool_registry import get_tool_registry
from tool_implementations import register_all_tools

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_tools():
    """Test all tools to ensure they execute"""
    
    logger.info("=" * 70)
    logger.info("🧪 TOOL EXECUTION TEST")
    logger.info("=" * 70)
    
    # Register all tools
    logger.info("\n📦 Registering tools...")
    registry = register_all_tools()
    available_tools = [t.name for t in registry.get_all_tools()]
    logger.info(f"✅ Registered {len(available_tools)} tools: {available_tools}")
    
    # Test 1: Direct function call
    logger.info("\n" + "─"*70)
    logger.info("TEST 1: Direct function execution")
    logger.info("─"*70)
    
    try:
        logger.info("Calling open_website('google') directly...")
        result = await open_website('google')
        logger.info(f"Result: {result}")
        if result['success']:
            logger.info("✅ Direct call succeeded")
        else:
            logger.error(f"❌ Direct call failed: {result.get('error')}")
    except Exception as e:
        logger.error(f"❌ Exception in direct call: {e}", exc_info=True)
    
    # Test 2: Registry execution
    logger.info("\n" + "─"*70)
    logger.info("TEST 2: Tool registry execution")
    logger.info("─"*70)
    
    try:
        logger.info("Executing via registry: open_website...")
        result = await registry.execute_tool('open_website', site_name='youtube')
        logger.info(f"Result: {result}")
        if result['success']:
            logger.info("✅ Registry call succeeded")
        else:
            logger.error(f"❌ Registry call failed: {result.get('error')}")
    except Exception as e:
        logger.error(f"❌ Exception in registry call: {e}", exc_info=True)
    
    # Test 3: Search
    logger.info("\n" + "─"*70)
    logger.info("TEST 3: Search execution")
    logger.info("─"*70)
    
    try:
        logger.info("Executing: search_google...")
        result = await registry.execute_tool('search_google', query='hello world')
        logger.info(f"Result: {result}")
        if result['success']:
            logger.info("✅ Search call succeeded")
        else:
            logger.error(f"❌ Search call failed: {result.get('error')}")
    except Exception as e:
        logger.error(f"❌ Exception in search call: {e}", exc_info=True)
    
    logger.info("\n" + "="*70)
    logger.info("🧪 TEST COMPLETE")
    logger.info("="*70)

if __name__ == "__main__":
    asyncio.run(test_tools())
