import json
from collections import deque
from datetime import datetime
from pathlib import Path
from config import Config

class MessageHistoryManager:
    def __init__(self):
        self.history = deque(maxlen=Config.MAX_HISTORY_MESSAGES)
        self.history_file = Config.HISTORY_FILE
        self.load_history()
        
    def add_message(self, sender, message, has_screenshot=False):
        """Add a message to history"""
        message_entry = {
            'timestamp': datetime.now().isoformat(),
            'sender': sender,
            'message': message,
            'has_screenshot': has_screenshot
        }
        self.history.append(message_entry)
        self.save_history()
        
    def get_context(self):
        """Get conversation context for Claude"""
        if not self.history:
            return "No previous conversation history.\n\nCurrent message:\n"
            
        context = "Previous conversation history (last 20 messages):\n\n"
        for i, msg in enumerate(self.history, 1):
            timestamp = datetime.fromisoformat(msg['timestamp']).strftime("%H:%M:%S")
            screenshot_note = " [with screenshot]" if msg.get('has_screenshot', False) else ""
            context += f"{i}. [{timestamp}] {msg['sender']}: {msg['message']}{screenshot_note}\n"
        context += "\nCurrent message:\n"
        return context
    
    def load_history(self):
        """Load history from file"""
        try:
            if self.history_file.exists():
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    history_data = json.load(f)
                    self.history = deque(history_data.get('messages', []), 
                                       maxlen=Config.MAX_HISTORY_MESSAGES)
        except Exception as e:
            print(f"Error loading history: {str(e)}")
            self.history = deque(maxlen=Config.MAX_HISTORY_MESSAGES)
    
    def save_history(self):
        """Save history to file"""
        try:
            history_data = {
                'last_updated': datetime.now().isoformat(),
                'messages': list(self.history)
            }
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving history: {str(e)}")
    
    def clear_history(self):
        """Clear all history"""
        self.history.clear()
        self.save_history()
    
    def export_history(self, filename, format='json'):
        """Export history to file"""
        if not self.history:
            raise ValueError("No history to export")
            
        if format == 'json':
            export_data = {
                'exported_at': datetime.now().isoformat(),
                'message_count': len(self.history),
                'messages': list(self.history)
            }
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
        else:
            # Export as text
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Claude Computer Use Assistant - Conversation History\n")
                f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Messages: {len(self.history)}\n\n")
                f.write("=" * 50 + "\n\n")
                
                for i, msg in enumerate(self.history, 1):
                    timestamp = datetime.fromisoformat(msg['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
                    screenshot_note = " [with screenshot]" if msg.get('has_screenshot', False) else ""
                    f.write(f"{i}. [{timestamp}] {msg['sender']}: {msg['message']}{screenshot_note}\n\n")
