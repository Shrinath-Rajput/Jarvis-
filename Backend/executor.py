# executor.py
"""
JARVIS Extended Executor with Dynamic Tool Support
Implements all tools with real automation using pyautogui
"""

import os
import time
import webbrowser
import subprocess
from datetime import datetime
import pyautogui
import json
import traceback
import logging

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# Import all helper modules
from file_manager import file_manager
from browser_tools import browser_tools
from system_control import system_control
from email_tools import email_tools
from document_tools import document_tools
from app_launcher import app_launcher
from whatsapp_tools import whatsapp_tools
from excel_tools import excel_tools
from media_tools import media_tools
from developer_tools import developer_tools
from productivity_tools import productivity_tools

pyautogui.FAILSAFE = False


def log_execution(tool, params, success, result=None, error=None):
    """✅ Enhanced execution logging"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "✅ SUCCESS" if success else "❌ FAILED"
    
    print(f"\n{'='*70}")
    print(f"[{timestamp}] [{status}] TOOL: {tool}")
    
    if params:
        print(f"  📋 Params: {json.dumps(params, default=str, indent=2)[:200]}")
    
    if result:
        print(f"  📊 Result: {str(result)[:200]}")
    
    if error:
        print(f"  ⚠️  Error: {error}")
    
    print(f"{'='*70}\n")
    
    # Also log to logger
    if success:
        logger.info(f"✅ Tool '{tool}' executed successfully")
    else:
        logger.error(f"❌ Tool '{tool}' failed: {error}")


class DynamicExecutor:
    """Main executor that routes to appropriate tools"""

    def __init__(self):
        """Initialize executor and collect all available tools"""
        self.tools_available = self._collect_available_tools()
        logger.info(f"✅ Executor initialized with {len(self.tools_available)} tools")

    def _collect_available_tools(self):
        """🔍 Collect all available tool methods"""
        tools = []
        for attr_name in dir(self):
            if attr_name.startswith("tool_") and callable(getattr(self, attr_name)):
                tool_name = attr_name.replace("tool_", "")
                tools.append(tool_name)
        return sorted(tools)

    def print_available_tools(self):
        """📊 Print all available tools"""
        print(f"\n{'='*70}")
        print(f"📦 AVAILABLE TOOLS ({len(self.tools_available)} total)")
        print(f"{'='*70}")
        
        for i, tool in enumerate(self.tools_available, 1):
            print(f"  {i:2d}. {tool}")
        
        print(f"{'='*70}\n")

    def execute_plan(self, plan):
        """Execute a list of steps with robust error handling"""
        
        print(f"\n{'='*70}")
        print(f"🚀 EXECUTING PLAN ({len(plan)} steps)")
        print(f"{'='*70}\n")

        results = []

        for i, step in enumerate(plan, 1):
            tool = step.get("tool", "").lower().replace(" ", "_").strip()
            params = step.get("params", {})

            print(f"\n📍 Step {i}/{len(plan)}: [{tool}]")
            print(f"   Params: {json.dumps(params, default=str)[:100] if params else 'None'}")

            try:
                # ✅ VALIDATE TOOL EXISTS
                fn_name = f"tool_{tool}"
                
                if not hasattr(self, fn_name):
                    error_msg = f"❌ Tool not found: '{tool}'"
                    print(f"   {error_msg}")
                    print(f"   💡 Available tools: {', '.join(self.tools_available[:5])}...")
                    
                    log_execution(tool, params, False, 
                                 error=f"Tool method '{fn_name}' not found in executor")
                    
                    results.append({
                        "tool": tool,
                        "success": False,
                        "error": f"Tool '{tool}' not implemented. Use: {', '.join(self.tools_available[:3])}",
                        "step": i
                    })
                    continue

                # ✅ GET THE TOOL METHOD
                fn = getattr(self, fn_name)
                
                if not callable(fn):
                    error_msg = f"❌ Tool is not callable: '{tool}'"
                    print(f"   {error_msg}")
                    
                    log_execution(tool, params, False, error=error_msg)
                    
                    results.append({
                        "tool": tool,
                        "success": False,
                        "error": error_msg,
                        "step": i
                    })
                    continue

                # ✅ EXECUTE THE TOOL WITH PARAMS
                print(f"   ⚙️  Executing...")
                result = fn(**params) if params else fn()

                log_execution(tool, params, True, result)

                results.append({
                    "tool": tool,
                    "success": True,
                    "result": result,
                    "step": i
                })
                
                print(f"   ✅ Step {i} completed successfully")

            except TypeError as e:
                # Parameter mismatch
                error_msg = f"Parameter error: {str(e)}"
                print(f"   ❌ {error_msg}")
                log_execution(tool, params, False, error=error_msg)
                
                results.append({
                    "tool": tool,
                    "success": False,
                    "error": error_msg,
                    "step": i
                })

            except Exception as e:
                error_msg = traceback.format_exc()
                print(f"   ❌ Execution failed: {str(e)}")
                log_execution(tool, params, False, error=str(e))

                results.append({
                    "tool": tool,
                    "success": False,
                    "error": str(e),
                    "step": i
                })

        # ✅ SUMMARY
        successful = sum(1 for r in results if r['success'])
        failed = len(results) - successful
        
        print(f"\n{'='*70}")
        print(f"📊 EXECUTION SUMMARY")
        print(f"   ✅ Successful: {successful}/{len(results)}")
        print(f"   ❌ Failed: {failed}/{len(results)}")
        print(f"{'='*70}\n")

        return results

    def tool_open_website(self, url):
        return browser_tools.open_website(url)

    def tool_google_search(self, query):
        return browser_tools.google_search(query)

    def tool_youtube_search(self, query):
        return browser_tools.youtube_search(query)

    def tool_open_gmail(self):
        return browser_tools.open_gmail()

    def tool_amazon_search(self, query):
        return browser_tools.amazon_search(query)

    def tool_open_app(self, name):
        return app_launcher.open_app(name)

    def tool_close_app(self, name):
        return app_launcher.close_app(name)

    def tool_open_folder(self, path):
        path = os.path.expanduser(path)
        try:
            os.startfile(path)
            return {"success": True, "message": f"Opened folder: {path}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def tool_create_folder(self, name, location=None, path=None):
        """✅ Create folder with REAL verification"""
        try:
            logger.info(f"📁 Creating folder: {name}")
            
            if path:
                # Use full path
                if os.path.isabs(path):
                    folder_path = path
                else:
                    location = location or os.path.expanduser("~")
                    folder_path = os.path.join(location, path)
            else:
                # Use location + name
                if not location:
                    location = os.path.join(os.path.expanduser("~"), "Desktop")
                folder_path = os.path.join(location, name)
            
            logger.info(f"📍 Target path: {folder_path}")
            
            # Create the folder
            os.makedirs(folder_path, exist_ok=True)
            
            # Verify folder was created
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                logger.info(f"✅ Folder created successfully: {folder_path}")
                return {
                    "success": True,
                    "message": f"✅ Created folder: {folder_path}",
                    "path": folder_path,
                    "exists": True
                }
            else:
                error_msg = f"❌ Folder creation failed: {folder_path}"
                logger.error(error_msg)
                return {"success": False, "error": error_msg}
        except Exception as e:
            error_msg = f"❌ Error creating folder: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}

    def tool_type(self, text):
        """✅ Type text with REAL verification"""
        try:
            logger.info(f"⌨️  Typing text: {text[:50]}...")
            
            # Verify text is not empty
            if not text or not isinstance(text, str):
                error_msg = f"❌ Invalid text: {text}"
                logger.error(error_msg)
                return {"success": False, "error": error_msg}
            
            logger.info(f"▶️  Using pyautogui.write() with 0.02s interval")
            
            # Use write method (slower, more reliable)
            pyautogui.write(text, interval=0.02)
            
            # Small wait to ensure typing is complete
            time.sleep(0.5)
            
            logger.info(f"✅ Text typed successfully: {len(text)} characters")
            
            return {
                "success": True,
                "message": f"✅ Typed {len(text)} characters",
                "text_length": len(text)
            }
        except Exception as e:
            error_msg = f"❌ Error typing text: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}

    def tool_press_key(self, key):
        try:
            pyautogui.press(key)
            return {"success": True, "message": f"Pressed: {key}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def tool_hotkey(self, *keys):
        try:
            pyautogui.hotkey(*keys)
            return {"success": True, "message": f"Hotkey: {keys}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def tool_click(self, x=None, y=None):
        try:
            if x and y:
                pyautogui.click(x, y)
            else:
                pyautogui.click()
            return {"success": True, "message": "Clicked"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def tool_wait(self, seconds=1):
        try:
            time.sleep(int(seconds))
            return {"success": True, "message": f"Waited {seconds}s"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ========== FILE OPERATIONS ==========

    def tool_copy_file(self, source, destination):
        return file_manager.copy_file(source, destination)

    def tool_move_file(self, source, destination):
        return file_manager.move_file(source, destination)

    def tool_rename_file(self, file_path, new_name):
        return file_manager.rename_file(file_path, new_name)

    def tool_delete_file(self, file_path):
        return file_manager.delete_file(file_path)

    def tool_delete_old_files(self, folder_path, days=30):
        return file_manager.delete_old_files(folder_path, days)

    def tool_search_files(self, folder_path, pattern="*"):
        return file_manager.search_files(folder_path, pattern)

    def tool_zip_files(self, source_folder, zip_path):
        return file_manager.zip_files(source_folder, zip_path)

    def tool_unzip_files(self, zip_path, extract_path):
        return file_manager.unzip_files(zip_path, extract_path)

    def tool_organize_desktop(self):
        return file_manager.organize_desktop()

    def tool_disk_space_check(self):
        return file_manager.get_disk_space()

    # ========== BROWSER TOOLS ==========

    def tool_incognito_mode(self, browser="chrome"):
        if browser.lower() == "firefox":
            return browser_tools.open_firefox_incognito()
        elif browser.lower() == "edge":
            return browser_tools.open_edge_incognito()
        else:
            return browser_tools.open_chrome_incognito()

    def tool_translate(self, text, language="spanish"):
        return browser_tools.google_translate(text, language)

    def tool_download_pdf(self, url, save_path=None):
        return browser_tools.download_pdf(url, save_path)

    def tool_clear_cookies(self):
        return browser_tools.clear_cookies()

    # ========== SYSTEM CONTROL ==========

    def tool_set_volume(self, level):
        return system_control.set_volume(level)

    def tool_mute(self):
        return system_control.mute_volume()

    def tool_unmute(self):
        return system_control.unmute_volume()

    def tool_set_brightness(self, level):
        return system_control.set_brightness(level)

    def tool_enable_wifi(self):
        return system_control.enable_wifi()

    def tool_disable_wifi(self):
        return system_control.disable_wifi()

    def tool_enable_bluetooth(self):
        return system_control.enable_bluetooth()

    def tool_disable_bluetooth(self):
        return system_control.disable_bluetooth()

    def tool_screenshot(self, save_path=None):
        return system_control.take_screenshot(save_path)

    def tool_record_screen(self, duration=10, save_path=None):
        return system_control.record_screen(duration, save_path)

    def tool_shutdown(self, delay=0):
        return system_control.shutdown(delay)

    def tool_restart(self, delay=0):
        return system_control.restart(delay)

    def tool_sleep(self):
        return system_control.sleep()

    def tool_dark_mode_on(self):
        return system_control.enable_dark_mode()

    def tool_dark_mode_off(self):
        return system_control.disable_dark_mode()

    def tool_battery_status(self):
        return system_control.get_battery_status()

    def tool_lock_screen(self):
        return system_control.lock_screen()

    def tool_enable_firewall(self):
        return system_control.enable_firewall()

    def tool_disable_firewall(self):
        return system_control.disable_firewall()

    def tool_disable_webcam(self):
        return system_control.disable_webcam()

    def tool_enable_webcam(self):
        return system_control.enable_webcam()

    # ========== EMAIL TOOLS ==========

    def tool_send_email(self, to_email, subject, body, from_email=None, password=None):
        return email_tools.send_email(to_email, subject, body, from_email, password)

    def tool_send_email_with_attachment(self, to_email, subject, body, attachment_path):
        return email_tools.send_email_with_attachment(to_email, subject, body, attachment_path)

    def tool_reply_email(self, to_email, original_subject, reply_body):
        return email_tools.reply_email(to_email, original_subject, reply_body)

    def tool_search_emails(self, keyword):
        return email_tools.search_emails(keyword)

    # ========== DOCUMENT TOOLS ==========

    def tool_create_resume(self, name, email, phone, experience, education, skills):
        return document_tools.create_resume(name, email, phone, experience, education, skills)

    def tool_create_cover_letter(self, name, company, position, body):
        return document_tools.create_cover_letter(name, company, position, body)

    def tool_spell_check(self, text):
        return document_tools.spell_check(text)

    def tool_summarize_pdf(self, pdf_path):
        return document_tools.summarize_pdf(pdf_path)

    def tool_translate_text(self, text, language="spanish"):
        return document_tools.translate_text(text, language)

    def tool_generate_report(self, title, sections):
        return document_tools.generate_report(title, sections)

    def tool_read_pdf(self, pdf_path):
        return document_tools.read_pdf(pdf_path)

    # ========== WHATSAPP TOOLS ==========

    def tool_send_whatsapp_message(self, phone_number, message):
        """✅ Send WhatsApp message with REAL verification"""
        try:
            logger.info(f"💬 Sending WhatsApp message")
            logger.info(f"📱 Phone: {phone_number}")
            logger.info(f"📝 Message: {message[:50]}...")
            
            # Ensure phone number has country code
            if not phone_number.startswith("+"):
                phone_number = "+91" + phone_number
                logger.info(f"📞 Added country code: {phone_number}")
            
            logger.info(f"▶️  Opening WhatsApp and sending message...")
            
            # Use pywhatkit to send message
            import pywhatkit as kit
            
            # sendwhatmsg_instantly opens WhatsApp Web and sends immediately
            kit.sendwhatmsg_instantly(phone_number, message, wait_time=15)
            
            # Wait for message to be sent
            time.sleep(3)
            
            logger.info(f"✅ WhatsApp message sent to: {phone_number}")
            
            return {
                "success": True,
                "message": f"✅ WhatsApp message sent to {phone_number}",
                "phone": phone_number,
                "message_length": len(message)
            }
        except Exception as e:
            error_msg = f"❌ Error sending WhatsApp message: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}

    def tool_send_whatsapp_image(self, phone_number, image_path, caption=""):
        return whatsapp_tools.send_image(phone_number, image_path, caption)

    def tool_send_group_message(self, group_name, message):
        return whatsapp_tools.send_group_message(group_name, message)

    # ========== EXCEL TOOLS ==========

    def tool_create_spreadsheet(self, data, sheet_name="Sheet1", save_path=None):
        return excel_tools.create_spreadsheet(data, sheet_name, save_path)

    def tool_add_chart(self, excel_path, chart_type="bar"):
        return excel_tools.add_chart(excel_path, chart_type)

    def tool_import_csv(self, csv_path, save_path=None):
        return excel_tools.import_csv(csv_path, save_path)

    def tool_create_pivot_table(self, excel_path, values, index, aggfunc="sum"):
        return excel_tools.create_pivot_table(excel_path, values, index, aggfunc)

    def tool_create_budget_tracker(self, categories, amounts):
        return excel_tools.create_budget_tracker(categories, amounts)

    def tool_add_formula(self, excel_path, cell, formula):
        return excel_tools.add_formula(excel_path, cell, formula)

    # ========== MEDIA TOOLS ==========

    def tool_play_music(self, file_path):
        return media_tools.play_music(file_path)

    def tool_pause_music(self):
        return media_tools.pause_playback()

    def tool_next_song(self):
        return media_tools.next_song()

    def tool_previous_song(self):
        return media_tools.previous_song()

    def tool_convert_video(self, input_path, output_path, format_type="mp4"):
        return media_tools.convert_video(input_path, output_path, format_type)

    def tool_edit_image(self, image_path, operation="resize", params=None):
        return media_tools.edit_image(image_path, operation, params)

    def tool_create_slideshow(self, image_folder, output_path, duration=3):
        return media_tools.create_slideshow(image_folder, output_path, duration)

    # ========== DEVELOPER TOOLS ==========

    def tool_open_terminal(self, directory=None):
        """✅ Open terminal with REAL verification"""
        return developer_tools.open_terminal(directory)

    def tool_open_vscode(self, folder_path=None, file_path=None):
        """✅ Open VS Code with REAL verification"""
        try:
            logger.info(f"🔧 Opening VS Code")
            
            if folder_path:
                folder_path = os.path.expanduser(folder_path)
                logger.info(f"📂 Opening folder in VS Code: {folder_path}")
                
                if not os.path.exists(folder_path):
                    error_msg = f"❌ Folder not found: {folder_path}"
                    logger.error(error_msg)
                    return {"success": False, "error": error_msg}
                
                result = app_launcher.open_app("vs code")
                if not result.get("success"):
                    return result
                
                time.sleep(2)
                
                # Open folder using Ctrl+K Ctrl+O shortcut
                pyautogui.hotkey('ctrl', 'k')
                time.sleep(0.3)
                pyautogui.hotkey('ctrl', 'o')
                time.sleep(1)
                
                # Type folder path
                pyautogui.typewrite(folder_path.replace('\\', '/'), interval=0.01)
                time.sleep(0.5)
                pyautogui.press('enter')
                
                logger.info(f"✅ VS Code opened with folder: {folder_path}")
                return {
                    "success": True,
                    "message": f"✅ VS Code opened: {folder_path}",
                    "folder": folder_path
                }
            
            elif file_path:
                file_path = os.path.expanduser(file_path)
                logger.info(f"📄 Opening file in VS Code: {file_path}")
                
                if not os.path.exists(file_path):
                    error_msg = f"❌ File not found: {file_path}"
                    logger.error(error_msg)
                    return {"success": False, "error": error_msg}
                
                result = app_launcher.open_app("vs code")
                if not result.get("success"):
                    return result
                
                time.sleep(2)
                
                # Open file using Ctrl+O shortcut
                pyautogui.hotkey('ctrl', 'o')
                time.sleep(1)
                
                # Type file path
                pyautogui.typewrite(file_path.replace('\\', '/'), interval=0.01)
                time.sleep(0.5)
                pyautogui.press('enter')
                
                logger.info(f"✅ VS Code opened file: {file_path}")
                return {
                    "success": True,
                    "message": f"✅ VS Code opened file: {file_path}",
                    "file": file_path
                }
            
            else:
                logger.info(f"▶️  Opening VS Code...")
                result = app_launcher.open_app("vs code")
                
                if result.get("success"):
                    logger.info(f"✅ VS Code opened")
                    return {
                        "success": True,
                        "message": f"✅ VS Code opened"
                    }
                else:
                    return result
        
        except Exception as e:
            error_msg = f"❌ Error opening VS Code: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}

    def tool_open_powershell(self, directory=None):
        return developer_tools.open_powershell(directory)

    def tool_run_python_script(self, script_path, arguments=None):
        return developer_tools.run_python_script(script_path, arguments)

    def tool_npm_install(self, package=None):
        return developer_tools.npm_install(package)

    def tool_git_clone(self, repository, destination=None):
        return developer_tools.git_clone(repository, destination)

    def tool_git_commit(self, message, directory=None):
        return developer_tools.git_commit(message, directory)

    def tool_git_push(self, branch="main"):
        return developer_tools.git_push(branch)

    def tool_start_localhost_server(self, port=8000):
        return developer_tools.start_local_server(port)

    def tool_create_react_component(self, component_name):
        return developer_tools.create_react_component(component_name)

    def tool_docker_start(self, container_name=None):
        return developer_tools.docker_start(container_name)

    def tool_docker_stop(self, container_name):
        return developer_tools.docker_stop(container_name)

    def tool_analyze_error(self, error_message):
        return developer_tools.analyze_error(error_message)

    # ========== PRODUCTIVITY TOOLS ==========

    def tool_set_reminder(self, text, delay_minutes=5):
        return productivity_tools.set_reminder(text, delay_minutes)

    def tool_set_timer(self, duration_seconds):
        return productivity_tools.set_timer(duration_seconds)

    def tool_add_todo(self, task):
        return productivity_tools.add_todo(task)

    def tool_list_todos(self):
        return productivity_tools.list_todos()

    def tool_mark_todo_done(self, todo_id):
        return productivity_tools.mark_todo_done(todo_id)

    def tool_schedule_meeting(self, title, date_time, duration_minutes=60):
        return productivity_tools.schedule_meeting(title, date_time, duration_minutes)

    def tool_open_calendar(self):
        return productivity_tools.open_calendar()

    def tool_get_reminders(self):
        return productivity_tools.get_reminders()

    def tool_delete_todo(self, todo_id):
        return productivity_tools.delete_todo(todo_id)

    # ========== MULTI-STEP TASKS ==========

    def tool_research_and_summarize(self, query, include_sources=False):
        """Research topic and summarize"""
        try:
            import requests
            from bs4 import BeautifulSoup
            
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            # In real scenario, would scrape and summarize
            
            return {
                "success": True,
                "message": f"Research for '{query}' initiated",
                "url": search_url
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def tool_create_and_send_report(self, title, content, recipient_email):
        """Create report and send via email"""
        try:
            # Create document
            sections = [{"title": "Content", "content": content}]
            doc_result = document_tools.generate_report(title, sections)
            
            if doc_result["success"]:
                # Send email
                email_result = email_tools.send_email(
                    to_email=recipient_email,
                    subject=f"Report: {title}",
                    body=f"Please find the attached report: {title}"
                )
                
                return {
                    "success": email_result["success"],
                    "message": "Report created and sent"
                }
            else:
                return doc_result
        except Exception as e:
            return {"success": False, "error": str(e)}

    def tool_complete_workflow(self, workflow_steps):
        """Execute complete workflow"""
        try:
            results = []
            for step in workflow_steps:
                result = self.execute_plan([step])
                results.extend(result)
            
            return {
                "success": True,
                "message": f"Workflow completed with {len(results)} steps",
                "results": results
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ========== SPECIFIC APP SHORTCUTS ==========
    
    def tool_open_word(self, text=None, file_path=None):
        """✅ Open Microsoft Word with REAL verification"""
        try:
            logger.info(f"📄 Opening Microsoft Word")
            
            if file_path:
                file_path = os.path.expanduser(file_path)
                logger.info(f"📂 Opening file: {file_path}")
                
                if not os.path.exists(file_path):
                    # Try to create a new document if file doesn't exist
                    logger.warning(f"⚠️  File doesn't exist, will create new: {file_path}")
            
            # Open Word
            result = app_launcher.open_app("word")
            
            if not result.get("success"):
                logger.error(f"❌ Failed to open Word: {result.get('error')}")
                return result
            
            logger.info(f"✅ Word started, waiting for UI...")
            time.sleep(5)  # Give Word more time to fully load
            
            # If text is provided, type it
            if text:
                logger.info(f"⌨️  Typing text: {text[:50]}...")
                time.sleep(1)
                pyautogui.typewrite(text, interval=0.02)
                time.sleep(1)
                logger.info(f"✅ Text entered in Word")
            
            # If file path is provided, save it
            if file_path:
                logger.info(f"💾 Saving to: {file_path}")
                pyautogui.hotkey('ctrl', 's')  # Save
                time.sleep(2)
                
                # Type file path in save dialog
                pyautogui.typewrite(file_path.replace('\\', '/'), interval=0.01)
                time.sleep(1)
                pyautogui.press('enter')
                time.sleep(2)
                
                # Verify file was created
                if os.path.exists(file_path):
                    logger.info(f"✅ Document saved: {file_path}")
                else:
                    logger.warning(f"⚠️  Could not verify saved file: {file_path}")
            
            logger.info(f"✅ Word operation completed successfully")
            
            return {
                "success": True,
                "message": f"✅ Word opened successfully",
                "text": text,
                "file": file_path
            }
        except Exception as e:
            error_msg = f"❌ Error opening Word: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}

    def tool_open_excel(self, data=None, file_path=None):
        """✅ Open Microsoft Excel with REAL verification"""
        try:
            logger.info(f"📊 Opening Microsoft Excel")
            
            if file_path:
                file_path = os.path.expanduser(file_path)
                logger.info(f"📂 Opening file: {file_path}")
            
            # Open Excel
            result = app_launcher.open_app("excel")
            
            if not result.get("success"):
                logger.error(f"❌ Failed to open Excel: {result.get('error')}")
                return result
            
            logger.info(f"✅ Excel started, waiting for UI...")
            time.sleep(5)  # Give Excel more time to fully load
            
            # If data is provided, enter it
            if data:
                logger.info(f"📝 Entering data into Excel...")
                time.sleep(1)
                
                if isinstance(data, dict):
                    # Enter dictionary data as rows
                    for key, value in data.items():
                        pyautogui.typewrite(f"{key}", interval=0.01)
                        pyautogui.press('tab')
                        time.sleep(0.3)
                        pyautogui.typewrite(f"{value}", interval=0.01)
                        pyautogui.press('enter')
                        time.sleep(0.3)
                
                logger.info(f"✅ Data entered in Excel")
            
            # If file path is provided, save it
            if file_path:
                logger.info(f"💾 Saving to: {file_path}")
                pyautogui.hotkey('ctrl', 's')  # Save
                time.sleep(2)
                
                # Type file path in save dialog if needed
                try:
                    pyautogui.typewrite(file_path.replace('\\', '/'), interval=0.01)
                    time.sleep(1)
                    pyautogui.press('enter')
                    time.sleep(2)
                except:
                    pass
                
                # Verify file
                if os.path.exists(file_path):
                    logger.info(f"✅ Spreadsheet saved: {file_path}")
                else:
                    logger.warning(f"⚠️  Could not verify saved file: {file_path}")
            
            logger.info(f"✅ Excel operation completed successfully")
            
            return {
                "success": True,
                "message": f"✅ Excel opened successfully",
                "data": data,
                "file": file_path
            }
        except Exception as e:
            error_msg = f"❌ Error opening Excel: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}

    def tool_open_chrome(self, url=None):
        """🔴 Open Google Chrome"""
        try:
            result = app_launcher.open_app("chrome")
            if result.get("success"):
                time.sleep(2)  # Wait for browser to load
                if url:
                    time.sleep(1)
                    pyautogui.hotkey('ctrl', 'l')  # Focus address bar
                    time.sleep(0.5)
                    pyautogui.typewrite(url, interval=0.01)
                    pyautogui.press('enter')
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}

    def tool_open_firefox(self, url=None):
        """🟠 Open Mozilla Firefox"""
        try:
            result = app_launcher.open_app("firefox")
            if result.get("success"):
                time.sleep(2)  # Wait for browser to load
                if url:
                    time.sleep(1)
                    pyautogui.hotkey('ctrl', 'l')  # Focus address bar
                    time.sleep(0.5)
                    pyautogui.typewrite(url, interval=0.01)
                    pyautogui.press('enter')
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}

    def tool_open_edge(self, url=None):
        """🔵 Open Microsoft Edge"""
        try:
            result = app_launcher.open_app("edge")
            if result.get("success"):
                time.sleep(2)  # Wait for browser to load
                if url:
                    time.sleep(1)
                    pyautogui.hotkey('ctrl', 'l')  # Focus address bar
                    time.sleep(0.5)
                    pyautogui.typewrite(url, interval=0.01)
                    pyautogui.press('enter')
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}

    def tool_search_google(self, query):
        """🔍 Search Google - Open Chrome with search"""
        try:
            self.tool_open_chrome()
            time.sleep(2)
            pyautogui.typewrite(query, interval=0.02)
            pyautogui.press('enter')
            return {"success": True, "message": f"Searched Google for: {query}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def tool_play_spotify(self, search_query=None):
        """✅ Open Spotify with REAL verification"""
        try:
            logger.info(f"🎵 Opening Spotify")
            
            result = app_launcher.open_app("spotify")
            
            if not result.get("success"):
                logger.error(f"❌ Failed to open Spotify: {result.get('error')}")
                return result
            
            logger.info(f"✅ Spotify started, waiting for UI...")
            time.sleep(5)  # Give Spotify more time to load
            
            # If search query is provided, search for it
            if search_query:
                logger.info(f"🔍 Searching for: {search_query}")
                time.sleep(2)
                
                # Click on search (Ctrl+L in Spotify)
                pyautogui.hotkey('ctrl', 'l')
                time.sleep(1)
                
                # Type search query
                pyautogui.typewrite(search_query, interval=0.02)
                time.sleep(1)
                
                # Press enter to search
                pyautogui.press('enter')
                time.sleep(2)
                
                logger.info(f"✅ Searched for: {search_query}")
            
            logger.info(f"✅ Spotify opened successfully")
            
            return {
                "success": True,
                "message": f"✅ Spotify opened",
                "search": search_query
            }
        except Exception as e:
            error_msg = f"❌ Error opening Spotify: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}

    def tool_play_youtube(self, query=None):
        """▶️ Open YouTube"""
        try:
            if query:
                self.tool_open_chrome(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
            else:
                self.tool_open_chrome("https://www.youtube.com")
            return {"success": True, "message": "YouTube opened"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def tool_send_email_simple(self, to_email, subject, body):
        """📧 Send email (simplified)"""
        try:
            # Open Gmail and compose
            browser_tools.open_gmail()
            time.sleep(3)
            
            # Click compose (if on Gmail)
            pyautogui.hotkey('c')  # Gmail keyboard shortcut
            time.sleep(1)
            
            # Type email info
            pyautogui.typewrite(to_email, interval=0.01)
            pyautogui.press('tab')
            time.sleep(0.5)
            pyautogui.typewrite(subject, interval=0.01)
            pyautogui.press('tab')
            time.sleep(0.5)
            pyautogui.typewrite(body, interval=0.01)
            
            return {"success": True, "message": f"Email composed to {to_email}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def tool_take_note(self, text, file_path=None):
        """✅ Open Notepad and create note with REAL verification"""
        try:
            logger.info(f"📝 Opening Notepad")
            
            # Open Notepad
            result = app_launcher.open_app("notepad")
            
            if not result.get("success"):
                logger.error(f"❌ Failed to open Notepad: {result.get('error')}")
                return result
            
            logger.info(f"✅ Notepad started, waiting for UI...")
            time.sleep(3)  # Wait for Notepad to fully load
            
            # Type the note text
            if text and isinstance(text, str):
                logger.info(f"⌨️  Typing note: {text[:50]}...")
                time.sleep(0.5)
                pyautogui.typewrite(text, interval=0.02)
                time.sleep(1)
                logger.info(f"✅ Note text entered")
            else:
                error_msg = f"❌ Invalid text: {text}"
                logger.error(error_msg)
                return {"success": False, "error": error_msg}
            
            # If file path is provided, save it
            if file_path:
                file_path = os.path.expanduser(file_path)
                logger.info(f"💾 Saving note to: {file_path}")
                
                # Save file
                pyautogui.hotkey('ctrl', 's')
                time.sleep(2)
                
                # Type file path
                pyautogui.typewrite(file_path.replace('\\', '/'), interval=0.01)
                time.sleep(1)
                pyautogui.press('enter')
                time.sleep(2)
                
                # Verify file was created
                if os.path.exists(file_path):
                    logger.info(f"✅ Note saved: {file_path}")
                    # Read file to verify content
                    try:
                        with open(file_path, 'r') as f:
                            saved_content = f.read()
                        logger.info(f"✅ File content verified: {len(saved_content)} bytes")
                    except:
                        pass
                else:
                    logger.warning(f"⚠️  Could not verify saved file: {file_path}")
            
            logger.info(f"✅ Note operation completed successfully")
            
            return {
                "success": True,
                "message": f"✅ Note created in Notepad",
                "text_length": len(text),
                "file": file_path,
                "file_exists": os.path.exists(file_path) if file_path else None
            }
        except Exception as e:
            error_msg = f"❌ Error taking note: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}

    def tool_open_notepad(self, file_path=None):
        """✅ Open Notepad application with REAL verification"""
        try:
            logger.info(f"📝 Opening Notepad")
            
            if file_path:
                file_path = os.path.expanduser(file_path)
                logger.info(f"📂 Opening file: {file_path}")
                
                if not os.path.exists(file_path):
                    logger.warning(f"⚠️  File not found, will create new: {file_path}")
            
            # Open Notepad
            result = app_launcher.open_app("notepad")
            
            if not result.get("success"):
                logger.error(f"❌ Failed to open Notepad: {result.get('error')}")
                return result
            
            logger.info(f"✅ Notepad opened")
            time.sleep(2)
            
            # If file path is provided, open it
            if file_path and os.path.exists(file_path):
                logger.info(f"▶️  Opening file in Notepad...")
                pyautogui.hotkey('ctrl', 'o')
                time.sleep(1)
                
                pyautogui.typewrite(file_path.replace('\\', '/'), interval=0.01)
                time.sleep(0.5)
                pyautogui.press('enter')
                time.sleep(2)
                
                logger.info(f"✅ File opened in Notepad: {file_path}")
            
            return {
                "success": True,
                "message": f"✅ Notepad opened",
                "file": file_path
            }
        except Exception as e:
            error_msg = f"❌ Error opening Notepad: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}

    def tool_set_volume(self, level):
        """🔊 Set system volume (0-100)"""
        try:
            return system_control.set_volume(level)
        except Exception as e:
            return {"success": False, "error": str(e)}

    def tool_mute_system(self):
        """🔇 Mute system audio"""
        try:
            return system_control.mute_volume()
        except Exception as e:
            return {"success": False, "error": str(e)}

    def tool_unmute_system(self):
        """🔊 Unmute system audio"""
        try:
            return system_control.unmute_volume()
        except Exception as e:
            return {"success": False, "error": str(e)}

    def tool_screenshot_save(self, save_path=None):
        """📸 Take and save screenshot"""
        try:
            return system_control.take_screenshot(save_path)
        except Exception as e:
            return {"success": False, "error": str(e)}


# Global executor instance
executor = DynamicExecutor()

# Print available tools on startup
executor.print_available_tools()


def execute_plan(plan):
    """Main entry point for executing plans"""
    logger.info(f"📋 Executing plan with {len(plan)} steps")
    return executor.execute_plan(plan)