"""
Enhanced Main Entry Point for Claude Computer Use Assistant
Uses the modern interface with improved functionality
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

from config import Config
from gui.enhanced_main_window import EnhancedMainWindow

def check_dependencies():
    """Check if all required dependencies are installed"""
    missing_deps = []
    
    try:
        import anthropic
    except ImportError:
        missing_deps.append("anthropic")
    
    try:
        import pyautogui
    except ImportError:
        missing_deps.append("pyautogui")
    
    try:
        import requests
    except ImportError:
        missing_deps.append("requests")
    
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        missing_deps.append("beautifulsoup4")
    
    try:
        from PIL import Image
    except ImportError:
        missing_deps.append("pillow")
    
    if missing_deps:
        deps_str = ", ".join(missing_deps)
        messagebox.showerror(
            "Missing Dependencies",
            f"The following required packages are missing:\n{deps_str}\n\n"
            f"Please install them using:\npip install {' '.join(missing_deps)}"
        )
        return False
    
    return True

def setup_pyautogui():
    """Setup PyAutoGUI with safe defaults"""
    try:
        import pyautogui
        pyautogui.FAILSAFE = Config.PYAUTOGUI_FAILSAFE
        pyautogui.PAUSE = Config.PYAUTOGUI_PAUSE
        
        # Test basic functionality
        pyautogui.position()
        return True
    except Exception as e:
        messagebox.showwarning(
            "PyAutoGUI Warning",
            f"PyAutoGUI setup failed: {str(e)}\n\n"
            "Computer automation features may not work properly.\n"
            "You can still use chat and other features."
        )
        return False

def check_api_key():
    """Check if API key is configured"""
    if not Config.ANTHROPIC_API_KEY:
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        
        # Show more helpful error message
        result = messagebox.askyesno(
            "API Key Required", 
            "ANTHROPIC_API_KEY not found.\n\n"
            "To use Claude AI Assistant, you need an Anthropic API key.\n\n"
            "Would you like to:\n"
            "• Get an API key from https://console.anthropic.com\n"
            "• Set it in your .env file\n"
            "• Or set it as an environment variable\n\n"
            "Click 'Yes' to open the Anthropic Console, or 'No' to exit.",
            icon='question'
        )
        
        if result:
            import webbrowser
            webbrowser.open("https://console.anthropic.com")
        
        root.destroy()
        return False
    
    return True

def create_directories():
    """Create necessary directories if they don't exist"""
    try:
        # Create logs directory
        logs_dir = project_dir / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        # Create exports directory
        exports_dir = project_dir / "exports"
        exports_dir.mkdir(exist_ok=True)
        
        # Create temp directory
        temp_dir = project_dir / "temp"
        temp_dir.mkdir(exist_ok=True)
        
        return True
    except Exception as e:
        print(f"Warning: Could not create directories: {str(e)}")
        return False

def main():
    """Enhanced main entry point"""
    print("🚀 Starting Claude AI Assistant...")
    
    # Check dependencies first
    if not check_dependencies():
        return
    
    # Create necessary directories
    create_directories()
    
    # Setup PyAutoGUI
    pyautogui_available = setup_pyautogui()
    
    # Check for API key
    if not check_api_key():
        return
    
    # Create and run the enhanced application
    try:
        print("🎨 Initializing modern interface...")
        app = EnhancedMainWindow()
        
        # Set PyAutoGUI availability flag
        if hasattr(app, 'computer_actions'):
            app.computer_actions.available = pyautogui_available
        
        print("✅ Claude AI Assistant ready!")
        app.run()
        
    except KeyboardInterrupt:
        print("\n👋 Claude AI Assistant stopped by user")
        
    except Exception as e:
        # Show error in both console and GUI
        error_msg = f"Failed to start Claude AI Assistant: {str(e)}"
        print(f"❌ {error_msg}")
        
        # Try to show GUI error if possible
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Application Error", error_msg)
            root.destroy()
        except:
            pass
        
        # Print traceback for debugging
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
