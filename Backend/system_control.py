# system_control.py
"""
System control operations for JARVIS
"""

import subprocess
import os
import psutil
import time
from datetime import datetime


class SystemControl:
    """Handle system operations"""
    
    @staticmethod
    def set_volume(level):
        """Set system volume (0-100)"""
        try:
            level = max(0, min(100, int(level)))
            
            # Windows volume control
            subprocess.run([
                'powershell', '-Command',
                f'$device = Get-AudioDevice -PlaybackVolume {level}; $device | Set-AudioDevice -DefaultPlayback'
            ], check=False)
            
            return {"success": True, "message": f"Volume set to {level}%"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def mute_volume():
        """Mute system volume"""
        try:
            subprocess.run([
                'powershell', '-Command',
                '(Get-AudioDevice -PlaybackVolume).Mute = $true'
            ], check=False)
            
            return {"success": True, "message": "Volume muted"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def unmute_volume():
        """Unmute system volume"""
        try:
            subprocess.run([
                'powershell', '-Command',
                '(Get-AudioDevice -PlaybackVolume).Mute = $false'
            ], check=False)
            
            return {"success": True, "message": "Volume unmuted"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def set_brightness(level):
        """Set screen brightness (0-100)"""
        try:
            level = max(0, min(100, int(level)))
            
            subprocess.run([
                'powershell', '-Command',
                f'(Get-WmiObject -Namespace root\\wmi -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, {level})'
            ], check=False)
            
            return {"success": True, "message": f"Brightness set to {level}%"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def enable_wifi():
        """Enable WiFi"""
        try:
            subprocess.run([
                'powershell', '-Command',
                'Enable-NetAdapter -Name "Wi-Fi" -Confirm:$false'
            ], check=False)
            
            return {"success": True, "message": "WiFi enabled"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def disable_wifi():
        """Disable WiFi"""
        try:
            subprocess.run([
                'powershell', '-Command',
                'Disable-NetAdapter -Name "Wi-Fi" -Confirm:$false'
            ], check=False)
            
            return {"success": True, "message": "WiFi disabled"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def enable_bluetooth():
        """Enable Bluetooth"""
        try:
            subprocess.run([
                'powershell', '-Command',
                'Get-Service bthserv | Start-Service'
            ], check=False)
            
            return {"success": True, "message": "Bluetooth enabled"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def disable_bluetooth():
        """Disable Bluetooth"""
        try:
            subprocess.run([
                'powershell', '-Command',
                'Get-Service bthserv | Stop-Service -Force'
            ], check=False)
            
            return {"success": True, "message": "Bluetooth disabled"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def take_screenshot(save_path=None):
        """Take a screenshot"""
        try:
            from PIL import ImageGrab
            
            if save_path is None:
                save_path = os.path.expanduser(f"~/Pictures/screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            
            save_path = os.path.expanduser(save_path)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            screenshot = ImageGrab.grab()
            screenshot.save(save_path)
            
            return {"success": True, "message": f"Screenshot saved to {save_path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def record_screen(duration=10, save_path=None):
        """Record screen (requires additional setup)"""
        try:
            if save_path is None:
                save_path = os.path.expanduser(f"~/Videos/recording_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
            
            save_path = os.path.expanduser(save_path)
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # Using Windows built-in screen recording
            subprocess.run([
                'powershell', '-Command',
                f'Start-ScreenRecording -Path "{save_path}" -Duration {duration}'
            ], check=False)
            
            return {"success": True, "message": f"Screen recording started: {duration}s"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def shutdown(delay=0):
        """Shutdown the system"""
        try:
            delay = int(delay)
            subprocess.run([
                'powershell', '-Command',
                f'Stop-Computer -Force -Delay {delay * 60}'
            ], check=False)
            
            return {"success": True, "message": f"System will shutdown in {delay} minutes"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def restart(delay=0):
        """Restart the system"""
        try:
            delay = int(delay)
            subprocess.run([
                'powershell', '-Command',
                f'Restart-Computer -Force -Delay {delay * 60}'
            ], check=False)
            
            return {"success": True, "message": f"System will restart in {delay} minutes"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def sleep():
        """Put system to sleep"""
        try:
            subprocess.run([
                'powershell', '-Command',
                'rundll32.exe powrprof.dll,SetSuspendState 0,1,0'
            ], check=False)
            
            return {"success": True, "message": "System going to sleep"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def enable_dark_mode():
        """Enable dark mode"""
        try:
            subprocess.run([
                'powershell', '-Command',
                'reg add HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize /v AppsUseLightTheme /t REG_DWORD /d 0 /f'
            ], check=False)
            
            return {"success": True, "message": "Dark mode enabled"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def disable_dark_mode():
        """Disable dark mode"""
        try:
            subprocess.run([
                'powershell', '-Command',
                'reg add HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize /v AppsUseLightTheme /t REG_DWORD /d 1 /f'
            ], check=False)
            
            return {"success": True, "message": "Dark mode disabled"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_battery_status():
        """Get battery status"""
        try:
            battery = psutil.sensors_battery()
            
            if battery:
                return {
                    "success": True,
                    "battery": {
                        "percent": battery.percent,
                        "is_plugged": battery.power_plugged,
                        "seconds_left": battery.secsleft
                    }
                }
            else:
                return {"success": False, "error": "Battery info not available"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def lock_screen():
        """Lock the screen"""
        try:
            subprocess.run([
                'powershell', '-Command',
                'rundll32.exe user32.dll,LockWorkStation'
            ], check=False)
            
            return {"success": True, "message": "Screen locked"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def enable_firewall():
        """Enable Windows Firewall"""
        try:
            subprocess.run([
                'powershell', '-Command',
                'Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True'
            ], check=False)
            
            return {"success": True, "message": "Firewall enabled"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def disable_firewall():
        """Disable Windows Firewall"""
        try:
            subprocess.run([
                'powershell', '-Command',
                'Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False'
            ], check=False)
            
            return {"success": True, "message": "Firewall disabled"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def disable_webcam():
        """Disable webcam"""
        try:
            subprocess.run([
                'powershell', '-Command',
                'Get-PnpDevice -FriendlyName "*Camera*" | Disable-PnpDevice -Confirm:$false'
            ], check=False)
            
            return {"success": True, "message": "Webcam disabled"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def enable_webcam():
        """Enable webcam"""
        try:
            subprocess.run([
                'powershell', '-Command',
                'Get-PnpDevice -FriendlyName "*Camera*" | Enable-PnpDevice -Confirm:$false'
            ], check=False)
            
            return {"success": True, "message": "Webcam enabled"}
        except Exception as e:
            return {"success": False, "error": str(e)}


# Export
system_control = SystemControl()
