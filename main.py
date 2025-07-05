import tkinter as tk
from tkinter import messagebox
from config import Config
from gui.main_window import MainWindow

def main():
    """Main entry point"""
    # Check for API key
    if not Config.ANTHROPIC_API_KEY:
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showerror(
            "API Key Missing", 
            "ANTHROPIC_API_KEY not found in environment variables.\n"
            "Please set your API key in a .env file or environment variable."
        )
        return
    
    # Create and run the main application
    try:
        app = MainWindow()
        app.run()
    except Exception as e:
        messagebox.showerror("Application Error", f"Failed to start application: {str(e)}")

if __name__ == "__main__":
    main()
