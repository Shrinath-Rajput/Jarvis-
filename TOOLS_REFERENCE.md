# JARVIS 1.0 - COMPLETE TOOLS REFERENCE

## Table of Contents
1. [Basic Automation](#basic-automation)
2. [File Management](#file-management)
3. [Browser Operations](#browser-operations)
4. [System Control](#system-control)
5. [Email](#email)
6. [Documents](#documents)
7. [Messaging](#messaging)
8. [Excel/Spreadsheets](#excelspreadsheets)
9. [Media](#media)
10. [Developer Tools](#developer-tools)
11. [Productivity](#productivity)
12. [Advanced Features](#advanced-features)

---

## BASIC AUTOMATION

### open_website
Open any website in default browser

**Parameters**:
- `url` (string, required): Full URL including protocol

**Example**:
```json
{
  "tool": "open_website",
  "params": {"url": "https://www.google.com"}
}
```

**Returns**:
```json
{"success": true, "message": "Opened https://www.google.com"}
```

---

### open_app
Open any application by name

**Parameters**:
- `name` (string, required): App name

**Supported Apps**:
word, excel, powerpoint, outlook, vs code, notepad++, chrome, firefox, edge, calculator, paint, spotify, vlc, zoom, teams, discord, settings, file_explorer, terminal, powershell

**Example**:
```json
{
  "tool": "open_app",
  "params": {"name": "vs code"}
}
```

---

### close_app
Close running application

**Parameters**:
- `name` (string, required): App name

**Example**:
```json
{
  "tool": "close_app",
  "params": {"name": "chrome"}
}
```

---

### open_folder
Open folder in file explorer

**Parameters**:
- `path` (string, required): Folder path

**Example**:
```json
{
  "tool": "open_folder",
  "params": {"path": "~/Documents"}
}
```

---

### create_folder
Create new folder

**Parameters**:
- `name` (string, required): Folder name
- `location` (string, optional): Parent directory
- `path` (string, optional): Full path

**Example**:
```json
{
  "tool": "create_folder",
  "params": {
    "name": "MyProject",
    "location": "~/Desktop"
  }
}
```

---

### type
Type text at current cursor position

**Parameters**:
- `text` (string, required): Text to type

**Example**:
```json
{
  "tool": "type",
  "params": {"text": "Hello World"}
}
```

---

### press_key
Press a single keyboard key

**Parameters**:
- `key` (string, required): Key name

**Valid Keys**: Return, Tab, Escape, Backspace, Delete, Space, Up, Down, Left, Right, Home, End, PageUp, PageDown, F1-F12, etc.

**Example**:
```json
{
  "tool": "press_key",
  "params": {"key": "Return"}
}
```

---

### hotkey
Execute keyboard shortcut

**Parameters**:
- `keys` (array, required): Keys combination

**Example**:
```json
{
  "tool": "hotkey",
  "params": {"keys": ["ctrl", "c"]}
}
```

**Common Shortcuts**:
- Copy: ["ctrl", "c"]
- Paste: ["ctrl", "v"]
- Save: ["ctrl", "s"]
- Undo: ["ctrl", "z"]
- Select All: ["ctrl", "a"]

---

### click
Click at specific coordinates

**Parameters**:
- `x` (integer, optional): X coordinate
- `y` (integer, optional): Y coordinate

**Example**:
```json
{
  "tool": "click",
  "params": {"x": 100, "y": 200}
}
```

---

### wait
Wait for specified duration

**Parameters**:
- `seconds` (integer, required): Seconds to wait

**Example**:
```json
{
  "tool": "wait",
  "params": {"seconds": 3}
}
```

---

## FILE MANAGEMENT

### copy_file
Copy file from source to destination

**Parameters**:
- `source` (string, required): Source file path
- `destination` (string, required): Destination path

**Example**:
```json
{
  "tool": "copy_file",
  "params": {
    "source": "~/Documents/file.txt",
    "destination": "~/Desktop/file.txt"
  }
}
```

---

### move_file
Move file to new location

**Parameters**:
- `source` (string, required): Source path
- `destination` (string, required): Destination path

**Example**:
```json
{
  "tool": "move_file",
  "params": {
    "source": "~/Downloads/file.pdf",
    "destination": "~/Documents/file.pdf"
  }
}
```

---

### rename_file
Rename a file

**Parameters**:
- `file_path` (string, required): Full file path
- `new_name` (string, required): New filename

**Example**:
```json
{
  "tool": "rename_file",
  "params": {
    "file_path": "~/Documents/old_name.txt",
    "new_name": "new_name.txt"
  }
}
```

---

### delete_file
Delete a file

**Parameters**:
- `file_path` (string, required): File path to delete

**Example**:
```json
{
  "tool": "delete_file",
  "params": {"file_path": "~/Documents/temp.txt"}
}
```

---

### delete_old_files
Delete files older than specified days

**Parameters**:
- `folder_path` (string, required): Folder to clean
- `days` (integer, optional, default: 30): Days threshold

**Example**:
```json
{
  "tool": "delete_old_files",
  "params": {
    "folder_path": "~/Downloads",
    "days": 60
  }
}
```

---

### search_files
Search for files matching pattern

**Parameters**:
- `folder_path` (string, required): Search location
- `pattern` (string, optional, default: "*"): Search pattern

**Example**:
```json
{
  "tool": "search_files",
  "params": {
    "folder_path": "~/Documents",
    "pattern": "*.pdf"
  }
}
```

---

### zip_files
Create ZIP archive

**Parameters**:
- `source_folder` (string, required): Folder to zip
- `zip_path` (string, required): Output ZIP path

**Example**:
```json
{
  "tool": "zip_files",
  "params": {
    "source_folder": "~/Documents/MyProject",
    "zip_path": "~/Desktop/MyProject.zip"
  }
}
```

---

### unzip_files
Extract ZIP archive

**Parameters**:
- `zip_path` (string, required): ZIP file path
- `extract_path` (string, required): Extract location

**Example**:
```json
{
  "tool": "unzip_files",
  "params": {
    "zip_path": "~/Desktop/archive.zip",
    "extract_path": "~/Documents"
  }
}
```

---

### organize_desktop
Auto-organize desktop files by type

**Parameters**: None

**Example**:
```json
{
  "tool": "organize_desktop",
  "params": {}
}
```

**Categories Created**:
- Documents (pdf, doc, docx, txt, xls, xlsx)
- Images (jpg, png, gif, bmp)
- Videos (mp4, avi, mkv, mov)
- Audio (mp3, wav, flac, aac)
- Archives (zip, rar, 7z)
- Code (py, js, html, css, java)

---

### disk_space_check
Check disk usage information

**Parameters**: None

**Example**:
```json
{
  "tool": "disk_space_check",
  "params": {}
}
```

**Returns**:
```json
{
  "success": true,
  "disks": [
    {
      "drive": "C:",
      "total_gb": 500,
      "used_gb": 250,
      "free_gb": 250,
      "percent": 50
    }
  ]
}
```

---

## BROWSER OPERATIONS

### google_search
Search Google for query

**Parameters**:
- `query` (string, required): Search query

**Example**:
```json
{
  "tool": "google_search",
  "params": {"query": "Python tutorials"}
}
```

---

### youtube_search
Search YouTube

**Parameters**:
- `query` (string, required): Search query

**Example**:
```json
{
  "tool": "youtube_search",
  "params": {"query": "machine learning"}
}
```

---

### open_gmail
Open Gmail inbox

**Parameters**: None

**Example**:
```json
{
  "tool": "open_gmail",
  "params": {}
}
```

---

### amazon_search
Search Amazon

**Parameters**:
- `query` (string, required): Product name

**Example**:
```json
{
  "tool": "amazon_search",
  "params": {"query": "laptop"}
}
```

---

### incognito_mode
Open browser in private mode

**Parameters**:
- `browser` (string, optional, default: "chrome"): Browser type

**Supported**: chrome, firefox, edge

**Example**:
```json
{
  "tool": "incognito_mode",
  "params": {"browser": "chrome"}
}
```

---

### translate
Translate text using Google Translate

**Parameters**:
- `text` (string, required): Text to translate
- `language` (string, optional, default: "spanish"): Target language

**Supported Languages**:
spanish, french, german, italian, portuguese, russian, japanese, chinese, korean

**Example**:
```json
{
  "tool": "translate",
  "params": {
    "text": "Hello world",
    "language": "spanish"
  }
}
```

---

### download_pdf
Download PDF from URL

**Parameters**:
- `url` (string, required): PDF URL
- `save_path` (string, optional): Save location

**Example**:
```json
{
  "tool": "download_pdf",
  "params": {
    "url": "https://example.com/file.pdf",
    "save_path": "~/Downloads/document.pdf"
  }
}
```

---

### clear_cookies
Clear browser cookies

**Parameters**: None

**Example**:
```json
{
  "tool": "clear_cookies",
  "params": {}
}
```

---

## SYSTEM CONTROL

### set_volume
Set system volume

**Parameters**:
- `level` (integer, required): Volume 0-100

**Example**:
```json
{
  "tool": "set_volume",
  "params": {"level": 75}
}
```

---

### mute
Mute system audio

**Parameters**: None

---

### unmute
Unmute system audio

**Parameters**: None

---

### set_brightness
Set screen brightness

**Parameters**:
- `level` (integer, required): Brightness 0-100

**Example**:
```json
{
  "tool": "set_brightness",
  "params": {"level": 50}
}
```

---

### enable_wifi
Enable WiFi

**Parameters**: None

---

### disable_wifi
Disable WiFi

**Parameters**: None

---

### enable_bluetooth
Enable Bluetooth

**Parameters**: None

---

### disable_bluetooth
Disable Bluetooth

**Parameters**: None

---

### screenshot
Take screenshot

**Parameters**:
- `save_path` (string, optional): Save location

**Example**:
```json
{
  "tool": "screenshot",
  "params": {"save_path": "~/Pictures/screen.png"}
}
```

---

### record_screen
Record screen video

**Parameters**:
- `duration` (integer, required): Duration in seconds
- `save_path` (string, optional): Save location

**Example**:
```json
{
  "tool": "record_screen",
  "params": {
    "duration": 30,
    "save_path": "~/Videos/recording.mp4"
  }
}
```

---

### shutdown
Shutdown computer

**Parameters**:
- `delay` (integer, optional, default: 0): Delay in minutes

**Example**:
```json
{
  "tool": "shutdown",
  "params": {"delay": 5}
}
```

---

### restart
Restart computer

**Parameters**:
- `delay` (integer, optional, default: 0): Delay in minutes

---

### sleep
Put computer to sleep

**Parameters**: None

---

### dark_mode_on
Enable dark mode

**Parameters**: None

---

### dark_mode_off
Disable dark mode

**Parameters**: None

---

### battery_status
Get battery information

**Parameters**: None

**Returns**:
```json
{
  "success": true,
  "battery": {
    "percent": 85,
    "is_plugged": true,
    "seconds_left": 3600
  }
}
```

---

### lock_screen
Lock screen

**Parameters**: None

---

### enable_firewall
Enable Windows Firewall

**Parameters**: None

---

### disable_firewall
Disable Windows Firewall

**Parameters**: None

---

### disable_webcam
Disable camera

**Parameters**: None

---

### enable_webcam
Enable camera

**Parameters**: None

---

## EMAIL

### send_email
Send email

**Parameters**:
- `to_email` (string, required): Recipient email
- `subject` (string, required): Email subject
- `body` (string, required): Email body
- `from_email` (string, optional): Sender email
- `password` (string, optional): Email password

**Example**:
```json
{
  "tool": "send_email",
  "params": {
    "to_email": "john@example.com",
    "subject": "Hello",
    "body": "How are you?"
  }
}
```

**Note**: Use app-specific passwords for Gmail

---

### send_email_with_attachment
Send email with file

**Parameters**:
- `to_email` (string, required): Recipient
- `subject` (string, required): Subject
- `body` (string, required): Body
- `attachment_path` (string, required): File path

**Example**:
```json
{
  "tool": "send_email_with_attachment",
  "params": {
    "to_email": "john@example.com",
    "subject": "Document",
    "body": "Here's the file",
    "attachment_path": "~/Documents/report.pdf"
  }
}
```

---

### reply_email
Reply to email

**Parameters**:
- `to_email` (string, required): Recipient
- `original_subject` (string, required): Original subject
- `reply_body` (string, required): Reply message

---

### search_emails
Search emails by keyword

**Parameters**:
- `keyword` (string, required): Search keyword

---

## DOCUMENTS

### create_resume
Generate resume document

**Parameters**:
- `name` (string, required): Full name
- `email` (string, required): Email address
- `phone` (string, required): Phone number
- `experience` (array, required): Experience list
- `education` (array, required): Education list
- `skills` (array, required): Skills list

**Example**:
```json
{
  "tool": "create_resume",
  "params": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "123-456-7890",
    "experience": [
      {
        "title": "Developer",
        "company": "Tech Corp",
        "description": "Built web applications"
      }
    ],
    "education": [
      {
        "degree": "BS Computer Science",
        "school": "University"
      }
    ],
    "skills": ["Python", "JavaScript", "React"]
  }
}
```

---

### create_cover_letter
Generate cover letter

**Parameters**:
- `name` (string, required): Your name
- `company` (string, required): Company name
- `position` (string, required): Job position
- `body` (string, required): Letter content

---

### spell_check
Check text for spelling errors

**Parameters**:
- `text` (string, required): Text to check

---

### summarize_pdf
Summarize PDF document

**Parameters**:
- `pdf_path` (string, required): PDF file path

---

### translate_text
Translate text

**Parameters**:
- `text` (string, required): Text to translate
- `language` (string, required): Target language

---

### generate_report
Create report document

**Parameters**:
- `title` (string, required): Report title
- `sections` (array, required): Report sections

**Example**:
```json
{
  "tool": "generate_report",
  "params": {
    "title": "Q1 Report",
    "sections": [
      {"title": "Overview", "content": "..."},
      {"title": "Results", "content": "..."}
    ]
  }
}
```

---

### read_pdf
Extract text from PDF

**Parameters**:
- `pdf_path` (string, required): PDF file path

---

## MESSAGING

### send_whatsapp_message
Send WhatsApp message

**Parameters**:
- `phone_number` (string, required): Recipient phone
- `message` (string, required): Message text

---

### send_whatsapp_image
Send image via WhatsApp

**Parameters**:
- `phone_number` (string, required): Recipient phone
- `image_path` (string, required): Image file path
- `caption` (string, optional): Image caption

---

### send_group_message
Send message to WhatsApp group

**Parameters**:
- `group_name` (string, required): Group name
- `message` (string, required): Message text

---

## EXCEL/SPREADSHEETS

### create_spreadsheet
Create Excel file

**Parameters**:
- `data` (dict, required): Data dictionary
- `sheet_name` (string, optional): Sheet name
- `save_path` (string, optional): Save location

**Example**:
```json
{
  "tool": "create_spreadsheet",
  "params": {
    "data": {
      "Name": ["Alice", "Bob"],
      "Age": [25, 30]
    },
    "save_path": "~/Documents/data.xlsx"
  }
}
```

---

### add_chart
Add chart to Excel

**Parameters**:
- `excel_path` (string, required): Excel file path
- `chart_type` (string, optional): "bar" or "pie"

---

### import_csv
Import CSV to Excel

**Parameters**:
- `csv_path` (string, required): CSV file path
- `save_path` (string, optional): Excel save path

---

### create_pivot_table
Create pivot table

**Parameters**:
- `excel_path` (string, required): Excel file path
- `values` (string, required): Column name for values
- `index` (string, required): Column name for index
- `aggfunc` (string, optional): Aggregation function

---

### create_budget_tracker
Create budget spreadsheet

**Parameters**:
- `categories` (array, required): Category names
- `amounts` (array, required): Amounts

**Example**:
```json
{
  "tool": "create_budget_tracker",
  "params": {
    "categories": ["Food", "Transport", "Entertainment"],
    "amounts": [5000, 2000, 1500]
  }
}
```

---

### add_formula
Add formula to cell

**Parameters**:
- `excel_path` (string, required): Excel file path
- `cell` (string, required): Cell reference (e.g., "A1")
- `formula` (string, required): Formula text

---

## MEDIA

### play_music
Play music file

**Parameters**:
- `file_path` (string, required): Audio file path

---

### pause_music
Pause playback

**Parameters**: None

---

### next_song
Play next track

**Parameters**: None

---

### previous_song
Play previous track

**Parameters**: None

---

### convert_video
Convert video format

**Parameters**:
- `input_path` (string, required): Input file path
- `output_path` (string, required): Output file path
- `format_type` (string, optional): Output format

---

### edit_image
Edit image

**Parameters**:
- `image_path` (string, required): Image file path
- `operation` (string, required): Operation type
- `params` (dict, optional): Operation parameters

**Operations**: resize, rotate, crop, blur, grayscale

---

### create_slideshow
Create video slideshow from images

**Parameters**:
- `image_folder` (string, required): Folder with images
- `output_path` (string, required): Video output path
- `duration` (integer, optional): Seconds per image

---

## DEVELOPER TOOLS

### open_terminal
Open command prompt/terminal

**Parameters**:
- `directory` (string, optional): Starting directory

---

### open_powershell
Open PowerShell

**Parameters**:
- `directory` (string, optional): Starting directory

---

### run_python_script
Execute Python script

**Parameters**:
- `script_path` (string, required): Script file path
- `arguments` (string, optional): Command arguments

---

### npm_install
Install npm package

**Parameters**:
- `package` (string, optional): Package name

---

### git_clone
Clone git repository

**Parameters**:
- `repository` (string, required): Repository URL
- `destination` (string, optional): Clone location

---

### git_commit
Commit changes

**Parameters**:
- `message` (string, required): Commit message
- `directory` (string, optional): Repository directory

---

### git_push
Push to remote

**Parameters**:
- `branch` (string, optional, default: "main"): Branch name

---

### start_localhost_server
Start local development server

**Parameters**:
- `port` (integer, optional, default: 8000): Port number

---

### create_react_component
Create React component file

**Parameters**:
- `component_name` (string, required): Component name

---

### docker_start
Start Docker container

**Parameters**:
- `container_name` (string, optional): Container name

---

### docker_stop
Stop Docker container

**Parameters**:
- `container_name` (string, required): Container name

---

### analyze_error
Analyze error message

**Parameters**:
- `error_message` (string, required): Error text

---

## PRODUCTIVITY

### set_reminder
Set reminder

**Parameters**:
- `text` (string, required): Reminder text
- `delay_minutes` (integer, optional, default: 5): Delay

---

### set_timer
Set timer

**Parameters**:
- `duration_seconds` (integer, required): Duration

---

### add_todo
Add task to todo list

**Parameters**:
- `task` (string, required): Task description

---

### list_todos
Get all todos

**Parameters**: None

---

### mark_todo_done
Mark task completed

**Parameters**:
- `todo_id` (string, required): Task ID

---

### schedule_meeting
Schedule meeting

**Parameters**:
- `title` (string, required): Meeting title
- `date_time` (string, required): Date and time
- `duration_minutes` (integer, optional): Duration

---

### open_calendar
Open calendar app

**Parameters**: None

---

### get_reminders
List active reminders

**Parameters**: None

---

### delete_todo
Delete task

**Parameters**:
- `todo_id` (string, required): Task ID

---

## ADVANCED FEATURES

### research_and_summarize
Research topic and summarize

**Parameters**:
- `query` (string, required): Search query
- `include_sources` (boolean, optional): Include sources

---

### create_and_send_report
Create report and email

**Parameters**:
- `title` (string, required): Report title
- `content` (string, required): Report content
- `recipient_email` (string, required): Email recipient

---

### complete_workflow
Execute multi-step workflow

**Parameters**:
- `workflow_steps` (array, required): Array of tools

**Example**:
```json
{
  "tool": "complete_workflow",
  "params": {
    "workflow_steps": [
      {"tool": "open_app", "params": {"name": "chrome"}},
      {"tool": "wait", "params": {"seconds": 2}},
      {"tool": "google_search", "params": {"query": "python"}}
    ]
  }
}
```

---

## Tips & Best Practices

1. **Always include wait times** between operations
2. **Use full paths** or ~/  for home directory
3. **Handle errors gracefully** in workflows
4. **Test individual tools** before complex workflows
5. **Use appropriate delays** for GUI operations
6. **Batch related operations** together
7. **Monitor resources** for long operations
8. **Store sensitive data** in environment variables

---

**Version**: 1.0 Extended
**Total Tools**: 100+
**Last Updated**: May 2024
