"""
Advanced AI Brain using Google Gemini API
Handles language understanding, reasoning, and response generation
"""
import google.generativeai as genai
import ollama
import json
import logging
import asyncio
from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    PRIMARY_LLM,
    FALLBACK_LLM,
    OLLAMA_MODEL,
    OLLAMA_BASE_URL,
    DEBUG,
)

# Setup logging
logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# ========================
# SYSTEM PROMPTS
# ========================

SYSTEM_PROMPT = """
You are JARVIS - an advanced autonomous AI assistant.

Your capabilities:
- Understand natural language perfectly
- Plan multi-step tasks
- Control computers and applications
- Navigate websites and fill forms
- Analyze images and screenshots
- Execute commands autonomously
- Remember context and history
- Adapt to user preferences
- Think step-by-step before acting

Your personality:
- Professional yet friendly
- Always helpful and thorough
- Think before you act
- Explain your reasoning when needed
- Ask clarifications only when truly necessary
- Be concise but complete

Guidelines:
- Always analyze the user's intent carefully
- Consider multiple approaches if needed
- Plan tasks step-by-step
- Anticipate potential issues
- Prioritize user safety
- Never execute harmful commands
"""

# ========================
# MAIN AI BRAIN
# ========================

class GeminiAI:
    """
    Advanced AI using Google Gemini
    """

    def __init__(self, model=GEMINI_MODEL):
        self.model = genai.GenerativeModel(model)
        self.conversation_history = []
        logger.info(f"Initialized Gemini AI with model: {model}")

    def chat(self, user_message, system_context=""):
        """
        Chat with Gemini AI
        
        Args:
            user_message: User's input text
            system_context: Additional context about current state
            
        Returns:
            AI response text
        """
        try:
            # Prepare context
            context = f"{SYSTEM_PROMPT}\n\nCurrent Context: {system_context}" if system_context else SYSTEM_PROMPT
            
            # Create message with full context
            message = f"{context}\n\nUser: {user_message}"
            
            # Get response
            response = self.model.generate_content(message)
            
            if response and response.text:
                logger.debug(f"Gemini response: {response.text[:200]}...")
                return response.text
            else:
                logger.warning("Empty response from Gemini")
                return "I couldn't generate a response. Please try again."
                
        except Exception as e:
            logger.error(f"Gemini error: {str(e)}")
            # Fallback to Ollama
            return self._fallback_ollama(user_message)

    async def generate_response(self, prompt: str) -> str:
        """
        Generate a response to a prompt (async version for autonomous agent)
        
        Args:
            prompt: The prompt to respond to
            
        Returns:
            Response text
        """
        try:
            logger.info(f"[Gemini] Generating response for prompt ({len(prompt)} chars)")
            
            # Run in thread to avoid blocking async loop
            response = await asyncio.to_thread(self._generate_response_sync, prompt)
            
            if response:
                logger.info(f"[Gemini] ✅ Generated {len(response)} char response")
                return response
            else:
                logger.warning("[Gemini] ⚠️ Empty response generated")
                return None
                
        except Exception as e:
            logger.error(f"[Gemini] ❌ Error generating response: {str(e)}", exc_info=True)
            return None
    
    def _generate_response_sync(self, prompt: str) -> str:
        """
        Synchronous response generation (called from async context)
        
        Args:
            prompt: The prompt to respond to
            
        Returns:
            Response text
        """
        try:
            logger.debug(f"[Gemini] Calling generate_content...")
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                logger.debug(f"[Gemini] Response text: {response.text[:300]}...")
                return response.text
            else:
                logger.warning("[Gemini] No text in response")
                return None
                
        except Exception as e:
            logger.error(f"[Gemini] Sync generation error: {str(e)}", exc_info=True)
            return None

    def analyze_image(self, image_path, question=""):
        """
        Analyze an image using Gemini's vision capabilities
        
        Args:
            image_path: Path to image file
            question: Question about the image
            
        Returns:
            Analysis result
        """
        try:
            import os
            if not os.path.exists(image_path):
                return f"Image file not found: {image_path}"
            
            # Upload file
            myfile = genai.upload_file(image_path)
            logger.info(f"Uploaded file: {image_path}")
            
            # Create prompt
            prompt = question if question else "Please analyze this image and describe what you see."
            
            # Generate content with image
            response = self.model.generate_content(
                [prompt, myfile]
            )
            
            result = response.text if response else "No analysis available"
            logger.debug(f"Vision analysis: {result[:200]}...")
            
            return result
            
        except Exception as e:
            logger.error(f"Vision analysis error: {str(e)}")
            return f"Could not analyze image: {str(e)}"

    def generate_with_streaming(self, user_message, callback=None):
        """
        Generate response with streaming support
        
        Args:
            user_message: User's input
            callback: Function to call with each chunk
            
        Yields:
            Response chunks
        """
        try:
            response = self.model.generate_content(
                f"{SYSTEM_PROMPT}\n\nUser: {user_message}",
                stream=True
            )
            
            full_response = ""
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    if callback:
                        callback(chunk.text)
                    yield chunk.text
                    
            return full_response
            
        except Exception as e:
            logger.error(f"Streaming error: {str(e)}")
            yield f"Error: {str(e)}"

    def _fallback_ollama(self, user_message):
        """Fallback to local Ollama"""
        try:
            logger.info("Falling back to Ollama")
            response = ollama.chat(
                model=OLLAMA_MODEL,
                base_url=OLLAMA_BASE_URL,
                messages=[
                    {
                        'role': 'system',
                        'content': SYSTEM_PROMPT
                    },
                    {
                        'role': 'user',
                        'content': user_message
                    }
                ]
            )
            return response['message']['content']
        except Exception as e:
            logger.error(f"Ollama fallback error: {str(e)}")
            return "Error: Could not generate response"

    def store_in_history(self, role, content):
        """Store message in conversation history"""
        self.conversation_history.append({
            'role': role,
            'content': content
        })
        logger.debug(f"Stored message: {role} - {content[:100]}...")

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Cleared conversation history")


# ========================
# OLLAMA FALLBACK
# ========================

class OllamaAI:
    """
    Fallback local AI using Ollama
    """

    def __init__(self, model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL):
        self.model = model
        self.base_url = base_url
        logger.info(f"Initialized Ollama AI with model: {model}")

    def chat(self, user_message, system_context=""):
        """Chat with Ollama"""
        try:
            response = ollama.chat(
                model=self.model,
                base_url=self.base_url,
                messages=[
                    {
                        'role': 'system',
                        'content': f"{SYSTEM_PROMPT}\n\n{system_context}" if system_context else SYSTEM_PROMPT
                    },
                    {
                        'role': 'user',
                        'content': user_message
                    }
                ]
            )
            return response['message']['content']
        except Exception as e:
            logger.error(f"Ollama error: {str(e)}")
            return "Error: Could not generate response"

    async def generate_response(self, prompt: str) -> str:
        """
        Generate a response to a prompt (async version for autonomous agent)
        
        Args:
            prompt: The prompt to respond to
            
        Returns:
            Response text
        """
        try:
            logger.info(f"[Ollama] Generating response for prompt ({len(prompt)} chars)")
            
            # Run in thread to avoid blocking async loop
            response = await asyncio.to_thread(self._generate_response_sync, prompt)
            
            if response:
                logger.info(f"[Ollama] ✅ Generated {len(response)} char response")
                return response
            else:
                logger.warning("[Ollama] ⚠️ Empty response generated")
                return None
                
        except Exception as e:
            logger.error(f"[Ollama] ❌ Error generating response: {str(e)}", exc_info=True)
            return None
    
    def _generate_response_sync(self, prompt: str) -> str:
        """
        Synchronous response generation (called from async context)
        
        Args:
            prompt: The prompt to respond to
            
        Returns:
            Response text
        """
        try:
            logger.debug(f"[Ollama] Calling chat...")
            response = ollama.chat(
                model=self.model,
                base_url=self.base_url,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ]
            )
            
            if response and 'message' in response and 'content' in response['message']:
                content = response['message']['content']
                logger.debug(f"[Ollama] Response text: {content[:300]}...")
                return content
            else:
                logger.warning("[Ollama] No content in response")
                return None
                
        except Exception as e:
            logger.error(f"[Ollama] Sync generation error: {str(e)}", exc_info=True)
            return None


# ========================
# AI FACTORY
# ========================

def get_ai_instance():
    """Get appropriate AI instance based on configuration"""
    if PRIMARY_LLM == "gemini":
        return GeminiAI()
    elif PRIMARY_LLM == "ollama":
        return OllamaAI()
    else:
        logger.warning(f"Unknown primary LLM: {PRIMARY_LLM}, using Ollama")
        return OllamaAI()


# ========================
# CONVENIENCE FUNCTIONS
# ========================

# Global AI instance
_ai_instance = None

def get_ai():
    """Get global AI instance"""
    global _ai_instance
    if _ai_instance is None:
        _ai_instance = get_ai_instance()
    return _ai_instance

def ask_ai(prompt, context=""):
    """Quick function to ask AI something"""
    return get_ai().chat(prompt, context)

def analyze_image(image_path, question=""):
    """Quick function to analyze an image"""
    ai = get_ai()
    if isinstance(ai, GeminiAI):
        return ai.analyze_image(image_path, question)
    else:
        return "Image analysis only available with Gemini"

if __name__ == "__main__":
    # Test the AI
    print("Testing JARVIS AI...")
    ai = get_ai()
    
    response = ai.chat("What can you do?")
    print(f"\nJARVIS: {response}\n")
    
    # Test image analysis (if available)
    print("✅ AI System initialized successfully")