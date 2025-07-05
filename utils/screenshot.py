import pyautogui
from PIL import Image, ImageTk
import io
import base64
from config import Config

class ScreenshotManager:
    def __init__(self):
        pyautogui.FAILSAFE = Config.PYAUTOGUI_FAILSAFE
        pyautogui.PAUSE = Config.PYAUTOGUI_PAUSE
        self.current_screenshot = None
        
    def take_screenshot(self):
        """Take a screenshot and return PIL Image"""
        try:
            screenshot = pyautogui.screenshot()
            self.current_screenshot = screenshot
            return screenshot
        except Exception as e:
            raise Exception(f"Failed to take screenshot: {str(e)}")
    
    def get_thumbnail(self, size=(200, 150)):
        """Get thumbnail of current screenshot"""
        if not self.current_screenshot:
            return None
            
        thumbnail = self.current_screenshot.copy()
        thumbnail.thumbnail(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(thumbnail)
    
    def to_base64(self, image=None):
        """Convert image to base64 string"""
        if image is None:
            image = self.current_screenshot
            
        if not image:
            return None
            
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        return base64.b64encode(buffer.getvalue()).decode()
