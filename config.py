import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Configuration
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    CLAUDE_MODEL = "claude-3-5-sonnet-20241022"
    
    # GUI Configuration
    WINDOW_SIZE = "1400x900"
    WINDOW_TITLE = "Claude Computer Use Assistant"
    THEME_BG = '#2b2b2b'
    CHAT_BG = '#1e1e1e'
    CHAT_FG = 'white'
    
    # History Configuration
    MAX_HISTORY_MESSAGES = 20
    HISTORY_FILE = Path("claude_chat_history.json")
    
    # PyAutoGUI Configuration
    PYAUTOGUI_PAUSE = 0.5
    PYAUTOGUI_FAILSAFE = True
    
    # Browser Configuration
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    REQUEST_TIMEOUT = 10
    
    # File Operations
    SUPPORTED_TEXT_EXTENSIONS = ['.txt', '.py', '.json', '.html', '.css', '.js', '.md']
    SUPPORTED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    BINARY_EXTENSIONS = ['.exe', '.dll', '.bin']
