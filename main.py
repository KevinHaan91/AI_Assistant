import os
import base64
import io
import time
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
        pyautogui.FAILSAFE = True
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
                        if tool_call.type == "tool_use" and tool_call.name == "computer":
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
                            
                            print(f"Action executed: {result}")

if __name__ == "__main__":
    assistant = ClaudeComputerUse()
    assistant.run_interactive_session()