import tkinter as tk
from tkinter import ttk, messagebox
import sys
from pathlib import Path

# Import configuration and components
from config import Config
from core.claude_client import ClaudeClient
from core.computer_actions import ComputerActions
from core.file_operations import FileOperations
from core.web_operations import WebOperations
from utils.history_manager import MessageHistoryManager
from gui.chat_panel import ChatPanel
from gui.control_panel import ControlPanel
from gui.dialogs import ConfigDialog, AboutDialog, HelpDialog

class MainWindow:
    """Main application window"""
    
    def __init__(self):
        # Initialize main window
        self.root = tk.Tk()
        self.root.title(Config.WINDOW_TITLE)
        self.root.geometry(Config.WINDOW_SIZE)
        self.root.configure(bg=Config.THEME_BG)
        
        # Initialize components
        self.initialize_components()
        
        # Create GUI
        self.create_menu()
        self.create_main_interface()
        
        # Bind events
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Show startup message
        self.show_startup_message()
        
    def initialize_components(self):
        """Initialize all application components"""
        try:
            # Core components
            self.claude_client = ClaudeClient()
            self.computer_actions = ComputerActions()
            self.file_operations = FileOperations()
            self.web_operations = WebOperations()
            self.history_manager = MessageHistoryManager()
            
        except Exception as e:
            messagebox.showerror("Initialization Error", f"Failed to initialize components: {str(e)}")
            sys.exit(1)
            
    def create_menu(self):
        """Create application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Chat", command=self.new_chat)
        file_menu.add_separator()
        file_menu.add_command(label="Export Chat...", command=self.export_chat)
        file_menu.add_command(label="Export Action Log...", command=self.export_action_log)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Clear Chat", command=self.clear_chat)
        edit_menu.add_command(label="Clear Action Log", command=self.clear_action_log)
        edit_menu.add_separator()
        edit_menu.add_command(label="Preferences...", command=self.show_preferences)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Take Screenshot", command=self.take_screenshot)
        tools_menu.add_command(label="Auto Screenshot", command=self.toggle_auto_screenshot)
        tools_menu.add_separator()
        tools_menu.add_command(label="Load Web Page...", command=self.load_web_page)
        tools_menu.add_command(label="Open File...", command=self.open_file)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Focus Chat Input", command=self.focus_chat_input)
        view_menu.add_command(label="Show Screenshot Tab", command=self.show_screenshot_tab)
        view_menu.add_command(label="Show File Operations Tab", command=self.show_file_operations_tab)
        view_menu.add_command(label="Show Web Operations Tab", command=self.show_web_operations_tab)
        view_menu.add_command(label="Show Action Log Tab", command=self.show_action_log_tab)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Help...", command=self.show_help)
        help_menu.add_separator()
        help_menu.add_command(label="About...", command=self.show_about)
        
    def create_main_interface(self):
        """Create the main interface"""
        # Create main paned window
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Left panel - Chat interface
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=2)
        
        # Right panel - Control panel
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=1)
        
        # Initialize control panel first (since chat panel depends on it)
        self.control_panel = ControlPanel(
            right_frame,
            self.claude_client,
            self.computer_actions,
            self.file_operations,
            self.web_operations,
            self.history_manager
        )
        
        # Initialize chat panel
        self.chat_panel = ChatPanel(
            left_frame,
            self.claude_client,
            self.control_panel,
            self.history_manager
        )
        
        # Set initial paned window position
        self.root.after(100, lambda: main_paned.sash_place(0, 700, 0))
        
    def show_startup_message(self):
        """Show startup message in chat"""
        self.chat_panel.add_system_message(
            "Claude Computer Use Assistant started successfully!\n"
            "Features available:\n"
            "• Chat with Claude AI\n"
            "• Take screenshots and automate computer actions\n"
            "• File operations (read, write, list)\n"
            "• Web page loading and content extraction\n"
            "• Conversation history management\n\n"
            "Type a message below to get started, or use Ctrl+Enter to send."
        )
        
    # Menu command implementations
    def new_chat(self):
        """Start a new chat session"""
        result = messagebox.askyesno(
            "New Chat", 
            "Start a new chat? This will clear the current conversation history."
        )
        if result:
            self.chat_panel.clear_chat()
            
    def export_chat(self):
        """Export chat history"""
        self.chat_panel.export_chat()
        
    def export_action_log(self):
        """Export action log"""
        self.control_panel.export_log()
        
    def clear_chat(self):
        """Clear chat history"""
        self.chat_panel.clear_chat()
        
    def clear_action_log(self):
        """Clear action log"""
        self.control_panel.clear_log()
        
    def show_preferences(self):
        """Show preferences dialog"""
        current_config = {
            'ANTHROPIC_API_KEY': Config.ANTHROPIC_API_KEY or '',
            'CLAUDE_MODEL': Config.CLAUDE_MODEL,
            'WINDOW_SIZE': Config.WINDOW_SIZE,
            'WINDOW_TITLE': Config.WINDOW_TITLE,
            'THEME_BG': Config.THEME_BG,
            'CHAT_BG': Config.CHAT_BG,
            'CHAT_FG': Config.CHAT_FG,
            'PYAUTOGUI_PAUSE': Config.PYAUTOGUI_PAUSE,
            'PYAUTOGUI_FAILSAFE': Config.PYAUTOGUI_FAILSAFE,
            'MAX_HISTORY_MESSAGES': Config.MAX_HISTORY_MESSAGES,
            'REQUEST_TIMEOUT': Config.REQUEST_TIMEOUT
        }
        
        dialog = ConfigDialog(self.root, current_config)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            # Apply new configuration
            self.apply_configuration(dialog.result)
            messagebox.showinfo("Settings Saved", "Configuration updated successfully!")
            
    def apply_configuration(self, new_config):
        """Apply new configuration settings"""
        try:
            # Update Config class attributes
            for key, value in new_config.items():
                if hasattr(Config, key):
                    setattr(Config, key, value)
            
            # Apply immediate changes
            if 'WINDOW_TITLE' in new_config:
                self.root.title(new_config['WINDOW_TITLE'])
                
            if 'THEME_BG' in new_config:
                self.root.configure(bg=new_config['THEME_BG'])
                
            # Update chat display colors
            if any(key in new_config for key in ['CHAT_BG', 'CHAT_FG']):
                self.chat_panel.chat_display.config(
                    bg=new_config.get('CHAT_BG', Config.CHAT_BG),
                    fg=new_config.get('CHAT_FG', Config.CHAT_FG)
                )
            
            # Update PyAutoGUI settings
            if 'PYAUTOGUI_PAUSE' in new_config:
                import pyautogui
                pyautogui.PAUSE = new_config['PYAUTOGUI_PAUSE']
                
            if 'PYAUTOGUI_FAILSAFE' in new_config:
                import pyautogui
                pyautogui.FAILSAFE = new_config['PYAUTOGUI_FAILSAFE']
                
            # Update history manager
            if 'MAX_HISTORY_MESSAGES' in new_config:
                from collections import deque
                self.history_manager.history = deque(
                    list(self.history_manager.history), 
                    maxlen=new_config['MAX_HISTORY_MESSAGES']
                )
                
            # Recreate Claude client if API settings changed
            if 'ANTHROPIC_API_KEY' in new_config or 'CLAUDE_MODEL' in new_config:
                self.claude_client = ClaudeClient()
                self.chat_panel.claude_client = self.claude_client
                
        except Exception as e:
            messagebox.showerror("Configuration Error", f"Error applying configuration: {str(e)}")
            
    def take_screenshot(self):
        """Take a screenshot"""
        self.control_panel.take_screenshot()
        
    def toggle_auto_screenshot(self):
        """Toggle auto screenshot mode"""
        self.control_panel.toggle_auto_screenshot()
        
    def load_web_page(self):
        """Load web page dialog"""
        from tkinter import simpledialog
        url = simpledialog.askstring("Load Web Page", "Enter URL:")
        if url:
            self.control_panel.url_var.set(url)
            self.control_panel.load_page()
            
    def open_file(self):
        """Open file dialog"""
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(
            title="Open File",
            filetypes=[
                ("All Files", "*.*"),
                ("Text Files", "*.txt"),
                ("Python Files", "*.py"),
                ("JSON Files", "*.json")
            ]
        )
        if file_path:
            self.control_panel.file_path_var.set(file_path)
            self.control_panel.read_file()
            
    def focus_chat_input(self):
        """Focus on chat input"""
        self.chat_panel.focus_input()
        
    def show_screenshot_tab(self):
        """Show screenshot tab"""
        self.control_panel.notebook.select(0)
        
    def show_file_operations_tab(self):
        """Show file operations tab"""
        self.control_panel.notebook.select(1)
        
    def show_web_operations_tab(self):
        """Show web operations tab"""
        self.control_panel.notebook.select(2)
        
    def show_action_log_tab(self):
        """Show action log tab"""
        self.control_panel.notebook.select(3)
        
    def show_help(self):
        """Show help dialog"""
        help_dialog = HelpDialog(self.root)
        
    def show_about(self):
        """Show about dialog"""
        about_dialog = AboutDialog(self.root)
        
    def on_closing(self):
        """Handle application closing"""
        try:
            # Stop auto screenshot if running
            if hasattr(self.control_panel, 'auto_screenshot'):
                self.control_panel.auto_screenshot = False
                
            # Save any pending history
            self.history_manager.save_history()
            
            # Close the application
            self.root.quit()
            self.root.destroy()
            
        except Exception as e:
            print(f"Error during shutdown: {str(e)}")
            self.root.destroy()
            
    def run(self):
        """Run the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()
        except Exception as e:
            messagebox.showerror("Application Error", f"Unexpected error: {str(e)}")
            self.on_closing()
