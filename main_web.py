# Claude Computer Use GUI Application with Browser Functionality
import os
import base64
import io
import time
import json
import shutil
import threading
import requests
import webbrowser
from pathlib import Path
from PIL import Image, ImageTk
import pyautogui
from anthropic import Anthropic
from dotenv import load_dotenv
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox, simpledialog
from collections import deque
from datetime import datetime
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import html

# Load environment variables
load_dotenv()

class ClaudeGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Claude Computer Use Assistant")
        self.root.geometry("1400x900")  # Slightly larger to accommodate browser features
        self.root.configure(bg='#2b2b2b')
        
        # Initialize Claude client
        try:
            self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to initialize Claude client: {str(e)}")
            self.client = None
        
        # Configure pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        
        # Variables
        self.current_screenshot = None
        self.is_processing = False
        self.current_page_content = None
        self.current_page_source = None
        self.current_url = None
        
        # Message history management
        self.message_history = deque(maxlen=20)  # Keep last 20 messages
        self.history_file = Path("claude_chat_history.json")
        self.load_message_history()
        
        # Browser session
        self.browser_session = requests.Session()
        self.browser_session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        self.setup_ui()
        
    def load_message_history(self):
        """Load message history from file"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history_data = json.load(f)
                    # Convert list back to deque
                    self.message_history = deque(history_data.get('messages', []), maxlen=20)
                    self.add_action_log(f"Loaded {len(self.message_history)} messages from history")
            else:
                self.add_action_log("No previous message history found")
        except Exception as e:
            self.add_action_log(f"Error loading history: {str(e)}")
            self.message_history = deque(maxlen=20)
    
    def save_message_history(self):
        """Save message history to file"""
        try:
            history_data = {
                'last_updated': datetime.now().isoformat(),
                'messages': list(self.message_history)
            }
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            self.add_action_log(f"Error saving history: {str(e)}")
    
    def add_message_to_history(self, sender, message, has_screenshot=False):
        """Add a message to the conversation history"""
        message_entry = {
            'timestamp': datetime.now().isoformat(),
            'sender': sender,
            'message': message,
            'has_screenshot': has_screenshot
        }
        self.message_history.append(message_entry)
        self.save_message_history()
    
    def get_conversation_context(self):
        """Get conversation context for Claude"""
        context = "Previous conversation history (last 20 messages):\n\n"
        for i, msg in enumerate(self.message_history, 1):
            timestamp = datetime.fromisoformat(msg['timestamp']).strftime("%H:%M:%S")
            screenshot_note = " [with screenshot]" if msg.get('has_screenshot', False) else ""
            context += f"{i}. [{timestamp}] {msg['sender']}: {msg['message']}{screenshot_note}\n"
        context += "\nCurrent message:\n"
        return context
        
    def setup_ui(self):
        """Set up the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Claude Computer Use Assistant", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Left panel - Controls
        left_panel = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        left_panel.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Screenshot button
        self.screenshot_btn = ttk.Button(left_panel, text="📸 Take Screenshot", 
                                        command=self.take_screenshot_gui)
        self.screenshot_btn.grid(row=0, column=0, pady=5, sticky=(tk.W, tk.E))
        
        # Browser operations frame
        browser_frame = ttk.LabelFrame(left_panel, text="Browser Operations", padding="5")
        browser_frame.grid(row=1, column=0, pady=10, sticky=(tk.W, tk.E))
        
        # URL input
        url_input_frame = ttk.Frame(browser_frame)
        url_input_frame.grid(row=0, column=0, pady=5, sticky=(tk.W, tk.E))
        url_input_frame.columnconfigure(0, weight=1)
        
        ttk.Label(url_input_frame, text="URL:").grid(row=0, column=0, sticky=tk.W)
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(url_input_frame, textvariable=self.url_var, width=40)
        self.url_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        self.url_entry.bind('<Return>', self.load_page_gui)
        
        ttk.Button(url_input_frame, text="🌐 Load Page", 
                  command=self.load_page_gui).grid(row=1, column=1)
        
        # Browser action buttons
        ttk.Button(browser_frame, text="👁️ View Page Content", 
                  command=self.view_page_content).grid(row=1, column=0, pady=2, sticky=(tk.W, tk.E))
        ttk.Button(browser_frame, text="🔍 View Page Source", 
                  command=self.view_page_source).grid(row=2, column=0, pady=2, sticky=(tk.W, tk.E))
        ttk.Button(browser_frame, text="🚀 Open in Default Browser", 
                  command=self.open_in_browser).grid(row=3, column=0, pady=2, sticky=(tk.W, tk.E))
        
        # Current page info
        self.page_info_var = tk.StringVar(value="No page loaded")
        page_info_label = ttk.Label(browser_frame, textvariable=self.page_info_var, 
                                   font=('Arial', 9), foreground='blue')
        page_info_label.grid(row=4, column=0, pady=5, sticky=(tk.W, tk.E))
        
        # History management frame
        history_frame = ttk.LabelFrame(left_panel, text="Message History", padding="5")
        history_frame.grid(row=2, column=0, pady=10, sticky=(tk.W, tk.E))
        
        ttk.Button(history_frame, text="📜 View History", 
                  command=self.view_history).grid(row=0, column=0, pady=2, sticky=(tk.W, tk.E))
        ttk.Button(history_frame, text="🗑️ Clear History", 
                  command=self.clear_history).grid(row=1, column=0, pady=2, sticky=(tk.W, tk.E))
        ttk.Button(history_frame, text="💾 Export History", 
                  command=self.export_history).grid(row=2, column=0, pady=2, sticky=(tk.W, tk.E))
        
        # History status
        self.history_status = ttk.Label(history_frame, text=f"Messages: {len(self.message_history)}/20", 
                                       font=('Arial', 9))
        self.history_status.grid(row=3, column=0, pady=5)
        
        # File operations frame
        file_frame = ttk.LabelFrame(left_panel, text="File Operations", padding="5")
        file_frame.grid(row=3, column=0, pady=10, sticky=(tk.W, tk.E))
        
        ttk.Button(file_frame, text="📁 Browse Files", 
                  command=self.browse_files).grid(row=0, column=0, pady=2, sticky=(tk.W, tk.E))
        ttk.Button(file_frame, text="📄 Read File", 
                  command=self.read_file_gui).grid(row=1, column=0, pady=2, sticky=(tk.W, tk.E))
        ttk.Button(file_frame, text="✏️ Write File", 
                  command=self.write_file_gui).grid(row=2, column=0, pady=2, sticky=(tk.W, tk.E))
        ttk.Button(file_frame, text="📋 List Directory", 
                  command=self.list_directory_gui).grid(row=3, column=0, pady=2, sticky=(tk.W, tk.E))
        
        # Screenshot preview
        self.screenshot_frame = ttk.LabelFrame(left_panel, text="Screenshot Preview", padding="5")
        self.screenshot_frame.grid(row=4, column=0, pady=10, sticky=(tk.W, tk.E))
        
        self.screenshot_label = ttk.Label(self.screenshot_frame, text="No screenshot taken")
        self.screenshot_label.grid(row=0, column=0)
        
        # Status
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(left_panel, textvariable=self.status_var, 
                                font=('Arial', 10), foreground='green')
        status_label.grid(row=5, column=0, pady=5)
        
        # Center panel - Chat
        chat_frame = ttk.LabelFrame(main_frame, text="Chat with Claude", padding="10")
        chat_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        chat_frame.columnconfigure(0, weight=1)
        chat_frame.rowconfigure(0, weight=1)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, 
                                                     font=('Consolas', 10), 
                                                     bg='#1e1e1e', fg='white',
                                                     insertbackground='white')
        self.chat_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Input frame
        input_frame = ttk.Frame(chat_frame)
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        input_frame.columnconfigure(0, weight=1)
        
        # Message input
        self.message_var = tk.StringVar()
        self.message_entry = ttk.Entry(input_frame, textvariable=self.message_var, 
                                      font=('Arial', 11))
        self.message_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.message_entry.bind('<Return>', self.send_message)
        
        # Send button
        self.send_btn = ttk.Button(input_frame, text="Send", command=self.send_message)
        self.send_btn.grid(row=0, column=1)
        
        # Right panel - Actions Log
        right_panel = ttk.LabelFrame(main_frame, text="Actions Log", padding="10")
        right_panel.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(0, weight=1)
        
        # Actions log
        self.actions_log = scrolledtext.ScrolledText(right_panel, wrap=tk.WORD, 
                                                    font=('Consolas', 9),
                                                    bg='#f0f0f0', width=30)
        self.actions_log.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Clear log button
        ttk.Button(right_panel, text="Clear Log", 
                  command=self.clear_actions_log).grid(row=1, column=0, pady=5)
        
        # Configure left panel column weights
        left_panel.columnconfigure(0, weight=1)
        browser_frame.columnconfigure(0, weight=1)
        url_input_frame.columnconfigure(0, weight=1)
        history_frame.columnconfigure(0, weight=1)
        file_frame.columnconfigure(0, weight=1)
        
        # Initialize chat
        self.add_chat_message("System", "Claude Computer Use Assistant started! 🚀")
        self.add_chat_message("System", "Take a screenshot, load a web page, or ask me to help with tasks!")
        
        # Load previous chat history into display
        self.load_chat_history_to_display()
    
    # Browser functionality methods
    def load_page_gui(self, event=None):
        """Load a web page through GUI"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("URL Required", "Please enter a URL to load.")
            return
        
        # Add http:// if no protocol specified
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            self.url_var.set(url)
        
        # Load page in background thread
        threading.Thread(target=self.load_page, args=(url,), daemon=True).start()
    
    def load_page(self, url):
        """Load a web page and extract content"""
        try:
            self.root.after(0, lambda: self.status_var.set("Loading page..."))
            self.root.after(0, lambda: self.add_action_log(f"Loading page: {url}"))
            
            # Make request
            response = self.browser_session.get(url, timeout=10)
            response.raise_for_status()
            
            # Store raw HTML source
            self.current_page_source = response.text
            self.current_url = url
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract text content
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text_content = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text_content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text_content = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Limit content length for display
            if len(text_content) > 5000:
                text_content = text_content[:5000] + "\n\n[Content truncated - full content available via View Page Content]"
            
            self.current_page_content = text_content
            
            # Update UI
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            self.root.after(0, lambda: self.page_info_var.set(f"Loaded: {domain}"))
            self.root.after(0, lambda: self.add_action_log(f"Page loaded successfully: {domain}"))
            self.root.after(0, lambda: self.status_var.set("Page loaded"))
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to load page: {str(e)}"
            self.root.after(0, lambda: self.add_action_log(error_msg))
            self.root.after(0, lambda: self.status_var.set("Page load failed"))
            self.root.after(0, lambda: messagebox.showerror("Load Error", error_msg))
        except Exception as e:
            error_msg = f"Error processing page: {str(e)}"
            self.root.after(0, lambda: self.add_action_log(error_msg))
            self.root.after(0, lambda: self.status_var.set("Page processing failed"))
    
    def view_page_content(self):
        """View the current page content in a new window"""
        if not self.current_page_content:
            messagebox.showwarning("No Page", "No page content loaded. Please load a page first.")
            return
        
        # Create content viewer window
        content_window = tk.Toplevel(self.root)
        content_window.title(f"Page Content - {self.current_url}")
        content_window.geometry("800x600")
        content_window.configure(bg='#2b2b2b')
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(content_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        content_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, 
                                               font=('Consolas', 10), 
                                               bg='#f8f8f8', fg='black')
        content_text.pack(fill=tk.BOTH, expand=True)
        
        # Insert content
        content_text.insert(tk.END, f"URL: {self.current_url}\n")
        content_text.insert(tk.END, f"Loaded: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        content_text.insert(tk.END, "=" * 80 + "\n\n")
        content_text.insert(tk.END, self.current_page_content)
        
        content_text.config(state=tk.DISABLED)
        
        # Add save button
        save_btn = ttk.Button(content_window, text="💾 Save Content", 
                             command=lambda: self.save_page_content("content"))
        save_btn.pack(pady=5)
        
        self.add_action_log("Opened page content viewer")
    
    def view_page_source(self):
        """View the current page source in a new window"""
        if not self.current_page_source:
            messagebox.showwarning("No Page", "No page source loaded. Please load a page first.")
            return
        
        # Create source viewer window
        source_window = tk.Toplevel(self.root)
        source_window.title(f"Page Source - {self.current_url}")
        source_window.geometry("900x700")
        source_window.configure(bg='#2b2b2b')
        
        # Create text widget with scrollbar
        text_frame = ttk.Frame(source_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        source_text = scrolledtext.ScrolledText(text_frame, wrap=tk.NONE, 
                                              font=('Consolas', 9), 
                                              bg='#1e1e1e', fg='#f0f0f0')
        source_text.pack(fill=tk.BOTH, expand=True)
        
        # Insert source with syntax highlighting (basic)
        source_text.insert(tk.END, f"<!-- URL: {self.current_url} -->\n")
        source_text.insert(tk.END, f"<!-- Loaded: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -->\n\n")
        source_text.insert(tk.END, self.current_page_source)
        
        source_text.config(state=tk.DISABLED)
        
        # Add save button
        save_btn = ttk.Button(source_window, text="💾 Save Source", 
                             command=lambda: self.save_page_content("source"))
        save_btn.pack(pady=5)
        
        self.add_action_log("Opened page source viewer")
    
    def save_page_content(self, content_type):
        """Save page content or source to file"""
        if content_type == "content" and not self.current_page_content:
            messagebox.showwarning("No Content", "No page content to save.")
            return
        elif content_type == "source" and not self.current_page_source:
            messagebox.showwarning("No Source", "No page source to save.")
            return
        
        # Get save location
        if content_type == "content":
            filename = filedialog.asksaveasfilename(
                title="Save Page Content",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            content_to_save = f"URL: {self.current_url}\nLoaded: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{'='*80}\n\n{self.current_page_content}"
        else:
            filename = filedialog.asksaveasfilename(
                title="Save Page Source",
                defaultextension=".html",
                filetypes=[("HTML files", "*.html"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            content_to_save = f"<!-- URL: {self.current_url} -->\n<!-- Loaded: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -->\n\n{self.current_page_source}"
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content_to_save)
                self.add_action_log(f"Saved page {content_type} to: {filename}")
                messagebox.showinfo("Saved", f"Page {content_type} saved to: {filename}")
            except Exception as e:
                error_msg = f"Error saving file: {str(e)}"
                self.add_action_log(error_msg)
                messagebox.showerror("Save Error", error_msg)
    
    def open_in_browser(self):
        """Open current URL in default browser"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("URL Required", "Please enter a URL first.")
            return
        
        # Add http:// if no protocol specified
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        try:
            webbrowser.open(url)
            self.add_action_log(f"Opened in browser: {url}")
        except Exception as e:
            error_msg = f"Failed to open browser: {str(e)}"
            self.add_action_log(error_msg)
            messagebox.showerror("Browser Error", error_msg)
    
    def load_chat_history_to_display(self):
        """Load previous chat history into the display"""
        if self.message_history:
            self.add_chat_message("System", f"--- Loaded {len(self.message_history)} previous messages ---")
            for msg in list(self.message_history)[-5:]:  # Show last 5 messages
                timestamp = datetime.fromisoformat(msg['timestamp']).strftime("%H:%M:%S")
                screenshot_note = " 📸" if msg.get('has_screenshot', False) else ""
                self.add_chat_message(f"{msg['sender']}{screenshot_note}", msg['message'])
    
    def view_history(self):
        """View conversation history in a new window"""
        history_window = tk.Toplevel(self.root)
        history_window.title("Conversation History")
        history_window.geometry("600x400")
        history_window.configure(bg='#2b2b2b')
        
        # History display
        history_text = scrolledtext.ScrolledText(history_window, wrap=tk.WORD, 
                                                font=('Consolas', 10), 
                                                bg='#1e1e1e', fg='white')
        history_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Populate history
        if self.message_history:
            for i, msg in enumerate(self.message_history, 1):
                timestamp = datetime.fromisoformat(msg['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
                screenshot_note = " [with screenshot]" if msg.get('has_screenshot', False) else ""
                history_text.insert(tk.END, f"{i}. [{timestamp}] {msg['sender']}: {msg['message']}{screenshot_note}\n\n")
        else:
            history_text.insert(tk.END, "No conversation history available.")
        
        history_text.config(state=tk.DISABLED)
    
    def clear_history(self):
        """Clear conversation history"""
        if messagebox.askyesno("Clear History", "Are you sure you want to clear the conversation history?"):
            self.message_history.clear()
            self.save_message_history()
            self.update_history_status()
            self.add_action_log("Conversation history cleared")
    
    def export_history(self):
        """Export conversation history to a file"""
        if not self.message_history:
            messagebox.showinfo("Export History", "No conversation history to export.")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Export Conversation History",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("Text files", "*.txt")]
        )
        
        if filename:
            try:
                if filename.endswith('.json'):
                    # Export as JSON
                    export_data = {
                        'exported_at': datetime.now().isoformat(),
                        'message_count': len(self.message_history),
                        'messages': list(self.message_history)
                    }
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(export_data, f, indent=2, ensure_ascii=False)
                else:
                    # Export as text
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"Claude Computer Use Assistant - Conversation History\n")
                        f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write(f"Messages: {len(self.message_history)}\n\n")
                        f.write("=" * 50 + "\n\n")
                        
                        for i, msg in enumerate(self.message_history, 1):
                            timestamp = datetime.fromisoformat(msg['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
                            screenshot_note = " [with screenshot]" if msg.get('has_screenshot', False) else ""
                            f.write(f"{i}. [{timestamp}] {msg['sender']}: {msg['message']}{screenshot_note}\n\n")
                
                self.add_action_log(f"History exported to: {filename}")
                messagebox.showinfo("Export Complete", f"History exported to: {filename}")
                
            except Exception as e:
                self.add_action_log(f"Export error: {str(e)}")
                messagebox.showerror("Export Error", f"Failed to export history: {str(e)}")
    
    def update_history_status(self):
        """Update the history status label"""
        self.history_status.config(text=f"Messages: {len(self.message_history)}/20")
        
    def add_chat_message(self, sender, message):
        """Add a message to the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        # Add timestamp
        timestamp = time.strftime("%H:%M:%S")
        
        # Color coding
        if sender == "You":
            color = "#4CAF50"  # Green
        elif sender == "Claude":
            color = "#2196F3"  # Blue
        else:
            color = "#FF9800"  # Orange for system messages
        
        # Insert message
        self.chat_display.insert(tk.END, f"[{timestamp}] {sender}: ", )
        self.chat_display.insert(tk.END, f"{message}\n\n")
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
        
        # Add to history (but not system messages)
        if sender not in ["System"]:
            self.add_message_to_history(sender, message, self.current_screenshot is not None)
            self.update_history_status()
        
    def add_action_log(self, action):
        """Add an action to the actions log"""
        self.actions_log.config(state=tk.NORMAL)
        timestamp = time.strftime("%H:%M:%S")
        self.actions_log.insert(tk.END, f"[{timestamp}] {action}\n")

        def clear_actions_log(self):
            """Clear the actions log"""
        self.actions_log.config(state=tk.NORMAL)
        self.actions_log.delete(1.0, tk.END)
        self.actions_log.config(state=tk.DISABLED)
        
    def take_screenshot_gui(self):
        """Take a screenshot and display preview"""
        try:
            self.status_var.set("Taking screenshot...")
            self.root.update()
            
            # Take screenshot
            screenshot = pyautogui.screenshot()
            self.current_screenshot = screenshot
            
            # Create thumbnail for preview
            thumbnail = screenshot.copy()
            thumbnail.thumbnail((200, 150), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(thumbnail)
            
            # Update preview
            self.screenshot_label.configure(image=photo)
            self.screenshot_label.image = photo  # Keep a reference
            
            self.add_action_log("Screenshot taken")
            self.status_var.set("Screenshot ready")
            
        except Exception as e:
            self.add_action_log(f"Screenshot error: {str(e)}")
            self.status_var.set("Screenshot failed")
            
    def send_message(self, event=None):
        """Send a message to Claude"""
        if self.is_processing:
            return
            
        message = self.message_var.get().strip()
        if not message:
            return
            
        if not self.client:
            messagebox.showerror("Error", "Claude client not initialized. Check your API key.")
            return
            
        self.message_var.set("")
        self.add_chat_message("You", message)
        
        # Process in background thread
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()
        
    def process_message(self, message):
        """Process message with Claude in background thread"""
        self.is_processing = True
        self.root.after(0, lambda: self.status_var.set("Processing..."))
        
        try:
            # Prepare message for Claude with context
            context = self.get_conversation_context()
            full_message = f"{context}{message}"
            
            # Add page context if available
            if self.current_page_content:
                full_message += f"\n\nCurrent page content:\n{self.current_page_content[:2000]}..."
            
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": full_message}
                    ]
                }
            ]
            
            # Add screenshot if available
            if self.current_screenshot:
                buffer = io.BytesIO()
                self.current_screenshot.save(buffer, format='PNG')
                img_str = base64.b64encode(buffer.getvalue()).decode()
                
                messages[0]["content"].append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": img_str
                    }
                })
            
            # Send to Claude
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=messages,
                tools=[
                    {
                        "name": "computer",
                        "description": "Use a computer to perform actions",
                        "input_schema": {
                            "type": "object",
                            "properties": {
                                "action": {
                                    "type": "string",
                                    "enum": ["click", "type", "scroll", "key", "move", "screenshot"]
                                },
                                "coordinate": {
                                    "type": "array",
                                    "items": {"type": "integer"},
                                    "description": "[x, y] coordinates for click/move actions"
                                },
                                "text": {
                                    "type": "string",
                                    "description": "Text to type"
                                },
                                "key": {
                                    "type": "string",
                                    "description": "Key to press"
                                },
                                "clicks": {
                                    "type": "integer",
                                    "description": "Number of scroll clicks"
                                }
                            },
                            "required": ["action"]
                        }
                    },
                    {
                        "name": "file_operations",
                        "description": "Perform file operations",
                        "input_schema": {
                            "type": "object",
                            "properties": {
                                "operation": {
                                    "type": "string",
                                    "enum": ["read", "write", "list", "delete", "copy", "move"]
                                },
                                "file_path": {"type": "string"},
                                "content": {"type": "string"},
                                "dest_path": {"type": "string"},
                                "mode": {"type": "string", "enum": ["w", "a"]}
                            },
                            "required": ["operation", "file_path"]
                        }
                    },
                    {
                        "name": "web_operations",
                        "description": "Perform web operations",
                        "input_schema": {
                            "type": "object",
                            "properties": {
                                "operation": {
                                    "type": "string",
                                    "enum": ["load_page", "get_content", "search_elements", "extract_links"]
                                },
                                "url": {"type": "string"},
                                "selector": {"type": "string"},
                                "search_text": {"type": "string"}
                            },
                            "required": ["operation"]
                        }
                    }
                ]
            )
            
            # Display Claude's response
            claude_text = response.content[0].text if response.content else "No response"
            self.root.after(0, lambda: self.add_chat_message("Claude", claude_text))
            
            # Execute any tool calls
            if response.stop_reason == "tool_use":
                for tool_call in response.content:
                    if tool_call.type == "tool_use":
                        self.root.after(0, lambda tc=tool_call: self.execute_tool_call(tc))
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.root.after(0, lambda: self.add_chat_message("System", error_msg))
        
        finally:
            self.is_processing = False
            self.root.after(0, lambda: self.status_var.set("Ready"))
            
    def execute_tool_call(self, tool_call):
        """Execute a tool call from Claude"""
        try:
            if tool_call.name == "computer":
                result = self.execute_computer_action(tool_call.input)
            elif tool_call.name == "file_operations":
                result = self.execute_file_operation(tool_call.input)
            elif tool_call.name == "web_operations":
                result = self.execute_web_operation(tool_call.input)
            else:
                result = f"Unknown tool: {tool_call.name}"
            
            self.add_action_log(result)
            
        except Exception as e:
            error_msg = f"Tool execution error: {str(e)}"
            self.add_action_log(error_msg)
            
    def execute_computer_action(self, action_data):
        """Execute computer actions"""
        action_type = action_data.get("action")
        
        if action_type == "click":
            x, y = action_data.get("coordinate", [0, 0])
            pyautogui.click(x, y)
            return f"Clicked at ({x}, {y})"
        
        elif action_type == "type":
            text = action_data.get("text", "")
            pyautogui.write(text)
            return f"Typed: {text}"
        
        elif action_type == "scroll":
            clicks = action_data.get("clicks", 3)
            pyautogui.scroll(clicks)
            return f"Scrolled {clicks} clicks"
        
        elif action_type == "key":
            key = action_data.get("key")
            pyautogui.press(key)
            return f"Pressed key: {key}"
        
        elif action_type == "move":
            x, y = action_data.get("coordinate", [0, 0])
            pyautogui.moveTo(x, y)
            return f"Moved mouse to ({x}, {y})"
        
        elif action_type == "screenshot":
            self.take_screenshot_gui()
            return "Screenshot taken"
        
        else:
            return f"Unknown action: {action_type}"
    
    def execute_web_operation(self, web_data):
        """Execute web operations"""
        operation = web_data.get("operation")
        
        if operation == "load_page":
            url = web_data.get("url")
            if url:
                self.url_var.set(url)
                threading.Thread(target=self.load_page, args=(url,), daemon=True).start()
                return f"Loading page: {url}"
            else:
                return "No URL provided for load_page operation"
        
        elif operation == "get_content":
            if self.current_page_content:
                return f"Current page content available ({len(self.current_page_content)} characters)"
            else:
                return "No page content available"
        
        elif operation == "search_elements":
            search_text = web_data.get("search_text")
            if self.current_page_content and search_text:
                if search_text.lower() in self.current_page_content.lower():
                    return f"Found '{search_text}' in current page content"
                else:
                    return f"'{search_text}' not found in current page content"
            else:
                return "No page content or search text provided"
        
        elif operation == "extract_links":
            if self.current_page_source:
                soup = BeautifulSoup(self.current_page_source, 'html.parser')
                links = []
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    text = link.get_text(strip=True)
                    if href.startswith('http') or href.startswith('/'):
                        links.append(f"{text}: {href}")
                return f"Found {len(links)} links: {links[:10]}"  # Return first 10 links
            else:
                return "No page source available"
        
        else:
            return f"Unknown web operation: {operation}"
            
    def execute_file_operation(self, file_data):
        """Execute file operations"""
        operation = file_data.get("operation")
        file_path = file_data.get("file_path")
        
        if operation == "read":
            return self.read_file(file_path)
        elif operation == "write":
            content = file_data.get("content", "")
            mode = file_data.get("mode", "w")
            return self.write_file(file_path, content, mode)
        elif operation == "list":
            return self.list_directory(file_path)
        elif operation == "delete":
            return self.delete_file(file_path)
        elif operation == "copy":
            dest_path = file_data.get("dest_path")
            return self.copy_file(file_path, dest_path)
        elif operation == "move":
            dest_path = file_data.get("dest_path")
            return self.move_file(file_path, dest_path)
        else:
            return f"Unknown file operation: {operation}"
    
    # File operation methods
    def read_file(self, file_path):
        """Read content from a file"""
        try:
            path = Path(file_path)
            if not path.exists():
                return f"File not found: {file_path}"
            
            if path.is_dir():
                return f"Path is a directory: {file_path}"
            
            # Handle different file types
            if path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                return f"Image file detected: {file_path}"
            elif path.suffix.lower() in ['.exe', '.dll', '.bin']:
                return f"Binary file detected: {file_path}"
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Show content in a new window if it's long
            if len(content) > 1000:
                self.show_file_content(file_path, content)
                return f"Read {len(content)} characters from {file_path} - displayed in new window"
            else:
                return f"File content ({len(content)} chars): {content[:500]}..."
            
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def show_file_content(self, file_path, content):
        """Show file content in a new window"""
        def create_window():
            content_window = tk.Toplevel(self.root)
            content_window.title(f"File Content - {Path(file_path).name}")
            content_window.geometry("700x500")
            content_window.configure(bg='#2b2b2b')
            
            # Create text widget with scrollbar
            text_frame = ttk.Frame(content_window)
            text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            content_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, 
                                                   font=('Consolas', 10), 
                                                   bg='#f8f8f8', fg='black')
            content_text.pack(fill=tk.BOTH, expand=True)
            
            # Insert content
            content_text.insert(tk.END, f"File: {file_path}\n")
            content_text.insert(tk.END, f"Size: {len(content)} characters\n")
            content_text.insert(tk.END, "=" * 50 + "\n\n")
            content_text.insert(tk.END, content)
            
            content_text.config(state=tk.DISABLED)
        
        # Schedule window creation on main thread
        self.root.after(0, create_window)
    
    def write_file(self, file_path, content, mode='w'):
        """Write content to a file"""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, mode, encoding='utf-8') as f:
                f.write(content)
            return f"Content written to: {file_path} ({len(content)} characters)"
            
        except Exception as e:
            return f"Error writing file: {str(e)}"
    
    def list_directory(self, dir_path="."):
        """List contents of a directory"""
        try:
            path = Path(dir_path)
            if not path.exists():
                return f"Directory not found: {dir_path}"
            
            if not path.is_dir():
                return f"Path is not a directory: {dir_path}"
            
            items = []
            for item in path.iterdir():
                if item.is_dir():
                    items.append(f"[DIR] {item.name}")
                else:
                    size = item.stat().st_size
                    items.append(f"[FILE] {item.name} ({size} bytes)")
            
            # Show in new window if many items
            if len(items) > 20:
                self.show_directory_listing(dir_path, items)
                return f"Listed {len(items)} items in {dir_path} - displayed in new window"
            else:
                return f"Directory contents ({len(items)} items):\n" + "\n".join(items[:20])
            
        except Exception as e:
            return f"Error listing directory: {str(e)}"
    
    def show_directory_listing(self, dir_path, items):
        """Show directory listing in a new window"""
        def create_window():
            listing_window = tk.Toplevel(self.root)
            listing_window.title(f"Directory Listing - {dir_path}")
            listing_window.geometry("600x400")
            listing_window.configure(bg='#2b2b2b')
            
            # Create text widget with scrollbar
            text_frame = ttk.Frame(listing_window)
            text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            listing_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, 
                                                   font=('Consolas', 10), 
                                                   bg='#f8f8f8', fg='black')
            listing_text.pack(fill=tk.BOTH, expand=True)
            
            # Insert listing
            listing_text.insert(tk.END, f"Directory: {dir_path}\n")
            listing_text.insert(tk.END, f"Items: {len(items)}\n")
            listing_text.insert(tk.END, "=" * 50 + "\n\n")
            
            for item in items:
                listing_text.insert(tk.END, f"{item}\n")
            
            listing_text.config(state=tk.DISABLED)
        
        # Schedule window creation on main thread
        self.root.after(0, create_window)
    
    def delete_file(self, file_path):
        """Delete a file"""
        try:
            path = Path(file_path)
            if not path.exists():
                return f"File not found: {file_path}"
            
            if path.is_dir():
                shutil.rmtree(path)
                return f"Directory deleted: {file_path}"
            else:
                path.unlink()
                return f"File deleted: {file_path}"
                
        except Exception as e:
            return f"Error deleting file: {str(e)}"
    
    def copy_file(self, source_path, dest_path):
        """Copy a file"""
        try:
            source = Path(source_path)
            dest = Path(dest_path)
            
            if not source.exists():
                return f"Source file not found: {source_path}"
            
            if source.is_dir():
                shutil.copytree(source, dest)
                return f"Directory copied: {source_path} -> {dest_path}"
            else:
                shutil.copy2(source, dest)
                return f"File copied: {source_path} -> {dest_path}"
                
        except Exception as e:
            return f"Error copying file: {str(e)}"
    
    def move_file(self, source_path, dest_path):
        """Move a file"""
        try:
            source = Path(source_path)
            dest = Path(dest_path)
            
            if not source.exists():
                return f"Source file not found: {source_path}"
            
            shutil.move(str(source), str(dest))
            return f"File moved: {source_path} -> {dest_path}"
            
        except Exception as e:
            return f"Error moving file: {str(e)}"
    
    # GUI file operation methods
    def browse_files(self):
        """Open file browser"""
        filename = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("All files", "*.*"), ("Text files", "*.txt"), 
                      ("Python files", "*.py"), ("JSON files", "*.json"),
                      ("HTML files", "*.html"), ("CSS files", "*.css"),
                      ("JavaScript files", "*.js")]
        )
        if filename:
            self.add_action_log(f"Selected file: {filename}")
            # Optionally read the file
            if messagebox.askyesno("Read File", f"Read the selected file?\n{filename}"):
                result = self.read_file(filename)
                self.add_action_log(result)
            
    def read_file_gui(self):
        """Read file through GUI"""
        filename = filedialog.askopenfilename(
            title="Select file to read",
            filetypes=[("Text files", "*.txt"), ("Python files", "*.py"),
                      ("JSON files", "*.json"), ("HTML files", "*.html"),
                      ("All files", "*.*")]
        )
        if filename:
            result = self.read_file(filename)
            self.add_action_log(result)
            
    def write_file_gui(self):
        """Write file through GUI"""
        filename = filedialog.asksaveasfilename(
            title="Select file to write",
            filetypes=[("Text files", "*.txt"), ("Python files", "*.py"),
                      ("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            content = simpledialog.askstring("File Content", "Enter content to write:", 
                                           initialvalue="# Enter your content here")
            if content is not None:  # User didn't cancel
                result = self.write_file(filename, content)
                self.add_action_log(result)
                
    def list_directory_gui(self):
        """List directory through GUI"""
        dirname = filedialog.askdirectory(title="Select directory to list")
        if dirname:
            result = self.list_directory(dirname)
            self.add_action_log(result)
    
    def run(self):
        """Start the GUI application"""
        self.add_action_log("Starting Claude Computer Use Assistant with Web Features")
        self.root.mainloop()

if __name__ == "__main__":
    app = ClaudeGUI()
    app.run()