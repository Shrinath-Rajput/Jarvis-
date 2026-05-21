# browser_tools.py
"""
Browser automation and control tools for JARVIS
"""

import webbrowser
import subprocess
import time
import os


class BrowserTools:
    """Handle browser operations"""
    
    @staticmethod
    def google_search(query):
        """Search Google"""
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            return {"success": True, "message": f"Searched Google for: {query}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def youtube_search(query):
        """Search YouTube"""
        try:
            search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            return {"success": True, "message": f"Searched YouTube for: {query}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def open_gmail():
        """Open Gmail"""
        try:
            webbrowser.open("https://mail.google.com/")
            return {"success": True, "message": "Opened Gmail"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def amazon_search(query):
        """Search Amazon"""
        try:
            search_url = f"https://www.amazon.com/s?k={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            return {"success": True, "message": f"Searched Amazon for: {query}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def open_chrome_incognito():
        """Open Chrome in incognito mode"""
        try:
            subprocess.Popen(['chrome', '--incognito'])
            return {"success": True, "message": "Opened Chrome in incognito mode"}
        except Exception as e:
            # Try alternative path
            try:
                subprocess.Popen(['C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', '--incognito'])
                return {"success": True, "message": "Opened Chrome in incognito mode"}
            except:
                return {"success": False, "error": str(e)}
    
    @staticmethod
    def open_firefox_incognito():
        """Open Firefox in private mode"""
        try:
            subprocess.Popen(['firefox', '--private-window'])
            return {"success": True, "message": "Opened Firefox in private mode"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def open_edge_incognito():
        """Open Edge in InPrivate mode"""
        try:
            subprocess.Popen(['msedge', '--inprivate'])
            return {"success": True, "message": "Opened Edge in InPrivate mode"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def open_website(url):
        """Open a website"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            webbrowser.open(url)
            return {"success": True, "message": f"Opened {url}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def google_translate(text, target_language="es"):
        """Translate text using Google Translate"""
        try:
            from urllib.parse import quote
            translate_url = f"https://translate.google.com/?sl=auto&tl={target_language}&text={quote(text)}&op=translate"
            webbrowser.open(translate_url)
            return {"success": True, "message": f"Opened translation for: {text}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def download_pdf(url, save_path=None):
        """Download a PDF from URL"""
        try:
            import requests
            
            if save_path is None:
                save_path = os.path.expanduser("~/Downloads/document.pdf")
            
            save_path = os.path.expanduser(save_path)
            
            response = requests.get(url)
            
            if response.status_code == 200:
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                
                return {"success": True, "message": f"PDF downloaded to {save_path}"}
            else:
                return {"success": False, "error": f"Failed to download PDF: {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def clear_cookies():
        """Clear browser cookies (Chrome)"""
        try:
            import subprocess
            import sys
            
            # Chrome cookie clearing
            subprocess.run([
                'powershell', '-Command',
                'Remove-Item -Path "$env:USERPROFILE\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies" -Force -ErrorAction SilentlyContinue'
            ])
            
            return {"success": True, "message": "Browser cookies cleared"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def open_bookmarks():
        """Open browser bookmarks"""
        try:
            bookmarks_path = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks")
            
            if os.path.exists(bookmarks_path):
                os.startfile(os.path.dirname(bookmarks_path))
                return {"success": True, "message": "Opened bookmarks folder"}
            else:
                return {"success": False, "error": "Bookmarks file not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}


# Export
browser_tools = BrowserTools()
