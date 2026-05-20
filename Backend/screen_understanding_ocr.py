# -*- coding: utf-8 -*-
"""
SCREEN UNDERSTANDING WITH OCR
===============================

Real-time screen analysis using:
- Tesseract OCR (text detection)
- Screenshot capture (mss)
- Image processing (PIL)
- Dynamic UI element detection

NO hardcoded coordinates.
Every action verified through OCR.
"""

import logging
import time
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import os

try:
    import pytesseract
    from PIL import Image, ImageDraw, ImageFilter
    PYTESSERACT_AVAILABLE = True
except ImportError:
    PYTESSERACT_AVAILABLE = False

try:
    import mss
    MSS_AVAILABLE = True
except ImportError:
    MSS_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TextElement:
    """Detected text element on screen"""
    text: str
    x: int
    y: int
    width: int
    height: int
    confidence: float
    
    def center(self) -> Tuple[int, int]:
        """Get center coordinates"""
        return (self.x + self.width // 2, self.y + self.height // 2)
    
    def bounds(self) -> Tuple[int, int, int, int]:
        """Get bounding box"""
        return (self.x, self.y, self.x + self.width, self.y + self.height)


@dataclass
class ScreenState:
    """Current state of the screen"""
    screenshot_path: str
    timestamp: float
    width: int
    height: int
    all_text: str
    text_elements: List[TextElement]
    window_title: str


class ScreenUnderstanding:
    """
    REAL-TIME SCREEN ANALYSIS
    - Captures screenshots
    - Performs OCR
    - Detects text elements
    - Finds clickable areas
    - Verifies screen changes
    """
    
    def __init__(self):
        """Initialize screen reader"""
        if not PYTESSERACT_AVAILABLE:
            logger.warning("⚠️ pytesseract not available - install: pip install pytesseract")
        if not MSS_AVAILABLE:
            logger.warning("⚠️ mss not available - install: pip install mss")
        if not NUMPY_AVAILABLE:
            logger.warning("⚠️ numpy not available - install: pip install numpy")
        
        self.last_screenshot = None
        self.last_ocr_result = None
        self.screenshot_dir = Path("./screenshots")
        self.screenshot_dir.mkdir(exist_ok=True)
        
        logger.info("✅ ScreenUnderstanding initialized")
    
    def screenshot(self, filename: Optional[str] = None) -> Optional[str]:
        """
        Take screenshot and save to file
        Returns: path to saved screenshot
        """
        if not MSS_AVAILABLE:
            logger.error("❌ mss not available")
            return None
        
        try:
            filename = filename or f"screen_{int(time.time())}.png"
            filepath = self.screenshot_dir / filename
            
            with mss.mss() as sct:
                # Get primary monitor
                monitor = sct.monitors[1]
                screenshot = sct.grab(monitor)
                
                # Convert to PIL Image
                img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
                
                # Save
                img.save(str(filepath))
                self.last_screenshot = str(filepath)
                
                logger.info(f"✅ Screenshot saved: {filepath}")
                return str(filepath)
        
        except Exception as e:
            logger.error(f"❌ Screenshot failed: {e}")
            return None
    
    def ocr_screenshot(self, image_path: Optional[str] = None) -> Dict:
        """
        Perform OCR on screenshot
        Returns: OCR data with text elements
        """
        if not PYTESSERACT_AVAILABLE:
            logger.error("❌ pytesseract not available")
            return {"text": "", "elements": []}
        
        try:
            image_path = image_path or self.last_screenshot
            
            if not image_path or not os.path.exists(image_path):
                logger.error(f"❌ Image not found: {image_path}")
                return {"text": "", "elements": []}
            
            img = Image.open(image_path)
            
            # Get full text
            full_text = pytesseract.image_to_string(img)
            
            # Get detailed data
            data = pytesseract.image_to_data(img, output_type='dict')
            
            # Parse elements
            elements = []
            for i in range(len(data['text'])):
                text = data['text'][i].strip()
                
                if not text or int(data['conf'][i]) < 0:
                    continue
                
                element = TextElement(
                    text=text,
                    x=int(data['left'][i]),
                    y=int(data['top'][i]),
                    width=int(data['width'][i]),
                    height=int(data['height'][i]),
                    confidence=float(data['conf'][i]) / 100
                )
                elements.append(element)
            
            self.last_ocr_result = {
                "text": full_text,
                "elements": elements,
                "timestamp": time.time()
            }
            
            logger.info(f"✅ OCR complete: {len(elements)} elements detected")
            return self.last_ocr_result
        
        except Exception as e:
            logger.error(f"❌ OCR failed: {e}")
            return {"text": "", "elements": []}
    
    def find_text(self, search_text: str, threshold: float = 0.8) -> Optional[TextElement]:
        """
        Find visible text element on screen
        - Case insensitive
        - Substring matching
        - Confidence threshold
        """
        if not self.last_ocr_result:
            logger.warning("⚠️ No OCR data - take screenshot first")
            return None
        
        search_lower = search_text.lower()
        elements = self.last_ocr_result.get("elements", [])
        
        # Exact match first
        for elem in elements:
            if elem.text.lower() == search_lower and elem.confidence >= threshold:
                logger.info(f"✅ Found text: '{elem.text}' at ({elem.center()})")
                return elem
        
        # Substring match
        for elem in elements:
            if search_lower in elem.text.lower() and elem.confidence >= threshold:
                logger.info(f"✅ Found text (partial): '{elem.text}' at ({elem.center()})")
                return elem
        
        logger.warning(f"❌ Text not found: '{search_text}'")
        return None
    
    def find_all_text(self, search_text: str, threshold: float = 0.8) -> List[TextElement]:
        """Find all instances of text on screen"""
        if not self.last_ocr_result:
            return []
        
        search_lower = search_text.lower()
        elements = self.last_ocr_result.get("elements", [])
        matches = []
        
        for elem in elements:
            if search_lower in elem.text.lower() and elem.confidence >= threshold:
                matches.append(elem)
        
        return matches
    
    def screen_changed(self, threshold: float = 0.1) -> bool:
        """
        Detect if screen changed since last screenshot
        Returns: True if significant change detected
        """
        if not self.last_screenshot:
            return True
        
        try:
            # Take new screenshot
            new_path = self.screenshot()
            if not new_path:
                return False
            
            # Compare OCR results
            old_ocr = self.last_ocr_result or {"text": ""}
            new_ocr = self.ocr_screenshot(new_path)
            
            old_text = old_ocr.get("text", "")
            new_text = new_ocr.get("text", "")
            
            # Calculate text difference
            if len(old_text) == 0:
                return True
            
            diff = abs(len(new_text) - len(old_text)) / max(len(old_text), 1)
            changed = diff > threshold
            
            logger.info(f"Screen change: {diff:.2%} ({'changed' if changed else 'same'})")
            return changed
        
        except Exception as e:
            logger.error(f"❌ Screen change detection failed: {e}")
            return False
    
    def get_screen_state(self) -> Optional[ScreenState]:
        """Get complete current screen state"""
        try:
            screenshot_path = self.screenshot()
            if not screenshot_path:
                return None
            
            ocr_data = self.ocr_screenshot(screenshot_path)
            
            # Get screen resolution
            if MSS_AVAILABLE:
                with mss.mss() as sct:
                    monitor = sct.monitors[1]
                    width = monitor['width']
                    height = monitor['height']
            else:
                width = height = 0
            
            # Try to get window title
            window_title = ""
            try:
                import pygetwindow
                active = pygetwindow.getActiveWindow()
                window_title = active.title if active else "Unknown"
            except:
                pass
            
            state = ScreenState(
                screenshot_path=screenshot_path,
                timestamp=time.time(),
                width=width,
                height=height,
                all_text=ocr_data.get("text", ""),
                text_elements=ocr_data.get("elements", []),
                window_title=window_title
            )
            
            return state
        
        except Exception as e:
            logger.error(f"❌ Failed to get screen state: {e}")
            return None
    
    def find_button(self, button_text: str) -> Optional[TextElement]:
        """Find clickable button by text"""
        return self.find_text(button_text, threshold=0.7)
    
    def find_input_field(self) -> Optional[TextElement]:
        """Find input field (search box, text area, etc)"""
        if not self.last_ocr_result:
            return None
        
        # Look for common input indicators
        elements = self.last_ocr_result.get("elements", [])
        
        input_keywords = ["search", "type", "enter", "find", "query", "input"]
        
        for elem in elements:
            if any(kw in elem.text.lower() for kw in input_keywords):
                return elem
        
        return None
    
    def text_visible(self, text: str) -> bool:
        """Check if text is visible on screen"""
        return self.find_text(text) is not None
    
    def wait_for_text(self, text: str, timeout: int = 10) -> bool:
        """
        Wait for text to appear on screen
        Returns: True if text appeared within timeout
        """
        start = time.time()
        
        while time.time() - start < timeout:
            self.screenshot()
            self.ocr_screenshot()
            
            if self.text_visible(text):
                logger.info(f"✅ Text appeared: '{text}'")
                return True
            
            time.sleep(0.5)
        
        logger.warning(f"❌ Text did not appear: '{text}'")
        return False
    
    def verify_action(self, expected_text: Optional[str] = None, 
                     unexpected_text: Optional[str] = None,
                     screen_changed_expected: bool = False) -> bool:
        """
        Verify that action had expected effect
        
        Args:
            expected_text: Text that should appear
            unexpected_text: Text that should NOT appear
            screen_changed_expected: Whether screen should change
        
        Returns: True if verification passed
        """
        try:
            time.sleep(0.5)  # Wait for screen to update
            
            self.screenshot()
            self.ocr_screenshot()
            
            # Check expected text
            if expected_text:
                if not self.text_visible(expected_text):
                    logger.warning(f"❌ Expected text not found: '{expected_text}'")
                    return False
                logger.info(f"✅ Verified text: '{expected_text}'")
            
            # Check unexpected text
            if unexpected_text:
                if self.text_visible(unexpected_text):
                    logger.warning(f"❌ Unexpected text found: '{unexpected_text}'")
                    return False
                logger.info(f"✅ Verified text absent: '{unexpected_text}'")
            
            # Check screen change
            if screen_changed_expected:
                if not self.screen_changed():
                    logger.warning("❌ Screen did not change as expected")
                    return False
                logger.info("✅ Screen changed as expected")
            
            return True
        
        except Exception as e:
            logger.error(f"❌ Verification failed: {e}")
            return False


# Global instance
_screen_understanding_instance = None


def get_screen_understanding() -> ScreenUnderstanding:
    """Get singleton screen understanding instance"""
    global _screen_understanding_instance
    if _screen_understanding_instance is None:
        _screen_understanding_instance = ScreenUnderstanding()
    return _screen_understanding_instance
