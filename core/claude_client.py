from anthropic import Anthropic
from config import Config
import io
import base64

class ClaudeClient:
    def __init__(self):
        if not Config.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        self.client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        
    def send_message(self, message, screenshot=None, page_content=None):
        """Send message to Claude with optional screenshot and page content"""
        # Prepare full message
        full_message = message
        
        if page_content:
            full_message += f"\n\nCurrent page content:\n{page_content[:2000]}..."
        
        # Prepare message structure
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": full_message}
                ]
            }
        ]
        
        # Add screenshot if provided
        if screenshot:
            buffer = io.BytesIO()
            screenshot.save(buffer, format='PNG')
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
            model=Config.CLAUDE_MODEL,
            max_tokens=1024,
            messages=messages,
            tools=self._get_tools()
        )
        
        return response
    
    def _get_tools(self):
        """Get tool definitions for Claude"""
        return [
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
