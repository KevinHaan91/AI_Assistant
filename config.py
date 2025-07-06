"""
Enhanced Configuration for Claude Computer Use Assistant
Modern settings with improved defaults and theme support
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Enhanced configuration with modern defaults"""
    
    # API Configuration
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
    
    # Application Info
    APP_NAME = "Claude AI Assistant"
    APP_VERSION = "2.0.0"
    APP_DESCRIPTION = "Modern AI Assistant with Computer Automation"
    
    # Window Configuration
    WINDOW_SIZE = os.getenv("WINDOW_SIZE", "1600x1000")
    WINDOW_MIN_SIZE = "1200x700"
    WINDOW_TITLE = os.getenv("WINDOW_TITLE", "Claude AI Assistant")
    
    # Modern Theme Colors (Dark Theme)
    THEME_BG = os.getenv("THEME_BG", "#0f0f0f")
    THEME_SECONDARY = os.getenv("THEME_SECONDARY", "#1a1a1a")
    THEME_SURFACE = os.getenv("THEME_SURFACE", "#1e1e1e")
    THEME_ACCENT = os.getenv("THEME_ACCENT", "#007acc")
    
    # Chat Colors
    CHAT_BG = os.getenv("CHAT_BG", "#1e1e1e")
    CHAT_FG = os.getenv("CHAT_FG", "#ffffff")
    CHAT_USER_COLOR = "#007acc"
    CHAT_ASSISTANT_COLOR = "#00d4aa"
    CHAT_SYSTEM_COLOR = "#808080"
    CHAT_ERROR_COLOR = "#ff6b6b"
    
    # Text Colors
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#b0b0b0"
    TEXT_TERTIARY = "#808080"
    TEXT_DISABLED = "#4a4a4a"
    
    # Status Colors
    STATUS_ONLINE = "#51cf66"
    STATUS_BUSY = "#ffd43b"
    STATUS_ERROR = "#ff6b6b"
    STATUS_OFFLINE = "#808080"
    
    # Typography
    FONT_FAMILY = os.getenv("FONT_FAMILY", "Segoe UI")
    FONT_SIZE_LARGE = 16
    FONT_SIZE_MEDIUM = 12
    FONT_SIZE_SMALL = 10
    FONT_CODE = "Consolas"
    
    # History Configuration
    MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", "20"))
    HISTORY_FILE = Path("claude_chat_history.json")
    AUTO_SAVE_HISTORY = True
    
    # PyAutoGUI Configuration
    PYAUTOGUI_PAUSE = float(os.getenv("PYAUTOGUI_PAUSE", "0.3"))
    PYAUTOGUI_FAILSAFE = os.getenv("PYAUTOGUI_FAILSAFE", "true").lower() == "true"
    
    # Enhanced Automation Settings
    SMART_DELAYS = True
    VERIFY_ACTIONS = True
    AUTO_RECOVERY = True
    HUMAN_LIKE_TIMING = True
    
    # Web Configuration
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
    MAX_REDIRECTS = 5
    
    # File Operations
    SUPPORTED_TEXT_EXTENSIONS = [
        '.txt', '.py', '.json', '.html', '.css', '.js', '.md', 
        '.csv', '.xml', '.yml', '.yaml', '.ini', '.cfg'
    ]
    SUPPORTED_IMAGE_EXTENSIONS = [
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'
    ]
    BINARY_EXTENSIONS = [
        '.exe', '.dll', '.bin', '.so', '.dylib'
    ]
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_TO_FILE = True
    LOG_FILE_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 3
    
    # Performance Settings
    MAX_SCREENSHOT_SIZE = (1920, 1080)
    COMPRESS_SCREENSHOTS = True
    THUMBNAIL_SIZE = (200, 150)
    
    # Security Settings
    SAFE_MODE = os.getenv("SAFE_MODE", "false").lower() == "true"
    CONFIRM_DANGEROUS_ACTIONS = True
    ALLOWED_DOMAINS = []  # Empty means all domains allowed
    
    # Feature Flags
    ENABLE_COMPUTER_ACTIONS = True
    ENABLE_FILE_OPERATIONS = True
    ENABLE_WEB_OPERATIONS = True
    ENABLE_MESSAGE_SENDING = True
    ENABLE_AUTO_SCREENSHOT = True
    
    # Advanced Features
    ENABLE_VOICE_COMMANDS = False  # Future feature
    ENABLE_GESTURE_CONTROL = False  # Future feature
    ENABLE_AI_SUGGESTIONS = True
    
    # Directories
    BASE_DIR = Path(__file__).parent
    LOGS_DIR = BASE_DIR / "logs"
    EXPORTS_DIR = BASE_DIR / "exports"
    TEMP_DIR = BASE_DIR / "temp"
    SCREENSHOTS_DIR = BASE_DIR / "screenshots"
    
    # API Limits
    MAX_MESSAGE_LENGTH = 100000
    MAX_CONTEXT_LENGTH = 150000
    RATE_LIMIT_REQUESTS = 50  # per minute
    
    # UI Settings
    ANIMATION_SPEED = 250  # milliseconds
    TOOLTIP_DELAY = 500
    AUTO_HIDE_NOTIFICATIONS = 5000  # 5 seconds
    
    # Keyboard Shortcuts
    SHORTCUTS = {
        'new_chat': 'Ctrl+N',
        'save_chat': 'Ctrl+S',
        'open_file': 'Ctrl+O',
        'screenshot': 'Ctrl+Shift+S',
        'settings': 'Ctrl+Comma',
        'help': 'F1',
        'fullscreen': 'F11',
        'quit': 'Ctrl+Q'
    }
    
    # Default Prompts
    SYSTEM_PROMPTS = {
        'welcome': (
            "You are Claude, an AI assistant integrated with computer automation capabilities. "
            "You can take screenshots, control the mouse and keyboard, read and write files, "
            "browse the web, and help with various computer tasks. "
            "Always be helpful, safe, and ask for confirmation before performing potentially "
            "destructive actions."
        ),
        'error_handling': (
            "If an action fails, explain what went wrong and suggest alternatives. "
            "Always prioritize user safety and data integrity."
        )
    }
    
    # Message Templates
    MESSAGE_TEMPLATES = {
        'screenshot_taken': "📸 Screenshot captured successfully",
        'file_read': "📖 File read successfully: {filename}",
        'file_written': "✏️ File written successfully: {filename}",
        'web_page_loaded': "🌐 Web page loaded: {url}",
        'action_completed': "✅ Action completed: {action}",
        'error_occurred': "❌ Error: {error}",
    }
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories"""
        directories = [
            cls.LOGS_DIR, 
            cls.EXPORTS_DIR, 
            cls.TEMP_DIR, 
            cls.SCREENSHOTS_DIR
        ]
        
        for directory in directories:
            directory.mkdir(exist_ok=True)
    
    @classmethod
    def get_theme_colors(cls):
        """Get theme colors as a dictionary"""
        return {
            'bg_primary': cls.THEME_BG,
            'bg_secondary': cls.THEME_SECONDARY,
            'surface': cls.THEME_SURFACE,
            'accent': cls.THEME_ACCENT,
            'text_primary': cls.TEXT_PRIMARY,
            'text_secondary': cls.TEXT_SECONDARY,
            'chat_bg': cls.CHAT_BG,
            'chat_fg': cls.CHAT_FG,
            'chat_user': cls.CHAT_USER_COLOR,
            'chat_assistant': cls.CHAT_ASSISTANT_COLOR,
            'status_online': cls.STATUS_ONLINE,
            'status_busy': cls.STATUS_BUSY,
            'status_error': cls.STATUS_ERROR,
        }
    
    @classmethod
    def validate_config(cls):
        """Validate configuration settings"""
        issues = []
        
        # Check API key
        if not cls.ANTHROPIC_API_KEY:
            issues.append("ANTHROPIC_API_KEY not set")
        
        # Check numeric values
        try:
            if cls.PYAUTOGUI_PAUSE < 0:
                issues.append("PYAUTOGUI_PAUSE must be non-negative")
        except (ValueError, TypeError):
            issues.append("PYAUTOGUI_PAUSE must be a number")
        
        try:
            if cls.MAX_HISTORY_MESSAGES < 1:
                issues.append("MAX_HISTORY_MESSAGES must be positive")
        except (ValueError, TypeError):
            issues.append("MAX_HISTORY_MESSAGES must be a number")
        
        # Check window size format
        try:
            width, height = cls.WINDOW_SIZE.split('x')
            width, height = int(width), int(height)
            if width < 800 or height < 600:
                issues.append("Window size too small (minimum 800x600)")
        except:
            issues.append("Invalid WINDOW_SIZE format (use WIDTHxHEIGHT)")
        
        return issues
    
    @classmethod
    def get_user_config_path(cls):
        """Get path to user configuration file"""
        return cls.BASE_DIR / "user_config.json"
    
    @classmethod
    def save_user_config(cls, config_dict):
        """Save user configuration to file"""
        import json
        try:
            with open(cls.get_user_config_path(), 'w') as f:
                json.dump(config_dict, f, indent=2)
            return True
        except Exception as e:
            print(f"Failed to save user config: {e}")
            return False
    
    @classmethod
    def load_user_config(cls):
        """Load user configuration from file"""
        import json
        try:
            config_path = cls.get_user_config_path()
            if config_path.exists():
                with open(config_path, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Failed to load user config: {e}")
        return {}

# Auto-create directories on import
Config.create_directories()

# Validate configuration
config_issues = Config.validate_config()
if config_issues:
    print("⚠️  Configuration Issues:")
    for issue in config_issues:
        print(f"   • {issue}")
