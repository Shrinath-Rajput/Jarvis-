# -*- coding: utf-8 -*-
"""
SCREEN UNDERSTANDING ENGINE
OCR + Element Detection + Dynamic UI Analysis

Key features:
- Multi-engine OCR (EasyOCR, Tesseract, Fallback)
- Text detection and localization
- Button/element identification
- Active window detection
- Screenshot analysis
- NO hardcoded UI mappings
"""

import os
import json
import logging
import base64
import cv2
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass, asdict
import mss
from PIL import Image, ImageDraw
import pyautogui
import time
import platform

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
    """Detected text element on screen"""
    text: str
    confidence: float
    x: int
    y: int
    width: int
    height: int
    
    def center(self) -> Tuple[int, int]:
        """Get center coordinates"""
        return (self.x + self.width // 2, self.y + self.height // 2)
    
    def to_dict(self) -> Dict:
        return {
            "text": self.text,
            "confidence": self.confidence,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height
        }


@dataclass
class ScreenState:
    """Current screen state"""
    timestamp: str
    screenshot_path: str
    width: int
    height: int
    text_elements: List[Dict]
    raw_text: str
    window_title: Optional[str] = None


# ======================================
# SCREEN UNDERSTANDING ENGINE
# ======================================

class ScreenUnderstanding:
    """
    Intelligent screen reading using multiple OCR engines.
    No hardcoding - dynamically understands any UI.
    """
    
    def __init__(self):
        self.screenshot_dir = Path("screenshots")
        self.screenshot_dir.mkdir(exist_ok=True)
        
        # Initialize OCR engines
        self.easy_reader = None
        self.pytesseract_available = False
        self.use_tesseract = False
        
        # Try EasyOCR
        if EASYOCR_AVAILABLE:
            try:
                logger.info("Loading EasyOCR...")
                self.easy_reader = easyocr.Reader(['en'], gpu=False)
                logger.info("✅ EasyOCR ready")
            except Exception as e:
                logger.warning(f"EasyOCR failed: {e}")
        
        # Try Tesseract
        if PYTESSERACT_AVAILABLE:
            try:
                # Try to find tesseract
                if platform.system() == "Windows":
                    possible_paths = [
                        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
                        r"D:\Program Files\Tesseract-OCR\tesseract.exe",
                    ]
                    for path in possible_paths:
                        if os.path.exists(path):
                            pytesseract.pytesseract.pytesseract_cmd = path
                            self.pytesseract_available = True
                            logger.info("✅ Tesseract ready")
                            break
                else:
                    self.pytesseract_available = True
            except Exception as e:
                logger.warning(f"Tesseract failed: {e}")
        
        logger.info("✅ ScreenUnderstanding initialized")
    
    def take_screenshot(self) -> str:
        """Take screenshot and save"""
        
        try:
            timestamp = int(time.time() * 1000)
            screenshot_path = self.screenshot_dir / f"screenshot_{timestamp}.png"
            
            screenshot = pyautogui.screenshot()
            screenshot.save(str(screenshot_path))
            
            logger.info(f"📸 Screenshot: {screenshot_path}")
            return str(screenshot_path)
        
        except Exception as e:
            logger.error(f"Screenshot error: {e}")
            return ""
    
    def analyze_screen(self) -> ScreenState:
        """Analyze current screen state"""
        
        try:
            screenshot_path = self.take_screenshot()
            
            # Load image
            image = cv2.imread(screenshot_path)
            height, width = image.shape[:2]
            
            # Get window title (Windows)
            window_title = None
            if platform.system() == "Windows":
                try:
                    import pygetwindow
                    active_window = pygetwindow.getActiveWindow()
                    window_title = active_window.title if active_window else None
                except:
                    pass
            
            # Extract text
            text_elements = self.extract_text(screenshot_path)
            raw_text = "\n".join([e.text for e in text_elements])
            
            state = ScreenState(
                timestamp=datetime.now().isoformat(),
                screenshot_path=screenshot_path,
                width=width,
                height=height,
                text_elements=[e.to_dict() for e in text_elements],
                raw_text=raw_text,
                window_title=window_title
            )
            
            logger.info(f"✅ Analyzed screen: {len(text_elements)} text elements found")
            return state
        
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            return None
    
    def extract_text(self, image_path: str) -> List[TextElement]:
        """Extract all text from image using best available OCR"""
        
        try:
            # Try EasyOCR first (most accurate)
            if self.easy_reader:
                return self._extract_with_easyocr(image_path)
            
            # Fallback to Tesseract
            if self.pytesseract_available:
                return self._extract_with_tesseract(image_path)
            
            # Last resort: basic PIL detection
            return self._extract_with_pil(image_path)
        
        except Exception as e:
            logger.error(f"Text extraction error: {e}")
            return []
    
    def _extract_with_easyocr(self, image_path: str) -> List[TextElement]:
        """Extract text using EasyOCR"""
        
        try:
            image = cv2.imread(image_path)
            
            # EasyOCR returns list of (bbox, text, confidence)
            results = self.easy_reader.readtext(image)
            
            elements = []
            for (bbox, text, confidence) in results:
                if text.strip():  # Skip empty
                    # bbox is array of 4 points
                    x_coords = [point[0] for point in bbox]
                    y_coords = [point[1] for point in bbox]
                    
                    x = int(min(x_coords))
                    y = int(min(y_coords))
                    width = int(max(x_coords) - x)
                    height = int(max(y_coords) - y)
                    
                    element = TextElement(
                        text=text.strip(),
                        confidence=float(confidence),
                        x=x, y=y,
                        width=width,
                        height=height
                    )
                    elements.append(element)
            
            return elements
        
        except Exception as e:
            logger.warning(f"EasyOCR error: {e}")
            return []
    
    def _extract_with_tesseract(self, image_path: str) -> List[TextElement]:
        """Extract text using Tesseract"""
        
        try:
            image = Image.open(image_path)
            
            # Get detailed data
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            
            elements = []
            for i in range(len(data['text'])):
                text = data['text'][i].strip()
                if text:
                    element = TextElement(
                        text=text,
                        confidence=float(data['conf'][i]) / 100.0,
                        x=int(data['left'][i]),
                        y=int(data['top'][i]),
                        width=int(data['width'][i]),
                        height=int(data['height'][i])
                    )
                    elements.append(element)
            
            return elements
        
        except Exception as e:
            logger.warning(f"Tesseract error: {e}")
            return []
    
    def _extract_with_pil(self, image_path: str) -> List[TextElement]:
        """Fallback text extraction (limited)"""
        
        try:
            image = Image.open(image_path)
            
            # This is a fallback - no actual OCR
            # In production, this would use pytesseract or similar
            logger.warning("Using PIL fallback (no OCR)")
            return []
        
        except Exception as e:
            logger.warning(f"PIL extraction failed: {e}")
            return []
    
    def find_text_on_screen(self, search_text: str, 
                           threshold: float = 0.6,
                           partial_match: bool = True) -> Optional[Union[TextElement, List[TextElement]]]:
        """
        Find text on screen (case-insensitive, fuzzy match)
        Returns matching element(s)
        """
        
        try:
            logger.info(f"🔍 Finding: '{search_text}'")
            
            # Take screenshot and analyze
            screenshot_path = self.take_screenshot()
            elements = self.extract_text(screenshot_path)
            
            if not elements:
                logger.warning("No text found on screen")
                return None
            
            # Search for matches
            matches = []
            search_lower = search_text.lower()
            
            for element in elements:
                element_lower = element.text.lower()
                
                # Exact match
                if element_lower == search_lower:
                    matches.append(element)
                    continue
                
                # Partial match (if enabled)
                if partial_match and search_lower in element_lower:
                    matches.append(element)
                    continue
                
                # Fuzzy match using simple similarity
                if partial_match:
                    similarity = self._string_similarity(search_lower, element_lower)
                    if similarity >= threshold:
                        matches.append(element)
            
            if matches:
                logger.info(f"✅ Found {len(matches)} matches for '{search_text}'")
                return matches[0] if len(matches) == 1 else matches
            else:
                logger.warning(f"No match for '{search_text}'")
                return None
        
        except Exception as e:
            logger.error(f"Find text error: {e}")
            return None
    
    def find_button(self, button_text: str) -> Optional[TextElement]:
        """Find and return button element"""
        return self.find_text_on_screen(button_text, partial_match=True)
    
    def get_visible_text(self) -> str:
        """Get all visible text on screen"""
        
        try:
            screenshot_path = self.take_screenshot()
            elements = self.extract_text(screenshot_path)
            
            return "\n".join([e.text for e in elements])
        
        except Exception as e:
            logger.error(f"Get visible text error: {e}")
            return ""
    
    def highlight_elements(self, image_path: str, elements: List[TextElement],
                          output_path: Optional[str] = None) -> str:
        """Draw bounding boxes on detected elements"""
        
        try:
            image = Image.open(image_path).convert("RGB")
            draw = ImageDraw.Draw(image)
            
            for element in elements:
                # Draw rectangle
                bbox = (
                    element.x,
                    element.y,
                    element.x + element.width,
                    element.y + element.height
                )
                draw.rectangle(bbox, outline="red", width=2)
                
                # Draw text label
                draw.text((element.x, element.y - 10), 
                         element.text[:20], 
                         fill="red")
            
            if output_path is None:
                output_path = self.screenshot_dir / f"highlighted_{int(time.time())}.png"
            
            image.save(output_path)
            logger.info(f"✅ Highlighted screenshot: {output_path}")
            
            return str(output_path)
        
        except Exception as e:
            logger.error(f"Highlight error: {e}")
            return ""
    
    def _string_similarity(self, s1: str, s2: str) -> float:
        """Calculate string similarity (0-1)"""
        
        # Simple character overlap similarity
        if not s1 or not s2:
            return 0.0
        
        matches = sum(1 for c in s1 if c in s2)
        return matches / max(len(s1), len(s2))


# ======================================
# GLOBAL FUNCTIONS
# ======================================

_screen_reader = None

def get_screen_reader() -> ScreenUnderstanding:
    """Get screen reader singleton"""
    global _screen_reader
    if _screen_reader is None:
        _screen_reader = ScreenUnderstanding()
    return _screen_reader

def take_screenshot() -> str:
    """Take screenshot"""
    return get_screen_reader().take_screenshot()

def extract_text(image_path: str) -> List[Dict]:
    """Extract text from image"""
    reader = get_screen_reader()
    elements = reader.extract_text(image_path)
    return [e.to_dict() for e in elements]

def find_text_on_screen(text: str):
    """Find text on screen"""
    return get_screen_reader().find_text_on_screen(text)

def analyze_screen() -> Dict:
    """Analyze current screen"""
    reader = get_screen_reader()
    state = reader.analyze_screen()
    return {
        "timestamp": state.timestamp,
        "screenshot": state.screenshot_path,
        "width": state.width,
        "height": state.height,
        "text_elements": state.text_elements,
        "raw_text": state.raw_text,
        "window_title": state.window_title
    }

def get_visible_text() -> str:
    """Get visible text on screen"""
    return get_screen_reader().get_visible_text()

# Export class
screen_understanding = get_screen_reader()
