import shutil
from pathlib import Path
from config import Config

class FileOperations:
    def __init__(self):
        self.supported_text_ext = Config.SUPPORTED_TEXT_EXTENSIONS
        self.supported_image_ext = Config.SUPPORTED_IMAGE_EXTENSIONS
        self.binary_ext = Config.BINARY_EXTENSIONS
        
    def execute_operation(self, operation_data):
        """Execute a file operation"""
        operation = operation_data.get("operation")
        file_path = operation_data.get("file_path")
        
        if operation == "read":
            return self.read_file(file_path)
        elif operation == "write":
            content = operation_data.get("content", "")
            mode = operation_data.get("mode", "w")
            return self.write_file(file_path, content, mode)
        elif operation == "list":
            return self.list_directory(file_path)
        elif operation == "delete":
            return self.delete_file(file_path)
        elif operation == "copy":
            dest_path = operation_data.get("dest_path")
            return self.copy_file(file_path, dest_path)
        elif operation == "move":
            dest_path = operation_data.get("dest_path")
            return self.move_file(file_path, dest_path)
        else:
            return f"Unknown file operation: {operation}"
    
    def read_file(self, file_path):
        """Read content from a file"""
        try:
            path = Path(file_path)
            if not path.exists():
                return f"File not found: {file_path}"
            
            if path.is_dir():
                return f"Path is a directory: {file_path}"
            
            # Handle different file types
            if path.suffix.lower() in self.supported_image_ext:
                return f"Image file detected: {file_path}"
            elif path.suffix.lower() in self.binary_ext:
                return f"Binary file detected: {file_path}"
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                'success': True,
                'content': content,
                'length': len(content),
                'path': file_path
            }
            
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
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
            
            return {
                'success': True,
                'items': items,
                'count': len(items),
                'path': dir_path
            }
            
        except Exception as e:
            return f"Error listing directory: {str(e)}"
    
    def delete_file(self, file_path):
        """Delete a file or directory"""
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
        """Copy a file or directory"""
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
        """Move a file or directory"""
        try:
            source = Path(source_path)
            dest = Path(dest_path)
            
            if not source.exists():
                return f"Source file not found: {source_path}"
            
            shutil.move(str(source), str(dest))
            return f"File moved: {source_path} -> {dest_path}"
            
        except Exception as e:
            return f"Error moving file: {str(e)}"
