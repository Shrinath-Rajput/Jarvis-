"""
======================================
SCREEN UNDERSTANDING ENGINE - AUTONOMOUS AI
OCR + Element Detection + Dynamic Analysis
======================================

Provides real-time screen reading capabilities
without any hardcoded UI mappings.
Uses multiple OCR engines and computer vision.
"""

import os
import json
import logging
import base64
import cv2
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
import mss
from PIL import Image
import pyautogui
import time

try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except:
    PYTESSERACT_AVAILABLE = False

try:
    import easyocr
    EASYOCR_AVAILABLE = True
except:
    EASYOCR_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ======================================
# DATA STRUCTURES
# ======================================

@dataclass
class TextElement:
    """Detected text on screen"""
    text: str
    confidence: float
    x: int
    y: int
    width: int
    height: int
    
    def center(self) -> Tuple[int, int]:
        return (self.x + self.width // 2, self.y + self.height // 2)


@dataclass
class ScreenState:
    """Current screen state"""
    timestamp: datetime
    screenshot_path: str
    window_title: str
    text_elements: List[TextElement]
    raw_text: str


# ======================================
# SCREEN UNDERSTANDING ENGINE
# ======================================

class ScreenUnderstanding:
    """
    Intelligent screen reading without hardcoding.
    Uses OCR + CV to understand any UI dynamically.
    """
    
    def __init__(self):
        self.screenshot_dir = Path("screenshots")
        self.screenshot_dir.mkdir(exist_ok=True)
        
        # Initialize OCR readers
        self.easy_reader = None
        self.pytesseract_available = False
        
        if EASYOCR_AVAILABLE:
            try:
                self.easy_reader = easyocr.Reader(['en'], gpu=False)
                logger.info("✅ EasyOCR loaded")
            except Exception as e:
                logger.warning(f"EasyOCR failed: {e}")
        
        if PYTESSERACT_AVAILABLE:
            try:
                pytesseract.pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
                self.pytesseract_available = True
                logger.info("✅ Tesseract loaded")
            except:
                logger.warning("Tesseract not available")
        
        if not self.easy_reader and not self.pytesseract_available:
            logger.warning("⚠️ No OCR engine available - install easyocr or tesseract")
        
        logger.info("✅ ScreenUnderstanding initialized")
    
    # ======================================
    # SCREENSHOT CAPTURE
    # ======================================
    
    def take_screenshot(self) -> Optional[Path]:
        """Capture current screen"""
        try:
            with mss.mss() as sct:
                monitor = sct.monitors[1]
                screenshot = sct.grab(monitor)
                
                img = Image.frombytes(
                    'RGB',
                    (screenshot.width, screenshot.height),
                    screenshot.rgb
                )
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                path = self.screenshot_dir / f"screen_{timestamp}.png"
                img.save(path)
                
                logger.info(f"📸 Screenshot: {path.name}")
                return path
        except Exception as e:
            logger.error(f"❌ Screenshot error: {e}")
            return None
    
    # ======================================
    # OCR ANALYSIS
    # ======================================
    
    def extract_text_with_positions(self, image_path: Path) -> List[TextElement]:
        """
        Extract text with positions using OCR.
        Tries multiple OCR engines for best results.
        """
        
        try:
            img = cv2.imread(str(image_path))
            if img is None:
                logger.error(f"Failed to load image: {image_path}")
                return []
            
            elements = []
            
            # Try EasyOCR first (better for complex layouts)
            if self.easy_reader:
                try:
                    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    results = self.easy_reader.readtext(rgb_img)
                    
                    for (bbox, text, confidence) in results:
                        if confidence > 0.2 and len(text.strip()) > 0:
                            x, y = int(bbox[0][0]), int(bbox[0][1])
                            w, h = int(bbox[2][0] - bbox[0][0]), int(bbox[2][1] - bbox[0][1])
                            
                            elements.append(TextElement(
                                text=text.strip(),
                                confidence=float(confidence),
                                x=x, y=y,
                                width=max(w, 1), height=max(h, 1)
                            ))
                    
                    logger.info(f"📖 EasyOCR: {len(elements)} text elements")
                    return elements
                except Exception as e:
                    logger.warning(f"EasyOCR error: {e}")
            
            # Fallback to Tesseract
            if self.pytesseract_available:
                try:
                    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
                    
                    for i in range(len(data['text'])):
                        if data['conf'][i] > 20 and len(data['text'][i].strip()) > 0:
                            elements.append(TextElement(
                                text=data['text'][i],
                                confidence=data['conf'][i] / 100.0,
                                x=data['left'][i],
                                y=data['top'][i],
                                width=max(data['width'][i], 1),
                                height=max(data['height'][i], 1)
                            ))
                    
                    logger.info(f"📖 Tesseract: {len(elements)} text elements")
                    return elements
                except Exception as e:
                    logger.warning(f"Tesseract error: {e}")
            
            return elements
        
        except Exception as e:
            logger.error(f"❌ OCR error: {e}")
            return []
    
    # ======================================
    # WINDOW TITLE
    # ======================================
    
    def get_active_window_title(self) -> str:
        """Get current active window title"""
        try:
            import subprocess
            result = subprocess.run(
                ['powershell', '-Command', 
                 '(Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | Select-Object -First 1).MainWindowTitle'],
                capture_output=True,
                text=True,
                timeout=3
            )
            title = result.stdout.strip()
            return title if title else "Unknown"
        except:
            return "Unknown"
    
    # ======================================
    # FULL SCREEN STATE
    # ======================================
    
    def analyze_screen(self) -> Optional[ScreenState]:
        """
        Perform complete screen analysis.
        Returns: ScreenState with all detected elements
        """
        
        try:
            # Capture
            screenshot_path = self.take_screenshot()
            if not screenshot_path:
                return None
            
            # Extract text
            text_elements = self.extract_text_with_positions(screenshot_path)
            raw_text = "\n".join([e.text for e in text_elements])
            
            # Window title
            window_title = self.get_active_window_title()
            
            state = ScreenState(
                timestamp=datetime.now(),
                screenshot_path=str(screenshot_path),
                window_title=window_title,
                text_elements=text_elements,
                raw_text=raw_text
            )
            
            logger.info(f"✅ Analysis: {window_title} | {len(text_elements)} elements")
            return state
        
        except Exception as e:
            logger.error(f"❌ Analysis error: {e}")
            return None
    
    # ======================================
    # SEARCH FOR TEXT
    # ======================================
    
    def find_text_on_screen(self, search_text: str) -> Optional[TextElement]:
        """
        Find specific text on screen.
        Returns: TextElement with position or None
        """
        
        try:
            # Take fresh screenshot
            screenshot_path = self.take_screenshot()
            if not screenshot_path:
                return None
            
            # Extract text
            elements = self.extract_text_with_positions(screenshot_path)
            
            # Search (case-insensitive, partial match)
            search_lower = search_text.lower().strip()
            
            for elem in elements:
                if search_lower in elem.text.lower():
                    logger.info(f"✅ Found: '{search_text}' at ({elem.x}, {elem.y})")
                    return elem
            
            logger.info(f"❌ Not found: '{search_text}'")
            return None
        
        except Exception as e:
            logger.error(f"❌ Find error: {e}")
            return None
    
    # ======================================
    # VERIFY ACTION
    # ======================================
    
    def verify_text_appeared(self, search_text: str, timeout: int = 5) -> bool:
        """
        Verify if text appeared after action.
        Used for validation after clicks/typing.
        """
        
        start = time.time()
        
        while time.time() - start < timeout:
            elem = self.find_text_on_screen(search_text)
            if elem:
                logger.info(f"✅ Verified: '{search_text}' appeared")
                return True
            time.sleep(0.3)
        
        logger.warning(f"⚠️ Timeout: '{search_text}' not verified")
        return False
    
    # ======================================
    # EXPORT STATE
    # ======================================
    
    def export_state(self, state: ScreenState) -> Dict:
        """Convert screen state to JSON-serializable dict"""
        
        return {
            "timestamp": state.timestamp.isoformat(),
            "screenshot_path": state.screenshot_path,
            "window_title": state.window_title,
            "text_elements": [asdict(e) for e in state.text_elements],
            "raw_text": state.raw_text,
            "element_count": len(state.text_elements)
        }


# ======================================
# SINGLETON
# ======================================

screen_understanding = ScreenUnderstanding()


def analyze_current_screen() -> Optional[ScreenState]:
    """Analyze current screen"""
    return screen_understanding.analyze_screen()


def find_text(text: str) -> Optional[TextElement]:
    """Find text on screen"""
    return screen_understanding.find_text_on_screen(text)


def verify_text(text: str, timeout: int = 5) -> bool:
    """Verify text appears"""
    return screen_understanding.verify_text_appeared(text, timeout)
    """Get or create screen understanding instance"""
    global _screen_understanding
    if _screen_understanding is None:
        _screen_understanding = ScreenUnderstanding()
    return _screen_understanding
