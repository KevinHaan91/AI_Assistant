import time
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext

class ActionLogger:
    def __init__(self, log_widget=None):
        self.log_widget = log_widget
        
    def log(self, message):
        """Log an action with timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        if self.log_widget:
            self.log_widget.config(state=tk.NORMAL)
            self.log_widget.insert(tk.END, f"{log_entry}\n")
            self.log_widget.config(state=tk.DISABLED)
            self.log_widget.see(tk.END)
        
        print(log_entry)  # Also print to console
        
    def clear(self):
        """Clear the log"""
        if self.log_widget:
            self.log_widget.config(state=tk.NORMAL)
            self.log_widget.delete(1.0, tk.END)
            self.log_widget.config(state=tk.DISABLED)
