"""
Enhanced Modern Main Window for Claude Computer Use Assistant
Features improved UI, better computer automation, and sleek design
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
from pathlib import Path

# Import configuration and components
from config import Config
from core.claude_client import ClaudeClient
from core.enhanced_computer_actions import EnhancedComputerActions
from core.file_operations import FileOperations
from core.web_operations import WebOperations
from utils.history_manager import MessageHistoryManager
from gui.modern_theme import ModernTheme, ModernStyler
from gui.modern_chat_panel import ModernChatPanel
from gui.modern_control_panel import ModernControlPanel
from gui.dialogs import ConfigDialog, AboutDialog, HelpDialog

class EnhancedMainWindow:
    """Enhanced main application window with modern styling"""
    
    def __init__(self):
        # Initialize theme
        self.theme = ModernTheme()
        self.styler = ModernStyler()
        
        # Initialize main window
        self.root = tk.Tk()
        self.setup_window()
        
        # Initialize components
        self.initialize_components()
        
        # Create GUI
        self.create_modern_interface()
        self.create_status_bar()
        self.setup_keyboard_shortcuts()
        
        # Bind events
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Show startup
        self.show_startup_animation()
        
    def setup_window(self):
        """Setup main window with modern styling"""
        self.root.title("Claude AI Assistant")
        self.root.geometry("1600x1000")
        self.root.minsize(1200, 700)
        
        # Apply modern styling
        self.styler.apply_modern_style(self.root)
        
        # Set window icon (if available)
        try:
            # You can add an icon file here
            # self.root.iconbitmap('assets/icon.ico')
            pass
        except:
            pass
            
        # Center window on screen
        self.center_window()
        
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def initialize_components(self):
        """Initialize all application components"""
        try:
            # Core components
            self.claude_client = ClaudeClient()
            self.computer_actions = EnhancedComputerActions()
            self.file_operations = FileOperations()
            self.web_operations = WebOperations()
            self.history_manager = MessageHistoryManager()
            
            # Status tracking
            self.connection_status = "offline"
            self.last_action = "Ready"
            
        except Exception as e:
            messagebox.showerror("Initialization Error", f"Failed to initialize components: {str(e)}")
            sys.exit(1)
            
    def create_modern_interface(self):
        """Create the modern interface layout"""
        # Main container
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill='both', expand=True)
        self.styler.apply_modern_style(self.main_container)
        
        # Header bar
        self.create_header_bar()
        
        # Content area with modern layout
        content_frame = tk.Frame(self.main_container)
        content_frame.pack(fill='both', expand=True, padx=self.theme.SPACING['md'], 
                          pady=(0, self.theme.SPACING['md']))
        self.styler.apply_modern_style(content_frame)
        
        # Create modern paned window
        self.main_paned = tk.PanedWindow(content_frame, orient=tk.HORIZONTAL,
                                        bg=self.theme.COLORS['bg_primary'],
                                        sashwidth=8,
                                        sashrelief='flat',
                                        handlepad=20)
        self.main_paned.pack(fill='both', expand=True)
        
        # Left panel - Chat interface (larger, always visible)
        self.chat_container = self.styler.create_modern_card(self.main_paned)
        self.main_paned.add(self.chat_container, width=1100, minsize=600, stretch='always')
        
        # Right panel - Control panel
        self.control_container = self.styler.create_modern_card(self.main_paned)
        self.main_paned.add(self.control_container, width=500, minsize=350, stretch='never')
        
        # Initialize panels with modern styling
        self.control_panel = ModernControlPanel(
            self.control_container,
            self.claude_client,
            self.computer_actions,
            self.file_operations,
            self.web_operations,
            self.history_manager,
            self.styler
        )
        
        self.chat_panel = ModernChatPanel(
            self.chat_container,
            self.claude_client,
            self.control_panel,
            self.history_manager,
            self.styler
        )
        
        # Set initial paned window position
        self.root.after(100, lambda: self.main_paned.sash_place(0, 1000, 0))
        
    def create_header_bar(self):
        """Create modern header bar with app title and controls"""
        header = tk.Frame(self.main_container, height=60)
        header.pack(fill='x', padx=self.theme.SPACING['md'], pady=self.theme.SPACING['md'])
        header.pack_propagate(False)
        self.styler.apply_modern_style(header)
        
        # App title and icon area
        title_frame = tk.Frame(header)
        title_frame.pack(side='left', fill='y')
        self.styler.apply_modern_style(title_frame)
        
        # App icon (emoji for now)
        icon_label = tk.Label(title_frame, text="🤖", font=("Segoe UI Emoji", 24))
        icon_label.pack(side='left', padx=(0, self.theme.SPACING['sm']))
        self.styler.apply_modern_style(icon_label)
        
        # App title
        title_label = tk.Label(title_frame, text="Claude AI Assistant", 
                              font=self.theme.FONTS['heading_large'])
        title_label.pack(side='left', anchor='w')
        self.styler.apply_modern_style(title_label, 'heading')
        
        # Quick action buttons
        actions_frame = tk.Frame(header)
        actions_frame.pack(side='right', fill='y')
        self.styler.apply_modern_style(actions_frame)
        
        # Screenshot button
        screenshot_btn = tk.Button(actions_frame, text="📸 Screenshot",
                                  command=self.quick_screenshot,
                                  padx=self.theme.SPACING['md'],
                                  pady=self.theme.SPACING['sm'])
        screenshot_btn.pack(side='right', padx=self.theme.SPACING['sm'])
        self.styler.apply_modern_style(screenshot_btn, 'primary')
        
        # Settings button
        settings_btn = tk.Button(actions_frame, text="⚙️ Settings",
                               command=self.show_preferences,
                               padx=self.theme.SPACING['md'],
                               pady=self.theme.SPACING['sm'])
        settings_btn.pack(side='right', padx=self.theme.SPACING['sm'])
        self.styler.apply_modern_style(settings_btn, 'secondary')
        
    def create_status_bar(self):
        """Create modern status bar"""
        status_frame = tk.Frame(self.main_container, height=30)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        self.styler.apply_modern_style(status_frame)
        
        # Connection status
        self.status_indicator = self.styler.create_status_indicator(status_frame, 'offline')
        self.status_indicator.pack(side='left', padx=self.theme.SPACING['md'])
        
        self.status_label = tk.Label(status_frame, text="Ready", 
                                    font=self.theme.FONTS['caption'])
        self.status_label.pack(side='left', padx=self.theme.SPACING['sm'])
        self.styler.apply_modern_style(self.status_label, 'caption')
        
        # Action counter
        self.action_count_label = tk.Label(status_frame, text="Actions: 0", 
                                          font=self.theme.FONTS['caption'])
        self.action_count_label.pack(side='right', padx=self.theme.SPACING['md'])
        self.styler.apply_modern_style(self.action_count_label, 'caption')
        
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Global shortcuts
        self.root.bind('<Control-n>', lambda e: self.new_chat())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.quick_save())
        self.root.bind('<Control-q>', lambda e: self.on_closing())
        self.root.bind('<F1>', lambda e: self.show_help())
        self.root.bind('<F11>', lambda e: self.toggle_fullscreen())
        self.root.bind('<Control-comma>', lambda e: self.show_preferences())
        
        # Screenshot shortcuts
        self.root.bind('<Control-Shift-s>', lambda e: self.quick_screenshot())
        self.root.bind('<Print>', lambda e: self.quick_screenshot())
        
    def show_startup_animation(self):
        """Show startup animation and check connectivity"""
        self.update_status("Initializing...", "busy")
        
        # Simulate startup checks
        self.root.after(500, self.check_api_connection)
        
    def check_api_connection(self):
        """Check API connection and update status"""
        try:
            # Test API connection here
            if Config.ANTHROPIC_API_KEY:
                self.update_status("Connected", "online")
                self.show_welcome_message()
            else:
                self.update_status("API Key Missing", "error")
                
        except Exception as e:
            self.update_status(f"Connection Error: {str(e)}", "error")
            
    def show_welcome_message(self):
        """Show enhanced welcome message"""
        welcome_msg = (
            "🚀 Claude AI Assistant Ready!\\n\\n"
            "Enhanced Features Available:\\n"
            "• 💬 Natural language chat with Claude\\n"
            "• 📸 Smart screenshot analysis\\n"
            "• 🖱️ Advanced computer automation\\n"
            "• 📁 Intelligent file operations\\n"
            "• 🌐 Web browsing and content extraction\\n"
            "• 📱 Message sending capabilities\\n"
            "• 🎨 Modern, responsive interface\\n\\n"
            "Pro Tips:\\n"
            "• Use Ctrl+Shift+S for quick screenshots\\n"
            "• Try natural commands like 'send text to Andrea'\\n"
            "• Use the control panel for direct tool access\\n\\n"
            "Ready to assist you! Type a message to get started."
        )
        
        self.chat_panel.add_system_message(welcome_msg)
        
    def update_status(self, message, status_type="offline"):
        """Update status bar with message and status"""
        self.status_label.config(text=message)
        
        # Update status indicator
        status_colors = {
            'online': self.theme.COLORS['status_online'],
            'busy': self.theme.COLORS['status_busy'],
            'error': self.theme.COLORS['status_error'],
            'offline': self.theme.COLORS['status_offline']
        }
        
        self.status_indicator.config(fg=status_colors.get(status_type, status_colors['offline']))
        self.connection_status = status_type
        
    # Enhanced menu command implementations
    def new_chat(self):
        """Start a new chat session"""
        result = messagebox.askyesno(
            "New Chat", 
            "Start a new chat? This will clear the current conversation history.",
            icon='question'
        )
        if result:
            self.chat_panel.clear_chat()
            self.update_status("New chat started", "online")
            
    def quick_screenshot(self):
        """Take a quick screenshot"""
        self.update_status("Taking screenshot...", "busy")
        self.control_panel.take_screenshot()
        self.update_status("Screenshot captured", "online")
        
    def quick_save(self):
        """Quick save current conversation"""
        try:
            self.chat_panel.export_chat()
            self.update_status("Chat exported", "online")
        except Exception as e:
            self.update_status(f"Export failed: {str(e)}", "error")
            
    def open_file(self):
        """Enhanced file opening"""
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(
            title="Open File",
            filetypes=[
                ("All Files", "*.*"),
                ("Text Files", "*.txt"),
                ("Python Files", "*.py"),
                ("JSON Files", "*.json"),
                ("Markdown Files", "*.md"),
                ("CSV Files", "*.csv")
            ]
        )
        if file_path:
            self.control_panel.file_path_var.set(file_path)
            self.control_panel.read_file()
            self.update_status(f"Opened: {Path(file_path).name}", "online")
            
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        current = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current)
        
    def show_preferences(self):
        """Show enhanced preferences dialog"""
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
            self.apply_configuration(dialog.result)
            self.update_status("Settings updated", "online")
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
                self.check_api_connection()
                
        except Exception as e:
            messagebox.showerror("Configuration Error", f"Error applying configuration: {str(e)}")
            self.update_status("Configuration error", "error")
            
    def show_help(self):
        """Show help dialog"""
        help_dialog = HelpDialog(self.root)
        
    def show_about(self):
        """Show about dialog"""
        about_dialog = AboutDialog(self.root)
        
    def on_closing(self):
        """Handle application closing with confirmation"""
        if messagebox.askokcancel("Quit", "Do you want to quit the Claude AI Assistant?"):
            try:
                # Stop auto screenshot if running
                if hasattr(self.control_panel, 'auto_screenshot'):
                    self.control_panel.auto_screenshot = False
                    
                # Save any pending history
                self.history_manager.save_history()
                
                # Update status
                self.update_status("Shutting down...", "offline")
                
                # Close the application
                self.root.quit()
                self.root.destroy()
                
            except Exception as e:
                print(f"Error during shutdown: {str(e)}")
                self.root.destroy()
                
    def run(self):
        """Run the enhanced application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.on_closing()
        except Exception as e:
            messagebox.showerror("Application Error", f"Unexpected error: {str(e)}")
            self.on_closing()

# For backward compatibility, create an alias
MainWindow = EnhancedMainWindow
