"""
Modern Control Panel for Claude Computer Use Assistant
Enhanced control interface with modern styling and improved tools
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import scrolledtext
import threading
from pathlib import Path
import webbrowser
from datetime import datetime
from config import Config
from utils.screenshot import ScreenshotManager
from utils.logging import ActionLogger
from gui.modern_theme import ModernTheme

class ModernControlPanel:
    def __init__(self, parent, claude_client, computer_actions, file_operations, web_operations, history_manager, styler):
        self.parent = parent
        self.claude_client = claude_client
        self.computer_actions = computer_actions
        self.file_operations = file_operations
        self.web_operations = web_operations
        self.history_manager = history_manager
        self.styler = styler
        self.theme = ModernTheme()
        self.screenshot_manager = ScreenshotManager()
        
        # Action counter
        self.action_count = 0
        
        # Create main control interface
        self.create_modern_control_interface()
        
        # Initialize logger after creating log_text widget
        self.logger = ActionLogger(self.log_text)
        
    def create_modern_control_interface(self):
        """Create the modern control interface"""
        # Main control container
        self.control_frame = tk.Frame(self.parent)
        self.control_frame.pack(fill='both', expand=True, padx=self.theme.SPACING['md'], 
                               pady=self.theme.SPACING['md'])
        self.styler.apply_modern_style(self.control_frame)
        
        # Control header
        self.create_control_header()
        
        # Modern tabbed interface
        self.create_modern_tabs()
        
    def create_control_header(self):
        """Create modern control header"""
        header_frame = tk.Frame(self.control_frame, height=50)
        header_frame.pack(fill='x', pady=(0, self.theme.SPACING['md']))
        header_frame.pack_propagate(False)
        self.styler.apply_modern_style(header_frame)
        
        # Tools title
        title_label = tk.Label(header_frame, text="🛠️ Tools", 
                              font=self.theme.FONTS['heading_medium'])
        title_label.pack(side='left', anchor='w')
        self.styler.apply_modern_style(title_label, 'heading')
        
        # Action counter
        self.action_counter_label = tk.Label(header_frame, text="Actions: 0", 
                                           font=self.theme.FONTS['caption'])
        self.action_counter_label.pack(side='right', anchor='e')
        self.styler.apply_modern_style(self.action_counter_label, 'caption')
        
    def create_modern_tabs(self):
        """Create modern tabbed interface"""
        # Create notebook with modern styling
        self.notebook = ttk.Notebook(self.control_frame, style='Modern.TNotebook')
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.create_screenshot_tab()
        self.create_computer_actions_tab()
        self.create_file_operations_tab()
        self.create_web_operations_tab()
        self.create_action_log_tab()
        
    def create_screenshot_tab(self):
        """Create enhanced screenshot control tab"""
        screenshot_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(screenshot_frame, text='📸 Screenshot')
        
        # Screenshot controls
        controls_frame = tk.Frame(screenshot_frame)
        controls_frame.pack(fill='x', padx=self.theme.SPACING['md'], pady=self.theme.SPACING['md'])
        self.styler.apply_modern_style(controls_frame)
        
        # Main screenshot button
        screenshot_btn = tk.Button(controls_frame, text="📸 Take Screenshot",
                                  command=self.take_screenshot,
                                  font=self.theme.FONTS['button'],
                                  padx=self.theme.SPACING['lg'],
                                  pady=self.theme.SPACING['sm'])
        screenshot_btn.pack(fill='x', pady=(0, self.theme.SPACING['sm']))
        self.styler.apply_modern_style(screenshot_btn, 'primary')
        
        # Auto screenshot controls
        auto_frame = tk.Frame(controls_frame)
        auto_frame.pack(fill='x', pady=self.theme.SPACING['sm'])
        self.styler.apply_modern_style(auto_frame)
        
        self.auto_screenshot_var = tk.BooleanVar()
        auto_check = tk.Checkbutton(auto_frame, text="Auto Screenshot",
                                   variable=self.auto_screenshot_var,
                                   command=self.toggle_auto_screenshot,
                                   font=self.theme.FONTS['body_medium'])
        auto_check.pack(side='left')
        self.styler.apply_modern_style(auto_check)
        
        # Interval selector
        interval_label = tk.Label(auto_frame, text="Interval (sec):",
                                 font=self.theme.FONTS['caption'])
        interval_label.pack(side='left', padx=(self.theme.SPACING['md'], self.theme.SPACING['sm']))
        self.styler.apply_modern_style(interval_label, 'caption')
        
        self.interval_var = tk.StringVar(value="2")
        interval_combo = ttk.Combobox(auto_frame, textvariable=self.interval_var,
                                     values=["1", "2", "3", "5", "10"], width=5,
                                     style='Modern.TCombobox')
        interval_combo.pack(side='left')
        
        # Screenshot display area
        display_frame = self.styler.create_modern_card(screenshot_frame)
        display_frame.pack(fill='both', expand=True, padx=self.theme.SPACING['md'], 
                          pady=(0, self.theme.SPACING['md']))
        
        # Screenshot info
        self.screenshot_info = tk.Label(display_frame, text="No screenshot taken",
                                       font=self.theme.FONTS['body_medium'])
        self.screenshot_info.pack(pady=self.theme.SPACING['md'])
        self.styler.apply_modern_style(self.screenshot_info)
        
        # Screenshot thumbnail
        self.screenshot_label = tk.Label(display_frame, text="📸\\nTake a screenshot\\nto see preview",
                                        font=self.theme.FONTS['body_large'],
                                        justify='center')
        self.screenshot_label.pack(expand=True, fill='both', padx=self.theme.SPACING['md'],
                                  pady=self.theme.SPACING['md'])
        self.styler.apply_modern_style(self.screenshot_label)
        
        # Auto screenshot variables
        self.auto_screenshot = False
        self.auto_screenshot_thread = None
        
    def create_computer_actions_tab(self):
        """Create enhanced computer actions tab"""
        actions_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(actions_frame, text='🖱️ Computer')
        
        # Quick actions
        quick_frame = self.styler.create_modern_card(actions_frame)
        quick_frame.pack(fill='x', padx=self.theme.SPACING['md'], pady=self.theme.SPACING['md'])
        
        quick_label = tk.Label(quick_frame, text="Quick Actions",
                              font=self.theme.FONTS['heading_small'])
        quick_label.pack(anchor='w', padx=self.theme.SPACING['md'], pady=(self.theme.SPACING['md'], 0))
        self.styler.apply_modern_style(quick_label, 'heading')
        
        # Action buttons grid
        actions_grid = tk.Frame(quick_frame)
        actions_grid.pack(fill='x', padx=self.theme.SPACING['md'], pady=self.theme.SPACING['md'])
        self.styler.apply_modern_style(actions_grid)
        
        # Row 1
        click_btn = tk.Button(actions_grid, text="🖱️ Click",
                             command=self.show_click_dialog,
                             width=12, font=self.theme.FONTS['button'])
        click_btn.grid(row=0, column=0, padx=self.theme.SPACING['sm'], pady=self.theme.SPACING['sm'])
        self.styler.apply_modern_style(click_btn, 'secondary')
        
        type_btn = tk.Button(actions_grid, text="⌨️ Type",
                            command=self.show_type_dialog,
                            width=12, font=self.theme.FONTS['button'])
        type_btn.grid(row=0, column=1, padx=self.theme.SPACING['sm'], pady=self.theme.SPACING['sm'])
        self.styler.apply_modern_style(type_btn, 'secondary')
        
        # Row 2
        scroll_btn = tk.Button(actions_grid, text="📜 Scroll",
                              command=self.show_scroll_dialog,
                              width=12, font=self.theme.FONTS['button'])
        scroll_btn.grid(row=1, column=0, padx=self.theme.SPACING['sm'], pady=self.theme.SPACING['sm'])
        self.styler.apply_modern_style(scroll_btn, 'secondary')
        
        key_btn = tk.Button(actions_grid, text="🔑 Key Press",
                           command=self.show_key_dialog,
                           width=12, font=self.theme.FONTS['button'])
        key_btn.grid(row=1, column=1, padx=self.theme.SPACING['sm'], pady=self.theme.SPACING['sm'])
        self.styler.apply_modern_style(key_btn, 'secondary')
        
        # Mouse position display
        position_frame = self.styler.create_modern_card(actions_frame)
        position_frame.pack(fill='x', padx=self.theme.SPACING['md'], pady=(0, self.theme.SPACING['md']))
        
        pos_label = tk.Label(position_frame, text="Mouse Position",
                            font=self.theme.FONTS['heading_small'])
        pos_label.pack(anchor='w', padx=self.theme.SPACING['md'], pady=(self.theme.SPACING['md'], 0))
        self.styler.apply_modern_style(pos_label, 'heading')
        
        self.mouse_pos_label = tk.Label(position_frame, text="X: 0, Y: 0",
                                       font=self.theme.FONTS['code'])
        self.mouse_pos_label.pack(padx=self.theme.SPACING['md'], pady=self.theme.SPACING['md'])
        self.styler.apply_modern_style(self.mouse_pos_label)
        
        # Start mouse tracking
        self.track_mouse_position()
        
    def create_file_operations_tab(self):
        """Create enhanced file operations tab"""
        file_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(file_frame, text='📁 Files')
        
        # File path section
        path_section = self.styler.create_modern_card(file_frame)
        path_section.pack(fill='x', padx=self.theme.SPACING['md'], pady=self.theme.SPACING['md'])
        
        path_label = tk.Label(path_section, text="File Path",
                             font=self.theme.FONTS['heading_small'])
        path_label.pack(anchor='w', padx=self.theme.SPACING['md'], pady=(self.theme.SPACING['md'], 0))
        self.styler.apply_modern_style(path_label, 'heading')
        
        path_frame = tk.Frame(path_section)
        path_frame.pack(fill='x', padx=self.theme.SPACING['md'], pady=self.theme.SPACING['md'])
        self.styler.apply_modern_style(path_frame)
        
        self.file_path_var = tk.StringVar()
        self.file_path_entry = tk.Entry(path_frame, textvariable=self.file_path_var,
                                       font=self.theme.FONTS['body_medium'])
        self.file_path_entry.pack(side='left', fill='x', expand=True,
                                 padx=(0, self.theme.SPACING['sm']))
        self.styler.apply_modern_style(self.file_path_entry)
        
        browse_btn = tk.Button(path_frame, text="📂 Browse",
                              command=self.browse_file,
                              font=self.theme.FONTS['button'])
        browse_btn.pack(side='right')
        self.styler.apply_modern_style(browse_btn, 'secondary')
        
        # File operations buttons
        ops_section = self.styler.create_modern_card(file_frame)
        ops_section.pack(fill='x', padx=self.theme.SPACING['md'], pady=(0, self.theme.SPACING['md']))
        
        ops_label = tk.Label(ops_section, text="Operations",
                            font=self.theme.FONTS['heading_small'])
        ops_label.pack(anchor='w', padx=self.theme.SPACING['md'], pady=(self.theme.SPACING['md'], 0))
        self.styler.apply_modern_style(ops_label, 'heading')
        
        ops_frame = tk.Frame(ops_section)
        ops_frame.pack(fill='x', padx=self.theme.SPACING['md'], pady=self.theme.SPACING['md'])
        self.styler.apply_modern_style(ops_frame)
        
        read_btn = tk.Button(ops_frame, text="📖 Read File",
                            command=self.read_file,
                            font=self.theme.FONTS['button'], width=12)
        read_btn.pack(side='left', padx=(0, self.theme.SPACING['sm']))
        self.styler.apply_modern_style(read_btn, 'primary')
        
        list_btn = tk.Button(ops_frame, text="📋 List Directory",
                            command=self.list_directory,
                            font=self.theme.FONTS['button'], width=12)
        list_btn.pack(side='left', padx=self.theme.SPACING['sm'])
        self.styler.apply_modern_style(list_btn, 'secondary')
        
        write_btn = tk.Button(ops_frame, text="✏️ Write File",
                             command=self.write_file,
                             font=self.theme.FONTS['button'], width=12)
        write_btn.pack(side='right')
        self.styler.apply_modern_style(write_btn, 'success')
        
        # File content display
        content_section = self.styler.create_modern_card(file_frame)
        content_section.pack(fill='both', expand=True, padx=self.theme.SPACING['md'],
                            pady=(0, self.theme.SPACING['md']))
        
        content_label = tk.Label(content_section, text="File Content",
                                font=self.theme.FONTS['heading_small'])
        content_label.pack(anchor='w', padx=self.theme.SPACING['md'], pady=(self.theme.SPACING['md'], 0))
        self.styler.apply_modern_style(content_label, 'heading')
        
        self.file_content_text = scrolledtext.ScrolledText(content_section, height=12,
                                                          font=self.theme.FONTS['code'])
        self.file_content_text.pack(fill='both', expand=True, padx=self.theme.SPACING['md'],
                                   pady=self.theme.SPACING['md'])
        self.styler.apply_modern_style(self.file_content_text)
        
    def create_web_operations_tab(self):
        """Create enhanced web operations tab"""
        web_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(web_frame, text='🌐 Web')
        
        # URL section
        url_section = self.styler.create_modern_card(web_frame)
        url_section.pack(fill='x', padx=self.theme.SPACING['md'], pady=self.theme.SPACING['md'])
        
        url_label = tk.Label(url_section, text="Web Address",
                            font=self.theme.FONTS['heading_small'])
        url_label.pack(anchor='w', padx=self.theme.SPACING['md'], pady=(self.theme.SPACING['md'], 0))
        self.styler.apply_modern_style(url_label, 'heading')
        
        url_frame = tk.Frame(url_section)
        url_frame.pack(fill='x', padx=self.theme.SPACING['md'], pady=self.theme.SPACING['md'])
        self.styler.apply_modern_style(url_frame)
        
        self.url_var = tk.StringVar()
        self.url_entry = tk.Entry(url_frame, textvariable=self.url_var,
                                 font=self.theme.FONTS['body_medium'])
        self.url_entry.pack(side='left', fill='x', expand=True,
                           padx=(0, self.theme.SPACING['sm']))
        self.url_entry.bind('<Return>', lambda e: self.load_page())
        self.styler.apply_modern_style(self.url_entry)
        
        load_btn = tk.Button(url_frame, text="🚀 Load",
                            command=self.load_page,
                            font=self.theme.FONTS['button'])
        load_btn.pack(side='right')
        self.styler.apply_modern_style(load_btn, 'primary')
        
        # Web operations
        ops_section = self.styler.create_modern_card(web_frame)
        ops_section.pack(fill='x', padx=self.theme.SPACING['md'], pady=(0, self.theme.SPACING['md']))
        
        ops_label = tk.Label(ops_section, text="Web Operations",
                            font=self.theme.FONTS['heading_small'])
        ops_label.pack(anchor='w', padx=self.theme.SPACING['md'], pady=(self.theme.SPACING['md'], 0))
        self.styler.apply_modern_style(ops_label, 'heading')
        
        ops_frame = tk.Frame(ops_section)
        ops_frame.pack(fill='x', padx=self.theme.SPACING['md'], pady=self.theme.SPACING['md'])
        self.styler.apply_modern_style(ops_frame)
        
        content_btn = tk.Button(ops_frame, text="📄 Get Content",
                               command=self.get_page_content,
                               font=self.theme.FONTS['button'], width=10)
        content_btn.pack(side='left', padx=(0, self.theme.SPACING['sm']))
        self.styler.apply_modern_style(content_btn, 'secondary')
        
        links_btn = tk.Button(ops_frame, text="🔗 Extract Links",
                             command=self.extract_links,
                             font=self.theme.FONTS['button'], width=10)
        links_btn.pack(side='left', padx=self.theme.SPACING['sm'])
        self.styler.apply_modern_style(links_btn, 'secondary')
        
        browser_btn = tk.Button(ops_frame, text="🌍 Open Browser",
                               command=self.open_in_browser,
                               font=self.theme.FONTS['button'], width=10)
        browser_btn.pack(side='right')
        self.styler.apply_modern_style(browser_btn, 'secondary')
        
        # Search frame
        search_section = self.styler.create_modern_card(web_frame)
        search_section.pack(fill='x', padx=self.theme.SPACING['md'], pady=(0, self.theme.SPACING['md']))
        
        search_label = tk.Label(search_section, text="Search in Page",
                               font=self.theme.FONTS['heading_small'])
        search_label.pack(anchor='w', padx=self.theme.SPACING['md'], pady=(self.theme.SPACING['md'], 0))
        self.styler.apply_modern_style(search_label, 'heading')
        
        search_frame = tk.Frame(search_section)
        search_frame.pack(fill='x', padx=self.theme.SPACING['md'], pady=self.theme.SPACING['md'])
        self.styler.apply_modern_style(search_frame)
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                                    font=self.theme.FONTS['body_medium'])
        self.search_entry.pack(side='left', fill='x', expand=True,
                              padx=(0, self.theme.SPACING['sm']))
        self.search_entry.bind('<Return>', lambda e: self.search_in_content())
        self.styler.apply_modern_style(self.search_entry)
        
        search_btn = tk.Button(search_frame, text="🔍 Search",
                              command=self.search_in_content,
                              font=self.theme.FONTS['button'])
        search_btn.pack(side='right')
        self.styler.apply_modern_style(search_btn, 'primary')
        
        # Web content display
        content_section = self.styler.create_modern_card(web_frame)
        content_section.pack(fill='both', expand=True, padx=self.theme.SPACING['md'],
                            pady=(0, self.theme.SPACING['md']))
        
        content_label = tk.Label(content_section, text="Web Content",
                                font=self.theme.FONTS['heading_small'])
        content_label.pack(anchor='w', padx=self.theme.SPACING['md'], pady=(self.theme.SPACING['md'], 0))
        self.styler.apply_modern_style(content_label, 'heading')
        
        self.web_content_text = scrolledtext.ScrolledText(content_section, height=8,
                                                         font=self.theme.FONTS['body_medium'])
        self.web_content_text.pack(fill='both', expand=True, padx=self.theme.SPACING['md'],
                                  pady=self.theme.SPACING['md'])
        self.styler.apply_modern_style(self.web_content_text)
        
    def create_action_log_tab(self):
        """Create enhanced action log tab"""
        log_frame = ttk.Frame(self.notebook, style='Modern.TFrame')
        self.notebook.add(log_frame, text='📝 Log')
        
        # Log controls
        controls_section = self.styler.create_modern_card(log_frame)
        controls_section.pack(fill='x', padx=self.theme.SPACING['md'], pady=self.theme.SPACING['md'])
        
        controls_label = tk.Label(controls_section, text="Log Controls",
                                 font=self.theme.FONTS['heading_small'])
        controls_label.pack(anchor='w', padx=self.theme.SPACING['md'], pady=(self.theme.SPACING['md'], 0))
        self.styler.apply_modern_style(controls_label, 'heading')
        
        controls_frame = tk.Frame(controls_section)
        controls_frame.pack(fill='x', padx=self.theme.SPACING['md'], pady=self.theme.SPACING['md'])
        self.styler.apply_modern_style(controls_frame)
        
        clear_btn = tk.Button(controls_frame, text="🗑️ Clear Log",
                             command=self.clear_log,
                             font=self.theme.FONTS['button'])
        clear_btn.pack(side='left', padx=(0, self.theme.SPACING['sm']))
        self.styler.apply_modern_style(clear_btn, 'secondary')
        
        export_btn = tk.Button(controls_frame, text="💾 Export Log",
                              command=self.export_log,
                              font=self.theme.FONTS['button'])
        export_btn.pack(side='left')
        self.styler.apply_modern_style(export_btn, 'secondary')
        
        # Auto-scroll toggle
        self.auto_scroll_var = tk.BooleanVar(value=True)
        auto_scroll_check = tk.Checkbutton(controls_frame, text="Auto-scroll",
                                          variable=self.auto_scroll_var,
                                          font=self.theme.FONTS['body_small'])
        auto_scroll_check.pack(side='right')
        self.styler.apply_modern_style(auto_scroll_check)
        
        # Log display
        log_section = self.styler.create_modern_card(log_frame)
        log_section.pack(fill='both', expand=True, padx=self.theme.SPACING['md'],
                        pady=(0, self.theme.SPACING['md']))
        
        log_label = tk.Label(log_section, text="Action Log",
                            font=self.theme.FONTS['heading_small'])
        log_label.pack(anchor='w', padx=self.theme.SPACING['md'], pady=(self.theme.SPACING['md'], 0))
        self.styler.apply_modern_style(log_label, 'heading')
        
        self.log_text = scrolledtext.ScrolledText(log_section, height=15, state=tk.DISABLED,
                                                 font=self.theme.FONTS['code'])
        self.log_text.pack(fill='both', expand=True, padx=self.theme.SPACING['md'],
                          pady=self.theme.SPACING['md'])
        self.styler.apply_modern_style(self.log_text)
        
    # Screenshot methods
    def take_screenshot(self):
        """Take a screenshot with enhanced feedback"""
        def screenshot_thread():
            try:
                screenshot = self.screenshot_manager.take_screenshot()
                thumbnail = self.screenshot_manager.get_thumbnail()
                
                # Update UI in main thread
                self.parent.after(0, self.update_screenshot_display, screenshot, thumbnail)
                self.log_action("Screenshot taken successfully")
                self.increment_action_counter()
                
            except Exception as e:
                self.log_action(f"Screenshot failed: {str(e)}")
                self.parent.after(0, lambda: messagebox.showerror("Screenshot Error", str(e)))
        
        threading.Thread(target=screenshot_thread, daemon=True).start()
        
    def update_screenshot_display(self, screenshot, thumbnail):
        """Update screenshot display with modern styling"""
        if thumbnail:
            self.screenshot_label.config(image=thumbnail, text="")
            self.screenshot_label.image = thumbnail  # Keep a reference
        
        if screenshot:
            size = screenshot.size
            self.screenshot_info.config(text=f"📸 {size[0]}×{size[1]} pixels • {datetime.now().strftime('%H:%M:%S')}")
        
    def toggle_auto_screenshot(self):
        """Toggle auto screenshot mode"""
        self.auto_screenshot = self.auto_screenshot_var.get()
        if self.auto_screenshot:
            self.start_auto_screenshot()
            self.log_action("Auto screenshot enabled")
        else:
            self.stop_auto_screenshot()
            self.log_action("Auto screenshot disabled")
            
    def start_auto_screenshot(self):
        """Start auto screenshot thread"""
        def auto_screenshot_loop():
            while self.auto_screenshot:
                try:
                    screenshot = self.screenshot_manager.take_screenshot()
                    thumbnail = self.screenshot_manager.get_thumbnail()
                    self.parent.after(0, self.update_screenshot_display, screenshot, thumbnail)
                    
                    # Wait based on interval
                    import time
                    interval = float(self.interval_var.get())
                    time.sleep(interval)
                    
                except Exception as e:
                    self.log_action(f"Auto screenshot error: {str(e)}")
                    break
        
        self.auto_screenshot_thread = threading.Thread(target=auto_screenshot_loop, daemon=True)
        self.auto_screenshot_thread.start()
        
    def stop_auto_screenshot(self):
        """Stop auto screenshot"""
        self.auto_screenshot = False
        
    # Computer action methods
    def show_click_dialog(self):
        """Show click dialog"""
        from tkinter import simpledialog
        coordinates = simpledialog.askstring("Click Action", "Enter coordinates (x,y):")
        if coordinates:
            try:
                x, y = map(int, coordinates.split(','))
                self.execute_computer_action({"action": "click", "coordinate": [x, y]})
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter coordinates as x,y")
                
    def show_type_dialog(self):
        """Show type dialog"""
        from tkinter import simpledialog
        text = simpledialog.askstring("Type Action", "Enter text to type:")
        if text:
            self.execute_computer_action({"action": "type", "text": text})
            
    def show_scroll_dialog(self):
        """Show scroll dialog"""
        from tkinter import simpledialog
        clicks = simpledialog.askinteger("Scroll Action", "Enter scroll clicks (positive=up, negative=down):")
        if clicks is not None:
            self.execute_computer_action({"action": "scroll", "clicks": clicks})
            
    def show_key_dialog(self):
        """Show key press dialog"""
        from tkinter import simpledialog
        key = simpledialog.askstring("Key Press", "Enter key to press (e.g., 'enter', 'space', 'ctrl+c'):")
        if key:
            self.execute_computer_action({"action": "key", "key": key})
            
    def execute_computer_action(self, action_data):
        """Execute computer action"""
        def action_thread():
            try:
                result = self.computer_actions.execute_action(action_data)
                self.log_action(f"Computer action: {result}")
                self.increment_action_counter()
            except Exception as e:
                self.log_action(f"Computer action failed: {str(e)}")
                
        threading.Thread(target=action_thread, daemon=True).start()
        
    def track_mouse_position(self):
        """Track and display mouse position"""
        try:
            import pyautogui
            x, y = pyautogui.position()
            self.mouse_pos_label.config(text=f"X: {x}, Y: {y}")
        except:
            pass
        
        # Update every 100ms
        self.parent.after(100, self.track_mouse_position)
        
    # File operation methods
    def browse_file(self):
        """Browse for file with enhanced dialog"""
        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=[
                ("All Files", "*.*"),
                ("Text Files", "*.txt"),
                ("Python Files", "*.py"),
                ("JSON Files", "*.json"),
                ("Markdown Files", "*.md"),
                ("CSV Files", "*.csv"),
                ("HTML Files", "*.html"),
                ("CSS Files", "*.css"),
                ("JavaScript Files", "*.js")
            ]
        )
        if file_path:
            self.file_path_var.set(file_path)
            
    def read_file(self):
        """Read file content with enhanced error handling"""
        file_path = self.file_path_var.get().strip()
        if not file_path:
            messagebox.showwarning("No File", "Please enter a file path or browse for a file")
            return
            
        def read_thread():
            try:
                operation_data = {
                    "operation": "read",
                    "file_path": file_path
                }
                result = self.file_operations.execute_operation(operation_data)
                
                # Update UI in main thread
                self.parent.after(0, self.update_file_content, result)
                self.log_action(f"Read file: {file_path}")
                self.increment_action_counter()
                
            except Exception as e:
                self.log_action(f"File read error: {str(e)}")
                self.parent.after(0, lambda: messagebox.showerror("File Error", str(e)))
        
        threading.Thread(target=read_thread, daemon=True).start()
        
    def update_file_content(self, result):
        """Update file content display"""
        self.file_content_text.delete(1.0, tk.END)
        
        if isinstance(result, dict) and result.get('success'):
            content = result.get('content', '')
            self.file_content_text.insert(1.0, content)
            self.log_action(f"File content loaded: {result.get('length', 0)} characters")
        else:
            self.file_content_text.insert(1.0, str(result))
            
    def list_directory(self):
        """List directory contents"""
        dir_path = self.file_path_var.get().strip() or "."
        
        def list_thread():
            try:
                operation_data = {
                    "operation": "list",
                    "file_path": dir_path
                }
                result = self.file_operations.execute_operation(operation_data)
                
                # Update UI in main thread
                self.parent.after(0, self.update_directory_listing, result)
                self.log_action(f"Listed directory: {dir_path}")
                self.increment_action_counter()
                
            except Exception as e:
                self.log_action(f"Directory list error: {str(e)}")
                self.parent.after(0, lambda: messagebox.showerror("Directory Error", str(e)))
        
        threading.Thread(target=list_thread, daemon=True).start()
        
    def update_directory_listing(self, result):
        """Update directory listing display"""
        self.file_content_text.delete(1.0, tk.END)
        
        if isinstance(result, dict) and result.get('success'):
            items = result.get('items', [])
            content = f"📁 Directory: {result.get('path', '')}\\n"
            content += f"📊 Items: {result.get('count', 0)}\\n\\n"
            content += "\\n".join(items)
            self.file_content_text.insert(1.0, content)
        else:
            self.file_content_text.insert(1.0, str(result))
            
    def write_file(self):
        """Write file content"""
        file_path = self.file_path_var.get().strip()
        if not file_path:
            messagebox.showwarning("No File", "Please enter a file path")
            return
            
        content = self.file_content_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("No Content", "Please enter content to write")
            return
            
        def write_thread():
            try:
                operation_data = {
                    "operation": "write",
                    "file_path": file_path,
                    "content": content
                }
                result = self.file_operations.execute_operation(operation_data)
                
                self.log_action(f"Wrote file: {file_path}")
                self.increment_action_counter()
                self.parent.after(0, lambda: messagebox.showinfo("Success", str(result)))
                
            except Exception as e:
                self.log_action(f"File write error: {str(e)}")
                self.parent.after(0, lambda: messagebox.showerror("File Error", str(e)))
        
        threading.Thread(target=write_thread, daemon=True).start()
        
    # Web operation methods
    def load_page(self):
        """Load web page with enhanced feedback"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("No URL", "Please enter a URL")
            return
            
        def load_thread():
            try:
                operation_data = {
                    "operation": "load_page",
                    "url": url
                }
                result = self.web_operations.execute_operation(operation_data)
                
                # Update UI in main thread
                self.parent.after(0, self.update_web_content, result)
                self.log_action(f"Loaded page: {url}")
                self.increment_action_counter()
                
            except Exception as e:
                self.log_action(f"Page load error: {str(e)}")
                self.parent.after(0, lambda: messagebox.showerror("Web Error", str(e)))
        
        threading.Thread(target=load_thread, daemon=True).start()
        
    def update_web_content(self, result):
        """Update web content display"""
        self.web_content_text.delete(1.0, tk.END)
        
        if isinstance(result, dict) and result.get('success'):
            content = result.get('content', '')
            domain = result.get('domain', 'Unknown')
            length = result.get('content_length', 0)
            
            header = f"🌐 Domain: {domain}\\n📊 Content: {length} characters\\n{'='*50}\\n\\n"
            self.web_content_text.insert(1.0, header + content)
            self.log_action(f"Web content loaded: {length} characters from {domain}")
        else:
            self.web_content_text.insert(1.0, str(result))
            
    def get_page_content(self):
        """Get current page content"""
        def content_thread():
            try:
                operation_data = {"operation": "get_content"}
                result = self.web_operations.execute_operation(operation_data)
                
                # Update UI in main thread
                self.parent.after(0, self.update_web_content, result)
                self.log_action("Retrieved current page content")
                self.increment_action_counter()
                
            except Exception as e:
                self.log_action(f"Get content error: {str(e)}")
                self.parent.after(0, lambda: messagebox.showerror("Web Error", str(e)))
        
        threading.Thread(target=content_thread, daemon=True).start()
        
    def extract_links(self):
        """Extract links from current page"""
        def extract_thread():
            try:
                operation_data = {"operation": "extract_links"}
                result = self.web_operations.execute_operation(operation_data)
                
                # Update UI in main thread
                self.parent.after(0, self.update_links_display, result)
                self.log_action("Extracted links from current page")
                self.increment_action_counter()
                
            except Exception as e:
                self.log_action(f"Extract links error: {str(e)}")
                self.parent.after(0, lambda: messagebox.showerror("Web Error", str(e)))
        
        threading.Thread(target=extract_thread, daemon=True).start()
        
    def update_links_display(self, result):
        """Update links display with enhanced formatting"""
        self.web_content_text.delete(1.0, tk.END)
        
        if isinstance(result, dict) and result.get('success'):
            links = result.get('links', [])
            total = result.get('total_count', 0)
            
            content = f"🔗 Found {total} links (showing first {len(links)}):\\n\\n"
            for i, link in enumerate(links, 1):
                text = link.get('text', 'No text')[:50]
                url = link.get('url', '')
                content += f"{i:2d}. {text}\\n    {url}\\n\\n"
            
            self.web_content_text.insert(1.0, content)
        else:
            self.web_content_text.insert(1.0, str(result))
            
    def search_in_content(self):
        """Search in current page content"""
        search_text = self.search_var.get().strip()
        if not search_text:
            messagebox.showwarning("No Search Text", "Please enter text to search")
            return
            
        def search_thread():
            try:
                operation_data = {
                    "operation": "search_elements",
                    "search_text": search_text
                }
                result = self.web_operations.execute_operation(operation_data)
                
                self.log_action(f"Searched for: {search_text}")
                self.increment_action_counter()
                self.parent.after(0, lambda: messagebox.showinfo("Search Result", str(result)))
                
            except Exception as e:
                self.log_action(f"Search error: {str(e)}")
                self.parent.after(0, lambda: messagebox.showerror("Search Error", str(e)))
        
        threading.Thread(target=search_thread, daemon=True).start()
        
    def open_in_browser(self):
        """Open URL in browser"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("No URL", "Please enter a URL")
            return
            
        try:
            result = self.web_operations.open_in_browser(url)
            self.log_action(f"Opened in browser: {url}")
            self.increment_action_counter()
            messagebox.showinfo("Success", str(result))
        except Exception as e:
            self.log_action(f"Browser open error: {str(e)}")
            messagebox.showerror("Browser Error", str(e))
            
    # Utility methods
    def increment_action_counter(self):
        """Increment action counter"""
        self.action_count += 1
        self.action_counter_label.config(text=f"Actions: {self.action_count}")
        
        # Update main window counter if available
        try:
            main_window = self.parent.master.master
            if hasattr(main_window, 'action_count_label'):
                main_window.action_count_label.config(text=f"Actions: {self.action_count}")
        except:
            pass
            
    def clear_log(self):
        """Clear action log"""
        self.logger.clear()
        self.log_action("Log cleared")
        
    def export_log(self):
        """Export action log"""
        file_path = filedialog.asksaveasfilename(
            title="Export Action Log",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                log_content = self.log_text.get(1.0, tk.END)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"Claude AI Assistant - Action Log\\n")
                    f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
                    f.write(f"Total Actions: {self.action_count}\\n")
                    f.write("="*50 + "\\n\\n")
                    f.write(log_content)
                self.log_action(f"Log exported to: {file_path}")
                messagebox.showinfo("Success", f"Log exported to {file_path}")
            except Exception as e:
                self.log_action(f"Export error: {str(e)}")
                messagebox.showerror("Export Error", str(e))
                
    def get_current_screenshot(self):
        """Get current screenshot for use by other components"""
        return self.screenshot_manager.current_screenshot
        
    def get_current_page_content(self):
        """Get current page content for use by other components"""
        return self.web_operations.current_page_content
        
    def log_action(self, message):
        """Log an action with timestamp and auto-scroll"""
        self.logger.log(message)
        
        # Auto-scroll if enabled
        if self.auto_scroll_var.get():
            self.log_text.see(tk.END)

# For backward compatibility
ControlPanel = ModernControlPanel
