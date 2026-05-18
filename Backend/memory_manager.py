"""
Memory Management System
Stores conversation history and execution logs for learning
"""
import json
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

from config import MEMORY_DIR, MEMORY_FILE, CONVERSATION_HISTORY_FILE, MAX_MEMORY_ITEMS, DEBUG

logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)
logger = logging.getLogger(__name__)


class MemoryManager:
    """
    Manages conversation history and action memory
    """
    
    def __init__(self):
        self.memory_file = MEMORY_DIR / "memory.json"
        self.conversation_file = MEMORY_DIR / "conversation.json"
        self.memory = self._load_memory()
        self.conversation_history = self._load_conversation()
        logger.info("MemoryManager initialized")
    
    # ========================
    # MEMORY STORAGE
    # ========================
    
    def _load_memory(self) -> Dict[str, Any]:
        """Load memory from file"""
        try:
            if self.memory_file.exists():
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                logger.debug(f"Loaded {len(data.get('items', []))} memory items")
                return data
        except Exception as e:
            logger.error(f"Load memory error: {str(e)}")
        
        return {
            'items': [],
            'created': datetime.now().isoformat(),
            'updated': datetime.now().isoformat()
        }
    
    def _save_memory(self):
        """Save memory to file"""
        try:
            self.memory['updated'] = datetime.now().isoformat()
            
            # Keep only max items
            if len(self.memory['items']) > MAX_MEMORY_ITEMS:
                self.memory['items'] = self.memory['items'][-MAX_MEMORY_ITEMS:]
            
            with open(self.memory_file, 'w') as f:
                json.dump(self.memory, f, indent=2)
            
            logger.debug("Memory saved")
        except Exception as e:
            logger.error(f"Save memory error: {str(e)}")
    
    def _load_conversation(self) -> List[Dict]:
        """Load conversation history"""
        try:
            if self.conversation_file.exists():
                with open(self.conversation_file, 'r') as f:
                    history = json.load(f)
                logger.debug(f"Loaded {len(history)} conversation items")
                return history
        except Exception as e:
            logger.error(f"Load conversation error: {str(e)}")
        
        return []
    
    def _save_conversation(self):
        """Save conversation history"""
        try:
            # Keep only max items
            history = self.conversation_history[-MAX_MEMORY_ITEMS:]
            
            with open(self.conversation_file, 'w') as f:
                json.dump(history, f, indent=2)
            
            logger.debug("Conversation saved")
        except Exception as e:
            logger.error(f"Save conversation error: {str(e)}")
    
    # ========================
    # MEMORY OPERATIONS
    # ========================
    
    def store_memory(self, key: str, value: Any, category: str = "general"):
        """
        Store a memory item
        
        Args:
            key: Memory key
            value: Memory value
            category: Category for organization
        """
        try:
            item = {
                'key': key,
                'value': value,
                'category': category,
                'timestamp': datetime.now().isoformat()
            }
            
            self.memory['items'].append(item)
            self._save_memory()
            logger.debug(f"Stored memory: {key}")
            return True
            
        except Exception as e:
            logger.error(f"Store memory error: {str(e)}")
            return False
    
    def get_memory(self, key: str):
        """Retrieve a memory item"""
        try:
            for item in reversed(self.memory['items']):
                if item.get('key') == key:
                    return item.get('value')
            return None
        except Exception as e:
            logger.error(f"Get memory error: {str(e)}")
            return None
    
    def get_memories_by_category(self, category: str) -> List[Dict]:
        """Get all memories in a category"""
        try:
            items = [
                item for item in self.memory['items']
                if item.get('category') == category
            ]
            return items
        except Exception as e:
            logger.error(f"Get memories by category error: {str(e)}")
            return []
    
    def delete_memory(self, key: str) -> bool:
        """Delete a memory item"""
        try:
            self.memory['items'] = [
                item for item in self.memory['items']
                if item.get('key') != key
            ]
            self._save_memory()
            return True
        except Exception as e:
            logger.error(f"Delete memory error: {str(e)}")
            return False
    
    def clear_memory(self) -> bool:
        """Clear all memory"""
        try:
            self.memory['items'] = []
            self._save_memory()
            logger.info("Memory cleared")
            return True
        except Exception as e:
            logger.error(f"Clear memory error: {str(e)}")
            return False
    
    # ========================
    # CONVERSATION HISTORY
    # ========================
    
    def add_conversation(self, role: str, content: str, metadata: Dict = None):
        """Add message to conversation history"""
        try:
            message = {
                'role': role,
                'content': content,
                'timestamp': datetime.now().isoformat(),
                'metadata': metadata or {}
            }
            
            self.conversation_history.append(message)
            self._save_conversation()
            logger.debug(f"Added {role} message to conversation")
            return True
            
        except Exception as e:
            logger.error(f"Add conversation error: {str(e)}")
            return False
    
    def get_conversation_history(self, limit: int = None) -> List[Dict]:
        """Get conversation history"""
        try:
            history = self.conversation_history
            if limit:
                history = history[-limit:]
            return history
        except Exception as e:
            logger.error(f"Get conversation error: {str(e)}")
            return []
    
    def get_conversation_context(self, num_messages: int = 10) -> str:
        """Get formatted conversation context for AI"""
        try:
            recent = self.conversation_history[-num_messages:]
            
            context = ""
            for msg in recent:
                role = msg['role'].upper()
                content = msg['content'][:100]  # Truncate for context
                context += f"{role}: {content}\n"
            
            return context
        except Exception as e:
            logger.error(f"Get conversation context error: {str(e)}")
            return ""
    
    def clear_conversation(self) -> bool:
        """Clear conversation history"""
        try:
            self.conversation_history = []
            self._save_conversation()
            logger.info("Conversation cleared")
            return True
        except Exception as e:
            logger.error(f"Clear conversation error: {str(e)}")
            return False
    
    # ========================
    # ACTION HISTORY
    # ========================
    
    def store_action(self, action: Dict, result: Dict, plan_id: str = None):
        """Store execution history"""
        try:
            entry = {
                'type': 'action',
                'action': action,
                'result': result,
                'plan_id': plan_id,
                'timestamp': datetime.now().isoformat()
            }
            
            self.store_memory(
                f"action_{datetime.now().timestamp()}",
                entry,
                category="actions"
            )
            return True
            
        except Exception as e:
            logger.error(f"Store action error: {str(e)}")
            return False
    
    def get_action_history(self, limit: int = 20) -> List[Dict]:
        """Get recent action history"""
        try:
            items = self.get_memories_by_category("actions")
            return items[-limit:] if limit else items
        except Exception as e:
            logger.error(f"Get action history error: {str(e)}")
            return []
    
    # ========================
    # INSIGHTS & LEARNING
    # ========================
    
    def get_common_tasks(self) -> Dict[str, int]:
        """Get most common task patterns"""
        try:
            tasks = {}
            for item in self.memory['items']:
                if item.get('category') == 'actions':
                    action_type = item.get('value', {}).get('action', {}).get('tool')
                    if action_type:
                        tasks[action_type] = tasks.get(action_type, 0) + 1
            
            return sorted(tasks.items(), key=lambda x: x[1], reverse=True)
        except Exception as e:
            logger.error(f"Get common tasks error: {str(e)}")
            return {}
    
    def get_success_rate(self) -> float:
        """Calculate overall success rate"""
        try:
            actions = self.get_memories_by_category("actions")
            if not actions:
                return 0
            
            successful = sum(
                1 for item in actions
                if item.get('value', {}).get('result', {}).get('success', False)
            )
            
            return (successful / len(actions)) * 100
        except Exception as e:
            logger.error(f"Get success rate error: {str(e)}")
            return 0
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get memory statistics"""
        try:
            return {
                'total_memories': len(self.memory['items']),
                'conversation_length': len(self.conversation_history),
                'success_rate': self.get_success_rate(),
                'common_tasks': dict(self.get_common_tasks()),
                'created': self.memory.get('created'),
                'last_updated': self.memory.get('updated'),
            }
        except Exception as e:
            logger.error(f"Get statistics error: {str(e)}")
            return {}


# ========================
# GLOBAL INSTANCE
# ========================

_memory_manager = None

def get_memory_manager():
    """Get global memory manager"""
    global _memory_manager
    if _memory_manager is None:
        _memory_manager = MemoryManager()
    return _memory_manager

# Convenience functions
def store_memory(key, value, category="general"):
    return get_memory_manager().store_memory(key, value, category)

def get_memory(key):
    return get_memory_manager().get_memory(key)

def add_conversation(role, content, metadata=None):
    return get_memory_manager().add_conversation(role, content, metadata)

def get_conversation_history(limit=None):
    return get_memory_manager().get_conversation_history(limit)

def get_conversation_context(num_messages=10):
    return get_memory_manager().get_conversation_context(num_messages)

if __name__ == "__main__":
    print("Testing MemoryManager...")
    
    manager = get_memory_manager()
    
    # Test memory storage
    manager.store_memory("test_key", "test_value", "testing")
    print("✅ Memory stored")
    
    # Test retrieval
    value = manager.get_memory("test_key")
    print(f"✅ Memory retrieved: {value}")
    
    # Test conversation
    manager.add_conversation("user", "Hello")
    manager.add_conversation("assistant", "Hi there!")
    print("✅ Conversation stored")
    
    # Test statistics
    stats = manager.get_statistics()
    print(f"✅ Statistics: {stats}")
    
    print("\n✅ MemoryManager tests complete")
