# productivity_tools.py
"""
Productivity tools for JARVIS
"""

import os
import json
import time
import subprocess
from datetime import datetime, timedelta


class ProductivityTools:
    """Handle productivity operations"""
    
    # In-memory storage for reminders and todos
    reminders = {}
    todos = {}
    
    @staticmethod
    def set_reminder(text, delay_minutes=5):
        """Set a reminder"""
        try:
            reminder_id = datetime.now().timestamp()
            reminder_time = datetime.now() + timedelta(minutes=delay_minutes)
            
            ProductivityTools.reminders[reminder_id] = {
                "text": text,
                "time": reminder_time.isoformat(),
                "created": datetime.now().isoformat()
            }
            
            return {
                "success": True,
                "message": f"Reminder set for {delay_minutes} minutes from now",
                "reminder_id": reminder_id
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def set_timer(duration_seconds):
        """Set a timer"""
        try:
            timer_id = datetime.now().timestamp()
            end_time = datetime.now() + timedelta(seconds=duration_seconds)
            
            return {
                "success": True,
                "message": f"Timer started for {duration_seconds} seconds",
                "timer_id": timer_id,
                "end_time": end_time.isoformat()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def add_todo(task):
        """Add task to todo list"""
        try:
            todo_id = datetime.now().timestamp()
            
            ProductivityTools.todos[todo_id] = {
                "task": task,
                "completed": False,
                "created": datetime.now().isoformat(),
                "due_date": None
            }
            
            return {
                "success": True,
                "message": "Task added to todo list",
                "todo_id": todo_id
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def list_todos():
        """List all todos"""
        try:
            todos_list = []
            for todo_id, todo in ProductivityTools.todos.items():
                todos_list.append({
                    "id": todo_id,
                    "task": todo["task"],
                    "completed": todo["completed"]
                })
            
            return {
                "success": True,
                "todos": todos_list
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def mark_todo_done(todo_id):
        """Mark todo as completed"""
        try:
            if todo_id in ProductivityTools.todos:
                ProductivityTools.todos[todo_id]["completed"] = True
                
                return {
                    "success": True,
                    "message": "Task marked as completed"
                }
            else:
                return {
                    "success": False,
                    "error": "Todo not found"
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def schedule_meeting(title, date_time, duration_minutes=60):
        """Schedule a meeting"""
        try:
            meeting_id = datetime.now().timestamp()
            
            # This could integrate with calendar apps
            meeting_data = {
                "title": title,
                "datetime": date_time,
                "duration": duration_minutes,
                "created": datetime.now().isoformat()
            }
            
            return {
                "success": True,
                "message": f"Meeting scheduled: {title}",
                "meeting_id": meeting_id,
                "details": meeting_data
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def open_calendar():
        """Open calendar application"""
        try:
            # Try Windows Calendar
            subprocess.Popen("outlookcal.exe", shell=True)
            
            return {"success": True, "message": "Calendar opened"}
        except Exception as e:
            try:
                # Fallback to Outlook
                subprocess.Popen("outlook.exe", shell=True)
                return {"success": True, "message": "Outlook opened"}
            except:
                return {"success": False, "error": str(e)}
    
    @staticmethod
    def get_reminders():
        """Get all active reminders"""
        try:
            active_reminders = []
            now = datetime.now()
            
            for reminder_id, reminder in ProductivityTools.reminders.items():
                reminder_time = datetime.fromisoformat(reminder["time"])
                
                if reminder_time > now:
                    active_reminders.append({
                        "id": reminder_id,
                        "text": reminder["text"],
                        "time": reminder["time"]
                    })
            
            return {
                "success": True,
                "reminders": active_reminders
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def delete_todo(todo_id):
        """Delete a todo"""
        try:
            if todo_id in ProductivityTools.todos:
                del ProductivityTools.todos[todo_id]
                return {"success": True, "message": "Task deleted"}
            else:
                return {"success": False, "error": "Todo not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}


# Export
productivity_tools = ProductivityTools()
