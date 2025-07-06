"""
Modern theme and styling for Claude Computer Use Assistant
Provides modern colors, fonts, and styling utilities
"""

import tkinter as tk
from tkinter import ttk
import platform

class ModernTheme:
    """Modern color scheme and styling configuration"""
    
    # Modern Color Palette - Grayscale UI with status colors
    COLORS = {
        # Primary backgrounds (UI panels, window, etc.)
        'bg_primary': '#23272f',        # Main background (dark gray)
        'bg_secondary': '#2d323b',     # Secondary panels (slightly lighter dark gray)
        'bg_tertiary': '#393e48',      # Cards and elevated elements (mid gray)
        'bg_quaternary': '#444955',    # Hover states and active elements (soft gray)

        # Surface colors (for cards, etc.)
        'surface': '#393e48',           # Card surfaces (mid gray)
        'surface_variant': '#23272f',  # Alternative surfaces (dark gray)
        'surface_hover': '#444955',    # Hover state for surfaces (soft gray)

        # Accent colors
        'accent_primary': '#5c5f66',     # Primary accent (medium gray)
        'accent_secondary': '#888b92',   # Secondary accent (light gray)
        'accent_tertiary': '#b0b3b8',    # Tertiary accent (lighter gray)
        'accent_success': '#4ade80',     # Green for success (keep for status)
        'accent_warning': '#facc15',     # Yellow for warnings (keep for status)
        'accent_info': '#60a5fa',        # Blue for info (keep for status)
        'accent_orange': '#fb923c',      # Orange accent (keep for status)

        # Text colors
        'text_primary': '#f3f4f6',       # Primary text (very light gray)
        'text_secondary': '#b0b3b8',     # Secondary text (lighter gray)
        'text_tertiary': '#888b92',      # Tertiary text (gray)
        'text_disabled': '#444955',      # Disabled text (soft gray)

        # Border colors
        'border_primary': '#393e48',     # Primary borders (mid gray)
        'border_secondary': '#23272f',   # Secondary borders (dark gray)
        'border_focus': '#888b92',       # Focus borders (light gray)

        # Chat specific colors
        'chat_bg': '#2d323b',            # Chat area background (slightly lighter dark gray)
        'chat_text': '#f3f4f6',          # Chat area text (very light gray)
        'chat_user': '#f3f4f6',          # User messages (very light gray)
        'chat_assistant': '#b0b3b8',     # Assistant messages (lighter gray)
        'chat_system': '#888b92',        # System messages (gray)
        'chat_error': '#f87171',         # Error messages (red, keep for visibility)
        'chat_timestamp': '#b0b3b8',     # Timestamps (lighter gray)

        # Status indicators
        'status_online': '#4ade80',      # Online/ready (green)
        'status_busy': '#facc15',        # Processing/busy (yellow)
        'status_error': '#f87171',       # Error state (red)
        'status_offline': '#888b92',     # Offline/disconnected (gray)
    }
    
    # Typography
    FONTS = {
        'heading_large': ('Inter', 22, 'bold'),
        'heading_medium': ('Inter', 17, 'bold'),
        'heading_small': ('Inter', 14, 'bold'),
        'body_large': ('Inter', 13),
        'body_medium': ('Inter', 12),
        'body_small': ('Inter', 11),
        'caption': ('Inter', 10),
        'code': ('Consolas', 11),
        'chat': ('Inter', 12),
        'button': ('Inter', 11, 'bold'),
    }
    
    # Spacing and sizing
    SPACING = {
        'xs': 4,
        'sm': 8,
        'md': 12,
        'lg': 16,
        'xl': 24,
        'xxl': 32,
    }
    
    BORDER_RADIUS = {
        'sm': 4,
        'md': 8,
        'lg': 12,
        'xl': 16,
    }
    
    # Animation timings (for future use)
    ANIMATIONS = {
        'fast': 150,
        'normal': 250,
        'slow': 400,
    }

class ModernStyler:
    """Utility class for applying modern styles to tkinter widgets"""
    
    def __init__(self):
        self.theme = ModernTheme()
        self.setup_ttk_styles()
    
    def setup_ttk_styles(self):
        """Configure ttk styles for modern appearance"""
        style = ttk.Style()
        
        # Configure modern frame styles
        style.configure('Modern.TFrame',
                       background=self.theme.COLORS['bg_secondary'],
                       borderwidth=0)
        
        style.configure('Card.TFrame',
                       background=self.theme.COLORS['surface'],
                       borderwidth=1,
                       relief='solid')
        
        # Configure modern button styles
        style.configure('Modern.TButton',
                       background=self.theme.COLORS['accent_primary'],
                       foreground=self.theme.COLORS['text_primary'],
                       borderwidth=0,
                       focuscolor=self.theme.COLORS['border_focus'],
                       font=self.theme.FONTS['button'])
        
        style.map('Modern.TButton',
                 background=[('active', self.theme.COLORS['accent_secondary']),
                           ('pressed', self.theme.COLORS['bg_quaternary'])])
        
        # Configure modern entry styles
        style.configure('Modern.TEntry',
                       background=self.theme.COLORS['surface'],
                       foreground=self.theme.COLORS['text_primary'],
                       borderwidth=1,
                       relief='solid',
                       insertcolor=self.theme.COLORS['text_primary'],
                       font=self.theme.FONTS['body_medium'])
        
        style.map('Modern.TEntry',
                 bordercolor=[('focus', self.theme.COLORS['border_focus'])])
        
        # Configure modern notebook styles
        style.configure('Modern.TNotebook',
                       background=self.theme.COLORS['bg_secondary'],
                       borderwidth=0)
        
        style.configure('Modern.TNotebook.Tab',
                       background=self.theme.COLORS['bg_tertiary'],
                       foreground=self.theme.COLORS['text_secondary'],
                       borderwidth=0,
                       padding=[12, 8],
                       font=self.theme.FONTS['body_medium'])
        
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', self.theme.COLORS['accent_primary']),
                           ('active', self.theme.COLORS['surface_hover'])],
                 foreground=[('selected', self.theme.COLORS['text_primary'])])
        
        # Configure modern label styles
        style.configure('Modern.TLabel',
                       background=self.theme.COLORS['bg_secondary'],
                       foreground=self.theme.COLORS['text_primary'],
                       font=self.theme.FONTS['body_medium'])
        
        style.configure('Heading.TLabel',
                       background=self.theme.COLORS['bg_secondary'],
                       foreground=self.theme.COLORS['text_primary'],
                       font=self.theme.FONTS['heading_medium'])
        
        style.configure('Caption.TLabel',
                       background=self.theme.COLORS['bg_secondary'],
                       foreground=self.theme.COLORS['text_secondary'],
                       font=self.theme.FONTS['caption'])
        
        # Configure modern scrollbar
        style.configure('Modern.Vertical.TScrollbar',
                       background=self.theme.COLORS['bg_tertiary'],
                       troughcolor=self.theme.COLORS['bg_secondary'],
                       borderwidth=0,
                       arrowcolor=self.theme.COLORS['text_secondary'])
        
    def apply_modern_style(self, widget, style_type='default'):
        """Apply modern styling to a widget"""
        colors = self.theme.COLORS
        fonts = self.theme.FONTS

        if isinstance(widget, tk.Tk) or isinstance(widget, tk.Toplevel):
            # Main window styling
            widget.configure(bg=colors['bg_primary'])

        elif isinstance(widget, tk.Frame):
            widget.configure(bg=colors['bg_secondary'], 
                           highlightthickness=0)

        elif isinstance(widget, tk.Text):
            # Modern text widget styling
            if style_type == 'chat':
                widget.configure(
                    bg=colors['chat_bg'],
                    fg=colors['chat_text'],
                    insertbackground=colors['chat_text'],
                    selectbackground=colors['accent_primary'],
                    selectforeground=colors['chat_text'],
                    highlightthickness=1,
                    highlightcolor=colors['border_focus'],
                    highlightbackground=colors['border_primary'],
                    borderwidth=0,
                    font=fonts['chat'],
                    wrap=tk.WORD,
                    relief='flat'
                )
            else:
                widget.configure(
                    bg=colors['surface'],
                    fg=colors['text_primary'],
                    insertbackground=colors['text_primary'],
                    selectbackground=colors['accent_primary'],
                    selectforeground=colors['text_primary'],
                    highlightthickness=1,
                    highlightcolor=colors['border_focus'],
                    highlightbackground=colors['border_primary'],
                    borderwidth=0,
                    font=fonts['body_medium'],
                    wrap=tk.WORD,
                    relief='flat'
                )
            
        elif isinstance(widget, tk.Button):
            # Modern button styling
            if style_type == 'primary':
                bg_color = colors['accent_primary']
                hover_color = colors['accent_secondary']
            elif style_type == 'danger':
                bg_color = colors['accent_tertiary']
                hover_color = '#ff5252'
            elif style_type == 'success':
                bg_color = colors['accent_success']
                hover_color = '#69db7c'
            else:
                bg_color = colors['surface']
                hover_color = colors['surface_hover']
            
            widget.configure(
                bg=bg_color,
                fg=colors['text_primary'],
                activebackground=hover_color,
                activeforeground=colors['text_primary'],
                highlightthickness=0,
                borderwidth=0,
                relief='flat',
                font=fonts['button'],
                cursor='hand2'
            )
            
        elif isinstance(widget, tk.Entry):
            # Modern entry styling
            widget.configure(
                bg=colors['surface'],
                fg=colors['text_primary'],
                insertbackground=colors['text_primary'],
                selectbackground=colors['accent_primary'],
                selectforeground=colors['text_primary'],
                highlightthickness=1,
                highlightcolor=colors['border_focus'],
                highlightbackground=colors['border_primary'],
                borderwidth=0,
                relief='flat',
                font=fonts['body_medium']
            )
            
        elif isinstance(widget, tk.Label):
            # Modern label styling
            font_type = fonts.get(style_type, fonts['body_medium'])
            text_color = colors['text_primary']
            
            if style_type == 'heading':
                font_type = fonts['heading_medium']
            elif style_type == 'caption':
                font_type = fonts['caption']
                text_color = colors['text_secondary']
            elif style_type == 'error':
                text_color = colors['accent_tertiary']
                
            widget.configure(
                bg=colors['bg_secondary'],
                fg=text_color,
                font=font_type
            )
    
    def create_modern_card(self, parent, **kwargs):
        """Create a modern card-style frame"""
        card = tk.Frame(parent, 
                       bg=self.theme.COLORS['surface'],
                       highlightthickness=1,
                       highlightcolor=self.theme.COLORS['border_primary'],
                       highlightbackground=self.theme.COLORS['border_primary'],
                       **kwargs)
        return card
    
    def create_gradient_frame(self, parent, start_color, end_color, **kwargs):
        """Create a frame with gradient background (simplified)"""
        # For now, use the start color (true gradients require canvas)
        frame = tk.Frame(parent, bg=start_color, **kwargs)
        return frame
    
    def add_hover_effect(self, widget, hover_color=None):
        """Add hover effect to a widget"""
        if hover_color is None:
            hover_color = self.theme.COLORS['surface_hover']
        
        original_color = widget.cget('bg')
        
        def on_enter(event):
            widget.configure(bg=hover_color)
        
        def on_leave(event):
            widget.configure(bg=original_color)
        
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)
    
    def create_status_indicator(self, parent, status='offline'):
        """Create a colored status indicator"""
        status_colors = {
            'online': self.theme.COLORS['status_online'],
            'busy': self.theme.COLORS['status_busy'],
            'error': self.theme.COLORS['status_error'],
            'offline': self.theme.COLORS['status_offline']
        }
        
        indicator = tk.Label(parent,
                           text='●',
                           fg=status_colors.get(status, status_colors['offline']),
                           bg=self.theme.COLORS['bg_secondary'],
                           font=('Arial', 12))
        return indicator

# Global theme instance
theme = ModernTheme()
styler = ModernStyler()
