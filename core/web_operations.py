import requests
import webbrowser
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from config import Config

class WebOperations:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': Config.USER_AGENT})
        self.current_url = None
        self.current_page_content = None
        self.current_page_source = None
        
    def execute_operation(self, operation_data):
        """Execute a web operation"""
        operation = operation_data.get("operation")
        
        if operation == "load_page":
            url = operation_data.get("url")
            return self.load_page(url)
        elif operation == "get_content":
            return self.get_current_content()
        elif operation == "search_elements":
            search_text = operation_data.get("search_text")
            return self.search_in_content(search_text)
        elif operation == "extract_links":
            return self.extract_links()
        else:
            return f"Unknown web operation: {operation}"
    
    def load_page(self, url):
        """Load a web page and extract content"""
        try:
            # Add protocol if missing
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # Make request
            response = self.session.get(url, timeout=Config.REQUEST_TIMEOUT)
            response.raise_for_status()
            
            # Store raw HTML source
            self.current_page_source = response.text
            self.current_url = url
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract text content
            for script in soup(["script", "style"]):
                script.decompose()
            
            text_content = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text_content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text_content = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Limit content length
            if len(text_content) > 5000:
                text_content = text_content[:5000] + "\n\n[Content truncated]"
            
            self.current_page_content = text_content
            
            parsed_url = urlparse(url)
            return {
                'success': True,
                'url': url,
                'domain': parsed_url.netloc,
                'content_length': len(text_content),
                'content': text_content
            }
            
        except requests.exceptions.RequestException as e:
            return f"Failed to load page: {str(e)}"
        except Exception as e:
            return f"Error processing page: {str(e)}"
    
    def get_current_content(self):
        """Get current page content"""
        if self.current_page_content:
            return {
                'success': True,
                'url': self.current_url,
                'content': self.current_page_content,
                'length': len(self.current_page_content)
            }
        else:
            return "No page content available"
    
    def search_in_content(self, search_text):
        """Search for text in current page content"""
        if not self.current_page_content or not search_text:
            return "No page content or search text provided"
        
        if search_text.lower() in self.current_page_content.lower():
            return f"Found '{search_text}' in current page content"
        else:
            return f"'{search_text}' not found in current page content"
    
    def extract_links(self):
        """Extract links from current page"""
        if not self.current_page_source:
            return "No page source available"
        
        try:
            soup = BeautifulSoup(self.current_page_source, 'html.parser')
            links = []
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                text = link.get_text(strip=True)
                if href.startswith(('http', '/')):
                    links.append({'text': text, 'url': href})
            
            return {
                'success': True,
                'links': links[:20],  # Return first 20 links
                'total_count': len(links)
            }
            
        except Exception as e:
            return f"Error extracting links: {str(e)}"
    
    def open_in_browser(self, url):
        """Open URL in default browser"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            webbrowser.open(url)
            return f"Opened in browser: {url}"
        except Exception as e:
            return f"Failed to open browser: {str(e)}"
