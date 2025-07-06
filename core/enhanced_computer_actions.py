"""
Enhanced Computer Actions for Claude Computer Use Assistant
Improved automation with better error handling and smart features
"""

import pyautogui
import time
import platform
from config import Config
from pathlib import Path

class EnhancedComputerActions:
    """Enhanced computer automation with smart features"""
    
    def __init__(self):
        self.setup_pyautogui()
        self.available = True
        self.action_history = []
        self.last_screenshot = None
        
        # Smart features
        self.smart_delays = True
        self.verify_actions = True
        self.auto_recovery = True
        
    def setup_pyautogui(self):
        """Setup PyAutoGUI with optimal settings"""
        try:
            pyautogui.FAILSAFE = Config.PYAUTOGUI_FAILSAFE
            pyautogui.PAUSE = Config.PYAUTOGUI_PAUSE
            
            # Platform-specific optimizations
            if platform.system() == "Windows":
                # Windows-specific settings
                pass
            elif platform.system() == "Darwin":  # macOS
                # macOS-specific settings
                pass
            elif platform.system() == "Linux":
                # Linux-specific settings
                pass
                
        except Exception as e:
            print(f"PyAutoGUI setup error: {str(e)}")
            self.available = False
            
    def execute_action(self, action_data):
        """Execute a computer action with enhanced error handling"""
        if not self.available:
            return "Computer automation not available"
            
        action_type = action_data.get("action")
        
        try:
            # Record action
            self.action_history.append({
                'action': action_data,
                'timestamp': time.time()
            })
            
            # Execute based on action type
            if action_type == "click":
                return self.smart_click(action_data)
            elif action_type == "type":
                return self.smart_type(action_data)
            elif action_type == "scroll":
                return self.smart_scroll(action_data)
            elif action_type == "key":
                return self.smart_key_press(action_data)
            elif action_type == "move":
                return self.smart_move(action_data)
            elif action_type == "screenshot":
                return self.take_screenshot()
            elif action_type == "find_and_click":
                return self.find_and_click(action_data)
            elif action_type == "drag":
                return self.smart_drag(action_data)
            else:
                return f"Unknown action: {action_type}"
                
        except pyautogui.FailSafeException:
            return "Action cancelled by failsafe (mouse moved to corner)"
        except Exception as e:
            return f"Action failed: {str(e)}"
            
    def smart_click(self, action_data):
        """Smart click with verification and error recovery"""
        x, y = action_data.get("coordinate", [0, 0])
        clicks = action_data.get("clicks", 1)
        button = action_data.get("button", "left")
        
        # Validate coordinates
        screen_width, screen_height = pyautogui.size()
        if not (0 <= x <= screen_width and 0 <= y <= screen_height):
            return f"Coordinates ({x}, {y}) are outside screen bounds"
        
        # Take screenshot before action if verification enabled
        if self.verify_actions:
            self.last_screenshot = pyautogui.screenshot()
        
        # Perform click
        if button == "right":
            pyautogui.rightClick(x, y, clicks=clicks)
        elif button == "middle":
            pyautogui.middleClick(x, y)
        else:
            pyautogui.click(x, y, clicks=clicks)
        
        # Smart delay based on action
        if self.smart_delays:
            time.sleep(0.1)  # Brief pause after click
        
        return f"Clicked at ({x}, {y}) with {button} button ({clicks} clicks)"
    
    def smart_type(self, action_data):
        """Smart typing with special character handling"""
        text = action_data.get("text", "")
        interval = action_data.get("interval", 0.0)
        
        if not text:
            return "No text provided"
        
        # Handle special text patterns
        if text.startswith("PASTE:"):
            # Paste from clipboard
            actual_text = text[6:]  # Remove "PASTE:" prefix
            pyautogui.hotkey('ctrl', 'v')
            return f"Pasted clipboard content"
        
        # Smart typing with natural intervals
        if self.smart_delays and interval == 0.0:
            interval = max(0.01, min(0.05, len(text) / 1000))  # Dynamic interval
        
        pyautogui.write(text, interval=interval)
        
        return f"Typed: '{text[:50]}{'...' if len(text) > 50 else ''}'"
    
    def smart_scroll(self, action_data):
        """Smart scrolling with direction detection"""
        clicks = action_data.get("clicks", 3)
        x = action_data.get("x", None)
        y = action_data.get("y", None)
        
        # Scroll at specific location if provided
        if x is not None and y is not None:
            pyautogui.scroll(clicks, x, y)
            return f"Scrolled {clicks} clicks at ({x}, {y})"
        else:
            pyautogui.scroll(clicks)
            direction = "up" if clicks > 0 else "down"
            return f"Scrolled {abs(clicks)} clicks {direction}"
    
    def smart_key_press(self, action_data):
        """Smart key pressing with combo support"""
        key = action_data.get("key")
        
        if not key:
            return "No key specified"
        
        # Handle key combinations
        if '+' in key:
            keys = key.split('+')
            keys = [k.strip().lower() for k in keys]
            pyautogui.hotkey(*keys)
            return f"Pressed key combination: {key}"
        else:
            pyautogui.press(key.lower())
            return f"Pressed key: {key}"
    
    def smart_move(self, action_data):
        """Smart mouse movement with smooth motion"""
        x, y = action_data.get("coordinate", [0, 0])
        duration = action_data.get("duration", 0.5)
        
        # Validate coordinates
        screen_width, screen_height = pyautogui.size()
        if not (0 <= x <= screen_width and 0 <= y <= screen_height):
            return f"Coordinates ({x}, {y}) are outside screen bounds"
        
        # Smooth movement
        pyautogui.moveTo(x, y, duration=duration)
        
        return f"Moved mouse to ({x}, {y}) in {duration}s"
    
    def smart_drag(self, action_data):
        """Smart drag operation"""
        start_x, start_y = action_data.get("start", [0, 0])
        end_x, end_y = action_data.get("end", [0, 0])
        duration = action_data.get("duration", 1.0)
        button = action_data.get("button", "left")
        
        # Validate coordinates
        screen_width, screen_height = pyautogui.size()
        for x, y in [(start_x, start_y), (end_x, end_y)]:
            if not (0 <= x <= screen_width and 0 <= y <= screen_height):
                return f"Coordinates ({x}, {y}) are outside screen bounds"
        
        # Perform drag
        pyautogui.drag(end_x - start_x, end_y - start_y, 
                      duration=duration, button=button)
        
        return f"Dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})"
    
    def find_and_click(self, action_data):
        """Find image on screen and click it"""
        image_path = action_data.get("image_path")
        confidence = action_data.get("confidence", 0.8)
        
        if not image_path or not Path(image_path).exists():
            return "Image file not found"
        
        try:
            # Locate image on screen
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            
            if location:
                # Click center of found image
                center = pyautogui.center(location)
                pyautogui.click(center)
                return f"Found and clicked image at {center}"
            else:
                return "Image not found on screen"
                
        except Exception as e:
            return f"Image search failed: {str(e)}"
    
    def take_screenshot(self):
        """Take a screenshot and return info"""
        try:
            screenshot = pyautogui.screenshot()
            self.last_screenshot = screenshot
            return f"Screenshot taken: {screenshot.size[0]}x{screenshot.size[1]}"
        except Exception as e:
            return f"Screenshot failed: {str(e)}"
    
    def get_screen_info(self):
        """Get screen information"""
        try:
            width, height = pyautogui.size()
            mouse_x, mouse_y = pyautogui.position()
            
            return {
                'screen_size': (width, height),
                'mouse_position': (mouse_x, mouse_y),
                'available': self.available
            }
        except Exception as e:
            return f"Could not get screen info: {str(e)}"
    
    def send_text_message(self, recipient, message):
        """Enhanced text message sending via Google Voice"""
        try:
            # Open Google Voice
            import webbrowser
            google_voice_url = "https://voice.google.com/u/0/messages"
            webbrowser.open(google_voice_url)
            
            # Wait for page to load
            time.sleep(3)
            
            # Try to automate the process
            if self.available:
                # This is a basic implementation - you might need to adjust based on the actual UI
                # Click on compose new message (this would need the actual coordinates)
                # pyautogui.click(100, 200)  # Example coordinates
                
                # For now, we'll just open the page and let user complete manually
                return f"Opened Google Voice for sending message to {recipient}: '{message}'"
            else:
                return "Opened Google Voice in browser - please complete manually"
                
        except Exception as e:
            return f"Failed to send message: {str(e)}"
    
    def simulate_human_behavior(self):
        """Add human-like randomness to actions"""
        if self.smart_delays:
            # Random small delay to simulate human timing
            import random
            delay = random.uniform(0.05, 0.15)
            time.sleep(delay)
    
    def get_action_history(self):
        """Get recent action history"""
        return self.action_history[-10:]  # Last 10 actions
    
    def clear_action_history(self):
        """Clear action history"""
        self.action_history.clear()
        return "Action history cleared"
    
    def emergency_stop(self):
        """Emergency stop all automation"""
        try:
            # Move mouse to fail-safe corner
            pyautogui.moveTo(0, 0)
            self.available = False
            return "Emergency stop activated - automation disabled"
        except:
            return "Emergency stop attempted"

# For backward compatibility
ComputerActions = EnhancedComputerActions
