# Claude Computer Use Assistant

A modular GUI application for interacting with Claude AI assistant with computer automation capabilities.

## Features

- **Chat Interface**: Natural language conversation with Claude AI
- **Screenshot Capture**: Take screenshots and send them to Claude for analysis
- **Computer Automation**: Let Claude perform mouse clicks, keyboard input, and other computer actions
- **File Operations**: Read, write, and manage files through Claude
- **Web Operations**: Load web pages, extract content, and browse the internet
- **Conversation History**: Automatic saving and loading of chat history
- **Action Logging**: Track all performed actions with timestamps

## Project Structure

```
claude_gui/
├── main.py                 # Entry point
├── config.py              # Configuration settings
├── .env.example           # Environment variables template
├── requirements.txt       # Python dependencies
├── gui/
│   ├── __init__.py
│   ├── main_window.py     # Main GUI window
│   ├── chat_panel.py      # Chat interface
│   ├── control_panel.py   # Control buttons and tools
│   └── dialogs.py         # Dialog windows
├── core/
│   ├── __init__.py
│   ├── claude_client.py   # Claude API integration
│   ├── computer_actions.py # Screen automation
│   ├── file_operations.py # File system operations
│   └── web_operations.py  # Web scraping and browser operations
└── utils/
    ├── __init__.py
    ├── history_manager.py # Message history management
    ├── screenshot.py      # Screenshot utilities
    └── logging.py         # Logging utilities
```

## Installation

1. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API Key**:
   - Copy `.env.example` to `.env`
   - Get your Anthropic API key from https://console.anthropic.com
   - Edit `.env` and replace `your_api_key_here` with your actual API key

3. **Run the Application**:
   ```bash
   python main.py
   ```

## Usage

### Basic Usage

1. Start the application by running `python main.py`
2. Take a screenshot using the Screenshot tab
3. Type a message in the chat interface
4. Check "Include Screenshot" to send the current screen to Claude
5. Press Ctrl+Enter or click "Send Message"

### Example Commands

- "Take a screenshot and tell me what you see"
- "Click on the Start button"
- "Read the file desktop.txt"
- "Load the webpage google.com"
- "Type 'hello world' in the currently focused text field"

### GUI Components

#### Chat Panel (Left Side)
- **Conversation History**: View all messages between you and Claude
- **Message Input**: Type your messages here
- **Include Screenshot**: Attach current screenshot to your message
- **Include Page Content**: Attach current web page content
- **Send Message**: Send your message (Ctrl+Enter)

#### Control Panel (Right Side)
- **Screenshot Tab**: Take screenshots and manage auto-capture
- **File Operations Tab**: Browse, read, and write files
- **Web Operations Tab**: Load web pages and extract content
- **Action Log Tab**: View all performed actions

### Menu Options

#### File Menu
- New Chat: Start a fresh conversation
- Export Chat: Save conversation history
- Export Action Log: Save action log

#### Edit Menu
- Clear Chat: Clear conversation history
- Clear Action Log: Clear action log
- Preferences: Configure application settings

#### Tools Menu
- Take Screenshot: Capture current screen
- Auto Screenshot: Continuously capture screenshots
- Load Web Page: Enter URL to load
- Open File: Browse and open a file

#### View Menu
- Focus Chat Input: Jump to message input area
- Show [Tab]: Switch to specific tool tab

#### Help Menu
- Help: View usage instructions
- About: Application information

## Configuration

The application can be configured through:

1. **Environment Variables** (`.env` file):
   - API key and model settings
   - Window appearance
   - Automation settings

2. **Preferences Dialog** (Edit > Preferences):
   - GUI interface for all settings
   - Real-time configuration updates

3. **Config.py** (for developers):
   - Default values and constants
   - Application-wide settings

## Dependencies

- `anthropic>=0.7.0` - Claude API client
- `python-dotenv>=1.0.0` - Environment variable management
- `pillow>=9.0.0` - Image processing
- `pyautogui>=0.9.54` - Computer automation
- `requests>=2.28.0` - HTTP requests
- `beautifulsoup4>=4.11.0` - HTML parsing
- `lxml>=4.9.0` - XML/HTML parser

## System Requirements

- Python 3.7+
- Windows, macOS, or Linux
- Internet connection for Claude API
- Screen access for screenshots
- Accessibility permissions (on macOS) for computer automation

## Security Notes

- API keys are stored locally in `.env` file
- No data is stored on external servers beyond Claude API calls
- Screenshot data is only sent to Claude when explicitly requested
- All file operations respect system permissions

## Troubleshooting

### Common Issues

1. **"API Key Missing" Error**:
   - Ensure `.env` file exists with valid API key
   - Check for extra spaces in the key

2. **Screenshot Not Working**:
   - Install pyautogui: `pip install pyautogui`
   - Grant accessibility permissions (macOS)
   - Check failsafe settings

3. **Computer Actions Not Working**:
   - Verify pyautogui permissions
   - Check coordinate bounds
   - Review failsafe configuration

4. **Web Operations Failing**:
   - Check internet connection
   - Try different URLs
   - Some sites may block automated requests

For more help, use the built-in Help dialog (Help > Help).

## Development

### Adding New Features

1. **Core Logic**: Add new functionality to the `core/` directory
2. **GUI Components**: Extend existing panels or create new ones in `gui/`
3. **Utilities**: Add helper functions to `utils/`
4. **Configuration**: Update `config.py` for new settings

### Code Organization

- Each module has a specific responsibility
- GUI components are separated from business logic
- Configuration is centralized
- Error handling is implemented throughout

### Testing

Run the application in development mode:
```bash
cd claude_gui
python main.py
```

## License

This project is provided as-is for educational and personal use.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Note**: This application requires an Anthropic API key to function. Claude API usage is subject to Anthropic's terms of service and pricing.
