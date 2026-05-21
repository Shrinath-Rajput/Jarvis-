# email_tools.py
"""
Email operations for JARVIS
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


class EmailTools:
    """Handle email operations"""
    
    @staticmethod
    def send_email(to_email, subject, body, from_email=None, password=None, attachments=None):
        """Send an email"""
        try:
            # Get credentials from environment or parameters
            from_email = from_email or os.getenv("EMAIL_USER", "")
            password = password or os.getenv("EMAIL_PASSWORD", "")
            
            if not from_email or not password:
                return {"success": False, "error": "Email credentials not configured"}
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Add attachments if provided
            if attachments:
                if isinstance(attachments, str):
                    attachments = [attachments]
                
                for attachment_path in attachments:
                    attachment_path = os.path.expanduser(attachment_path)
                    
                    if os.path.exists(attachment_path):
                        with open(attachment_path, 'rb') as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                        
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(attachment_path)}')
                        msg.attach(part)
            
            # Send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_email, password)
            server.send_message(msg)
            server.quit()
            
            return {"success": True, "message": f"Email sent to {to_email}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def send_email_with_attachment(to_email, subject, body, attachment_path, from_email=None, password=None):
        """Send email with attachment"""
        return EmailTools.send_email(
            to_email=to_email,
            subject=subject,
            body=body,
            from_email=from_email,
            password=password,
            attachments=[attachment_path]
        )
    
    @staticmethod
    def reply_email(to_email, original_subject, reply_body, from_email=None, password=None):
        """Reply to an email"""
        try:
            subject = f"Re: {original_subject}"
            return EmailTools.send_email(
                to_email=to_email,
                subject=subject,
                body=reply_body,
                from_email=from_email,
                password=password
            )
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def search_emails(keyword, from_email=None, password=None):
        """Search emails (requires IMAP setup)"""
        try:
            from_email = from_email or os.getenv("EMAIL_USER", "")
            password = password or os.getenv("EMAIL_PASSWORD", "")
            
            if not from_email or not password:
                return {"success": False, "error": "Email credentials not configured"}
            
            import imaplib
            
            server = imaplib.IMAP4_SSL('imap.gmail.com')
            server.login(from_email, password)
            server.select('INBOX')
            
            status, data = server.search(None, 'ALL', f'TEXT "{keyword}"')
            
            email_ids = data[0].split()
            
            server.close()
            server.logout()
            
            return {"success": True, "found": len(email_ids), "email_ids": [id.decode() for id in email_ids]}
        except Exception as e:
            return {"success": False, "error": str(e)}


# Export
email_tools = EmailTools()
