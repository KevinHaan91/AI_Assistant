"""
Modern Chat Panel for Claude Computer Use Assistant
Enhanced chat interface with modern styling and improved messaging
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from datetime import datetime
import re
import webbrowser
from config import Config
from gui.modern_theme import ModernTheme

class ModernChatPanel:
    def __init__(self, parent, claude_client, control_panel, history_manager, styler):
        self.parent = parent
        self.claude_client = claude_client
        self.control_panel = control_panel
        self.history_manager = history_manager
        self.styler = styler
        self.theme = ModernTheme()
        
        # Message counter
        self.message_count = 0
        
        # Create chat interface
        self.create_modern_chat_interface()
        
        # Load conversation history
        self.load_conversation_history()
        
    def create_modern_chat_interface(self):
        """Create the modern chat interface"""
        # Main chat container with card style and shadow
        self.chat_frame = tk.Frame(self.parent, bg=self.theme.COLORS['surface'], bd=0, highlightthickness=0)
        self.chat_frame.pack(fill='both', expand=True, padx=self.theme.SPACING['xl'], pady=self.theme.SPACING['xl'])
        self.chat_frame.configure(relief='flat')
        self.chat_frame.configure(highlightbackground=self.theme.COLORS['border_primary'])
        self.chat_frame.configure(highlightcolor=self.theme.COLORS['border_primary'])
        self.chat_frame.configure(highlightthickness=2)
        self.chat_frame.configure(borderwidth=0)
        self.chat_frame.configure(cursor='arrow')
        self.styler.apply_modern_style(self.chat_frame)
        
        # Chat header
        self.create_chat_header()
        
        # Chat display area
        self.create_chat_display()
        
        # Input area
        self.create_modern_input_area()
        
    def create_chat_header(self):
        """Create modern chat header with status and controls"""
        header_frame = tk.Frame(self.chat_frame, height=50)
        header_frame.pack(fill='x', pady=(0, self.theme.SPACING['md']))
        header_frame.pack_propagate(False)
        self.styler.apply_modern_style(header_frame)
        
        # Chat title
        title_label = tk.Label(header_frame, text="💬 Conversation", 
                              font=self.theme.FONTS['heading_medium'])
        title_label.pack(side='left', anchor='w')
        self.styler.apply_modern_style(title_label, 'heading')
        
        # Chat controls
        controls_frame = tk.Frame(header_frame)
        controls_frame.pack(side='right', fill='y')
        self.styler.apply_modern_style(controls_frame)
        
        # Clear chat button
        clear_btn = tk.Button(controls_frame, text="🗑️",
                             command=self.clear_chat_with_confirmation,
                             width=3, height=1)
        clear_btn.pack(side='right', padx=self.theme.SPACING['sm'])
        self.styler.apply_modern_style(clear_btn, 'secondary')
        
        # Export chat button
        export_btn = tk.Button(controls_frame, text="💾",
                              command=self.export_chat,
                              width=3, height=1)
        export_btn.pack(side='right', padx=self.theme.SPACING['sm'])
        self.styler.apply_modern_style(export_btn, 'secondary')
        
    def create_chat_display(self):
        """Create modern chat display area"""
        # Chat display container
        display_container = tk.Frame(self.chat_frame)
        display_container.pack(fill='both', expand=True, pady=(0, self.theme.SPACING['md']))
        self.styler.apply_modern_style(display_container)
        
        # Create scrollable text widget with modern styling
        self.chat_display = tk.Text(
            display_container,
            wrap=tk.WORD,
            state=tk.DISABLED,
            cursor='arrow',
            spacing1=4,
            spacing2=2,
            spacing3=4,
            padx=self.theme.SPACING['md'],
            pady=self.theme.SPACING['md'],
            height=18 # Ensure chat area is always visible
        )
        
        # Modern scrollbar
        scrollbar = ttk.Scrollbar(display_container, orient='vertical', 
                                 command=self.chat_display.yview,
                                 style='Modern.Vertical.TScrollbar')
        self.chat_display.configure(yscrollcommand=scrollbar.set)
        
        # Pack elements
        scrollbar.pack(side='right', fill='y')
        self.chat_display.pack(side='left', fill='both', expand=True)
        
        # Apply modern styling
        self.styler.apply_modern_style(self.chat_display, 'chat')
        
        # Configure modern text tags
        self.setup_modern_text_tags()
        
        # Bind events for interactive features
        self.chat_display.bind('<Button-1>', self.on_chat_click)
        self.chat_display.bind('<Motion>', self.on_chat_hover)
        
    def setup_modern_text_tags(self):
        """Setup modern text formatting tags"""
        colors = self.theme.COLORS
        fonts = self.theme.FONTS
        
        # User message styling
        self.chat_display.tag_config('user_name', 
                                    foreground=colors['chat_user'], 
                                    font=fonts['heading_small'])
        self.chat_display.tag_config('user_msg', 
                                    foreground=colors['text_primary'], 
                                    font=fonts['chat'],
                                    lmargin1=20, lmargin2=20)
        
        # Assistant message styling
        self.chat_display.tag_config('assistant_name', 
                                    foreground=colors['chat_assistant'], 
                                    font=fonts['heading_small'])
        self.chat_display.tag_config('assistant_msg', 
                                    foreground=colors['text_primary'], 
                                    font=fonts['chat'],
                                    lmargin1=20, lmargin2=20)
        
        # System message styling
        self.chat_display.tag_config('system', 
                                    foreground=colors['chat_system'], 
                                    font=fonts['body_small'],
                                    justify='center')
        
        # Error message styling
        self.chat_display.tag_config('error', 
                                    foreground=colors['chat_error'], 
                                    font=fonts['body_medium'])
        
        # Timestamp styling
        self.chat_display.tag_config('timestamp', 
                                    foreground=colors['chat_timestamp'], 
                                    font=fonts['caption'])
        
        # Special styling for different message types
        self.chat_display.tag_config('code', 
                                    foreground=colors['text_secondary'], 
                                    font=fonts['code'],
                                    background=colors['bg_tertiary'])
        
        self.chat_display.tag_config('link', 
                                    foreground=colors['accent_primary'], 
                                    font=fonts['body_medium'],
                                    underline=True)
        
        self.chat_display.tag_config('highlight', 
                                    background=colors['accent_primary'],
                                    foreground=colors['text_primary'])
        
        # Message bubbles (using background colors)
        self.chat_display.tag_config('user_bubble', 
                                    background=colors['bg_tertiary'],
                                    relief='flat')
        self.chat_display.tag_config('assistant_bubble', 
                                    background=colors['surface'],
                                    relief='flat')
        
    def create_modern_input_area(self):
        """Create modern message input area"""
        # Input container with rounded corners and shadow
        input_container = tk.Frame(self.chat_frame, bg=self.theme.COLORS['surface_variant'])
        input_container.pack(fill='x', pady=(self.theme.SPACING['lg'], 0), padx=self.theme.SPACING['lg'])
        input_container.configure(highlightbackground=self.theme.COLORS['border_primary'], highlightthickness=1, bd=0)
        input_container.configure(relief='flat')
        input_container.configure(borderwidth=0)
        input_container.configure(cursor='arrow')
        input_container.configure(pady=self.theme.SPACING['md'])
        self.styler.apply_modern_style(input_container)
        
        # Input options frame
        options_frame = tk.Frame(input_container)
        options_frame.pack(fill='x', pady=(0, self.theme.SPACING['sm']))
        self.styler.apply_modern_style(options_frame)
        
        # Attachment options
        self.include_screenshot_var = tk.BooleanVar(value=False)
        screenshot_check = tk.Checkbutton(
            options_frame, 
            text="📸 Include Screenshot",
            variable=self.include_screenshot_var,
            font=self.theme.FONTS['body_small']
        )
        screenshot_check.pack(side='left', padx=(0, self.theme.SPACING['md']))
        self.styler.apply_modern_style(screenshot_check)
        
        self.include_page_content_var = tk.BooleanVar(value=False)
        page_check = tk.Checkbutton(
            options_frame,
            text="🌐 Include Web Content",
            variable=self.include_page_content_var,
            font=self.theme.FONTS['body_small']
        )
        page_check.pack(side='left', padx=(0, self.theme.SPACING['md']))
        self.styler.apply_modern_style(page_check)
        
        # Quick actions
        quick_actions_frame = tk.Frame(options_frame)
        quick_actions_frame.pack(side='right')
        self.styler.apply_modern_style(quick_actions_frame)
        
        # Quick screenshot button
        quick_screenshot_btn = tk.Button(quick_actions_frame, text="📸",
                                        command=self.quick_screenshot,
                                        width=3)
        quick_screenshot_btn.pack(side='right', padx=self.theme.SPACING['sm'])
        self.styler.apply_modern_style(quick_screenshot_btn, 'secondary')
        
        # Input text area with modern styling
        input_frame = tk.Frame(input_container)
        input_frame.pack(fill='x')
        self.styler.apply_modern_style(input_frame)
        
        # Modern text input with more padding and rounded corners
        self.message_input = tk.Text(
            input_frame,
            height=3,
            wrap=tk.WORD,
            font=("Segoe UI", 13),
            padx=self.theme.SPACING['xl'],
            pady=self.theme.SPACING['md'],
            bg=self.theme.COLORS['chat_bg'],
            fg=self.theme.COLORS['text_tertiary'],
            insertbackground=self.theme.COLORS['chat_text'],
            highlightbackground=self.theme.COLORS['accent_secondary'],
            highlightcolor=self.theme.COLORS['accent_success'],
            highlightthickness=2,
            relief='flat',
            borderwidth=0,
            spacing1=8, spacing2=6, spacing3=8,
            tabs=('1c',)
        )
        self.message_input.pack(side='left', fill='both', expand=True, padx=(0, self.theme.SPACING['md']))
        self.message_input.configure(cursor='xterm')
        self.message_input.insert('1.0', 'Type your message here...')
        self.message_input.config(fg=self.theme.COLORS['text_tertiary'])
        self.message_input.bind('<FocusIn>', self.clear_placeholder)
        self.message_input.bind('<FocusOut>', self.restore_placeholder)
        
        # Send button container
        send_container = tk.Frame(input_frame)
        send_container.pack(side='right', fill='y')
        self.styler.apply_modern_style(send_container)
        
        # Modern send button: pill shape, icon, bold color
        self.send_button = tk.Button(
            send_container,
            text="➤",
            command=self.send_message,
            width=3,
            height=1,
            font=("Segoe UI", 16, "bold"),
            bg=self.theme.COLORS['accent_success'],
            fg=self.theme.COLORS['chat_bg'],
            activebackground=self.theme.COLORS['accent_secondary'],
            activeforeground=self.theme.COLORS['chat_bg'],
            relief='flat',
            borderwidth=0,
            highlightthickness=0,
            cursor='hand2',
            padx=18,
            pady=6
        )
        self.send_button.pack(fill='y', expand=False, pady=(self.theme.SPACING['sm'], 0), padx=(self.theme.SPACING['md'], 0))
        self.send_button.bind('<Enter>', lambda e: self.send_button.config(bg=self.theme.COLORS['accent_secondary']))
        self.send_button.bind('<Leave>', lambda e: self.send_button.config(bg=self.theme.COLORS['accent_success']))
        
        # Bind keyboard shortcuts
        self.message_input.bind('<Control-Return>', self.send_message_event)
        self.message_input.bind('<KeyRelease>', self.on_input_change)
        
        # Auto-resize input
        self.message_input.bind('<Configure>', self.auto_resize_input)
        
    def auto_resize_input(self, event=None):
        """Auto-resize input based on content"""
        lines = self.message_input.get('1.0', 'end-1c').count('\\n') + 1
        new_height = min(max(lines, 2), 8)  # Between 2 and 8 lines
        if self.message_input.cget('height') != new_height:
            self.message_input.configure(height=new_height)
            
    def on_input_change(self, event=None):
        """Handle input changes for real-time features"""
        content = self.message_input.get('1.0', 'end-1c').strip()
        
        # Update send button state
        if content:
            self.styler.apply_modern_style(self.send_button, 'primary')
            self.send_button.config(state='normal')
        else:
            self.styler.apply_modern_style(self.send_button, 'secondary')
        
        # Auto-resize
        self.auto_resize_input()
        
    def quick_screenshot(self):
        """Take a quick screenshot and enable include option"""
        self.control_panel.take_screenshot()
        self.include_screenshot_var.set(True)
        self.add_system_message("📸 Screenshot captured and will be included with next message")
        
    def send_message_event(self, event):
        """Handle Enter key press"""
        self.send_message()
        return 'break'  # Prevent default Enter behavior
        
    def send_message(self):
        """Send message to Claude with enhanced features"""
        message = self.message_input.get('1.0', 'end-1c').strip()
        if not message:
            messagebox.showwarning("Empty Message", "Please enter a message")
            return
            
        # Check for special commands
        if self.handle_special_commands(message):
            return
            
        # Get optional attachments
        screenshot = None
        page_content = None
        
        if self.include_screenshot_var.get():
            screenshot = self.control_panel.get_current_screenshot()
            if not screenshot:
                messagebox.showwarning("No Screenshot", "Please take a screenshot first")
                return
                
        if self.include_page_content_var.get():
            page_content = self.control_panel.get_current_page_content()
            if not page_content:
                messagebox.showwarning("No Page Content", "Please load a web page first")
                return
        
        # Clear input and reset options
        self.message_input.delete('1.0', 'end')
        self.include_screenshot_var.set(False)
        self.include_page_content_var.set(False)
        
        # Add user message to chat
        self.add_user_message(message, has_screenshot=screenshot is not None)
        
        # Update status and send in separate thread
        if hasattr(self.parent.master.master, 'update_status'):
            self.parent.master.master.update_status("Sending message...", "busy")
        
        threading.Thread(target=self.send_message_thread, 
                        args=(message, screenshot, page_content), daemon=True).start()
        
    def handle_special_commands(self, message):
        """Handle special commands like sending texts"""
        message_lower = message.lower()
        
        # Text message commands
        text_patterns = [
            r'send (?:text|message) to (\\w+)',
            r'text (\\w+)',
            r'message (\\w+)'
        ]
        
        for pattern in text_patterns:
            match = re.search(pattern, message_lower)
            if match:
                recipient = match.group(1)
                return self.handle_text_command(message, recipient)
        
        # Screenshot commands
        if any(cmd in message_lower for cmd in ['take screenshot', 'capture screen', 'screenshot']):
            self.quick_screenshot()
            return True
            
        return False
        
    def handle_text_command(self, original_message, recipient):
        """Handle text sending commands"""
        # Extract the message content
        content_patterns = [
            r'saying? [\"\'](.*?)[\"\']',
            r'saying? (.*?)$',
            r'send (?:text|message) to \\w+ (.*?)$',
        ]
        
        message_content = None
        for pattern in content_patterns:
            match = re.search(pattern, original_message, re.IGNORECASE)
            if match:
                message_content = match.group(1).strip()
                break
        
        if not message_content:
            self.add_system_message(f"❓ What would you like to text {recipient}? Please specify the message content.")
            return True
        
        # Show confirmation dialog
        result = messagebox.askyesno(
            "Send Text Message",
            f"Send '{message_content}' to {recipient}?\\n\\nThis will open Google Voice in your browser.",
            icon='question'
        )
        
        if result:
            self.send_text_message(recipient, message_content)
        
        return True
        
    def send_text_message(self, recipient, message_content):
        """Send text message via Google Voice"""
        try:
            # Open Google Voice with pre-filled message
            google_voice_url = f"https://voice.google.com/u/0/messages"
            webbrowser.open(google_voice_url)
            
            self.add_system_message(
                f"🚀 Opening Google Voice to send '{message_content}' to {recipient}\\n"
                f"📱 Please complete the sending process in your browser."
            )
            
            # You could add automation here using pyautogui if needed
            # For now, we're opening the browser for manual completion
            
        except Exception as e:
            self.add_system_message(f"❌ Error opening Google Voice: {str(e)}")
        
    def send_message_thread(self, message, screenshot=None, page_content=None):
        """Send message in separate thread"""
        try:
            # Add conversation context
            context = self.history_manager.get_context()
            full_message = context + message
            
            # Send to Claude
            response = self.claude_client.send_message(full_message, screenshot, page_content)
            
            # Process response
            self.parent.after(0, self.process_claude_response, response)
            
        except Exception as e:
            error_message = f"Error sending message: {str(e)}"
            self.parent.after(0, self.handle_error, error_message)
            
    def process_claude_response(self, response):
        """Process Claude's response with enhanced formatting"""
        try:
            # Extract text content
            text_content = ""
            tool_calls = []
            
            for content_block in response.content:
                if content_block.type == "text":
                    text_content += content_block.text
                elif content_block.type == "tool_use":
                    tool_calls.append(content_block)
            
            # Add Claude's text response to chat
            if text_content:
                self.add_assistant_message(text_content)
            
            # Execute tool calls if any
            if tool_calls:
                self.execute_tool_calls(tool_calls)
                
            # Update status
            if hasattr(self.parent.master.master, 'update_status'):
                self.parent.master.master.update_status("Response received", "online")
            
        except Exception as e:
            error_message = f"Error processing response: {str(e)}"
            self.handle_error(error_message)
            
    def execute_tool_calls(self, tool_calls):
        """Execute tool calls from Claude"""
        for tool_call in tool_calls:
            tool_name = tool_call.name
            tool_input = tool_call.input
            
            self.add_system_message(f"🔧 Executing {tool_name}: {tool_input}")
            
            try:
                if tool_name == "computer":
                    result = self.control_panel.computer_actions.execute_action(tool_input)
                elif tool_name == "file_operations":
                    result = self.control_panel.file_operations.execute_operation(tool_input)
                elif tool_name == "web_operations":
                    result = self.control_panel.web_operations.execute_operation(tool_input)
                else:
                    result = f"Unknown tool: {tool_name}"
                
                # Log the action
                self.control_panel.log_action(f"Tool: {tool_name} - {str(result)[:100]}")
                
                # Add result to chat
                self.add_system_message(f"✅ Result: {str(result)[:500]}")
                
            except Exception as e:
                error_msg = f"Tool execution error: {str(e)}"
                self.add_system_message(f"❌ {error_msg}")
                self.control_panel.log_action(error_msg)
                
    def add_user_message(self, message, has_screenshot=False):
        """Add a user message with modern styling"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.message_count += 1
        
        # Add to history
        self.history_manager.add_message("User", message, has_screenshot)
        
        # Add to display with modern formatting
        self.chat_display.config(state=tk.NORMAL)
        
        # Add spacing
        self.chat_display.insert(tk.END, "\n")
        
        # Add timestamp
        self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        
        # Add user name with modern styling
        self.chat_display.insert(tk.END, "You: ", 'user_name')
        
        # Add message content
        self.format_and_insert_message(message, 'user_msg')
        
        # Add screenshot indicator
        if has_screenshot:
            self.chat_display.insert(tk.END, " 📸", 'timestamp')
        
        self.chat_display.insert(tk.END, "\n")
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def add_assistant_message(self, message):
        """Add an assistant message with modern styling"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Add to history
        self.history_manager.add_message("Claude", message)
        
        # Add to display
        self.chat_display.config(state=tk.NORMAL)
        
        # Add spacing
        self.chat_display.insert(tk.END, "\n")
        
        # Add timestamp
        self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        
        # Add assistant name
        self.chat_display.insert(tk.END, "Claude: ", 'assistant_name')
        
        # Add message content with enhanced formatting
        self.format_and_insert_message(message, 'assistant_msg')
        
        self.chat_display.insert(tk.END, "\n")
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def add_system_message(self, message):
        """Add a system message with modern styling"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.chat_display.config(state=tk.NORMAL)
        
        # Add spacing
        self.chat_display.insert(tk.END, "\n")
        
        # Add timestamp and system indicator
        self.chat_display.insert(tk.END, f"[{timestamp}] ⚙️ ", 'timestamp')
        
        # Add message
        self.chat_display.insert(tk.END, f"{message}\n", 'system')
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def format_and_insert_message(self, message, default_tag):
        """Format and insert message with syntax highlighting"""
        # Simple formatting for code blocks
        if '```' in message:
            parts = message.split('```')
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    # Regular text
                    self.chat_display.insert(tk.END, part, default_tag)
                else:
                    # Code block
                    self.chat_display.insert(tk.END, part, 'code')
        else:
            # Check for links
            import re
            url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
            
            if re.search(url_pattern, message):
                # Split by URLs and format accordingly
                parts = re.split(f'({url_pattern})', message)
                for part in parts:
                    if re.match(url_pattern, part):
                        self.chat_display.insert(tk.END, part, 'link')
                    else:
                        self.chat_display.insert(tk.END, part, default_tag)
            else:
                # Regular message
                self.chat_display.insert(tk.END, message, default_tag)
        
    def handle_error(self, error_message):
        """Handle and display errors with modern styling"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n[{timestamp}] ❌ Error: {error_message}\n\n", 'error')
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
        # Update status
        if hasattr(self.parent.master.master, 'update_status'):
            self.parent.master.master.update_status("Error occurred", "error")
        
        # Log error
        self.control_panel.log_action(f"ERROR: {error_message}")
        
    def clear_chat_with_confirmation(self):
        """Clear chat with modern confirmation dialog"""
        result = messagebox.askyesno(
            "Clear Chat", 
            "This will clear the chat display and conversation history. Continue?",
            icon='question'
        )
        
        if result:
            self.clear_chat()
            
    def clear_chat(self):
        """Clear chat display and history"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        self.history_manager.clear_history()
        self.control_panel.log_action("Chat cleared")
        
        # Update status
        if hasattr(self.parent.master.master, 'update_status'):
            self.parent.master.master.update_status("Chat cleared", "online")
            
        # Reset message counter
        self.message_count = 0
        
    def export_chat(self):
        """Export chat history"""
        from tkinter import filedialog
        
        if not self.history_manager.history:
            messagebox.showinfo("No History", "No conversation history to export")
            return
            
        file_path = filedialog.asksaveasfilename(
            title="Export Chat History",
            defaultextension=".txt",
            filetypes=[
                ("Text Files", "*.txt"),
                ("JSON Files", "*.json"),
                ("All Files", "*.*")
            ]
        )
        
        if file_path:
            try:
                if file_path.endswith('.json'):
                    self.history_manager.export_history(file_path, 'json')
                else:
                    self.history_manager.export_history(file_path, 'text')
                    
                self.control_panel.log_action(f"Chat exported to: {file_path}")
                self.add_system_message(f"💾 Chat exported to {file_path}")
                
            except Exception as e:
                error_msg = f"Export failed: {str(e)}"
                self.control_panel.log_action(error_msg)
                messagebox.showerror("Export Error", error_msg)
                
    def load_conversation_history(self):
        """Load and display conversation history with modern styling"""
        try:
            if self.history_manager.history:
                self.chat_display.config(state=tk.NORMAL)
                self.chat_display.insert(tk.END, "═══ Previous Conversation History ═══\n\n", 'system')
                
                for msg in self.history_manager.history:
                    timestamp = datetime.fromisoformat(msg['timestamp']).strftime("%H:%M:%S")
                    sender = msg['sender']
                    message = msg['message']
                    has_screenshot = msg.get('has_screenshot', False)
                    
                    # Add timestamp
                    self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
                    
                    # Add sender name with appropriate styling
                    if sender.lower() == 'user':
                        self.chat_display.insert(tk.END, f"{sender}: ", 'user_name')
                        tag = 'user_msg'
                    elif sender.lower() == 'claude':
                        self.chat_display.insert(tk.END, f"{sender}: ", 'assistant_name')
                        tag = 'assistant_msg'
                    else:
                        self.chat_display.insert(tk.END, f"{sender}: ", 'system')
                        tag = 'system'
                    
                    # Add message content
                    self.format_and_insert_message(message, tag)
                    
                    # Add screenshot indicator
                    if has_screenshot:
                        self.chat_display.insert(tk.END, " 📸", 'timestamp')
                        
                    self.chat_display.insert(tk.END, "\n\n")
                
                self.chat_display.insert(tk.END, "═══ End of Previous History ═══\n\n", 'system')
                self.chat_display.config(state=tk.DISABLED)
                self.chat_display.see(tk.END)
                
        except Exception as e:
            error_msg = f"Error loading conversation history: {str(e)}"
            self.add_system_message(error_msg)
            
    def on_chat_click(self, event):
        """Handle clicks on chat content (e.g., links)"""
        # Get the index of the click
        index = self.chat_display.index(f"@{event.x},{event.y}")
        
        # Check if clicked on a link
        tags = self.chat_display.tag_names(index)
        if 'link' in tags:
            # Get the link text
            range_start = self.chat_display.tag_prevrange('link', index + '+1c')[0]
            range_end = self.chat_display.tag_nextrange('link', index)[1]
            link_text = self.chat_display.get(range_start, range_end)
            
            # Open the link
            try:
                webbrowser.open(link_text)
                self.add_system_message(f"🌐 Opened link: {link_text}")
            except Exception as e:
                self.add_system_message(f"❌ Failed to open link: {str(e)}")
                
    def on_chat_hover(self, event):
        """Handle mouse hover for interactive elements"""
        index = self.chat_display.index(f"@{event.x},{event.y}")
        tags = self.chat_display.tag_names(index)
        
        if 'link' in tags:
            self.chat_display.config(cursor='hand2')
        else:
            self.chat_display.config(cursor='arrow')
            
    def set_message_input(self, text):
        """Set text in message input (used by other components)"""
        self.message_input.delete('1.0', 'end')
        self.message_input.insert('1.0', text)
        self.message_input.focus()
        
    def get_message_input(self):
        """Get text from message input"""
        return self.message_input.get('1.0', 'end-1c').strip()
        
    def focus_input(self):
        """Focus on message input"""
        self.message_input.focus()

    def clear_placeholder(self, event=None):
        if self.message_input.get('1.0', 'end-1c').strip() == 'Type your message here...':
            self.message_input.delete('1.0', 'end')
            self.message_input.config(fg=self.theme.COLORS['chat_text'], bg=self.theme.COLORS['chat_bg'])

    def restore_placeholder(self, event=None):
        if not self.message_input.get('1.0', 'end-1c').strip():
            self.message_input.insert('1.0', 'Type your message here...')
            self.message_input.config(fg=self.theme.COLORS['text_tertiary'], bg=self.theme.COLORS['chat_bg'])
