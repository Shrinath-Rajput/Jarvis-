"""
Screen Understanding Engine
Analyzes screenshots to understand current UI state
"""
import mss
import cv2
import numpy as np
import easyocr
import logging
import json
from datetime import datetime
from typing import Dict, List, Tuple, Any
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# =========================
# SCREEN CAPTURE
# =========================

class ScreenCapture:
    """Captures and processes screen screenshots"""
    
    def __init__(self):
        self.last_screenshot = None
        self.last_capture_time = None
        self.ocr_reader = easyocr.Reader(['en'], gpu=False)
        logger.info("ScreenCapture initialized with OCR")
    
    def capture(self) -> np.ndarray:
        """
        Capture current screen
        
        Returns:
            np.ndarray: Screenshot in BGR format (OpenCV)
        """
        try:
            with mss.mss() as sct:
                monitor = sct.monitors[1]  # Primary monitor
                screenshot = sct.grab(monitor)
                img = np.array(screenshot)
                # MSS returns BGRA, convert to BGR
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                self.last_screenshot = img
                self.last_capture_time = datetime.now()
                return img
        except Exception as e:
            logger.error(f"Screen capture error: {e}")
            return None
    
    def save_screenshot(self, filename: str = None) -> str:
        """
        Save screenshot to disk
        
        Args:
            filename: Optional custom filename
            
        Returns:
            str: Path to saved file
        """
        if self.last_screenshot is None:
            self.capture()
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        screenshots_dir = os.path.join(
            os.path.dirname(__file__), "screenshots"
        )
        os.makedirs(screenshots_dir, exist_ok=True)
        
        filepath = os.path.join(screenshots_dir, filename)
        cv2.imwrite(filepath, self.last_screenshot)
        logger.info(f"Screenshot saved: {filepath}")
        return filepath


# =========================
# TEXT EXTRACTION
# =========================

class TextExtractor:
    """Extracts text and OCR data from screenshots"""
    
    def __init__(self, ocr_reader):
        self.ocr_reader = ocr_reader
    
    def extract_text(self, screenshot: np.ndarray) -> List[Dict[str, Any]]:
        """
        Extract all text from screenshot using OCR
        
        Args:
            screenshot: Screenshot image
            
        Returns:
            List of text elements with positions
        """
        try:
            results = self.ocr_reader.readtext(screenshot)
            
            text_elements = []
            for (bbox, text, confidence) in results:
                # bbox is [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
                x_coords = [point[0] for point in bbox]
                y_coords = [point[1] for point in bbox]
                
                element = {
                    'text': text,
                    'confidence': float(confidence),
                    'bbox': {
                        'x': int(min(x_coords)),
                        'y': int(min(y_coords)),
                        'width': int(max(x_coords) - min(x_coords)),
                        'height': int(max(y_coords) - min(y_coords)),
                        'center': {
                            'x': int((min(x_coords) + max(x_coords)) / 2),
                            'y': int((min(y_coords) + max(y_coords)) / 2)
                        }
                    }
                }
                text_elements.append(element)
            
            logger.info(f"Extracted {len(text_elements)} text elements")
            return text_elements
        except Exception as e:
            logger.error(f"OCR extraction error: {e}")
            return []
    
    def get_text_at_position(self, 
                            text_elements: List[Dict],
                            x: int, y: int,
                            tolerance: int = 50) -> str:
        """
        Get text near a specific position
        
        Args:
            text_elements: List of extracted text elements
            x, y: Position to search around
            tolerance: Search radius in pixels
            
        Returns:
            str: Concatenated text near position
        """
        nearby = []
        for elem in text_elements:
            bbox = elem['bbox']
            center = bbox['center']
            distance = ((center['x'] - x)**2 + (center['y'] - y)**2)**0.5
            if distance <= tolerance:
                nearby.append((distance, elem['text']))
        
        nearby.sort(key=lambda x: x[0])
        return ' '.join([text for _, text in nearby])


# =========================
# SCREEN UNDERSTANDING
# =========================

class ScreenUnderstanding:
    """Main screen understanding engine"""
    
    def __init__(self):
        self.screen_capture = ScreenCapture()
        self.text_extractor = TextExtractor(self.screen_capture.ocr_reader)
        self.last_state = None
        logger.info("ScreenUnderstanding initialized")
    
    def analyze_screen(self) -> Dict[str, Any]:
        """
        Complete screen analysis
        
        Returns:
            Dict with screen state information
        """
        # Capture screenshot
        screenshot = self.screen_capture.capture()
        if screenshot is None:
            return {'error': 'Failed to capture screen'}
        
        # Extract text
        text_elements = self.text_extractor.extract_text(screenshot)
        
        # Create state
        state = {
            'timestamp': datetime.now().isoformat(),
            'screenshot_size': {
                'width': screenshot.shape[1],
                'height': screenshot.shape[0]
            },
            'text_elements': text_elements,
            'all_text': ' '.join([elem['text'] for elem in text_elements]),
            'element_count': len(text_elements)
        }
        
        # Detect changes from last state
        if self.last_state:
            state['changed'] = self._detect_change(
                self.last_state, state
            )
        else:
            state['changed'] = True
        
        self.last_state = state
        return state
    
    def _detect_change(self, last_state: Dict, current_state: Dict) -> bool:
        """
        Detect if screen has changed significantly
        
        Args:
            last_state: Previous screen state
            current_state: Current screen state
            
        Returns:
            bool: True if screen changed significantly
        """
        # Simple heuristic: check if text changed
        last_text = set(last_state.get('all_text', '').split())
        current_text = set(current_state.get('all_text', '').split())
        
        # If more than 20% of text changed, consider it a change
        if len(last_text) == 0:
            return True
        
        diff = len(last_text.symmetric_difference(current_text))
        change_ratio = diff / max(len(last_text), len(current_text))
        
        return change_ratio > 0.2
    
    def find_clickable_element(self, target_text: str,
                               text_elements: List[Dict] = None,
                               fuzzy: bool = True) -> Dict or None:
        """
        Find clickable element by text
        
        Args:
            target_text: Text to search for
            text_elements: List of text elements (uses last if None)
            fuzzy: Use fuzzy matching
            
        Returns:
            Element dict with position, or None
        """
        if text_elements is None:
            if self.last_state:
                text_elements = self.last_state.get('text_elements', [])
            else:
                return None
        
        target_lower = target_text.lower()
        
        for elem in text_elements:
            elem_text = elem['text'].lower()
            
            if fuzzy:
                # Fuzzy match: check if target is substring
                if target_lower in elem_text or elem_text in target_lower:
                    return elem
            else:
                # Exact match
                if elem_text == target_lower:
                    return elem
        
        return None
    
    def get_visible_text(self) -> str:
        """
        Get all visible text on current screen
        
        Returns:
            str: All visible text
        """
        if self.last_state:
            return self.last_state.get('all_text', '')
        return ''
    
    def describe_current_screen(self) -> str:
        """
        Generate natural language description of current screen
        
        Returns:
            str: Description for LLM
        """
        if not self.last_state:
            return "Screen not analyzed yet"
        
        state = self.last_state
        description = f"""
Current Screen State:
- Size: {state['screenshot_size']['width']}x{state['screenshot_size']['height']}
- Elements visible: {state['element_count']}
- Changed since last: {state.get('changed', False)}

Visible Text:
{state['all_text'][:500]}...

Top Elements:
"""
        # Add top 10 elements
        for i, elem in enumerate(state['text_elements'][:10]):
            bbox = elem['bbox']
            description += f"\n{i+1}. '{elem['text']}' at ({bbox['center']['x']}, {bbox['center']['y']})"
        
        return description


# =========================
# SINGLETON INSTANCE
# =========================

_screen_understanding = None

def get_screen_understanding() -> ScreenUnderstanding:
    """Get or create screen understanding instance"""
    global _screen_understanding
    if _screen_understanding is None:
        _screen_understanding = ScreenUnderstanding()
    return _screen_understanding
