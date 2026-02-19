"""
Biralo Desktop App - Modern GUI for Biralo AI Assistant
Redesigned with modern UI/UX principles
"""
import customtkinter as ctk
import threading
import subprocess
import json
import os
from pathlib import Path
from datetime import datetime
import sys
import shutil
from PIL import Image

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Modern premium color scheme
COLORS = {
    "primary": "#8B5CF6",        # Vivid Violet
    "primary_hover": "#7C3AED",  # Darker Violet
    "secondary": "#D946EF",       # Fuchsia
    "accent": "#06B6D4",          # Cyan
    "success": "#10B981",         # Emerald
    "warning": "#F59E0B",         # Amber
    "error": "#EF4444",           # Rose
    "bg_dark": "#030712",         # Slate 950 (Extremely dark)
    "bg_medium": "#111827",       # Slate 900
    "bg_light": "#1F2937",        # Slate 800
    "bg_glass": "#1F2937",        # Simulated glass
    "text_primary": "#F9FAFB",    # Slate 50
    "text_secondary": "#9CA3AF",  # Slate 400
    "border": "#374151",          # Slate 700
    "glow": "#8B5CF6",             # Primary glow
    "god_mode": "#F59E0B",        # Amber/Gold for God Mode
}


def get_biralo_command():
    """Get the correct biralo command based on environment"""
    if shutil.which("biralo"):
        return ["biralo"]
    
    venv_python = None
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        venv_python = sys.executable
    
    if not venv_python:
        venv_paths = [
            Path("venv/Scripts/python.exe"),
            Path("venv/bin/python"),
            Path("../venv/Scripts/python.exe"),
            Path("../venv/bin/python"),
        ]
        for venv_path in venv_paths:
            if venv_path.exists():
                venv_python = str(venv_path.absolute())
                break
    
    if venv_python:
        try:
            result = subprocess.run(
                [venv_python, "-m", "biralo", "--help"],
                capture_output=True, timeout=2
            )
            if result.returncode == 0:
                return [venv_python, "-m", "biralo"]
        except:
            pass
    
    try:
        result = subprocess.run(
            ["python", "-m", "biralo", "--help"],
            capture_output=True, timeout=2
        )
        if result.returncode == 0:
            return ["python", "-m", "biralo"]
    except:
        pass
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "biralo", "--help"],
            capture_output=True, timeout=2
        )
        if result.returncode == 0:
            return [sys.executable, "-m", "biralo"]
    except:
        pass
    
    return ["python", "-m", "biralo"]


class ModernButton(ctk.CTkButton):
    """Custom modern button with a premium feel"""
    def __init__(self, *args, **kwargs):
        fg_color = kwargs.pop("fg_color", COLORS["primary"])
        hover_color = kwargs.pop("hover_color", COLORS["primary_hover"])
        super().__init__(
            *args, 
            fg_color=fg_color, 
            hover_color=hover_color, 
            corner_radius=12,
            height=45,
            font=ctk.CTkFont(size=13, weight="bold"),
            **kwargs
        )


class ModernCard(ctk.CTkFrame):
    """Modern card with subtle border and glassy background"""
    def __init__(self, *args, **kwargs):
        border_color = kwargs.pop("border_color", COLORS["border"])
        super().__init__(
            *args, 
            fg_color=COLORS["bg_glass"], 
            border_color=border_color, 
            border_width=1, 
            corner_radius=20,
            **kwargs
        )


class BiraloApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window setup with modern title bar
        self.title("Biralo AI")
        self.geometry("1200x800")
        self.minsize(900, 600)
        
        # Configure window background
        self.configure(fg_color=COLORS["bg_dark"])
        
        # Config path
        self.config_path = Path.home() / ".biralo" / "config.json"
        
        # State
        self.chat_history = []
        self.gateway_process = None
        self.is_processing = False
        self.agent = None
        self.async_loop = None
        self.god_mode = False
        
        # Get biralo command
        self.biralo_cmd = get_biralo_command()
        print(f"Using Biralo command: {' '.join(self.biralo_cmd)}")
        
        # Setup UI
        self.setup_ui()
        self.load_config_status()
        
        # Initialize persistent agent in background
        threading.Thread(target=self.initialize_agent, daemon=True).start()
        
    def setup_ui(self):
        """Setup the modern UI"""
        # Grid layout - sidebar + main content
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create sidebar with modern design
        self.create_sidebar()
        
        # Create main content area
        self.create_main_area()
        
    def create_sidebar(self):
        """Create a premium, modern sidebar"""
        # Sidebar container with a sleek background
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color=COLORS["bg_medium"], border_width=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.grid_columnconfigure(0, weight=1)
        
        # Sidebar decorative border (simulated via frame)
        self.sidebar_border = ctk.CTkFrame(self.sidebar, width=1, corner_radius=0, fg_color=COLORS["border"])
        self.sidebar_border.place(relx=1, rely=0, relheight=1, anchor="ne")
        
        # Logo section
        logo_container = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_container.grid(row=0, column=0, padx=25, pady=(40, 20), sticky="ew")
        logo_container.grid_columnconfigure(0, weight=1)
        
        # Load and display logo image
        logo_path = Path("D:/biralo/biralo-logo.png")
        if logo_path.exists():
            img = Image.open(logo_path)
            self.logo_image = ctk.CTkImage(light_image=img, dark_image=img, size=(64, 64))
            self.logo_label = ctk.CTkLabel(
                logo_container,
                text="",
                image=self.logo_image
            )
        else:
            # Fallback to text if image not found
            self.logo_label = ctk.CTkLabel(
                logo_container,
                text="✨ Biralo",
                font=ctk.CTkFont(size=32, weight="bold"),
                text_color=COLORS["primary"]
            )
        self.logo_label.grid(row=0, column=0)
        
        self.logo_tagline = ctk.CTkLabel(
            logo_container,
            text="AI ASSISTANT",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=COLORS["text_secondary"]
        )
        self.logo_tagline.grid(row=1, column=0, pady=(0, 20))
        
        # Status indicator - redesigned to be more integrated
        self.status_container = ctk.CTkFrame(self.sidebar, fg_color=COLORS["bg_light"], corner_radius=15, height=40)
        self.status_container.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.status_container.grid_propagate(False)
        self.status_container.grid_columnconfigure(1, weight=1)
        
        self.status_dot = ctk.CTkFrame(self.status_container, width=8, height=8, corner_radius=4, fg_color=COLORS["warning"])
        self.status_dot.grid(row=0, column=0, padx=(15, 8), pady=16)
        
        self.status_label = ctk.CTkLabel(
            self.status_container,
            text="System Ready",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS["text_secondary"]
        )
        self.status_label.grid(row=0, column=1, sticky="w")
        
        # Navigation
        nav_items = [
            ("💬", "Chat", self.show_chat),
            ("⚙️", "Settings", self.show_config),
            ("🌐", "Gateway", self.show_gateway),
            ("ℹ️", "About", self.show_about),
        ]
        
        self.nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.nav_frame.grid(row=2, column=0, padx=15, pady=25, sticky="ew")
        self.nav_frame.grid_columnconfigure(0, weight=1)
        
        self.nav_btns = []
        for i, (icon, text, cmd) in enumerate(nav_items):
            btn = ctk.CTkButton(
                self.nav_frame,
                text=f"  {icon}  {text}",
                command=cmd,
                height=45,
                corner_radius=10,
                fg_color="transparent",
                hover_color=COLORS["bg_light"],
                text_color=COLORS["text_secondary"],
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="w"
            )
            btn.grid(row=i, column=0, pady=2, sticky="ew")
            self.nav_btns.append(btn)
            
        # Quick actions
        divider = ctk.CTkFrame(self.sidebar, height=1, fg_color=COLORS["border"])
        divider.grid(row=3, column=0, padx=25, pady=(10, 20), sticky="ew")
        
        quick_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        quick_frame.grid(row=4, column=0, padx=20, sticky="ew")
        
        new_chat_btn = ctk.CTkButton(
            quick_frame,
            text="➕  NEW CONVERSATION",
            command=self.clear_chat,
            height=40,
            corner_radius=20,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            font=ctk.CTkFont(size=11, weight="bold")
        )
        new_chat_btn.pack(fill="x", pady=5)
        
        # Bottom section for theme toggle and version
        bottom_container = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        bottom_container.grid(row=5, column=0, sticky="ew", pady=(100, 20))
        bottom_container.grid_columnconfigure(0, weight=1)
        
        self.theme_switch = ctk.CTkSwitch(
            bottom_container,
            text="DARK MODE",
            command=self.toggle_theme,
            onvalue="dark",
            offvalue="light",
            progress_color=COLORS["primary"],
            button_color=COLORS["text_primary"],
            font=ctk.CTkFont(size=10, weight="bold")
        )
        self.theme_switch.pack(pady=10)
        self.theme_switch.select()
        
        # God Mode Toggle - High visibility
        self.god_mode_switch = ctk.CTkSwitch(
            bottom_container,
            text="⚡ GOD MODE",
            command=self.toggle_god_mode,
            progress_color=COLORS["god_mode"],
            button_color=COLORS["text_primary"],
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=COLORS["text_secondary"]
        )
        self.god_mode_switch.pack(pady=(5, 10))
        
        version_label = ctk.CTkLabel(
            bottom_container,
            text="VERSION 0.1.3",
            font=ctk.CTkFont(size=9, weight="bold"),
            text_color=COLORS["border"]
        )
        version_label.pack()
        
    def create_main_area(self):
        """Create main content area with modern design"""
        # Main container
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color=COLORS["bg_dark"])
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        
        # Create all views
        self.create_chat_view()
        self.create_config_view()
        self.create_gateway_view()
        self.create_about_view()
        
        # Show chat by default
        self.show_chat()
        
    def create_chat_view(self):
        """Create a premium chat interface"""
        self.chat_view = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.chat_view.grid_columnconfigure(0, weight=1)
        self.chat_view.grid_rowconfigure(0, weight=1)
        
        # Main chat area
        chat_main_frame = ctk.CTkFrame(self.chat_view, fg_color="transparent")
        chat_main_frame.grid(row=0, column=0, sticky="nsew")
        chat_main_frame.grid_columnconfigure(0, weight=1)
        chat_main_frame.grid_rowconfigure(1, weight=1)
        
        # Chat Header
        header = ctk.CTkFrame(chat_main_frame, fg_color="transparent", height=70)
        header.grid(row=0, column=0, padx=30, pady=(20, 0), sticky="ew")
        header.grid_propagate(False)
        
        self.chat_title = ctk.CTkLabel(
            header,
            text="Conversation",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=COLORS["text_primary"]
        )
        self.chat_title.pack(side="left")
        
        self.processing_indicator = ctk.CTkLabel(
            header,
            text="●",
            font=ctk.CTkFont(size=14),
            text_color=COLORS["primary"]
        )
        # Hidden by default
        
        # Messages Display
        self.chat_scroll = ctk.CTkScrollableFrame(
            chat_main_frame,
            fg_color="transparent",
            scrollbar_button_color=COLORS["primary"],
            scrollbar_button_hover_color=COLORS["primary_hover"]
        )
        self.chat_scroll.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.chat_scroll.grid_columnconfigure(0, weight=1)
        
        # Floating Input Bar
        input_container = ctk.CTkFrame(self.chat_view, fg_color="transparent", height=100)
        input_container.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))
        input_container.grid_propagate(False)
        
        # The actual floating bar
        self.input_bar = ctk.CTkFrame(
            input_container,
            fg_color=COLORS["bg_light"],
            corner_radius=30,
            border_width=1,
            border_color=COLORS["border"]
        )
        self.input_bar.pack(fill="both", expand=True)
        self.input_bar.grid_columnconfigure(0, weight=1)
        self.input_bar.grid_rowconfigure(0, weight=1)
        
        # Text input
        self.chat_input = ctk.CTkEntry(
            self.input_bar,
            placeholder_text="TALK TO BIRALO...",
            height=50,
            font=ctk.CTkFont(size=13, weight="bold"),
            corner_radius=0,
            border_width=0,
            fg_color="transparent",
            placeholder_text_color=COLORS["text_secondary"]
        )
        self.chat_input.grid(row=0, column=0, padx=(25, 10), sticky="ew")
        self.chat_input.bind("<Return>", lambda e: self.send_message())
        
        # Send button - redesigned as an icon button
        self.send_btn = ctk.CTkButton(
            self.input_bar,
            text="↑",
            command=self.send_message,
            width=40,
            height=40,
            corner_radius=20,
            fg_color=COLORS["primary"],
            hover_color=COLORS["primary_hover"],
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.send_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Welcome message
        self.create_welcome_message()
        
    def create_welcome_message(self):
        """Create a beautiful, modern welcome screen"""
        welcome = ctk.CTkFrame(self.chat_scroll, fg_color="transparent")
        welcome.grid(row=0, column=0, pady=60, sticky="ew")
        welcome.grid_columnconfigure(0, weight=1)
        
        # Animated-feel icon container
        icon_box = ctk.CTkFrame(welcome, width=80, height=80, corner_radius=20, fg_color=COLORS["bg_light"])
        icon_box.pack(pady=(0, 25))
        icon_box.pack_propagate(False)
        
        icon_label = ctk.CTkLabel(
            icon_box,
            text="✨",
            font=ctk.CTkFont(size=40)
        )
        icon_label.place(relx=0.5, rely=0.5, anchor="center")
        
        title = ctk.CTkLabel(
            welcome,
            text="How can I help you today?",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COLORS["text_primary"]
        )
        title.pack(pady=(0, 5))
        
        subtitle = ctk.CTkLabel(
            welcome,
            text="I'M BIRALO, YOUR MODERN AI COMPANION",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=COLORS["primary"]
        )
        subtitle.pack(pady=(0, 40))
        
        # Quick suggestions in a grid
        sugg_frame = ctk.CTkFrame(welcome, fg_color="transparent")
        sugg_frame.pack()
        
        suggestions = [
            ("✍️", "Write a creative poem"),
            ("🌦️", "Check today's weather"),
            ("⚛️", "Explain quantum physics"),
            ("🎵", "Play music on YouTube")
        ]
        
        for i, (icon, text) in enumerate(suggestions):
            btn = ctk.CTkButton(
                sugg_frame,
                text=f"{icon}  {text}",
                command=lambda t=text: self.quick_message(t),
                height=45,
                width=240,
                corner_radius=12,
                fg_color=COLORS["bg_light"],
                hover_color=COLORS["bg_glass"],
                text_color=COLORS["text_primary"],
                font=ctk.CTkFont(size=12, weight="bold"),
                border_width=1,
                border_color=COLORS["border"]
            )
            btn.grid(row=i//2, column=i%2, padx=8, pady=8)
        
        self.message_row = 1
        
    def create_config_view(self):
        """Create modern settings view"""
        self.config_view = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.config_view.grid_columnconfigure(0, weight=1)
        self.config_view.grid_rowconfigure(1, weight=1)
        
        # Header
        header = ctk.CTkFrame(self.config_view, fg_color="transparent")
        header.grid(row=0, column=0, padx=30, pady=(30, 10), sticky="ew")
        
        title = ctk.CTkLabel(
            header,
            text="Settings",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORS["text_primary"]
        )
        title.pack(side="left")
        
        # Config card
        config_card = ModernCard(self.config_view)
        config_card.grid(row=1, column=0, padx=30, pady=10, sticky="nsew")
        config_card.grid_columnconfigure(0, weight=1)
        config_card.grid_rowconfigure(0, weight=1)
        
        self.config_display = ctk.CTkTextbox(
            config_card,
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color="transparent",
            text_color=COLORS["text_primary"],
            scrollbar_button_color=COLORS["primary"],
            corner_radius=15
        )
        self.config_display.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Action buttons
        btn_frame = ctk.CTkFrame(self.config_view, fg_color="transparent")
        btn_frame.grid(row=2, column=0, padx=30, pady=(10, 30), sticky="ew")
        
        buttons = [
            ("🔄  RELOAD", self.load_config_display, COLORS["primary"]),
            ("📝  EDIT FILE", self.open_config_file, COLORS["bg_light"]),
            ("🚀  INITIALIZE", self.initialize_biralo, COLORS["success"]),
        ]
        
        for i, (text, cmd, color) in enumerate(buttons):
            btn = ModernButton(
                btn_frame,
                text=text,
                command=cmd,
                width=140,
                fg_color=color,
            )
            btn.pack(side="left", padx=(0, 12))
            
    def create_gateway_view(self):
        """Create modern gateway view"""
        self.gateway_view = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.gateway_view.grid_columnconfigure(0, weight=1)
        self.gateway_view.grid_rowconfigure(1, weight=1)
        
        # Header
        header = ctk.CTkFrame(self.gateway_view, fg_color="transparent")
        header.grid(row=0, column=0, padx=30, pady=(30, 10), sticky="ew")
        
        title = ctk.CTkLabel(
            header,
            text="Gateway Services",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COLORS["text_primary"]
        )
        title.pack(side="left")
        
        # Gateway log card
        log_card = ModernCard(self.gateway_view)
        log_card.grid(row=1, column=0, padx=30, pady=10, sticky="nsew")
        log_card.grid_columnconfigure(0, weight=1)
        log_card.grid_rowconfigure(0, weight=1)
        
        self.gateway_log = ctk.CTkTextbox(
            log_card,
            font=ctk.CTkFont(family="Consolas", size=12),
            fg_color="transparent",
            text_color=COLORS["accent"],
            corner_radius=15,
            scrollbar_button_color=COLORS["primary"],
        )
        self.gateway_log.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Control buttons
        btn_frame = ctk.CTkFrame(self.gateway_view, fg_color="transparent")
        btn_frame.grid(row=2, column=0, padx=30, pady=(10, 30), sticky="ew")
        
        self.start_gateway_btn = ModernButton(
            btn_frame,
            text="▶  START GATEWAY",
            command=self.start_gateway,
            fg_color=COLORS["success"],
            width=180
        )
        self.start_gateway_btn.pack(side="left", padx=(0, 12))
        
        self.stop_gateway_btn = ModernButton(
            btn_frame,
            text="⏹  STOP GATEWAY",
            command=self.stop_gateway,
            fg_color=COLORS["error"],
            width=180,
            state="disabled"
        )
        self.stop_gateway_btn.pack(side="left", padx=(0, 12))
        
        clear_btn = ModernButton(
            btn_frame,
            text="🗑  CLEAR LOG",
            command=lambda: self.gateway_log.delete("1.0", "end"),
            fg_color=COLORS["bg_light"],
            width=140
        )
        clear_btn.pack(side="left")
        
    def create_about_view(self):
        """Create modern about view"""
        self.about_view = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.about_view.grid_columnconfigure(0, weight=1)
        
        # About card
        about_card = ModernCard(self.about_view)
        about_card.grid(row=0, column=0, padx=60, pady=60, sticky="nsew")
        about_card.grid_columnconfigure(0, weight=1)
        
        # Title with accent
        title = ctk.CTkLabel(
            about_card,
            text="BIRALO AI",
            font=ctk.CTkFont(size=42, weight="bold"),
            text_color=COLORS["primary"]
        )
        title.grid(row=0, column=0, pady=(50, 5))
        
        tagline = ctk.CTkLabel(
            about_card,
            text="THE ULTRA-LIGHTWEIGHT COMPANION",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=COLORS["text_secondary"]
        )
        tagline.grid(row=1, column=0, pady=(0, 30))
        
        # Features list in a clean layout
        features_frame = ctk.CTkFrame(about_card, fg_color="transparent")
        features_frame.grid(row=2, column=0, pady=20)
        
        features = [
            "✦  SMART REASONING",
            "✦  SECURE GATEWAY",
            "✦  FAST PERFORMANCE",
            "✦  MODERN UI/UX"
        ]
        
        for i, feature in enumerate(features):
            f_label = ctk.CTkLabel(
                features_frame,
                text=feature,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=COLORS["text_primary"]
            )
            f_label.grid(row=i, column=0, pady=5, sticky="w")
        
        # Action links
        links_frame = ctk.CTkFrame(about_card, fg_color="transparent")
        links_frame.grid(row=3, column=0, pady=(40, 50))
        
        ModernButton(
            links_frame,
            text="🐙  GITHUB SOURCE",
            command=lambda: self.open_url("https://github.com/HKUDS/biralo"),
            width=200
        ).pack(side="left", padx=10)
        
        ModernButton(
            links_frame,
            text="📚  DOCUMENTATION",
            command=lambda: self.open_url("https://github.com/HKUDS/biralo#readme"),
            fg_color=COLORS["bg_light"],
            width=200
        ).pack(side="left", padx=10)
        
    def show_chat(self):
        self.hide_all_views()
        self.chat_view.grid(row=0, column=0, sticky="nsew")
        
    def show_config(self):
        self.hide_all_views()
        self.config_view.grid(row=0, column=0, sticky="nsew")
        self.load_config_display()
        
    def show_gateway(self):
        self.hide_all_views()
        self.gateway_view.grid(row=0, column=0, sticky="nsew")
        
    def show_about(self):
        self.hide_all_views()
        self.about_view.grid(row=0, column=0, sticky="nsew")
        
    def hide_all_views(self):
        self.chat_view.grid_forget()
        self.config_view.grid_forget()
        self.gateway_view.grid_forget()
        self.about_view.grid_forget()
        
    def toggle_theme(self):
        mode = self.theme_switch.get()
        ctk.set_appearance_mode(mode)
        
    def quick_message(self, message):
        """Quick send a predefined message"""
        self.show_chat()
        self.chat_input.delete(0, "end")
        self.chat_input.insert(0, message)
        self.send_message()
        
    def send_message(self):
        message = self.chat_input.get().strip()
        if not message or self.is_processing:
            return
            
        # Show processing state
        self.is_processing = True
        self.send_btn.configure(state="disabled", fg_color=COLORS["bg_light"])
        self.processing_indicator.pack(side="left", padx=10)
        
        # Display user message
        self.display_message("You", message)
        self.chat_input.delete(0, "end")
        
        # Send to Biralo in background
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()
        
    def initialize_agent(self, force_unrestricted=False):
        """Initialize the Biralo agent in-process for faster local state management"""
        try:
            import asyncio
            from biralo.agent.loop import AgentLoop
            from biralo.config.loader import load_config
            from biralo.bus.queue import MessageBus
            from biralo.providers.litellm_provider import LiteLLMProvider
            
            # Create or reuse event loop
            if not self.async_loop:
                self.async_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.async_loop)
            
            config = load_config()
            bus = MessageBus()
            p = config.get_provider()
            model = config.agents.defaults.model
            
            provider = LiteLLMProvider(
                api_key=p.api_key if p else None,
                api_base=config.get_api_base(),
                default_model=model,
                extra_headers=p.extra_headers if p else None,
                provider_name=config.get_provider_name(),
            )
            
            # Determine workspace and restrictions
            workspace = config.workspace_path
            restrict = config.tools.restrict_to_workspace
            
            if force_unrestricted:
                # GOD MODE: No restrictions, elevated workspace (drive root on Windows)
                import platform
                workspace = Path("C:/" if platform.system() == "Windows" else "/")
                restrict = False
                self.after(0, lambda: self.status_label.configure(text="GOD MODE ACTIVE ⚡", text_color=COLORS["god_mode"]))
                self.after(0, lambda: self.status_dot.configure(fg_color=COLORS["god_mode"]))
                self.after(0, lambda: self.configure(border_color=COLORS["god_mode"], border_width=2))
            
            self.agent = AgentLoop(
                bus=bus,
                provider=provider,
                workspace=workspace,
                brave_api_key=config.tools.web.search.api_key if hasattr(config.tools.web, 'search') else None,
                exec_config=config.tools.exec,
                restrict_to_workspace=restrict,
                vision_model=config.agents.defaults.vision_model,
            )
            
            if not force_unrestricted:
                self.after(0, lambda: self.status_label.configure(text="AI Engine Ready", text_color=COLORS["success"]))
        except Exception as e:
            print(f"Failed to initialize in-process agent: {e}")
            self.after(0, lambda: self.status_label.configure(text="CLI Mode Active", text_color=COLORS["warning"]))

    def toggle_god_mode(self):
        """Toggle God Mode on/off and re-initialize agent"""
        is_on = self.god_mode_switch.get()
        self.god_mode = bool(is_on)
        
        # UI Feedback
        if self.god_mode:
            self.display_message("System", "⚡ GOD MODE ACTIVATED: UNRESTRICTED SYSTEM ACCESS GRANTED.")
            # Re-initialize with full powers
            threading.Thread(target=self.initialize_agent, args=(True,), daemon=True).start()
        else:
            self.display_message("System", "God Mode Deactivated. Restrictions restored.")
            self.after(0, lambda: self.configure(border_width=0))
            self.after(0, self.load_config_status)
            # Re-initialize with standard restrictions
            threading.Thread(target=self.initialize_agent, args=(False,), daemon=True).start()

    def process_message(self, message):
        """Process messages using the local agent state if available, otherwise fallback to CLI"""
        if self.agent and self.async_loop:
            # Use persistent in-process agent
            def run_async():
                try:
                    import asyncio
                    asyncio.set_event_loop(self.async_loop)
                    response = self.async_loop.run_until_complete(
                        self.agent.process_direct(message, session_key="desktop-app")
                    )
                    
                    if response:
                        self.after(0, lambda r=response: self.display_message("Biralo", r))
                    else:
                        self.after(0, lambda: self.display_message("System", "No response"))
                    
                    self.after(0, self.reset_processing)
                except Exception as err:
                    error_msg = str(err)
                    self.after(0, lambda msg=error_msg: self.display_message("System", f"Internal Error: {msg}"))
                    self.after(0, self.reset_processing)
            
            threading.Thread(target=run_async, daemon=True).start()
            return

        # Fallback: Use CLI subprocess if in-process agent didn't initialize
        try:
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            env['PYTHONUTF8'] = '1'
            
            result = subprocess.run(
                self.biralo_cmd + ["agent", "-m", message],
                capture_output=True,
                text=True,
                timeout=60,
                encoding='utf-8',
                errors='replace',
                env=env
            )
            
            output = result.stdout.strip() if result.stdout else ""
            
            if output:
                self.after(0, lambda o=output: self.display_message("Biralo", o))
            else:
                self.after(0, lambda: self.display_message("System", "No response received via CLI"))
                
            self.after(0, self.reset_processing)
                
        except subprocess.TimeoutExpired:
            self.after(0, lambda: self.display_message("System", "Request timed out (CLI)"))
            self.after(0, self.reset_processing)
        except Exception as e:
            self.after(0, lambda msg=str(e): self.display_message("System", f"CLI Error: {msg}"))
            self.after(0, self.reset_processing)
            
    def reset_processing(self):
        """Reset processing state"""
        self.is_processing = False
        self.send_btn.configure(state="normal")
        self.processing_indicator.grid_forget()
        
    def display_message(self, sender, message):
        """Display a message with a premium bubble design"""
        timestamp = datetime.now().strftime("%H:%M")
        
        msg_container = ctk.CTkFrame(self.chat_scroll, fg_color="transparent")
        msg_container.grid(row=self.message_row, column=0, pady=12, padx=20, sticky="ew")
        msg_container.grid_columnconfigure(0, weight=1)
        
        if sender == "You":
            # User message - Right aligned, primary gradient feel
            bubble = ctk.CTkFrame(
                msg_container,
                fg_color=COLORS["primary"],
                corner_radius=18
            )
            bubble.grid(row=0, column=0, sticky="e")
            
            msg_label = ctk.CTkLabel(
                bubble,
                text=message,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="white",
                wraplength=500,
                justify="left"
            )
            msg_label.pack(padx=18, pady=12)
            
        elif sender == "Biralo":
            # AI message - Left aligned, glassy feel
            inner_container = ctk.CTkFrame(msg_container, fg_color="transparent")
            inner_container.grid(row=0, column=0, sticky="w")
            
            # Mini avatar shortcut
            avatar = ctk.CTkLabel(
                inner_container,
                text="✨",
                font=ctk.CTkFont(size=18),
                text_color=COLORS["primary"]
            )
            avatar.pack(side="left", anchor="nw", padx=(0, 10), pady=2)
            
            bubble = ctk.CTkFrame(
                inner_container,
                fg_color=COLORS["bg_light"],
                corner_radius=18,
                border_width=1,
                border_color=COLORS["border"]
            )
            bubble.pack(side="left")
            
            msg_label = ctk.CTkLabel(
                bubble,
                text=message,
                font=ctk.CTkFont(size=14),
                text_color=COLORS["text_primary"],
                wraplength=550,
                justify="left"
            )
            msg_label.pack(padx=18, pady=12)
            
        else:
            # System message - Integrated look
            bubble = ctk.CTkFrame(
                msg_container,
                fg_color=COLORS["bg_medium"],
                corner_radius=10,
                border_width=1,
                border_color=COLORS["border"]
            )
            bubble.grid(row=0, column=0)
            
            msg_label = ctk.CTkLabel(
                bubble,
                text=f"NOTIFICATION: {message.upper()}",
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=COLORS["text_secondary"]
            )
            msg_label.pack(padx=12, pady=6)
        
        self.message_row += 1
        self.chat_scroll._parent_canvas.yview_moveto(1.0)
        
    def clear_chat(self):
        # Remove all message widgets
        for widget in self.chat_scroll.winfo_children():
            widget.destroy()
        
        self.create_welcome_message()
        self.message_row = 1
        
    def load_config_status(self):
        if self.config_path.exists():
            self.status_label.configure(text="System Ready", text_color=COLORS["success"])
            self.status_dot.configure(fg_color=COLORS["success"])
        else:
            self.status_label.configure(text="Action Needed", text_color=COLORS["warning"])
            self.status_dot.configure(fg_color=COLORS["warning"])
            
    def load_config_display(self):
        self.config_display.delete("1.0", "end")
        
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    formatted = json.dumps(config, indent=2)
                    self.config_display.insert("1.0", formatted)
            except Exception as e:
                self.config_display.insert("1.0", f"Error loading config: {str(e)}")
        else:
            self.config_display.insert("1.0", "Config file not found. Click 'Initialize' to create it.")
            
    def open_config_file(self):
        if self.config_path.exists():
            if sys.platform == "win32":
                os.startfile(self.config_path)
            elif sys.platform == "darwin":
                subprocess.run(["open", self.config_path])
            else:
                subprocess.run(["xdg-open", self.config_path])
        else:
            self.show_error_dialog("Config file not found")
            
    def initialize_biralo(self):
        def run_init():
            try:
                result = subprocess.run(
                    self.biralo_cmd + ["onboard"],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    self.after(0, lambda: self.show_success_dialog("Biralo initialized successfully!"))
                    self.after(0, self.load_config_status)
                    self.after(0, self.load_config_display)
                else:
                    self.after(0, lambda: self.show_error_dialog(f"Initialization failed: {result.stderr}"))
                    
            except FileNotFoundError:
                self.after(0, lambda: self.show_error_dialog("Biralo not found. Please install: pip install biralo-ai"))
            except Exception as e:
                self.after(0, lambda: self.show_error_dialog(f"Error: {str(e)}"))
                
        threading.Thread(target=run_init, daemon=True).start()
        
    def start_gateway(self):
        if self.gateway_process:
            self.gateway_log_message("Gateway already running")
            return
            
        def run_gateway():
            try:
                env = os.environ.copy()
                env['PYTHONIOENCODING'] = 'utf-8'
                
                self.gateway_process = subprocess.Popen(
                    self.biralo_cmd + ["gateway"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    env=env,
                    encoding='utf-8',
                    errors='replace'
                )
                
                self.after(0, lambda: self.start_gateway_btn.configure(state="disabled", fg_color=COLORS["bg_light"]))
                self.after(0, lambda: self.stop_gateway_btn.configure(state="normal", fg_color=COLORS["error"]))
                self.after(0, lambda: self.gateway_log_message("🚀 Gateway started"))
                
                for line in self.gateway_process.stdout:
                    self.after(0, lambda l=line.strip(): self.gateway_log_message(l))
                    
            except FileNotFoundError:
                self.after(0, lambda: self.gateway_log_message("Error: Biralo not found"))
            except Exception as e:
                self.after(0, lambda: self.gateway_log_message(f"Error: {str(e)}"))
            finally:
                self.gateway_process = None
                self.after(0, lambda: self.start_gateway_btn.configure(state="normal", fg_color=COLORS["success"]))
                self.after(0, lambda: self.stop_gateway_btn.configure(state="disabled", fg_color=COLORS["bg_light"]))
                
        threading.Thread(target=run_gateway, daemon=True).start()
        
    def stop_gateway(self):
        if self.gateway_process:
            self.gateway_process.terminate()
            self.gateway_log_message("Gateway stopped")
            self.gateway_process = None
            self.start_gateway_btn.configure(state="normal", fg_color=COLORS["success"])
            self.stop_gateway_btn.configure(state="disabled", fg_color=COLORS["bg_light"])
            
    def gateway_log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.gateway_log.insert("end", f"[{timestamp}] {message}\n")
        self.gateway_log.see("end")
        
    def show_success_dialog(self, message):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Success")
        dialog.geometry("400x200")
        dialog.configure(fg_color=COLORS["bg_dark"])
        dialog.transient(self)
        dialog.grab_set()
        
        card = ModernCard(dialog)
        card.pack(padx=20, pady=20, fill="both", expand=True)
        
        label = ctk.CTkLabel(
            card,
            text=f"✓  {message.upper()}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS["success"]
        )
        label.pack(pady=(40, 20))
        
        ModernButton(
            card,
            text="DISMISS",
            command=dialog.destroy,
            width=120,
            fg_color=COLORS["bg_light"]
        ).pack(pady=10)
        
    def show_error_dialog(self, message):
        dialog = ctk.CTkToplevel(self)
        dialog.title("System Error")
        dialog.geometry("400x200")
        dialog.configure(fg_color=COLORS["bg_dark"])
        dialog.transient(self)
        dialog.grab_set()
        
        card = ModernCard(dialog, border_color=COLORS["error"])
        card.pack(padx=20, pady=20, fill="both", expand=True)
        
        label = ctk.CTkLabel(
            card,
            text=f"✕  {message.upper()}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COLORS["error"]
        )
        label.pack(pady=(40, 20))
        
        ModernButton(
            card,
            text="UNDERSTOOD",
            command=dialog.destroy,
            width=140,
            fg_color=COLORS["error"]
        ).pack(pady=10)
        
    def open_url(self, url):
        import webbrowser
        webbrowser.open(url)
        
    def on_closing(self):
        if self.gateway_process:
            self.gateway_process.terminate()
        self.destroy()


if __name__ == "__main__":
    app = BiraloApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
