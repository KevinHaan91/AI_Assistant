import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import scrolledtext
import threading
from pathlib import Path
from config import Config
from utils.screenshot import ScreenshotManager
from utils.logging import ActionLogger

class ControlPanel:
    def __init__(self, parent, claude_client, computer_actions, file_operations, web_operations, history_manager):
        self.parent = parent
        self.claude_client = claude_client
        self.computer_actions = computer_actions
        self.file_operations = file_operations
        self.web_operations = web_operations
        self.history_manager = history_manager
        self.screenshot_manager = ScreenshotManager()
        
        # Create main control frame
        self.control_frame = ttk.Frame(parent)
        self.control_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.control_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.create_screenshot_tab()
        self.create_file_operations_tab()
        self.create_web_operations_tab()
        self.create_action_log_tab()
        
        # Initialize logger
        self.logger = ActionLogger(self.log_text)
        
    def create_screenshot_tab(self):
        """Create screenshot control tab"""
        screenshot_frame = ttk.Frame(self.notebook)
        self.notebook.add(screenshot_frame, text='Screenshot')
        
        # Screenshot controls
        controls_frame = ttk.Frame(screenshot_frame)
        controls_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(controls_frame, text="Take Screenshot", 
                  command=self.take_screenshot).pack(side='left', padx=5)
        ttk.Button(controls_frame, text="Auto Screenshot", 
                  command=self.toggle_auto_screenshot).pack(side='left', padx=5)
        
        # Screenshot display
        self.screenshot_frame = ttk.Frame(screenshot_frame)
        self.screenshot_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Screenshot info
        self.screenshot_info = ttk.Label(self.screenshot_frame, text="No screenshot taken")
        self.screenshot_info.pack(pady=5)
        
        # Screenshot thumbnail
        self.screenshot_label = ttk.Label(self.screenshot_frame)
        self.screenshot_label.pack(pady=5)
        
        # Auto screenshot variables
        self.auto_screenshot = False
        self.auto_screenshot_thread = None
        
    def create_file_operations_tab(self):
        """Create file operations tab"""
        file_frame = ttk.Frame(self.notebook)
        self.notebook.add(file_frame, text='File Ops')
        
        # File path entry
        path_frame = ttk.Frame(file_frame)
        path_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(path_frame, text="File Path:").pack(side='left')
        self.file_path_var = tk.StringVar()
        self.file_path_entry = ttk.Entry(path_frame, textvariable=self.file_path_var, width=50)
        self.file_path_entry.pack(side='left', padx=5, expand=True, fill='x')
        ttk.Button(path_frame, text="Browse", command=self.browse_file).pack(side='left', padx=5)
        
        # File operations buttons
        ops_frame = ttk.Frame(file_frame)
        ops_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(ops_frame, text="Read File", command=self.read_file).pack(side='left', padx=2)
        ttk.Button(ops_frame, text="List Directory", command=self.list_directory).pack(side='left', padx=2)
        ttk.Button(ops_frame, text="Write File", command=self.write_file).pack(side='left', padx=2)
        
        # File content display
        content_frame = ttk.Frame(file_frame)
        content_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        ttk.Label(content_frame, text="File Content:").pack(anchor='w')
        self.file_content_text = scrolledtext.ScrolledText(content_frame, height=15)
        self.file_content_text.pack(fill='both', expand=True)
        
    def create_web_operations_tab(self):
        """Create web operations tab"""
        web_frame = ttk.Frame(self.notebook)
        self.notebook.add(web_frame, text='Web Ops')
        
        # URL entry
        url_frame = ttk.Frame(web_frame)
        url_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(url_frame, text="URL:").pack(side='left')
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=50)
        self.url_entry.pack(side='left', padx=5, expand=True, fill='x')
        self.url_entry.bind('<Return>', lambda e: self.load_page())
        
        # Web operations buttons
        web_ops_frame = ttk.Frame(web_frame)
        web_ops_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(web_ops_frame, text="Load Page", command=self.load_page).pack(side='left', padx=2)
        ttk.Button(web_ops_frame, text="Get Content", command=self.get_page_content).pack(side='left', padx=2)
        ttk.Button(web_ops_frame, text="Extract Links", command=self.extract_links).pack(side='left', padx=2)
        ttk.Button(web_ops_frame, text="Open in Browser", command=self.open_in_browser).pack(side='left', padx=2)
        
        # Search frame
        search_frame = ttk.Frame(web_frame)
        search_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side='left')
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind('<Return>', lambda e: self.search_in_content())
        ttk.Button(search_frame, text="Search", command=self.search_in_content).pack(side='left', padx=2)
        
        # Web content display
        web_content_frame = ttk.Frame(web_frame)
        web_content_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        ttk.Label(web_content_frame, text="Web Content:").pack(anchor='w')
        self.web_content_text = scrolledtext.ScrolledText(web_content_frame, height=15)
        self.web_content_text.pack(fill='both', expand=True)
        
    def create_action_log_tab(self):
        """Create action log tab"""
        log_frame = ttk.Frame(self.notebook)
        self.notebook.add(log_frame, text='Action Log')
        
        # Log controls
        log_controls_frame = ttk.Frame(log_frame)
        log_controls_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(log_controls_frame, text="Clear Log", command=self.clear_log).pack(side='left', padx=5)
        ttk.Button(log_controls_frame, text="Export Log", command=self.export_log).pack(side='left', padx=5)
        
        # Log display
        log_display_frame = ttk.Frame(log_frame)
        log_display_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        ttk.Label(log_display_frame, text="Action Log:").pack(anchor='w')
        self.log_text = scrolledtext.ScrolledText(log_display_frame, height=20, state=tk.DISABLED)
        self.log_text.pack(fill='both', expand=True)
        
    def take_screenshot(self):
        """Take a screenshot"""
        def screenshot_thread():
            try:
                screenshot = self.screenshot_manager.take_screenshot()
                thumbnail = self.screenshot_manager.get_thumbnail()
                
                # Update UI in main thread
                self.parent.after(0, self.update_screenshot_display, screenshot, thumbnail)
                self.logger.log("Screenshot taken successfully")
                
            except Exception as e:
                self.logger.log(f"Screenshot failed: {str(e)}")
                self.parent.after(0, lambda: messagebox.showerror("Screenshot Error", str(e)))
        
        # Run screenshot in separate thread to avoid blocking UI
        threading.Thread(target=screenshot_thread, daemon=True).start()
        
    def update_screenshot_display(self, screenshot, thumbnail):
        """Update screenshot display"""
        if thumbnail:
            self.screenshot_label.config(image=thumbnail)
            self.screenshot_label.image = thumbnail  # Keep a reference
            
        size = screenshot.size if screenshot else (0, 0)
        self.screenshot_info.config(text=f"Screenshot: {size[0]}x{size[1]} pixels")
        
    def toggle_auto_screenshot(self):
        """Toggle auto screenshot mode"""
        self.auto_screenshot = not self.auto_screenshot
        if self.auto_screenshot:
            self.start_auto_screenshot()
            self.logger.log("Auto screenshot enabled")
        else:
            self.stop_auto_screenshot()
            self.logger.log("Auto screenshot disabled")
            
    def start_auto_screenshot(self):
        """Start auto screenshot thread"""
        def auto_screenshot_loop():
            while self.auto_screenshot:
                try:
                    screenshot = self.screenshot_manager.take_screenshot()
                    thumbnail = self.screenshot_manager.get_thumbnail()
                    self.parent.after(0, self.update_screenshot_display, screenshot, thumbnail)
                    
                    # Wait before next screenshot
                    import time
                    time.sleep(2)  # Take screenshot every 2 seconds
                    
                except Exception as e:
                    self.logger.log(f"Auto screenshot error: {str(e)}")
                    break
        
        self.auto_screenshot_thread = threading.Thread(target=auto_screenshot_loop, daemon=True)
        self.auto_screenshot_thread.start()
        
    def stop_auto_screenshot(self):
        """Stop auto screenshot"""
        self.auto_screenshot = False
        
    def browse_file(self):
        """Browse for file"""
        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=[
                ("All Files", "*.*"),
                ("Text Files", "*.txt"),
                ("Python Files", "*.py"),
                ("JSON Files", "*.json")
            ]
        )
        if file_path:
            self.file_path_var.set(file_path)
            
    def read_file(self):
        """Read file content"""
        file_path = self.file_path_var.get().strip()
        if not file_path:
            messagebox.showwarning("No File", "Please enter a file path")
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
                self.logger.log(f"Read file: {file_path}")
                
            except Exception as e:
                self.logger.log(f"File read error: {str(e)}")
                self.parent.after(0, lambda: messagebox.showerror("File Error", str(e)))
        
        threading.Thread(target=read_thread, daemon=True).start()
        
    def update_file_content(self, result):
        """Update file content display"""
        self.file_content_text.delete(1.0, tk.END)
        
        if isinstance(result, dict) and result.get('success'):
            content = result.get('content', '')
            self.file_content_text.insert(1.0, content)
            self.logger.log(f"File content loaded: {result.get('length', 0)} characters")
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
                self.logger.log(f"Listed directory: {dir_path}")
                
            except Exception as e:
                self.logger.log(f"Directory list error: {str(e)}")
                self.parent.after(0, lambda: messagebox.showerror("Directory Error", str(e)))
        
        threading.Thread(target=list_thread, daemon=True).start()
        
    def update_directory_listing(self, result):
        """Update directory listing display"""
        self.file_content_text.delete(1.0, tk.END)
        
        if isinstance(result, dict) and result.get('success'):
            items = result.get('items', [])
            content = f"Directory: {result.get('path', '')}\n"
            content += f"Items: {result.get('count', 0)}\n\n"
            content += "\n".join(items)
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
                
                self.logger.log(f"Wrote file: {file_path}")
                self.parent.after(0, lambda: messagebox.showinfo("Success", str(result)))
                
            except Exception as e:
                self.logger.log(f"File write error: {str(e)}")
                self.parent.after(0, lambda: messagebox.showerror("File Error", str(e)))
        
        threading.Thread(target=write_thread, daemon=True).start()
        
    def load_page(self):
        """Load web page"""
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
                self.logger.log(f"Loaded page: {url}")
                
            except Exception as e:
                self.logger.log(f"Page load error: {str(e)}")
                self.parent.after(0, lambda: messagebox.showerror("Web Error", str(e)))
        
        threading.Thread(target=load_thread, daemon=True).start()
        
    def update_web_content(self, result):
        """Update web content display"""
        self.web_content_text.delete(1.0, tk.END)
        
        if isinstance(result, dict) and result.get('success'):
            content = result.get('content', '')
            self.web_content_text.insert(1.0, content)
            self.logger.log(f"Web content loaded: {result.get('content_length', 0)} characters")
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
                self.logger.log("Retrieved current page content")
                
            except Exception as e:
                self.logger.log(f"Get content error: {str(e)}")
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
                self.logger.log("Extracted links from current page")
                
            except Exception as e:
                self.logger.log(f"Extract links error: {str(e)}")
                self.parent.after(0, lambda: messagebox.showerror("Web Error", str(e)))
        
        threading.Thread(target=extract_thread, daemon=True).start()
        
    def update_links_display(self, result):
        """Update links display"""
        self.web_content_text.delete(1.0, tk.END)
        
        if isinstance(result, dict) and result.get('success'):
            links = result.get('links', [])
            total = result.get('total_count', 0)
            
            content = f"Found {total} links (showing first {len(links)}):\n\n"
            for i, link in enumerate(links, 1):
                content += f"{i}. {link.get('text', 'No text')} - {link.get('url', '')}\n"
            
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
                
                self.logger.log(f"Searched for: {search_text}")
                self.parent.after(0, lambda: messagebox.showinfo("Search Result", str(result)))
                
            except Exception as e:
                self.logger.log(f"Search error: {str(e)}")
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
            self.logger.log(f"Opened in browser: {url}")
            messagebox.showinfo("Success", str(result))
        except Exception as e:
            self.logger.log(f"Browser open error: {str(e)}")
            messagebox.showerror("Browser Error", str(e))
            
    def clear_log(self):
        """Clear action log"""
        self.logger.clear()
        
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
                    f.write(log_content)
                self.logger.log(f"Log exported to: {file_path}")
                messagebox.showinfo("Success", f"Log exported to {file_path}")
            except Exception as e:
                self.logger.log(f"Export error: {str(e)}")
                messagebox.showerror("Export Error", str(e))
                
    def get_current_screenshot(self):
        """Get current screenshot for use by other components"""
        return self.screenshot_manager.current_screenshot
        
    def get_current_page_content(self):
        """Get current page content for use by other components"""
        return self.web_operations.current_page_content
        
    def log_action(self, message):
        """Log an action (used by other components)"""
        self.logger.log(message)
