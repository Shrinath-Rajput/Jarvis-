# whatsapp_tools.py
"""
WhatsApp operations for JARVIS
"""

import pywhatkit as kit
import time


class WhatsAppTools:
    """Handle WhatsApp operations"""
    
    @staticmethod
    def send_message(phone_number, message, wait_time=15):
        """Send WhatsApp message"""
        try:
            # Ensure phone number has country code
            if not phone_number.startswith("+"):
                phone_number = "+91" + phone_number  # Default to India, modify as needed
            
            kit.sendwhatmsg_instantly(phone_number, message, wait_time=wait_time)
            
            return {"success": True, "message": f"Message sent to {phone_number}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def send_image(phone_number, image_path, caption=""):
        """Send image via WhatsApp"""
        try:
            import os
            
            image_path = os.path.expanduser(image_path)
            
            if not os.path.exists(image_path):
                return {"success": False, "error": f"Image not found: {image_path}"}
            
            if not phone_number.startswith("+"):
                phone_number = "+91" + phone_number
            
            kit.sendwhatsapp_image(phone_number, image_path, caption=caption)
            
            return {"success": True, "message": f"Image sent to {phone_number}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def send_group_message(group_name, message, wait_time=15):
        """Send message to WhatsApp group"""
        try:
            kit.sendwhatmsg_to_group(group_name, message, wait_time=wait_time)
            
            return {"success": True, "message": f"Message sent to group: {group_name}"}
        except Exception as e:
            return {"success": False, "error": str(e)}


# Export
whatsapp_tools = WhatsAppTools()
