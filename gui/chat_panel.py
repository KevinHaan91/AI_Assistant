import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from datetime import datetime
from config import Config

class ChatPanel:
    def __init__(self, parent, claude_client, control_panel, history_manager):
        self.parent = parent
        self.claude_client = claude_client
        self.control_panel = control_panel
        self.history_manager = history_manager
        
        # Create main chat frame
        self.chat_frame = ttk.Frame(parent)
        self.chat_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create chat interface
        self.create_chat_interface()
        
        # Load conversation history
        self.load_conversation_history()
        
    def create_chat_interface(self):
        """Create the chat interface"""
        # Chat display area
        chat_display_frame = ttk.Frame(self.chat_frame)
        chat_display_frame.pack(fill='both', expand=True, pady=(0, 5))
        
        # Chat history
        chat_label = ttk.Label(chat_display_frame, text="Conversation History:")
        chat_label.pack(anchor='w')
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_display_frame,
            height=20,
            wrap=tk.WORD,
            bg=Config.CHAT_BG,
            fg=Config.CHAT_FG,
            insertbackground='white',
            font=('Consolas', 10)
        )
        self.chat_display.pack(fill='both', expand=True)
        
        # Configure text tags for styling
        self.chat_display.tag_config('user', foreground='#88cc88', font=('Consolas', 10, 'bold'))
        self.chat_display.tag_config('claude', foreground='#88ccff', font=('Consolas', 10, 'bold'))
        self.chat_display.tag_config('system', foreground='#cccccc', font=('Consolas', 9, 'italic'))
        self.chat_display.tag_config('timestamp', foreground='#888888', font=('Consolas', 8))
        self.chat_display.tag_config('error', foreground='#ff6666', font=('Consolas', 10, 'bold'))
        
        # Input area
        input_frame = ttk.Frame(self.chat_frame)
        input_frame.pack(fill='x', pady=(5, 0))
        
        # Message input
        input_label = ttk.Label(input_frame, text="Your message:")
        input_label.pack(anchor='w')
        
        # Input text area
        input_text_frame = ttk.Frame(input_frame)
        input_text_frame.pack(fill='x', pady=(2, 5))
        
        self.message_input = scrolledtext.ScrolledText(
            input_text_frame,
            height=4,
            wrap=tk.WORD,
            font=('Consolas', 10)
        )
        self.message_input.pack(fill='both', expand=True)
        
        # Bind Enter key (Ctrl+Enter to send, Enter for new line)
        self.message_input.bind('<Control-Return>', self.send_message_event)
        
        # Control buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill='x', pady=(5, 0))
        
        # Send button
        self.send_button = ttk.Button(button_frame, text="Send Message (Ctrl+Enter)", command=self.send_message)
        self.send_button.pack(side='left', padx=(0, 5))
        
        # Include screenshot checkbox
        self.include_screenshot_var = tk.BooleanVar(value=False)
        self.screenshot_checkbox = ttk.Checkbutton(
            button_frame,
            text="Include Screenshot",
            variable=self.include_screenshot_var
        )
        self.screenshot_checkbox.pack(side='left', padx=5)
        
        # Include page content checkbox
        self.include_page_content_var = tk.BooleanVar(value=False)
        self.page_content_checkbox = ttk.Checkbutton(
            button_frame,
            text="Include Page Content",
            variable=self.include_page_content_var
        )
        self.page_content_checkbox.pack(side='left', padx=5)
        
        # Clear chat button
        self.clear_button = ttk.Button(button_frame, text="Clear Chat", command=self.clear_chat)
        self.clear_button.pack(side='right', padx=(5, 0))
        
        # Export chat button
        self.export_button = ttk.Button(button_frame, text="Export Chat", command=self.export_chat)
        self.export_button.pack(side='right', padx=5)
        
        # Status label
        self.status_label = ttk.Label(input_frame, text="Ready", foreground='green')
        self.status_label.pack(anchor='w', pady=(5, 0))
        
    def send_message_event(self, event):
        """Handle Enter key press"""
        self.send_message()
        return 'break'  # Prevent default Enter behavior
        
    def send_message(self):
        """Send message to Claude"""
        message = self.message_input.get(1.0, tk.END).strip()
        if not message:
            messagebox.showwarning("Empty Message", "Please enter a message")
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
        
        # Clear input
        self.message_input.delete(1.0, tk.END)
        
        # Add user message to chat
        self.add_message("User", message, has_screenshot=screenshot is not None)
        
        # Update status
        self.update_status("Sending message...", 'orange')
        
        # Send in separate thread
        threading.Thread(target=self.send_message_thread, args=(message, screenshot, page_content), daemon=True).start()
        
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
        """Process Claude's response"""
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
                self.add_message("Claude", text_content)
            
            # Execute tool calls if any
            if tool_calls:
                self.execute_tool_calls(tool_calls)
                
            # Update status
            self.update_status("Response received", 'green')
            
        except Exception as e:
            error_message = f"Error processing response: {str(e)}"
            self.handle_error(error_message)
            
    def execute_tool_calls(self, tool_calls):
        """Execute tool calls from Claude"""
        for tool_call in tool_calls:
            tool_name = tool_call.name
            tool_input = tool_call.input
            
            self.add_system_message(f"Executing {tool_name}: {tool_input}")
            
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
                self.add_system_message(f"Result: {str(result)[:500]}")
                
            except Exception as e:
                error_msg = f"Tool execution error: {str(e)}"
                self.add_system_message(error_msg)
                self.control_panel.log_action(error_msg)
                
    def add_message(self, sender, message, has_screenshot=False):
        """Add a message to the chat display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Add to history
        self.history_manager.add_message(sender, message, has_screenshot)
        
        # Add to display
        self.chat_display.config(state=tk.NORMAL)
        
        # Insert timestamp
        self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        
        # Insert sender name
        if sender.lower() == 'user':
            self.chat_display.insert(tk.END, f"{sender}: ", 'user')
        elif sender.lower() == 'claude':
            self.chat_display.insert(tk.END, f"{sender}: ", 'claude')
        else:
            self.chat_display.insert(tk.END, f"{sender}: ", 'system')
        
        # Insert message
        self.chat_display.insert(tk.END, message)
        
        # Add screenshot indicator
        if has_screenshot:
            self.chat_display.insert(tk.END, " [📷]", 'system')
        
        self.chat_display.insert(tk.END, "\n\n")
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def add_system_message(self, message):
        """Add a system message to the chat"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        self.chat_display.insert(tk.END, "System: ", 'system')
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
    def handle_error(self, error_message):
        """Handle and display errors"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
        self.chat_display.insert(tk.END, "Error: ", 'error')
        self.chat_display.insert(tk.END, f"{error_message}\n\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
        # Update status
        self.update_status("Error occurred", 'red')
        
        # Log error
        self.control_panel.log_action(f"ERROR: {error_message}")
        
    def update_status(self, message, color='black'):
        """Update status label"""
        self.status_label.config(text=message, foreground=color)
        
    def clear_chat(self):
        """Clear chat display and history"""
        result = messagebox.askyesno(
            "Clear Chat", 
            "This will clear the chat display and conversation history. Continue?"
        )
        
        if result:
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete(1.0, tk.END)
            self.chat_display.config(state=tk.DISABLED)
            
            self.history_manager.clear_history()
            self.control_panel.log_action("Chat cleared")
            self.update_status("Chat cleared", 'green')
            
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
                messagebox.showinfo("Success", f"Chat exported to {file_path}")
                
            except Exception as e:
                error_msg = f"Export failed: {str(e)}"
                self.control_panel.log_action(error_msg)
                messagebox.showerror("Export Error", error_msg)
                
    def load_conversation_history(self):
        """Load and display conversation history"""
        try:
            if self.history_manager.history:
                self.chat_display.config(state=tk.NORMAL)
                self.chat_display.insert(tk.END, "=== Previous Conversation History ===\n\n", 'system')
                
                for msg in self.history_manager.history:
                    timestamp = datetime.fromisoformat(msg['timestamp']).strftime("%H:%M:%S")
                    sender = msg['sender']
                    message = msg['message']
                    has_screenshot = msg.get('has_screenshot', False)
                    
                    # Insert timestamp
                    self.chat_display.insert(tk.END, f"[{timestamp}] ", 'timestamp')
                    
                    # Insert sender name with appropriate styling
                    if sender.lower() == 'user':
                        self.chat_display.insert(tk.END, f"{sender}: ", 'user')
                    elif sender.lower() == 'claude':
                        self.chat_display.insert(tk.END, f"{sender}: ", 'claude')
                    else:
                        self.chat_display.insert(tk.END, f"{sender}: ", 'system')
                    
                    # Insert message
                    self.chat_display.insert(tk.END, message)
                    
                    # Add screenshot indicator
                    if has_screenshot:
                        self.chat_display.insert(tk.END, " [📷]", 'system')
                        
                    self.chat_display.insert(tk.END, "\n\n")
                
                self.chat_display.insert(tk.END, "=== End of Previous History ===\n\n", 'system')
                self.chat_display.config(state=tk.DISABLED)
                self.chat_display.see(tk.END)
                
        except Exception as e:
            error_msg = f"Error loading conversation history: {str(e)}"
            self.add_system_message(error_msg)
            
    def set_message_input(self, text):
        """Set text in message input (used by other components)"""
        self.message_input.delete(1.0, tk.END)
        self.message_input.insert(1.0, text)
        self.message_input.focus()
        
    def get_message_input(self):
        """Get text from message input"""
        return self.message_input.get(1.0, tk.END).strip()
        
    def focus_input(self):
        """Focus on message input"""
        self.message_input.focus()
