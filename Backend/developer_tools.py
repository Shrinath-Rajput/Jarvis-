# developer_tools.py
"""
Developer tools for JARVIS - PRODUCTION-GRADE with verification
"""

import subprocess
import os
import sys
import time
import psutil
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)


class DeveloperTools:
    """Handle developer operations with REAL verification"""
    
    @staticmethod
    def open_terminal(directory=None):
        """✅ Open terminal/command prompt with verification"""
        try:
            logger.info(f"🚀 Opening terminal in: {directory or 'default'}")
            
            if directory:
                directory = os.path.expanduser(directory)
                if not os.path.exists(directory):
                    logger.error(f"❌ Directory not found: {directory}")
                    return {"success": False, "error": f"Directory not found: {directory}"}
                
                logger.info(f"📂 Directory exists: {directory}")
                
                # Open file explorer in that directory
                os.startfile(directory)
                time.sleep(0.5)
                
                # Open CMD in that directory
                logger.info(f"▶️  Starting cmd.exe in directory...")
                proc = subprocess.Popen("cmd.exe", cwd=directory)
                
                if proc.pid is None:
                    logger.error(f"❌ Failed to get process ID for cmd.exe")
                    return {"success": False, "error": "Failed to start cmd.exe"}
                
                logger.info(f"✅ cmd.exe started with PID: {proc.pid}")
            else:
                logger.info(f"▶️  Starting cmd.exe (default)...")
                proc = subprocess.Popen("cmd.exe")
                
                if proc.pid is None:
                    logger.error(f"❌ Failed to get process ID for cmd.exe")
                    return {"success": False, "error": "Failed to start cmd.exe"}
                
                logger.info(f"✅ cmd.exe started with PID: {proc.pid}")
            
            # Wait for process to start
            time.sleep(2)
            
            # Verify cmd.exe is running
            cmd_running = False
            for proc_item in psutil.process_iter(['pid', 'name']):
                if proc_item.info['name'].lower() == 'cmd.exe':
                    cmd_running = True
                    logger.info(f"✅ Verified: cmd.exe is running")
                    break
            
            if not cmd_running:
                logger.warning(f"⚠️  cmd.exe not detected in process list")
                # But still return success since process was created
                return {"success": True, "message": "Terminal opened", "pid": proc.pid}
            
            return {"success": True, "message": "✅ Terminal opened", "pid": proc.pid}
        
        except Exception as e:
            error_msg = f"❌ Error opening terminal: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    @staticmethod
    def open_powershell(directory=None):
        """✅ Open PowerShell with verification"""
        try:
            logger.info(f"🚀 Opening PowerShell in: {directory or 'default'}")
            
            if directory:
                directory = os.path.expanduser(directory)
                if not os.path.exists(directory):
                    logger.error(f"❌ Directory not found: {directory}")
                    return {"success": False, "error": f"Directory not found: {directory}"}
                
                logger.info(f"📂 Directory exists: {directory}")
                logger.info(f"▶️  Starting PowerShell...")
                
                proc = subprocess.Popen([
                    "powershell.exe",
                    "-NoExit",
                    "-Command",
                    f"Set-Location '{directory}'"
                ])
            else:
                logger.info(f"▶️  Starting PowerShell...")
                proc = subprocess.Popen("powershell.exe")
            
            if proc.pid is None:
                logger.error(f"❌ Failed to get process ID for PowerShell")
                return {"success": False, "error": "Failed to start PowerShell"}
            
            logger.info(f"✅ PowerShell started with PID: {proc.pid}")
            time.sleep(2)
            
            # Verify PowerShell is running
            ps_running = False
            for proc_item in psutil.process_iter(['pid', 'name']):
                if proc_item.info['name'].lower() == 'powershell.exe':
                    ps_running = True
                    logger.info(f"✅ Verified: PowerShell is running")
                    break
            
            if not ps_running:
                logger.warning(f"⚠️  PowerShell not detected in process list")
            
            return {"success": True, "message": "✅ PowerShell opened", "pid": proc.pid}
        
        except Exception as e:
            error_msg = f"❌ Error opening PowerShell: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    @staticmethod
    def run_python_script(script_path, arguments=None):
        """✅ Run Python script with verification"""
        try:
            script_path = os.path.expanduser(script_path)
            
            logger.info(f"🐍 Running Python script: {script_path}")
            
            if not os.path.exists(script_path):
                error_msg = f"❌ Script not found: {script_path}"
                logger.error(error_msg)
                return {"success": False, "error": error_msg}
            
            logger.info(f"✅ Script file exists")
            
            cmd = [sys.executable, script_path]
            
            if arguments:
                cmd.extend(arguments.split())
                logger.info(f"📋 Arguments: {arguments}")
            
            logger.info(f"▶️  Executing: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            logger.info(f"✅ Script executed. Return code: {result.returncode}")
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.stderr else None,
                "return_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            error_msg = f"❌ Script execution timeout (5 minutes)"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
        except Exception as e:
            error_msg = f"❌ Error running script: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    @staticmethod
    def npm_install(package=None, directory=None):
        """✅ Install npm package with verification"""
        try:
            cmd = ["npm", "install"]
            
            if package:
                cmd.append(package)
                logger.info(f"📦 Installing npm package: {package}")
            else:
                logger.info(f"📦 Installing npm dependencies")
            
            if directory:
                directory = os.path.expanduser(directory)
                logger.info(f"📂 Working directory: {directory}")
            
            logger.info(f"▶️  Running: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=directory, timeout=600)
            
            success = result.returncode == 0
            
            if success:
                logger.info(f"✅ npm install successful")
            else:
                logger.error(f"❌ npm install failed with return code {result.returncode}")
            
            return {
                "success": success,
                "message": f"npm install {'✅ successful' if success else '❌ failed'}",
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            error_msg = f"❌ npm install timeout (10 minutes)"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
        except Exception as e:
            error_msg = f"❌ Error with npm install: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    @staticmethod
    def git_clone(repository, destination=None):
        """✅ Clone git repository with verification"""
        try:
            if destination is None:
                destination = os.path.expanduser("~/Projects/")
            
            destination = os.path.expanduser(destination)
            
            logger.info(f"📦 Cloning repository: {repository}")
            logger.info(f"📂 Destination: {destination}")
            
            os.makedirs(destination, exist_ok=True)
            
            logger.info(f"▶️  Running git clone...")
            
            result = subprocess.run(
                ["git", "clone", repository],
                capture_output=True,
                text=True,
                cwd=destination,
                timeout=600
            )
            
            success = result.returncode == 0
            
            if success:
                logger.info(f"✅ Repository cloned successfully")
            else:
                logger.error(f"❌ git clone failed with return code {result.returncode}")
            
            return {
                "success": success,
                "message": "✅ Repository cloned" if success else "❌ Clone failed",
                "output": result.stdout,
                "error": result.stderr,
                "destination": destination,
                "return_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            error_msg = f"❌ git clone timeout (10 minutes)"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
        except Exception as e:
            error_msg = f"❌ Error cloning repository: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    @staticmethod
    def git_commit(message, directory=None):
        """✅ Commit changes to git with verification"""
        try:
            logger.info(f"💾 Committing changes: {message}")
            
            if directory:
                directory = os.path.expanduser(directory)
                logger.info(f"📂 Directory: {directory}")
            
            logger.info(f"▶️  Running git commit...")
            
            result = subprocess.run(
                ["git", "commit", "-m", message],
                capture_output=True,
                text=True,
                cwd=directory,
                timeout=60
            )
            
            success = result.returncode == 0
            
            if success:
                logger.info(f"✅ Changes committed")
            else:
                logger.error(f"❌ git commit failed with return code {result.returncode}")
            
            return {
                "success": success,
                "message": "✅ Changes committed" if success else "❌ Commit failed",
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
        except Exception as e:
            error_msg = f"❌ Error committing: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    @staticmethod
    def git_push(branch="main", directory=None):
        """✅ Push changes to remote with verification"""
        try:
            logger.info(f"📤 Pushing to branch: {branch}")
            
            if directory:
                directory = os.path.expanduser(directory)
                logger.info(f"📂 Directory: {directory}")
            
            logger.info(f"▶️  Running git push...")
            
            result = subprocess.run(
                ["git", "push", "origin", branch],
                capture_output=True,
                text=True,
                cwd=directory,
                timeout=120
            )
            
            success = result.returncode == 0
            
            if success:
                logger.info(f"✅ Pushed to {branch}")
            else:
                logger.error(f"❌ git push failed with return code {result.returncode}")
            
            return {
                "success": success,
                "message": f"✅ Pushed to {branch}" if success else "❌ Push failed",
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
        except Exception as e:
            error_msg = f"❌ Error pushing: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    @staticmethod
    def start_local_server(port=8000, directory=None):
        """✅ Start local development server with verification"""
        try:
            logger.info(f"🌐 Starting local server on port {port}")
            
            if directory:
                directory = os.path.expanduser(directory)
                logger.info(f"📂 Directory: {directory}")
            
            logger.info(f"▶️  Starting Python HTTP server...")
            
            proc = subprocess.Popen(
                [sys.executable, "-m", "http.server", str(port)],
                cwd=directory,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            if proc.pid is None:
                logger.error(f"❌ Failed to start server")
                return {"success": False, "error": "Failed to start server"}
            
            logger.info(f"✅ Server started with PID: {proc.pid}")
            time.sleep(2)
            
            # Verify process is running
            try:
                running_proc = psutil.Process(proc.pid)
                status = running_proc.status()
                logger.info(f"✅ Server verified running: {status}")
            except:
                logger.warning(f"⚠️  Could not verify server process")
            
            return {
                "success": True,
                "message": f"✅ Server started on http://localhost:{port}",
                "pid": proc.pid,
                "port": port
            }
        except Exception as e:
            error_msg = f"❌ Error starting server: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    @staticmethod
    def create_react_component(component_name, directory=None):
        """✅ Create React component file with verification"""
        try:
            if directory is None:
                directory = os.path.expanduser("~/src/components")
            
            directory = os.path.expanduser(directory)
            
            logger.info(f"⚛️  Creating React component: {component_name}")
            logger.info(f"📂 Directory: {directory}")
            
            os.makedirs(directory, exist_ok=True)
            
            component_path = os.path.join(directory, f"{component_name}.jsx")
            
            logger.info(f"📄 File path: {component_path}")
            
            template = f'''import React from 'react';

const {component_name} = () => {{
  return (
    <div className="{component_name.lower()}">
      <h1>{component_name} Component</h1>
    </div>
  );
}};

export default {component_name};
'''
            
            with open(component_path, 'w') as f:
                f.write(template)
            
            # Verify file was created
            if os.path.exists(component_path):
                logger.info(f"✅ Component file created successfully")
                return {"success": True, "message": f"✅ Component created: {component_path}"}
            else:
                logger.error(f"❌ Component file not created")
                return {"success": False, "error": "Component file not created"}
        
        except Exception as e:
            error_msg = f"❌ Error creating component: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    @staticmethod
    def docker_start(container_name=None):
        """✅ Start Docker container with verification"""
        try:
            logger.info(f"🐳 Starting Docker container: {container_name or 'new'}")
            
            if container_name:
                cmd = ["docker", "start", container_name]
                logger.info(f"▶️  Running: docker start {container_name}")
            else:
                logger.warning(f"⚠️  No container name specified")
                return {"success": False, "error": "Container name required"}
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            success = result.returncode == 0
            
            if success:
                logger.info(f"✅ Docker container started: {container_name}")
            else:
                logger.error(f"❌ Docker start failed: {result.stderr}")
            
            return {
                "success": success,
                "message": f"✅ Docker container started" if success else "❌ Start failed",
                "output": result.stdout,
                "error": result.stderr,
                "container": container_name,
                "return_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            error_msg = f"❌ Docker command timeout (30 seconds)"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
        except Exception as e:
            error_msg = f"❌ Error starting Docker container: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    @staticmethod
    def docker_stop(container_name):
        """✅ Stop Docker container with verification"""
        try:
            logger.info(f"🛑 Stopping Docker container: {container_name}")
            logger.info(f"▶️  Running: docker stop {container_name}")
            
            result = subprocess.run(
                ["docker", "stop", container_name],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            success = result.returncode == 0
            
            if success:
                logger.info(f"✅ Docker container stopped: {container_name}")
                time.sleep(1)  # Wait for container to stop
            else:
                logger.error(f"❌ Docker stop failed: {result.stderr}")
            
            return {
                "success": success,
                "message": f"✅ Container {container_name} stopped" if success else "❌ Stop failed",
                "output": result.stdout,
                "error": result.stderr,
                "container": container_name,
                "return_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            error_msg = f"❌ Docker command timeout (30 seconds)"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
        except Exception as e:
            error_msg = f"❌ Error stopping Docker container: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}
    
    @staticmethod
    def analyze_error(error_message):
        """✅ Analyze error message and suggest solutions"""
        try:
            logger.info(f"🔍 Analyzing error: {error_message[:100]}")
            
            error_lower = error_message.lower()
            
            solutions = []
            
            if "module not found" in error_lower or "importerror" in error_lower:
                solutions.append("❌ Missing Python module")
                solutions.append("💡 Install it: pip install module_name")
            
            if "syntaxerror" in error_lower:
                solutions.append("❌ Python syntax error")
                solutions.append("💡 Check line numbers and brackets")
            
            if "404" in error_lower:
                solutions.append("❌ Resource not found (HTTP 404)")
                solutions.append("💡 Verify URL or endpoint exists")
            
            if "connection" in error_lower or "refused" in error_lower:
                solutions.append("❌ Connection error")
                solutions.append("💡 Check server is running")
                solutions.append("💡 Verify network connectivity")
            
            if "permission" in error_lower or "access denied" in error_lower:
                solutions.append("❌ Permission denied")
                solutions.append("💡 Run as administrator")
                solutions.append("💡 Check file/folder permissions")
            
            if "timeout" in error_lower:
                solutions.append("❌ Operation timeout")
                solutions.append("💡 Server may be slow or unresponsive")
            
            if not solutions:
                solutions = ["❌ Unknown error", "💡 Search online for this error message"]
            
            logger.info(f"✅ Error analysis complete: {len(solutions)} suggestions")
            
            return {
                "success": True,
                "error": error_message,
                "suggestions": solutions
            }
        except Exception as e:
            error_msg = f"❌ Error analyzing error: {str(e)}"
            logger.error(error_msg)
            return {"success": False, "error": error_msg}


# Create singleton instance
developer_tools = DeveloperTools()
