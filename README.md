# Claude AI Assistant v2.0 🤖✨

A **modern, sleek GUI application** for interacting with Claude AI with advanced computer automation capabilities. Now featuring enhanced messaging, improved automation, and a beautiful modern interface.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-brightgreen.svg)
![Claude](https://img.shields.io/badge/Claude-3.5%20Sonnet-orange.svg)

## 🆕 What's New in v2.0

### ✨ **Modern Interface**
- **Dark theme** with beautiful Material Design-inspired colors
- **Responsive layout** with smooth interactions
- **Enhanced typography** and improved readability
- **Status indicators** and real-time feedback
- **Modern cards and panels** for better organization

### 🚀 **Enhanced Features**
- **Smart text messaging** - Send texts to contacts via Google Voice
- **Improved computer automation** with verification and error recovery
- **Enhanced file operations** with better format support
- **Advanced web operations** with content extraction
- **Real-time mouse tracking** and position display
- **Auto-screenshot capabilities** with customizable intervals

### 🎯 **Better User Experience**
- **Keyboard shortcuts** for power users
- **Quick action buttons** in the header
- **Interactive chat** with clickable links and formatted code
- **Smart command recognition** for natural language requests
- **Action history** and logging with export capabilities

## 🚀 Quick Start

### 1. **Easy Launch**
```bash
# Windows
./launch.bat

# Mac/Linux
chmod +x launch.sh
./launch.sh
```

### 2. **Manual Setup**
```bash
# Clone or download the project
cd AI_Assistant

# Create virtual environment
python -m venv env

# Activate environment
# Windows:
env\Scripts\activate
# Mac/Linux:
source env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up your API key
cp .env.example .env
# Edit .env and add your Anthropic API key

# Run the application
python main.py
```

### 3. **Get Your API Key**
1. Visit [Anthropic Console](https://console.anthropic.com)
2. Create an account or sign in
3. Generate an API key
4. Add it to your `.env` file:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## 💬 Smart Text Messaging

### **Natural Language Commands**
Just type naturally in the chat:
- `"Send text to Andrea saying working on an AI app"`
- `"Text mom that I'll be home late"`
- `"Message John: Can we meet tomorrow?"`

### **How It Works**
1. **Smart Detection** - The app recognizes messaging intent
2. **Confirmation Dialog** - Shows what will be sent to whom
3. **Google Voice Integration** - Opens your browser to complete the send
4. **Status Feedback** - Confirms the action and logs it

## 🖥️ Enhanced Computer Automation

### **Smart Actions**
- **Click** with coordinate validation and verification
- **Type** with natural timing and special character support
- **Scroll** with intelligent direction detection
- **Key combinations** with hotkey support
- **Drag and drop** with smooth motion
- **Screenshot** with automatic thumbnails

### **Safety Features**
- **Failsafe protection** - Move mouse to corner to stop
- **Coordinate validation** - Prevents out-of-bounds actions
- **Action verification** - Screenshots before/after actions
- **Human-like timing** - Realistic delays between actions
- **Emergency stop** - Instant automation disable

### **Example Commands**
```
"Take a screenshot and tell me what you see"
"Click at coordinates 500, 300"
"Type 'Hello World' in the active window"
"Scroll down 5 times"
"Press Ctrl+C to copy"
```

## 📁 Advanced File Operations

### **Supported Formats**
- **Text files**: `.txt`, `.md`, `.csv`, `.json`, `.xml`, `.yml`
- **Code files**: `.py`, `.js`, `.html`, `.css`, `.sql`
- **Config files**: `.ini`, `.cfg`, `.env`
- **Images**: `.jpg`, `.png`, `.gif`, `.webp`, `.svg`

### **Smart Features**
- **Syntax highlighting** for code files
- **Large file handling** with progress indicators
- **Directory browsing** with file type detection
- **Auto-format detection** for different file types
- **Safe write operations** with backup creation

### **Example Commands**
```
"Read the file config.json and explain its structure"
"List all Python files in the current directory"
"Create a new file called notes.txt with my meeting agenda"
"Show me the contents of the logs folder"
```

## 🌐 Web Operations & Browsing

### **Enhanced Web Features**
- **Smart page loading** with content extraction
- **Link extraction** with organization
- **Text search** within loaded pages
- **Content filtering** and summarization
- **Multi-format support** (HTML, JSON, XML)

### **Browser Integration**
- **Auto-open** pages in your default browser
- **Content caching** for faster re-access
- **Link validation** and safety checking
- **Mobile-friendly** user agent handling

### **Example Commands**
```
"Load the webpage python.org and summarize what it's about"
"Find all links on the current page related to documentation"
"Search for 'tutorial' in the loaded page content"
"Open google.com in my browser"
```

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New chat |
| `Ctrl+S` | Save/Export chat |
| `Ctrl+O` | Open file |
| `Ctrl+Shift+S` | Take screenshot |
| `Ctrl+Enter` | Send message |
| `Ctrl+,` | Open settings |
| `F1` | Show help |
| `F11` | Toggle fullscreen |
| `Ctrl+Q` | Quit application |

## 🎨 Interface Overview

### **Main Layout**
```
┌─────────────────────────────────────────────────┐
│ 🤖 Claude AI Assistant    📸 Screenshot ⚙️ Settings │
├─────────────────────────┬───────────────────────┤
│                         │                       │
│     💬 Chat Panel       │    🛠️ Control Panel    │
│                         │                       │
│  • Conversation history │  📸 Screenshot        │
│  • Message input        │  🖱️ Computer Actions   │
│  • Smart commands       │  📁 File Operations   │
│  • Interactive links    │  🌐 Web Operations    │
│                         │  📝 Action Log        │
├─────────────────────────┴───────────────────────┤
│ ● Connected | Ready | Actions: 0               │
└─────────────────────────────────────────────────┘
```

### **Control Panel Tabs**

#### 📸 **Screenshot Tab**
- Take instant screenshots
- Auto-screenshot with custom intervals
- View thumbnail previews
- One-click screenshot for messages

#### 🖱️ **Computer Actions Tab**
- Quick action buttons (Click, Type, Scroll, Keys)
- Real-time mouse position tracking
- Smart coordinate validation
- Action history and verification

#### 📁 **File Operations Tab**
- File browser with modern dialog
- Content preview with syntax highlighting
- Write/edit capabilities
- Directory listing and navigation

#### 🌐 **Web Operations Tab**
- URL loading with progress feedback
- Content extraction and display
- Link extraction and organization
- In-page search functionality

#### 📝 **Action Log Tab**
- Real-time action logging
- Export capabilities
- Auto-scroll toggle
- Timestamp tracking

## 🔧 Configuration & Customization

### **Theme Customization**
Edit your `.env` file to customize colors:
```env
THEME_BG=#0f0f0f
THEME_ACCENT=#007acc
CHAT_BG=#1e1e1e
FONT_FAMILY=Segoe UI
```

### **Automation Settings**
```env
PYAUTOGUI_PAUSE=0.3
PYAUTOGUI_FAILSAFE=true
SMART_DELAYS=true
VERIFY_ACTIONS=true
```

### **Advanced Options**
```env
MAX_HISTORY_MESSAGES=20
REQUEST_TIMEOUT=10
LOG_LEVEL=INFO
SAFE_MODE=false
```

## 🛡️ Safety & Security

### **Built-in Safety Features**
- **API key encryption** and secure storage
- **Action confirmation** for potentially dangerous operations
- **Failsafe mechanisms** to prevent runaway automation
- **Input validation** and sanitization
- **Error recovery** and graceful degradation

### **Privacy Protection**
- **Local operation** - no data sent to third parties
- **Conversation history** stored locally only
- **Screenshot data** processed locally
- **Optional logging** with user control

## 🐛 Troubleshooting

### **Common Issues**

#### **"API Key Missing" Error**
1. Ensure you have a `.env` file in the project directory
2. Add your Anthropic API key: `ANTHROPIC_API_KEY=your_key_here`
3. Restart the application

#### **Screenshot Not Working**
1. **Windows**: Ensure the app has screen capture permissions
2. **macOS**: Grant accessibility permissions in System Preferences
3. **Linux**: Install required X11 libraries
4. Try disabling failsafe: `PYAUTOGUI_FAILSAFE=false`

#### **Computer Actions Not Responding**
1. Check if PyAutoGUI is properly installed: `pip install pyautogui`
2. Verify screen coordinates are within bounds
3. Try increasing the pause delay: `PYAUTOGUI_PAUSE=1.0`
4. Ensure no other applications are blocking input

#### **Web Operations Failing**
1. Check your internet connection
2. Some websites block automated requests
3. Try different URLs or user agents
4. Verify firewall/antivirus isn't blocking requests

### **Getting Help**
1. Check the **Action Log** tab for detailed error messages
2. Use **Help > Help** for built-in documentation
3. Enable verbose logging: `LOG_LEVEL=DEBUG`
4. Check the `logs/` directory for detailed error logs

## 🔮 Future Features (Roadmap)

- **🗣️ Voice Commands** - Control the app with speech
- **👋 Gesture Control** - Mouse gesture recognition
- **🔌 Plugin System** - Custom tool integration
- **☁️ Cloud Sync** - Cross-device conversation sync
- **🤖 AI Suggestions** - Proactive action recommendations
- **📱 Mobile Companion** - Remote control via mobile app

## 📈 Performance Tips

### **Optimize for Speed**
- Close unnecessary applications during automation
- Use smaller screenshot intervals for auto-capture
- Clear chat history periodically
- Disable verbose logging in production

### **Memory Management**
- The app automatically manages screenshot memory
- Large file operations use streaming
- Chat history has configurable limits
- Temporary files are auto-cleaned

## 💡 Pro Tips

### **Power User Features**
1. **Custom Shortcuts** - Define your own keyboard shortcuts
2. **Batch Operations** - Queue multiple actions
3. **Smart Recognition** - The app learns your common patterns
4. **Context Awareness** - Claude remembers previous actions

### **Workflow Integration**
1. **Morning Routine** - "Take screenshot, check weather, open calendar"
2. **Work Setup** - "Open my project files and start development server"
3. **Communication** - "Check messages and send updates to team"
4. **Evening Wrap** - "Save work, backup files, send summary email"

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report Bugs** - Use the issue tracker
2. **Suggest Features** - Share your ideas
3. **Improve Code** - Submit pull requests
4. **Update Documentation** - Help others learn
5. **Share Examples** - Show cool use cases

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Anthropic** for the amazing Claude AI API
- **Python Community** for excellent libraries
- **Open Source Contributors** who make this possible
- **Beta Testers** who helped refine the experience

---

**Made with ❤️ for the AI automation community**

*Ready to supercharge your productivity with AI? [Get started now!](#-quick-start)*
