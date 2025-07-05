import pyautogui
from config import Config

class ComputerActions:
    def __init__(self):
        pyautogui.FAILSAFE = Config.PYAUTOGUI_FAILSAFE
        pyautogui.PAUSE = Config.PYAUTOGUI_PAUSE
        
    def execute_action(self, action_data):
        """Execute a computer action"""
        action_type = action_data.get("action")
        
        if action_type == "click":
            x, y = action_data.get("coordinate", [0, 0])
            pyautogui.click(x, y)
            return f"Clicked at ({x}, {y})"
        
        elif action_type == "type":
            text = action_data.get("text", "")
            pyautogui.write(text)
            return f"Typed: {text}"
        
        elif action_type == "scroll":
            clicks = action_data.get("clicks", 3)
            pyautogui.scroll(clicks)
            return f"Scrolled {clicks} clicks"
        
        elif action_type == "key":
            key = action_data.get("key")
            pyautogui.press(key)
            return f"Pressed key: {key}"
        
        elif action_type == "move":
            x, y = action_data.get("coordinate", [0, 0])
            pyautogui.moveTo(x, y)
            return f"Moved mouse to ({x}, {y})"
        
        elif action_type == "screenshot":
            # This would be handled by the screenshot manager
            return "Screenshot action requested"
        
        else:
            return f"Unknown action: {action_type}"
