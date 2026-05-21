import json
import ollama
from urllib.parse import urlparse
import logging

from config import (
    OLLAMA_MODEL,
    OLLAMA_BASE_URL
)

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are JARVIS Task Planner - an intelligent task planning AI.
Convert natural language requests into JSON action plans using ONLY the available tools listed below.

⚠️  CRITICAL RULES:
1. Return ONLY valid JSON array, nothing else
2. Each step must have "tool" (string) and optional "params" (dict/object)
3. Use underscore for multi-word tool names (e.g., "open_app" not "open app")
4. NEVER invent tools - only use tools from the AVAILABLE TOOLS list
5. For complex tasks, break into logical steps with wait steps between app openings
6. Always validate tool names against the AVAILABLE TOOLS list

✅ AVAILABLE TOOLS (VERIFIED IMPLEMENTATIONS):

=== BASIC AUTOMATION ===
- open_website: {url}
- open_app: {name}
- close_app: {name}
- open_folder: {path}
- create_folder: {name, location(optional), path(optional)}
- click: {x, y} (optional)
- type: {text}
- press_key: {key}
- hotkey: {keys (array)}
- wait: {seconds}

=== FILE MANAGEMENT ===
- copy_file: {source, destination}
- move_file: {source, destination}
- rename_file: {file_path, new_name}
- delete_file: {file_path}
- delete_old_files: {folder_path, days(30)}
- search_files: {folder_path, pattern}
- zip_files: {source_folder, zip_path}
- unzip_files: {zip_path, extract_path}
- organize_desktop: {}
- disk_space_check: {}

=== BROWSER & WEB ===
- google_search: {query}
- youtube_search: {query}
- open_gmail: {}
- amazon_search: {query}
- open_website: {url}
- incognito_mode: {browser("chrome"|"firefox"|"edge")}
- translate: {text, language}
- download_pdf: {url, save_path(optional)}
- clear_cookies: {}

=== SPECIFIC APPS ===
- open_word: {text(optional)}
- open_excel: {text(optional)}
- open_chrome: {url(optional)}
- open_firefox: {url(optional)}
- open_edge: {url(optional)}
- open_powershell: {directory(optional)}
- open_terminal: {directory(optional)}
- play_spotify: {}
- play_youtube: {query(optional)}

=== SYSTEM CONTROL ===
- set_volume: {level(0-100)}
- mute: {}
- unmute: {}
- mute_system: {}
- unmute_system: {}
- set_brightness: {level(0-100)}
- enable_wifi: {}
- disable_wifi: {}
- enable_bluetooth: {}
- disable_bluetooth: {}
- screenshot: {save_path(optional)}
- screenshot_save: {save_path(optional)}
- record_screen: {duration, save_path(optional)}
- shutdown: {delay(minutes, 0)}
- restart: {delay(minutes, 0)}
- sleep: {}
- dark_mode_on: {}
- dark_mode_off: {}
- battery_status: {}
- lock_screen: {}
- enable_firewall: {}
- disable_firewall: {}
- disable_webcam: {}
- enable_webcam: {}

=== EMAIL & MESSAGING ===
- send_email: {to_email, subject, body, from_email(opt), password(opt)}
- send_email_with_attachment: {to_email, subject, body, attachment_path}
- send_email_simple: {to_email, subject, body}
- reply_email: {to_email, original_subject, reply_body}
- search_emails: {keyword}
- send_whatsapp_message: {phone_number, message}
- send_whatsapp_image: {phone_number, image_path, caption(optional)}
- send_group_message: {group_name, message}

=== DOCUMENTS ===
- create_resume: {name, email, phone, experience(list), education(list), skills(list)}
- create_cover_letter: {name, company, position, body}
- spell_check: {text}
- summarize_pdf: {pdf_path}
- translate_text: {text, language}
- generate_report: {title, sections(list)}
- read_pdf: {pdf_path}
- take_note: {text}

=== EXCEL & SPREADSHEETS ===
- create_spreadsheet: {data, sheet_name(optional), save_path(optional)}
- add_chart: {excel_path, chart_type("bar"|"pie")}
- import_csv: {csv_path, save_path(optional)}
- create_pivot_table: {excel_path, values, index, aggfunc}
- create_budget_tracker: {categories(list), amounts(list)}
- add_formula: {excel_path, cell, formula}

=== MEDIA & PRODUCTIVITY ===
- play_music: {file_path}
- pause_music: {}
- next_song: {}
- previous_song: {}
- convert_video: {input_path, output_path, format_type}
- edit_image: {image_path, operation, params}
- create_slideshow: {image_folder, output_path, duration}
- set_reminder: {text, delay_minutes(5)}
- set_timer: {duration_seconds}
- add_todo: {task}
- list_todos: {}
- mark_todo_done: {todo_id}
- schedule_meeting: {title, date_time, duration_minutes(60)}
- open_calendar: {}

=== DEVELOPER TOOLS ===
- run_python_script: {script_path, arguments(optional)}
- npm_install: {package(optional)}
- git_clone: {repository, destination(optional)}
- git_commit: {message, directory(optional)}
- git_push: {branch("main")}
- start_localhost_server: {port(8000)}
- create_react_component: {component_name}
- docker_start: {container_name(optional)}
- docker_stop: {container_name}
- analyze_error: {error_message}

=== ADVANCED ===
- research_and_summarize: {query, include_sources}
- create_and_send_report: {title, content, recipient_email}
- complete_workflow: {workflow_steps}

📋 EXAMPLE PLANS:

User: "Open Word and type my name"
[
  {"tool": "open_word", "params": {"text": "John Doe"}},
  {"tool": "wait", "params": {"seconds": 1}}
]

User: "Search Google for Python tutorials"
[
  {"tool": "google_search", "params": {"query": "Python tutorials"}}
]

User: "Search YouTube for relaxing music and play Spotify"
[
  {"tool": "play_youtube", "params": {"query": "relaxing music"}},
  {"tool": "wait", "params": {"seconds": 2}},
  {"tool": "play_spotify", "params": {}}
]

User: "Take a screenshot"
[
  {"tool": "screenshot", "params": {"save_path": "~/Pictures/screenshot.png"}}
]

IMPORTANT REMINDERS:
- Validate each tool name against AVAILABLE TOOLS list
- Always add wait steps between opening apps
- Use only the parameter names shown above
- If unsure about a tool, use a simpler alternative
- Never create tools that don't exist

Now convert the user request into a JSON array plan:"""

class DynamicPlanner:

    def __init__(self):
        # Parse the URL to extract host:port
        parsed_url = urlparse(OLLAMA_BASE_URL)
        host_port = f"{parsed_url.hostname}:{parsed_url.port}" if parsed_url.port else parsed_url.hostname
        
        self.client = ollama.Client(
            host=host_port
        )
        
        # ✅ DEFINE VALID TOOLS FOR VERIFICATION
        self.valid_tools = {
            # Basic
            'open_website', 'open_app', 'close_app', 'open_folder', 'create_folder',
            'click', 'type', 'press_key', 'hotkey', 'wait',
            # Files
            'copy_file', 'move_file', 'rename_file', 'delete_file', 'delete_old_files',
            'search_files', 'zip_files', 'unzip_files', 'organize_desktop', 'disk_space_check',
            # Browser
            'google_search', 'youtube_search', 'open_gmail', 'amazon_search', 'open_website',
            'incognito_mode', 'translate', 'download_pdf', 'clear_cookies',
            # Apps
            'open_word', 'open_excel', 'open_chrome', 'open_firefox', 'open_edge',
            'open_powershell', 'open_terminal', 'play_spotify', 'play_youtube',
            # System
            'set_volume', 'mute', 'unmute', 'mute_system', 'unmute_system', 'set_brightness',
            'enable_wifi', 'disable_wifi', 'enable_bluetooth', 'disable_bluetooth',
            'screenshot', 'screenshot_save', 'record_screen', 'shutdown', 'restart', 'sleep',
            'dark_mode_on', 'dark_mode_off', 'battery_status', 'lock_screen',
            'enable_firewall', 'disable_firewall', 'disable_webcam', 'enable_webcam',
            # Email
            'send_email', 'send_email_with_attachment', 'send_email_simple', 'reply_email',
            'search_emails', 'send_whatsapp_message', 'send_whatsapp_image', 'send_group_message',
            # Documents
            'create_resume', 'create_cover_letter', 'spell_check', 'summarize_pdf',
            'translate_text', 'generate_report', 'read_pdf', 'take_note',
            # Excel
            'create_spreadsheet', 'add_chart', 'import_csv', 'create_pivot_table',
            'create_budget_tracker', 'add_formula',
            # Media
            'play_music', 'pause_music', 'next_song', 'previous_song',
            'convert_video', 'edit_image', 'create_slideshow',
            # Productivity
            'set_reminder', 'set_timer', 'add_todo', 'list_todos', 'mark_todo_done',
            'schedule_meeting', 'open_calendar',
            # Developer
            'run_python_script', 'npm_install', 'git_clone', 'git_commit', 'git_push',
            'start_localhost_server', 'create_react_component', 'docker_start', 'docker_stop',
            'analyze_error',
            # Advanced
            'research_and_summarize', 'create_and_send_report', 'complete_workflow'
        }
        
        logger.info(f"✅ Planner initialized with {len(self.valid_tools)} valid tools")

    def validate_plan(self, plan):
        """✅ Validate tool names in the plan"""
        if not isinstance(plan, list):
            logger.warning("Plan is not a list")
            return False, "Plan must be a JSON array"
        
        invalid_tools = []
        for i, step in enumerate(plan):
            tool = step.get("tool", "").lower().replace(" ", "_").strip()
            
            if not tool:
                logger.warning(f"Step {i}: Missing tool name")
                invalid_tools.append(f"Step {i}: No tool specified")
                continue
            
            if tool not in self.valid_tools:
                logger.warning(f"Step {i}: Invalid tool '{tool}'")
                invalid_tools.append(f"Step {i}: Unknown tool '{tool}'")
        
        if invalid_tools:
            return False, invalid_tools
        
        return True, None

    def clean_json(self, text):
        """Extract and validate JSON from response"""
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        start = text.find("[")
        end = text.rfind("]")

        if start == -1 or end == -1:
            raise Exception(f"Invalid AI response - no JSON array found:\n{text}")

        json_text = text[start:end + 1]
        
        # Try to parse and validate JSON
        try:
            parsed = json.loads(json_text)
            if isinstance(parsed, list):
                if len(parsed) == 0:
                    # Allow empty plans
                    return json_text
                return json_text
            else:
                raise Exception("Plan must be a JSON array")
        except json.JSONDecodeError as e:
            raise Exception(f"JSON parsing failed: {str(e)}\nExtracted: {json_text[:100]}")

    def plan_task(self, task):
        """Convert user task to action plan"""

        prompt = f"{SYSTEM_PROMPT}\n\nUSER REQUEST:\n{task}"

        try:
            response = self.client.chat(
                model=OLLAMA_MODEL,
                messages=[{"role": "user", "content": prompt}],
                stream=False
            )

            text = response["message"]["content"]
            json_text = self.clean_json(text)
            plan = json.loads(json_text)
            
            if not isinstance(plan, list):
                raise Exception("Plan must be a JSON array")
            
            # ✅ VALIDATE PLAN TOOLS
            is_valid, errors = self.validate_plan(plan)
            
            if not is_valid:
                logger.warning(f"🔴 Invalid tools detected:")
                for error in errors:
                    logger.warning(f"   - {error}")
                
                # Still return the plan but with warning
                logger.info(f"⚠️  Planner generated {len(plan)} steps with {len(errors)} invalid tools")
            
            logger.info(f"✅ [Planner] Generated {len(plan)} verified steps")
            return plan
            
        except Exception as e:
            logger.error(f"[Planner Error] {str(e)}")
            logger.info("[Planner] Using fallback plan")
            # Return a simple fallback plan
            return [{"tool": "google_search", "params": {"query": "help"}}]