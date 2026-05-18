"""
Browser Automation and Web Interaction System
Uses Playwright for robust website navigation and interaction
"""
import logging
import time
import os
from pathlib import Path
from datetime import datetime

try:
    from playwright.sync_api import sync_playwright, expect
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

from config import (
    HEADLESS_BROWSER,
    BROWSER_TIMEOUT,
    WAIT_FOR_NAVIGATION,
    SCREENSHOTS_DIR,
    DEBUG,
)

logging.basicConfig(level=logging.DEBUG if DEBUG else logging.INFO)
logger = logging.getLogger(__name__)

# ========================
# BROWSER MANAGER
# ========================

class BrowserManager:
    """
    Manages browser instances and interactions
    """

    def __init__(self):
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError("Playwright not installed. Run: pip install playwright")
        
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.is_open = False
        logger.info("BrowserManager initialized")

    def launch(self):
        """Launch a new browser instance"""
        try:
            self.playwright = sync_playwright().start()
            
            self.browser = self.playwright.chromium.launch(
                headless=HEADLESS_BROWSER,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                ]
            )
            
            self.context = self.browser.new_context(
                viewport={'width': 1920, 'height': 1080}
            )
            
            self.page = self.context.new_page()
            self.page.set_default_timeout(BROWSER_TIMEOUT)
            self.page.set_default_navigation_timeout(WAIT_FOR_NAVIGATION)
            
            self.is_open = True
            logger.info("Browser launched successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to launch browser: {str(e)}")
            return False

    def close(self):
        """Close the browser"""
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            
            self.is_open = False
            logger.info("Browser closed")
            return True
            
        except Exception as e:
            logger.error(f"Error closing browser: {str(e)}")
            return False

    # ========================
    # NAVIGATION
    # ========================

    def navigate(self, url):
        """Navigate to a URL"""
        try:
            if not self.is_open:
                self.launch()
            
            if not url.startswith(('http://', 'https://')):
                url = f'https://{url}'
            
            self.page.goto(url)
            logger.info(f"Navigated to: {url}")
            return True
            
        except Exception as e:
            logger.error(f"Navigation error: {str(e)}")
            return False

    def go_back(self):
        """Go to previous page"""
        try:
            self.page.go_back()
            logger.info("Went back to previous page")
            return True
        except Exception as e:
            logger.error(f"Go back error: {str(e)}")
            return False

    def go_forward(self):
        """Go to next page"""
        try:
            self.page.go_forward()
            logger.info("Went forward")
            return True
        except Exception as e:
            logger.error(f"Go forward error: {str(e)}")
            return False

    def refresh(self):
        """Refresh the page"""
        try:
            self.page.reload()
            logger.info("Page refreshed")
            return True
        except Exception as e:
            logger.error(f"Refresh error: {str(e)}")
            return False

    # ========================
    # INTERACTION
    # ========================

    def click(self, selector):
        """Click an element by selector"""
        try:
            self.page.click(selector)
            logger.info(f"Clicked: {selector}")
            return True
        except Exception as e:
            logger.error(f"Click error: {str(e)}")
            return False

    def click_text(self, text):
        """Click element containing text"""
        try:
            selector = f'text={text}'
            self.page.click(selector)
            logger.info(f"Clicked text: {text}")
            return True
        except Exception as e:
            logger.error(f"Click text error: {str(e)}")
            return False

    def type_text(self, selector, text, delay=0):
        """Type text into an element"""
        try:
            self.page.fill(selector, '')
            self.page.type(selector, text, delay=delay)
            logger.info(f"Typed into {selector}: {text[:50]}...")
            return True
        except Exception as e:
            logger.error(f"Type error: {str(e)}")
            return False

    def find_and_type(self, label_text, input_text):
        """Find label by text and type into associated input"""
        try:
            # Find label element
            label = self.page.locator(f"label:has-text('{label_text}')")
            
            # Get associated input
            input_selector = label.evaluate("el => el.getAttribute('for')")
            
            if input_selector:
                self.page.fill(f"#{input_selector}", input_text)
            else:
                # Try finding input inside label
                self.page.fill(f"label:has-text('{label_text}') >> input", input_text)
            
            logger.info(f"Typed into field '{label_text}': {input_text[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"Find and type error: {str(e)}")
            return False

    def select_dropdown(self, selector, value):
        """Select dropdown option"""
        try:
            self.page.select_option(selector, value)
            logger.info(f"Selected '{value}' from {selector}")
            return True
        except Exception as e:
            logger.error(f"Dropdown select error: {str(e)}")
            return False

    def submit_form(self, selector="form"):
        """Submit a form"""
        try:
            self.page.click(f"{selector} >> button[type='submit']")
            logger.info("Form submitted")
            return True
        except Exception as e:
            logger.error(f"Form submit error: {str(e)}")
            return False

    # ========================
    # WAITING & CONDITIONS
    # ========================

    def wait_for_element(self, selector, timeout=10000):
        """Wait for element to appear"""
        try:
            self.page.wait_for_selector(selector, timeout=timeout)
            logger.info(f"Element appeared: {selector}")
            return True
        except Exception as e:
            logger.error(f"Wait for element error: {str(e)}")
            return False

    def wait_for_text(self, text, timeout=10000):
        """Wait for text to appear"""
        try:
            self.page.wait_for_selector(f"text={text}", timeout=timeout)
            logger.info(f"Text appeared: {text}")
            return True
        except Exception as e:
            logger.error(f"Wait for text error: {str(e)}")
            return False

    def wait_for_navigation(self):
        """Wait for navigation to complete"""
        try:
            with self.page.expect_navigation():
                pass
            logger.info("Navigation completed")
            return True
        except Exception as e:
            logger.error(f"Wait for navigation error: {str(e)}")
            return False

    def wait(self, seconds):
        """Wait for specified seconds"""
        time.sleep(seconds)
        logger.info(f"Waited {seconds} seconds")
        return True

    # ========================
    # DATA EXTRACTION
    # ========================

    def get_text(self, selector):
        """Get text from element"""
        try:
            text = self.page.text_content(selector)
            logger.info(f"Got text from {selector}")
            return text
        except Exception as e:
            logger.error(f"Get text error: {str(e)}")
            return None

    def get_attribute(self, selector, attribute):
        """Get element attribute"""
        try:
            value = self.page.get_attribute(selector, attribute)
            logger.info(f"Got {attribute} from {selector}")
            return value
        except Exception as e:
            logger.error(f"Get attribute error: {str(e)}")
            return None

    def get_page_content(self):
        """Get all page content"""
        try:
            content = self.page.content()
            return content
        except Exception as e:
            logger.error(f"Get page content error: {str(e)}")
            return None

    def extract_links(self):
        """Extract all links from page"""
        try:
            links = self.page.eval_on_selector_all(
                'a',
                'elements => elements.map(el => ({text: el.innerText, href: el.href}))'
            )
            logger.info(f"Extracted {len(links)} links")
            return links
        except Exception as e:
            logger.error(f"Extract links error: {str(e)}")
            return []

    # ========================
    # SCREENSHOTS
    # ========================

    def screenshot(self, name=None):
        """Take a screenshot"""
        try:
            if not name:
                name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            filepath = SCREENSHOTS_DIR / f"{name}.png"
            self.page.screenshot(path=str(filepath))
            logger.info(f"Screenshot saved: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Screenshot error: {str(e)}")
            return None

    def get_page_title(self):
        """Get page title"""
        try:
            return self.page.title()
        except Exception as e:
            logger.error(f"Get title error: {str(e)}")
            return None

    def get_current_url(self):
        """Get current URL"""
        try:
            return self.page.url
        except Exception as e:
            logger.error(f"Get URL error: {str(e)}")
            return None


# ========================
# GLOBAL INSTANCE
# ========================

_browser_manager = None

def get_browser():
    """Get global browser manager"""
    global _browser_manager
    if _browser_manager is None:
        _browser_manager = BrowserManager()
    return _browser_manager

def close_browser():
    """Close global browser"""
    global _browser_manager
    if _browser_manager:
        _browser_manager.close()
        _browser_manager = None

# ========================
# CONVENIENCE FUNCTIONS
# ========================

def navigate(url):
    """Quick navigate function"""
    browser = get_browser()
    if not browser.is_open:
        browser.launch()
    return browser.navigate(url)

def click(selector):
    """Quick click function"""
    return get_browser().click(selector)

def type_text(selector, text):
    """Quick type function"""
    return get_browser().type_text(selector, text)

def wait(seconds):
    """Quick wait function"""
    return get_browser().wait(seconds)

if __name__ == "__main__":
    print("Testing Browser Automation...")
    
    browser = get_browser()
    browser.launch()
    
    # Test navigation
    browser.navigate("https://google.com")
    print(f"✅ Navigated to: {browser.get_current_url()}")
    
    # Test screenshot
    screenshot_path = browser.screenshot("test")
    print(f"✅ Screenshot taken: {screenshot_path}")
    
    browser.close()
    print("✅ Browser tests complete")
