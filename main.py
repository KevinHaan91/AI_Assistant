
import os
import base64
import io
import time
import json
import shutil
from pathlib import Path
from PIL import Image
import pyautogui
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ClaudeComputerUse:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        # Disable pyautogui failsafe (optional - be careful!)
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0.5
    
    def take_screenshot(self):
        """Take a screenshot and return as base64 encoded string"""
        screenshot = pyautogui.screenshot()
        buffer = io.BytesIO()
        screenshot.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return img_str
    
    def execute_action(self, action_type, **kwargs):
        """Execute computer actions based on Claude's instructions"""
        try:
            if action_type == "click":
                x, y = kwargs.get("x"), kwargs.get("y")
                pyautogui.click(x, y)
                return f"Clicked at ({x}, {y})"
            
            elif action_type == "type":
                text = kwargs.get("text", "")
                pyautogui.write(text)
                return f"Typed: {text}"
            
            elif action_type == "scroll":
                clicks = kwargs.get("clicks", 3)
                pyautogui.scroll(clicks)
                return f"Scrolled {clicks} clicks"
            
            elif action_type == "key":
                key = kwargs.get("key")
                pyautogui.press(key)
                return f"Pressed key: {key}"
            
            elif action_type == "move":
                x, y = kwargs.get("x"), kwargs.get("y")
                pyautogui.moveTo(x, y)
                return f"Moved mouse to ({x}, {y})"
            
            else:
                return f"Unknown action type: {action_type}"
                
        except Exception as e:
            return f"Error executing action: {str(e)}"
    
    def read_file(self, file_path):
        """Read content from a file"""
        try:
            path = Path(file_path)
            if not path.exists():
                return f"File not found: {file_path}"
            
            if path.is_dir():
                return f"Path is a directory, not a file: {file_path}"
            
            # Handle different file types
            if path.suffix.lower() in ['.txt', '.py', '.js', '.html', '.css', '.json', '.xml', '.csv']:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return f"File content ({len(content)} characters):\n{content}"
            
            elif path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                return f"Image file detected: {file_path} (use image viewing tools to display)"
            
            elif path.suffix.lower() in ['.pdf', '.doc', '.docx']:
                return f"Document file detected: {file_path} (requires specialized tools to read)"
            
            else:
                # Try to read as text anyway
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    return f"File content ({len(content)} characters):\n{content}"
                except UnicodeDecodeError:
                    return f"Binary file detected: {file_path} (cannot display as text)"
                    
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def write_file(self, file_path, content, mode='w'):
        """Write content to a file"""
        try:
            path = Path(file_path)
            
            # Create directory if it doesn't exist
            path.parent.mkdir(parents=True, exist_ok=True)
            
            if mode == 'a':  # append
                with open(path, 'a', encoding='utf-8') as f:
                    f.write(content)
                return f"Content appended to: {file_path}"
            else:  # overwrite
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return f"Content written to: {file_path}"
                
        except Exception as e:
            return f"Error writing file: {str(e)}"
    
    def list_directory(self, dir_path="."):
        """List contents of a directory"""
        try:
            path = Path(dir_path)
            if not path.exists():
                return f"Directory not found: {dir_path}"
            
            if not path.is_dir():
                return f"Path is not a directory: {dir_path}"
            
            items = []
            for item in path.iterdir():
                if item.is_dir():
                    items.append(f"📁 {item.name}/")
                else:
                    size = item.stat().st_size
                    items.append(f"📄 {item.name} ({size} bytes)")
            
            return f"Directory contents of {dir_path}:\n" + "\n".join(sorted(items))
            
        except Exception as e:
            return f"Error listing directory: {str(e)}"
    
    def delete_file(self, file_path):
        """Delete a file or directory"""
        try:
            path = Path(file_path)
            if not path.exists():
                return f"File/directory not found: {file_path}"
            
            if path.is_dir():
                shutil.rmtree(path)
                return f"Directory deleted: {file_path}"
            else:
                path.unlink()
                return f"File deleted: {file_path}"
                
        except Exception as e:
            return f"Error deleting file: {str(e)}"
    
    def copy_file(self, source_path, dest_path):
        """Copy a file from source to destination"""
        try:
            source = Path(source_path)
            dest = Path(dest_path)
            
            if not source.exists():
                return f"Source file not found: {source_path}"
            
            # Create destination directory if needed
            dest.parent.mkdir(parents=True, exist_ok=True)
            
            if source.is_dir():
                shutil.copytree(source, dest, dirs_exist_ok=True)
                return f"Directory copied from {source_path} to {dest_path}"
            else:
                shutil.copy2(source, dest)
                return f"File copied from {source_path} to {dest_path}"
                
        except Exception as e:
            return f"Error copying file: {str(e)}"
    
    def move_file(self, source_path, dest_path):
        """Move a file from source to destination"""
        try:
            source = Path(source_path)
            dest = Path(dest_path)
            
            if not source.exists():
                return f"Source file not found: {source_path}"
            
            # Create destination directory if needed
            dest.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.move(str(source), str(dest))
            return f"File moved from {source_path} to {dest_path}"
                
        except Exception as e:
            return f"Error moving file: {str(e)}"
    
    def send_to_claude(self, message, screenshot_b64=None):
        """Send message and screenshot to Claude"""
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": message}
                ]
            }
        ]
        
        # Add screenshot if provided
        if screenshot_b64:
            messages[0]["content"].append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": screenshot_b64
                }
            })
        
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",  # Use appropriate model
                max_tokens=1024,
                messages=messages,
                tools=[
                    {
                        "name": "computer",
                        "description": "Use a computer to perform actions",
                        "input_schema": {
                            "type": "object",
                            "properties": {
                                "action": {
                                    "type": "string",
                                    "enum": ["click", "type", "scroll", "key", "move", "screenshot"]
                                },
                                "coordinate": {
                                    "type": "array",
                                    "items": {"type": "integer"},
                                    "description": "[x, y] coordinates for click/move actions"
                                },
                                "text": {
                                    "type": "string",
                                    "description": "Text to type"
                                },
                                "key": {
                                    "type": "string",
                                    "description": "Key to press (e.g., 'enter', 'tab', 'escape')"
                                },
                                "clicks": {
                                    "type": "integer",
                                    "description": "Number of scroll clicks"
                                }
                            },
                            "required": ["action"]
                        }
                    },
                    {
                        "name": "file_operations",
                        "description": "Perform file and directory operations",
                        "input_schema": {
                            "type": "object",
                            "properties": {
                                "operation": {
                                    "type": "string",
                                    "enum": ["read", "write", "list", "delete", "copy", "move"]
                                },
                                "file_path": {
                                    "type": "string",
                                    "description": "Path to the file or directory"
                                },
                                "content": {
                                    "type": "string",
                                    "description": "Content to write (for write operations)"
                                },
                                "dest_path": {
                                    "type": "string",
                                    "description": "Destination path (for copy/move operations)"
                                },
                                "mode": {
                                    "type": "string",
                                    "enum": ["w", "a"],
                                    "description": "Write mode: 'w' for overwrite, 'a' for append"
                                }
                            },
                            "required": ["operation", "file_path"]
                        }
                    }
                ]
            )
            return response
        except Exception as e:
            print(f"Error communicating with Claude: {str(e)}")
            return None
    
    def run_interactive_session(self):
        """Run an interactive session with Claude"""
        print("Claude Computer Use Assistant Started!")
        print("Type 'quit' to exit, 'screenshot' to take a screenshot")
        print("-" * 50)
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'quit':
                print("Goodbye!")
                break
            
            if user_input.lower() == 'screenshot':
                screenshot = self.take_screenshot()
                print("Screenshot taken!")
                continue
            
            # Take screenshot and send to Claude
            screenshot = self.take_screenshot()
            response = self.send_to_claude(user_input, screenshot)
            
            if response:
                print(f"\nClaude: {response.content[0].text}")
                
                # Check if Claude wants to use tools
                if response.stop_reason == "tool_use":
                    for tool_call in response.content:
                        if tool_call.type == "tool_use":
                            if tool_call.name == "computer":
                                action_data = tool_call.input
                                action_type = action_data.get("action")
                                
                                if action_type == "click":
                                    x, y = action_data.get("coordinate", [0, 0])
                                    result = self.execute_action("click", x=x, y=y)
                                elif action_type == "type":
                                    text = action_data.get("text", "")
                                    result = self.execute_action("type", text=text)
                                elif action_type == "key":
                                    key = action_data.get("key", "")
                                    result = self.execute_action("key", key=key)
                                elif action_type == "scroll":
                                    clicks = action_data.get("clicks", 3)
                                    result = self.execute_action("scroll", clicks=clicks)
                                elif action_type == "move":
                                    x, y = action_data.get("coordinate", [0, 0])
                                    result = self.execute_action("move", x=x, y=y)
                                elif action_type == "screenshot":
                                    result = "Screenshot taken"
                                else:
                                    result = f"Unknown action: {action_type}"
                                
                                print(f"Computer action executed: {result}")
                            
                            elif tool_call.name == "file_operations":
                                file_data = tool_call.input
                                operation = file_data.get("operation")
                                file_path = file_data.get("file_path")
                                
                                if operation == "read":
                                    result = self.read_file(file_path)
                                elif operation == "write":
                                    content = file_data.get("content", "")
                                    mode = file_data.get("mode", "w")
                                    result = self.write_file(file_path, content, mode)
                                elif operation == "list":
                                    result = self.list_directory(file_path)
                                elif operation == "delete":
                                    result = self.delete_file(file_path)
                                elif operation == "copy":
                                    dest_path = file_data.get("dest_path")
                                    result = self.copy_file(file_path, dest_path)
                                elif operation == "move":
                                    dest_path = file_data.get("dest_path")
                                    result = self.move_file(file_path, dest_path)
                                else:
                                    result = f"Unknown file operation: {operation}"
                                
                                print(f"File operation executed: {result}")
                                
                                # If it's a read operation, also show Claude the result
                                if operation == "read" and not result.startswith("Error"):
                                    print(f"\nFile content preview:\n{result[:500]}{'...' if len(result) > 500 else ''}")
    
    def run_file_commands(self):
        """Run file operation commands directly"""
        print("\nDirect File Operations:")
        print("Commands: read <file>, write <file> <content>, list <dir>, delete <file>")
        print("          copy <source> <dest>, move <source> <dest>")
        print("Type 'back' to return to main chat")
        
        while True:
            cmd = input("\nFile> ").strip()
            if cmd.lower() == 'back':
                break
            
            parts = cmd.split(' ', 2)
            if len(parts) < 2:
                print("Invalid command format")
                continue
            
            operation = parts[0].lower()
            file_path = parts[1]
            
            if operation == "read":
                result = self.read_file(file_path)
                print(result)
            elif operation == "write":
                if len(parts) < 3:
                    print("Write command requires content: write <file> <content>")
                    continue
                content = parts[2]
                result = self.write_file(file_path, content)
                print(result)
            elif operation == "list":
                result = self.list_directory(file_path)
                print(result)
            elif operation == "delete":
                confirm = input(f"Are you sure you want to delete '{file_path}'? (y/N): ")
                if confirm.lower() == 'y':
                    result = self.delete_file(file_path)
                    print(result)
                else:
                    print("Deletion cancelled")
            elif operation == "copy":
                if len(parts) < 3:
                    print("Copy command requires destination: copy <source> <dest>")
                    continue
                dest_path = parts[2]
                result = self.copy_file(file_path, dest_path)
                print(result)
            elif operation == "move":
                if len(parts) < 3:
                    print("Move command requires destination: move <source> <dest>")
                    continue
                dest_path = parts[2]
                result = self.move_file(file_path, dest_path)
                print(result)
            else:
                print(f"Unknown operation: {operation}")
    
    def run_interactive_session(self):
        """Run an interactive session with Claude"""
        print("Claude Computer Use Assistant with File Operations Started!")
        print("Type 'quit' to exit")
        print("Type 'screenshot' to take a screenshot")
        print("Type 'files' for direct file operations")
        print("-" * 60)
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'quit':
                print("Goodbye!")
                break
            
            if user_input.lower() == 'screenshot':
                screenshot = self.take_screenshot()
                print("Screenshot taken!")
                continue
            
            if user_input.lower() == 'files':
                self.run_file_commands()
                continue
            
            # Take screenshot and send to Claude
            screenshot = self.take_screenshot()
            response = self.send_to_claude(user_input, screenshot)
            
            if response:
                print(f"\nClaude: {response.content[0].text}")
                
                # Check if Claude wants to use tools
                if response.stop_reason == "tool_use":
                    for tool_call in response.content:
                        if tool_call.type == "tool_use":
                            if tool_call.name == "computer":
                                action_data = tool_call.input
                                action_type = action_data.get("action")
                                
                                if action_type == "click":
                                    x, y = action_data.get("coordinate", [0, 0])
                                    result = self.execute_action("click", x=x, y=y)
                                elif action_type == "type":
                                    text = action_data.get("text", "")
                                    result = self.execute_action("type", text=text)
                                elif action_type == "key":
                                    key = action_data.get("key", "")
                                    result = self.execute_action("key", key=key)
                                elif action_type == "scroll":
                                    clicks = action_data.get("clicks", 3)
                                    result = self.execute_action("scroll", clicks=clicks)
                                elif action_type == "move":
                                    x, y = action_data.get("coordinate", [0, 0])
                                    result = self.execute_action("move", x=x, y=y)
                                elif action_type == "screenshot":
                                    result = "Screenshot taken"
                                else:
                                    result = f"Unknown action: {action_type}"
                                
                                print(f"Computer action executed: {result}")
                            
                            elif tool_call.name == "file_operations":
                                file_data = tool_call.input
                                operation = file_data.get("operation")
                                file_path = file_data.get("file_path")
                                
                                if operation == "read":
                                    result = self.read_file(file_path)
                                elif operation == "write":
                                    content = file_data.get("content", "")
                                    mode = file_data.get("mode", "w")
                                    result = self.write_file(file_path, content, mode)
                                elif operation == "list":
                                    result = self.list_directory(file_path)
                                elif operation == "delete":
                                    result = self.delete_file(file_path)
                                elif operation == "copy":
                                    dest_path = file_data.get("dest_path")
                                    result = self.copy_file(file_path, dest_path)
                                elif operation == "move":
                                    dest_path = file_data.get("dest_path")
                                    result = self.move_file(file_path, dest_path)
                                else:
                                    result = f"Unknown file operation: {operation}"
                                
                                print(f"File operation executed: {result}")
                                
                                # If it's a read operation, also show Claude the result
                                if operation == "read" and not result.startswith("Error"):
                                    print(f"\nFile content preview:\n{result[:500]}{'...' if len(result) > 500 else ''}")
                    

if __name__ == "__main__":
    assistant = ClaudeComputerUse()
    assistant.run_interactive_session()