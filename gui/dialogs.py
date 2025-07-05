import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog, scrolledtext
from pathlib import Path
import json

class ConfigDialog:
    """Configuration dialog for application settings"""
    
    def __init__(self, parent, current_config):
        self.parent = parent
        self.current_config = current_config
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Configuration Settings")
        self.dialog.geometry("500x400")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.center_dialog()
        
        # Create UI
        self.create_widgets()
        
        # Bind events
        self.dialog.protocol("WM_DELETE_WINDOW", self.cancel)
        
    def center_dialog(self):
        """Center dialog on parent window"""
        self.dialog.update_idletasks()
        x = (self.parent.winfo_x() + (self.parent.winfo_width() // 2) - 
             (self.dialog.winfo_width() // 2))
        y = (self.parent.winfo_y() + (self.parent.winfo_height() // 2) - 
             (self.dialog.winfo_height() // 2))
        self.dialog.geometry(f"+{x}+{y}")
        
    def create_widgets(self):
        """Create dialog widgets"""
        # Main frame
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True, pady=(0, 10))
        
        # API Configuration tab
        self.create_api_tab(notebook)
        
        # GUI Configuration tab
        self.create_gui_tab(notebook)
        
        # PyAutoGUI Configuration tab
        self.create_pyautogui_tab(notebook)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x')
        
        ttk.Button(button_frame, text="Save", command=self.save).pack(side='right', padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=self.cancel).pack(side='right')
        ttk.Button(button_frame, text="Reset to Defaults", command=self.reset_defaults).pack(side='left')
        
    def create_api_tab(self, notebook):
        """Create API configuration tab"""
        api_frame = ttk.Frame(notebook)
        notebook.add(api_frame, text="API Settings")
        
        # API Key
        ttk.Label(api_frame, text="Anthropic API Key:").pack(anchor='w', pady=(5, 0))
        self.api_key_var = tk.StringVar(value=self.current_config.get('ANTHROPIC_API_KEY', ''))
        self.api_key_entry = ttk.Entry(api_frame, textvariable=self.api_key_var, show='*', width=50)
        self.api_key_entry.pack(fill='x', pady=(2, 10))
        
        # Show/Hide button
        self.show_key_var = tk.BooleanVar()
        ttk.Checkbutton(api_frame, text="Show API Key", 
                       variable=self.show_key_var,
                       command=self.toggle_api_key_visibility).pack(anchor='w', pady=(0, 10))
        
        # Claude Model
        ttk.Label(api_frame, text="Claude Model:").pack(anchor='w', pady=(5, 0))
        self.model_var = tk.StringVar(value=self.current_config.get('CLAUDE_MODEL', 'claude-3-5-sonnet-20241022'))
        model_combo = ttk.Combobox(api_frame, textvariable=self.model_var, width=47)
        model_combo['values'] = [
            'claude-3-5-sonnet-20241022',
            'claude-3-opus-20240229',
            'claude-3-sonnet-20240229',
            'claude-3-haiku-20240307'
        ]
        model_combo.pack(fill='x', pady=(2, 10))
        
        # API Test button
        ttk.Button(api_frame, text="Test API Connection", 
                  command=self.test_api_connection).pack(pady=10)
        
    def create_gui_tab(self, notebook):
        """Create GUI configuration tab"""
        gui_frame = ttk.Frame(notebook)
        notebook.add(gui_frame, text="GUI Settings")
        
        # Window Size
        ttk.Label(gui_frame, text="Window Size:").pack(anchor='w', pady=(5, 0))
        self.window_size_var = tk.StringVar(value=self.current_config.get('WINDOW_SIZE', '1400x900'))
        ttk.Entry(gui_frame, textvariable=self.window_size_var, width=50).pack(fill='x', pady=(2, 10))
        
        # Window Title
        ttk.Label(gui_frame, text="Window Title:").pack(anchor='w', pady=(5, 0))
        self.window_title_var = tk.StringVar(value=self.current_config.get('WINDOW_TITLE', 'Claude Computer Use Assistant'))
        ttk.Entry(gui_frame, textvariable=self.window_title_var, width=50).pack(fill='x', pady=(2, 10))
        
        # Theme Colors
        colors_frame = ttk.LabelFrame(gui_frame, text="Color Theme")
        colors_frame.pack(fill='x', pady=10)
        
        # Background Color
        ttk.Label(colors_frame, text="Background Color:").pack(anchor='w', pady=(5, 0))
        self.theme_bg_var = tk.StringVar(value=self.current_config.get('THEME_BG', '#2b2b2b'))
        ttk.Entry(colors_frame, textvariable=self.theme_bg_var, width=50).pack(fill='x', pady=(2, 5), padx=5)
        
        # Chat Background
        ttk.Label(colors_frame, text="Chat Background:").pack(anchor='w', pady=(5, 0))
        self.chat_bg_var = tk.StringVar(value=self.current_config.get('CHAT_BG', '#1e1e1e'))
        ttk.Entry(colors_frame, textvariable=self.chat_bg_var, width=50).pack(fill='x', pady=(2, 5), padx=5)
        
        # Chat Foreground
        ttk.Label(colors_frame, text="Chat Text Color:").pack(anchor='w', pady=(5, 0))
        self.chat_fg_var = tk.StringVar(value=self.current_config.get('CHAT_FG', 'white'))
        ttk.Entry(colors_frame, textvariable=self.chat_fg_var, width=50).pack(fill='x', pady=(2, 10), padx=5)
        
    def create_pyautogui_tab(self, notebook):
        """Create PyAutoGUI configuration tab"""
        pyautogui_frame = ttk.Frame(notebook)
        notebook.add(pyautogui_frame, text="Automation Settings")
        
        # PyAutoGUI Pause
        ttk.Label(pyautogui_frame, text="Action Delay (seconds):").pack(anchor='w', pady=(5, 0))
        self.pause_var = tk.StringVar(value=str(self.current_config.get('PYAUTOGUI_PAUSE', 0.5)))
        ttk.Entry(pyautogui_frame, textvariable=self.pause_var, width=50).pack(fill='x', pady=(2, 10))
        
        # Failsafe
        self.failsafe_var = tk.BooleanVar(value=self.current_config.get('PYAUTOGUI_FAILSAFE', True))
        ttk.Checkbutton(pyautogui_frame, text="Enable Failsafe (move mouse to corner to stop)",
                       variable=self.failsafe_var).pack(anchor='w', pady=10)
        
        # History Configuration
        history_frame = ttk.LabelFrame(pyautogui_frame, text="History Settings")
        history_frame.pack(fill='x', pady=10)
        
        # Max History Messages
        ttk.Label(history_frame, text="Max History Messages:").pack(anchor='w', pady=(5, 0))
        self.max_history_var = tk.StringVar(value=str(self.current_config.get('MAX_HISTORY_MESSAGES', 20)))
        ttk.Entry(history_frame, textvariable=self.max_history_var, width=50).pack(fill='x', pady=(2, 10), padx=5)
        
        # Request Timeout
        ttk.Label(pyautogui_frame, text="Web Request Timeout (seconds):").pack(anchor='w', pady=(5, 0))
        self.timeout_var = tk.StringVar(value=str(self.current_config.get('REQUEST_TIMEOUT', 10)))
        ttk.Entry(pyautogui_frame, textvariable=self.timeout_var, width=50).pack(fill='x', pady=(2, 10))
        
    def toggle_api_key_visibility(self):
        """Toggle API key visibility"""
        if self.show_key_var.get():
            self.api_key_entry.config(show='')
        else:
            self.api_key_entry.config(show='*')
            
    def test_api_connection(self):
        """Test API connection"""
        api_key = self.api_key_var.get().strip()
        if not api_key:
            messagebox.showwarning("No API Key", "Please enter an API key first")
            return
            
        # Simple test (you would implement actual API test here)
        messagebox.showinfo("API Test", "API key format appears valid. Full connection test would require actual implementation.")
        
    def reset_defaults(self):
        """Reset to default values"""
        result = messagebox.askyesno("Reset Defaults", "Reset all settings to defaults?")
        if result:
            defaults = {
                'CLAUDE_MODEL': 'claude-3-5-sonnet-20241022',
                'WINDOW_SIZE': '1400x900',
                'WINDOW_TITLE': 'Claude Computer Use Assistant',
                'THEME_BG': '#2b2b2b',
                'CHAT_BG': '#1e1e1e',
                'CHAT_FG': 'white',
                'PYAUTOGUI_PAUSE': 0.5,
                'PYAUTOGUI_FAILSAFE': True,
                'MAX_HISTORY_MESSAGES': 20,
                'REQUEST_TIMEOUT': 10
            }
            
            self.model_var.set(defaults['CLAUDE_MODEL'])
            self.window_size_var.set(defaults['WINDOW_SIZE'])
            self.window_title_var.set(defaults['WINDOW_TITLE'])
            self.theme_bg_var.set(defaults['THEME_BG'])
            self.chat_bg_var.set(defaults['CHAT_BG'])
            self.chat_fg_var.set(defaults['CHAT_FG'])
            self.pause_var.set(str(defaults['PYAUTOGUI_PAUSE']))
            self.failsafe_var.set(defaults['PYAUTOGUI_FAILSAFE'])
            self.max_history_var.set(str(defaults['MAX_HISTORY_MESSAGES']))
            self.timeout_var.set(str(defaults['REQUEST_TIMEOUT']))
            
    def save(self):
        """Save configuration"""
        try:
            # Validate inputs
            pause_val = float(self.pause_var.get())
            max_history_val = int(self.max_history_var.get())
            timeout_val = int(self.timeout_var.get())
            
            if pause_val < 0 or max_history_val < 1 or timeout_val < 1:
                raise ValueError("Invalid numeric values")
                
            # Build result dictionary
            self.result = {
                'ANTHROPIC_API_KEY': self.api_key_var.get().strip(),
                'CLAUDE_MODEL': self.model_var.get(),
                'WINDOW_SIZE': self.window_size_var.get(),
                'WINDOW_TITLE': self.window_title_var.get(),
                'THEME_BG': self.theme_bg_var.get(),
                'CHAT_BG': self.chat_bg_var.get(),
                'CHAT_FG': self.chat_fg_var.get(),
                'PYAUTOGUI_PAUSE': pause_val,
                'PYAUTOGUI_FAILSAFE': self.failsafe_var.get(),
                'MAX_HISTORY_MESSAGES': max_history_val,
                'REQUEST_TIMEOUT': timeout_val
            }
            
            self.dialog.destroy()
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please check numeric values")
            
    def cancel(self):
        """Cancel dialog"""
        self.result = None
        self.dialog.destroy()


class AboutDialog:
    """About dialog"""
    
    def __init__(self, parent):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("About")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.center_dialog(parent)
        
        # Create content
        self.create_content()
        
    def center_dialog(self, parent):
        """Center dialog on parent"""
        self.dialog.update_idletasks()
        x = (parent.winfo_x() + (parent.winfo_width() // 2) - 
             (self.dialog.winfo_width() // 2))
        y = (parent.winfo_y() + (parent.winfo_height() // 2) - 
             (self.dialog.winfo_height() // 2))
        self.dialog.geometry(f"+{x}+{y}")
        
    def create_content(self):
        """Create about content"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, text="Claude Computer Use Assistant", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 10))
        
        # Version
        version_label = ttk.Label(main_frame, text="Version 1.0.0")
        version_label.pack(pady=(0, 20))
        
        # Description
        description = (
            "A GUI application for interacting with Claude AI assistant\n"
            "with computer automation capabilities.\n\n"
            "Features:\n"
            "• Chat interface with Claude\n"
            "• Screen capture and automation\n"
            "• File operations\n"
            "• Web scraping and browsing\n"
            "• Conversation history management\n\n"
            "Built with Python and Tkinter"
        )
        
        description_label = ttk.Label(main_frame, text=description, justify='left')
        description_label.pack(pady=(0, 20))
        
        # Close button
        ttk.Button(main_frame, text="Close", command=self.dialog.destroy).pack()


class HelpDialog:
    """Help dialog with usage instructions"""
    
    def __init__(self, parent):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Help - Usage Instructions")
        self.dialog.geometry("700x600")
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.center_dialog(parent)
        
        # Create content
        self.create_content()
        
    def center_dialog(self, parent):
        """Center dialog on parent"""
        self.dialog.update_idletasks()
        x = (parent.winfo_x() + (parent.winfo_width() // 2) - 
             (self.dialog.winfo_width() // 2))
        y = (parent.winfo_y() + (parent.winfo_height() // 2) - 
             (self.dialog.winfo_height() // 2))
        self.dialog.geometry(f"+{x}+{y}")
        
    def create_content(self):
        """Create help content"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Create notebook for different help sections
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True, pady=(0, 10))
        
        # Getting Started tab
        self.create_getting_started_tab(notebook)
        
        # Chat Interface tab
        self.create_chat_help_tab(notebook)
        
        # Tools tab
        self.create_tools_help_tab(notebook)
        
        # Troubleshooting tab
        self.create_troubleshooting_tab(notebook)
        
        # Close button
        ttk.Button(main_frame, text="Close", command=self.dialog.destroy).pack()
        
    def create_getting_started_tab(self, notebook):
        """Create getting started help tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Getting Started")
        
        text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=('Arial', 10))
        text_widget.pack(fill='both', expand=True, padx=5, pady=5)
        
        content = """
GETTING STARTED

1. Setup API Key:
   - Get your Anthropic API key from https://console.anthropic.com
   - Go to Settings > Configuration and enter your API key
   - Or create a .env file with ANTHROPIC_API_KEY=your_key_here

2. First Steps:
   - Take a screenshot using the Screenshot tab
   - Type a message in the chat interface
   - Check "Include Screenshot" to send the current screen to Claude
   - Press Ctrl+Enter or click "Send Message"

3. Basic Usage:
   - Chat with Claude using natural language
   - Ask Claude to perform computer actions
   - Use file operations to read/write files
   - Load web pages and extract content

4. Example Commands:
   - "Take a screenshot and tell me what you see"
   - "Click on the Start button"
   - "Read the file desktop.txt"
   - "Load the webpage google.com"
"""
        
        text_widget.insert(1.0, content)
        text_widget.config(state=tk.DISABLED)
        
    def create_chat_help_tab(self, notebook):
        """Create chat interface help tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Chat Interface")
        
        text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=('Arial', 10))
        text_widget.pack(fill='both', expand=True, padx=5, pady=5)
        
        content = """
CHAT INTERFACE

Basic Usage:
- Type your message in the input area at the bottom
- Press Ctrl+Enter to send (or click Send Message button)
- View conversation history in the main chat area

Options:
- Include Screenshot: Attach current screenshot to your message
- Include Page Content: Attach current web page content

Keyboard Shortcuts:
- Ctrl+Enter: Send message
- Enter: New line in message

Message History:
- Automatically saved and loaded between sessions
- Export chat history using the Export button
- Clear chat history using the Clear button

Status Indicators:
- Green: Ready/Success
- Orange: Processing
- Red: Error occurred

Tips:
- Be specific in your requests
- Include context about what you want to accomplish
- Use screenshots to help Claude see your desktop
"""
        
        text_widget.insert(1.0, content)
        text_widget.config(state=tk.DISABLED)
        
    def create_tools_help_tab(self, notebook):
        """Create tools help tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Tools & Features")
        
        text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=('Arial', 10))
        text_widget.pack(fill='both', expand=True, padx=5, pady=5)
        
        content = """
TOOLS & FEATURES

Screenshot Tab:
- Take Screenshot: Capture current screen
- Auto Screenshot: Continuously capture screenshots
- View thumbnail of current screenshot

File Operations Tab:
- Browse and select files
- Read file content
- List directory contents
- Write new files
- Supported formats: .txt, .py, .json, .html, .css, .js, .md

Web Operations Tab:
- Load web pages by URL
- Extract page content as text
- Search within page content
- Extract all links from page
- Open URLs in default browser

Action Log Tab:
- View all performed actions
- Export action log
- Clear log history

Tool Integration:
Claude can automatically use these tools when you ask:
- "Click on [location]" → Computer actions
- "Read file [path]" → File operations
- "Load webpage [URL]" → Web operations
"""
        
        text_widget.insert(1.0, content)
        text_widget.config(state=tk.DISABLED)
        
    def create_troubleshooting_tab(self, notebook):
        """Create troubleshooting help tab"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Troubleshooting")
        
        text_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=('Arial', 10))
        text_widget.pack(fill='both', expand=True, padx=5, pady=5)
        
        content = """
TROUBLESHOOTING

Common Issues:

1. "API Key Missing" Error:
   - Ensure ANTHROPIC_API_KEY is set in environment or .env file
   - Check API key is valid at https://console.anthropic.com
   - Verify no extra spaces in the key

2. Screenshot Not Working:
   - Check if pyautogui is installed: pip install pyautogui
   - On Linux: may need additional packages for screenshot functionality
   - Try disabling failsafe in settings if mouse moves to corner

3. File Operations Failing:
   - Check file permissions
   - Ensure file paths are correct
   - For binary files, use appropriate tools outside the application

4. Web Operations Not Working:
   - Check internet connection
   - Some websites may block automated requests
   - Try different URLs if one fails

5. Computer Actions Not Working:
   - Ensure pyautogui permissions are granted
   - On macOS: may need accessibility permissions
   - Check if coordinates are within screen bounds

Performance Tips:
- Close unnecessary applications for better screenshot performance
- Use smaller screenshot intervals for auto-capture
- Clear chat history periodically to improve performance

Getting Help:
- Check the Action Log for detailed error messages
- Enable verbose logging in settings
- Report issues with specific error messages
"""
        
        text_widget.insert(1.0, content)
        text_widget.config(state=tk.DISABLED)
