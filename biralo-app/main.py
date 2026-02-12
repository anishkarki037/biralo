"""
Biralo Desktop App - Modern GUI for Biralo AI Assistant
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

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def get_biralo_command():
    """Get the correct biralo command based on environment"""
    # First, try to find 'biralo' in PATH
    if shutil.which("biralo"):
        return ["biralo"]
    
    # Check if we're in a virtual environment
    venv_python = None
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        # We're in a venv, use the venv's python
        venv_python = sys.executable
    
    # Try current directory's venv
    if not venv_python:
        venv_paths = [
            Path("venv/Scripts/python.exe"),  # Windows
            Path("venv/bin/python"),           # Unix
            Path("../venv/Scripts/python.exe"),
            Path("../venv/bin/python"),
        ]
        for venv_path in venv_paths:
            if venv_path.exists():
                venv_python = str(venv_path.absolute())
                break
    
    # Try the venv python if found
    if venv_python:
        try:
            result = subprocess.run(
                [venv_python, "-m", "biralo", "--help"],
                capture_output=True,
                timeout=2
            )
            if result.returncode == 0:
                return [venv_python, "-m", "biralo"]
        except:
            pass
    
    # Try with 'python' command (might be in venv)
    try:
        result = subprocess.run(
            ["python", "-m", "biralo", "--help"],
            capture_output=True,
            timeout=2
        )
        if result.returncode == 0:
            return ["python", "-m", "biralo"]
    except:
        pass
    
    # Try with 'python3' command
    try:
        result = subprocess.run(
            ["python3", "-m", "biralo", "--help"],
            capture_output=True,
            timeout=2
        )
        if result.returncode == 0:
            return ["python3", "-m", "biralo"]
    except:
        pass
    
    # Try current sys.executable as last resort
    try:
        result = subprocess.run(
            [sys.executable, "-m", "biralo", "--help"],
            capture_output=True,
            timeout=2
        )
        if result.returncode == 0:
            return [sys.executable, "-m", "biralo"]
    except:
        pass
    
    # Default fallback - use 'python' and hope for the best
    return ["python", "-m", "biralo"]


class BiraloApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.title("🐈 Biralo AI Assistant")
        self.geometry("1200x800")
        self.minsize(900, 600)
        
        # Config path
        self.config_path = Path.home() / ".biralo" / "config.json"
        
        # State
        self.chat_history = []
        self.gateway_process = None
        
        # Get biralo command
        self.biralo_cmd = get_biralo_command()
        print(f"Using Biralo command: {' '.join(self.biralo_cmd)}")  # Debug info
        
        # Setup UI
        self.setup_ui()
        self.load_config_status()
        
    def setup_ui(self):
        # Grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.grid_rowconfigure(6, weight=1)
        
        # Logo
        try:
            # Try to load the logo image
            logo_path = Path(__file__).parent.parent / "biralo-logo.png"
            if logo_path.exists():
                from PIL import Image
                logo_image = Image.open(logo_path)
                # Resize to fit sidebar
                logo_image = logo_image.resize((200, 200), Image.Resampling.LANCZOS)
                logo_photo = ctk.CTkImage(light_image=logo_image, dark_image=logo_image, size=(200, 200))
                self.logo_label = ctk.CTkLabel(self.sidebar, image=logo_photo, text="")
                self.logo_label.image = logo_photo  # Keep a reference
            else:
                # Fallback to text if image not found
                self.logo_label = ctk.CTkLabel(
                    self.sidebar, 
                    text="🐈 Biralo", 
                    font=ctk.CTkFont(size=28, weight="bold")
                )
        except Exception:
            # Fallback to text if image loading fails
            self.logo_label = ctk.CTkLabel(
                self.sidebar, 
                text="🐈 Biralo", 
                font=ctk.CTkFont(size=28, weight="bold")
            )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Status indicator
        self.status_frame = ctk.CTkFrame(self.sidebar)
        self.status_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.status_label = ctk.CTkLabel(
            self.status_frame, 
            text="● Offline", 
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=5)
        
        # Navigation buttons
        self.chat_btn = ctk.CTkButton(
            self.sidebar, 
            text="💬 Chat", 
            command=self.show_chat,
            height=40
        )
        self.chat_btn.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.config_btn = ctk.CTkButton(
            self.sidebar, 
            text="⚙️ Configuration", 
            command=self.show_config,
            height=40
        )
        self.config_btn.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        self.gateway_btn = ctk.CTkButton(
            self.sidebar, 
            text="🌐 Gateway", 
            command=self.show_gateway,
            height=40
        )
        self.gateway_btn.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        
        self.about_btn = ctk.CTkButton(
            self.sidebar, 
            text="ℹ️ About", 
            command=self.show_about,
            height=40
        )
        self.about_btn.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        
        # Theme toggle
        self.theme_switch = ctk.CTkSwitch(
            self.sidebar, 
            text="Dark Mode",
            command=self.toggle_theme,
            onvalue="dark",
            offvalue="light"
        )
        self.theme_switch.grid(row=7, column=0, padx=20, pady=20, sticky="s")
        self.theme_switch.select()
        
        # Main content area
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Create all views
        self.create_chat_view()
        self.create_config_view()
        self.create_gateway_view()
        self.create_about_view()
        
        # Show chat by default
        self.show_chat()
        
    def create_chat_view(self):
        self.chat_view = ctk.CTkFrame(self.main_frame)
        self.chat_view.grid_columnconfigure(0, weight=1)
        self.chat_view.grid_rowconfigure(0, weight=1)
        
        # Chat display with scrollable frame for message bubbles
        self.chat_scroll = ctk.CTkScrollableFrame(
            self.chat_view,
            fg_color=("gray95", "gray10")
        )
        self.chat_scroll.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="nsew")
        self.chat_scroll.grid_columnconfigure(0, weight=1)
        
        # Welcome message
        welcome_frame = ctk.CTkFrame(self.chat_scroll, fg_color="transparent")
        welcome_frame.grid(row=0, column=0, pady=20, sticky="ew")
        
        welcome_text = ctk.CTkLabel(
            welcome_frame,
            text="👋 Welcome to Biralo!\nAsk me anything...",
            font=ctk.CTkFont(size=16),
            text_color=("gray50", "gray60")
        )
        welcome_text.pack()
        
        self.message_row = 1  # Track row for new messages
        
        # Input frame
        self.input_frame = ctk.CTkFrame(self.chat_view, fg_color="transparent")
        self.input_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        # Input with better styling
        self.chat_input = ctk.CTkEntry(
            self.input_frame, 
            placeholder_text="Type your message...",
            height=50,
            font=ctk.CTkFont(size=14),
            border_width=2,
            corner_radius=25
        )
        self.chat_input.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.chat_input.bind("<Return>", lambda e: self.send_message())
        
        # Send button with icon
        self.send_btn = ctk.CTkButton(
            self.input_frame, 
            text="Send ➤",
            command=self.send_message,
            width=100,
            height=50,
            corner_radius=25,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("#3B8ED0", "#1F6AA5"),
            hover_color=("#2E7AB8", "#144870")
        )
        self.send_btn.grid(row=0, column=1)
        
        self.clear_btn = ctk.CTkButton(
            self.input_frame, 
            text="Clear",
            command=self.clear_chat,
            width=80,
            height=50,
            corner_radius=25,
            font=ctk.CTkFont(size=14),
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40")
        )
        self.clear_btn.grid(row=0, column=2, padx=(10, 0))
        
    def create_config_view(self):
        self.config_view = ctk.CTkFrame(self.main_frame)
        self.config_view.grid_columnconfigure(0, weight=1)
        self.config_view.grid_rowconfigure(1, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            self.config_view, 
            text="Configuration",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Config display
        self.config_display = ctk.CTkTextbox(
            self.config_view,
            font=ctk.CTkFont(family="Courier", size=12)
        )
        self.config_display.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="nsew")
        
        # Buttons
        btn_frame = ctk.CTkFrame(self.config_view)
        btn_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        self.reload_config_btn = ctk.CTkButton(
            btn_frame, 
            text="Reload Config",
            command=self.load_config_display,
            height=40
        )
        self.reload_config_btn.pack(side="left", padx=(0, 10))
        
        self.open_config_btn = ctk.CTkButton(
            btn_frame, 
            text="Open in Editor",
            command=self.open_config_file,
            height=40
        )
        self.open_config_btn.pack(side="left", padx=(0, 10))
        
        self.init_btn = ctk.CTkButton(
            btn_frame, 
            text="Initialize Biralo",
            command=self.initialize_biralo,
            height=40,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.init_btn.pack(side="left")
        
    def create_gateway_view(self):
        self.gateway_view = ctk.CTkFrame(self.main_frame)
        self.gateway_view.grid_columnconfigure(0, weight=1)
        self.gateway_view.grid_rowconfigure(1, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            self.gateway_view, 
            text="Gateway Control",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Gateway log
        self.gateway_log = ctk.CTkTextbox(
            self.gateway_view,
            font=ctk.CTkFont(family="Courier", size=11)
        )
        self.gateway_log.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="nsew")
        
        # Control buttons
        btn_frame = ctk.CTkFrame(self.gateway_view)
        btn_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        self.start_gateway_btn = ctk.CTkButton(
            btn_frame, 
            text="▶ Start Gateway",
            command=self.start_gateway,
            height=40,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.start_gateway_btn.pack(side="left", padx=(0, 10))
        
        self.stop_gateway_btn = ctk.CTkButton(
            btn_frame, 
            text="⏹ Stop Gateway",
            command=self.stop_gateway,
            height=40,
            fg_color="red",
            hover_color="darkred",
            state="disabled"
        )
        self.stop_gateway_btn.pack(side="left", padx=(0, 10))
        
        self.clear_log_btn = ctk.CTkButton(
            btn_frame, 
            text="Clear Log",
            command=lambda: self.gateway_log.delete("1.0", "end"),
            height=40,
            fg_color="gray40",
            hover_color="gray30"
        )
        self.clear_log_btn.pack(side="left")
        
    def create_about_view(self):
        self.about_view = ctk.CTkFrame(self.main_frame)
        self.about_view.grid_columnconfigure(0, weight=1)
        
        # Logo
        logo = ctk.CTkLabel(
            self.about_view, 
            text="🐈",
            font=ctk.CTkFont(size=80)
        )
        logo.grid(row=0, column=0, pady=(40, 20))
        
        # Title
        title = ctk.CTkLabel(
            self.about_view, 
            text="Biralo AI Assistant",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.grid(row=1, column=0, pady=10)
        
        # Version
        version = ctk.CTkLabel(
            self.about_view, 
            text="Version 0.1.3",
            font=ctk.CTkFont(size=14)
        )
        version.grid(row=2, column=0, pady=5)
        
        # Description
        desc = ctk.CTkLabel(
            self.about_view, 
            text="Ultra-lightweight personal AI assistant\n~4,000 lines of core code",
            font=ctk.CTkFont(size=14),
            justify="center"
        )
        desc.grid(row=3, column=0, pady=20)
        
        # Links
        links_frame = ctk.CTkFrame(self.about_view)
        links_frame.grid(row=4, column=0, pady=20)
        
        github_btn = ctk.CTkButton(
            links_frame, 
            text="GitHub",
            command=lambda: self.open_url("https://github.com/HKUDS/biralo"),
            width=150,
            height=40
        )
        github_btn.pack(pady=5)
        
        docs_btn = ctk.CTkButton(
            links_frame, 
            text="Documentation",
            command=lambda: self.open_url("https://github.com/HKUDS/biralo#readme"),
            width=150,
            height=40
        )
        docs_btn.pack(pady=5)
        
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
        
    def send_message(self):
        message = self.chat_input.get().strip()
        if not message:
            return
            
        # Display user message
        self.display_message("You", message)
        self.chat_input.delete(0, "end")
        
        # Send to Biralo in background
        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()
        
    def process_message(self, message):
        try:
            # Try to use Biralo API directly to avoid console encoding issues
            try:
                import asyncio
                from biralo.agent.loop import AgentLoop
                from biralo.config.loader import load_config
                from biralo.bus.queue import MessageBus
                from biralo.providers.litellm_provider import LiteLLMProvider
                
                async def get_response():
                    config = load_config()
                    bus = MessageBus()
                    
                    # Create provider
                    p = config.get_provider()
                    model = config.agents.defaults.model
                    
                    provider = LiteLLMProvider(
                        api_key=p.api_key if p else None,
                        api_base=config.get_api_base(),
                        default_model=model,
                        extra_headers=p.extra_headers if p else None,
                        provider_name=config.get_provider_name(),
                    )
                    
                    # Create agent loop
                    agent = AgentLoop(
                        bus=bus,
                        provider=provider,
                        workspace=config.workspace_path,
                        brave_api_key=config.tools.web.search.api_key if hasattr(config.tools.web, 'search') else None,
                        exec_config=config.tools.exec,
                        restrict_to_workspace=config.tools.restrict_to_workspace,
                    )
                    
                    response = await agent.process_direct(message, session_key="desktop-app")
                    return response
                
                # Run in thread to avoid blocking UI
                def run_async():
                    try:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        response = loop.run_until_complete(get_response())
                        loop.close()
                        
                        if response:
                            self.after(0, lambda r=response: self.display_message("Biralo", r))
                        else:
                            self.after(0, lambda: self.display_message("System", "No response"))
                    except Exception as err:
                        error_msg = str(err)
                        self.after(0, lambda msg=error_msg: self.display_message("System", f"Error: {msg}"))
                
                import threading
                threading.Thread(target=run_async, daemon=True).start()
                return
                
            except ImportError as import_err:
                # Fall back to CLI if direct import fails
                self.display_message("System", f"Direct API unavailable, using CLI fallback")
            except Exception as api_err:
                # If API fails, fall back to CLI
                self.display_message("System", f"API error, using CLI fallback: {str(api_err)}")
            
            # Fallback: Use CLI with encoding workarounds
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
                self.display_message("Biralo", output)
            else:
                self.display_message("System", "No response received. Try: python -m biralo agent -m \"your message\"")
            
        except subprocess.TimeoutExpired:
            self.display_message("System", "Request timed out")
        except Exception as e:
            self.display_message("System", f"Error: {str(e)}")
            
    def display_message(self, sender, message):
        timestamp = datetime.now().strftime("%H:%M")
        
        # Create message bubble frame
        msg_container = ctk.CTkFrame(self.chat_scroll, fg_color="transparent")
        msg_container.grid(row=self.message_row, column=0, pady=8, padx=10, sticky="ew")
        msg_container.grid_columnconfigure(0, weight=1)
        
        if sender == "You":
            # User message - right aligned, blue
            bubble_frame = ctk.CTkFrame(msg_container, fg_color="transparent")
            bubble_frame.grid(row=0, column=0, sticky="e")
            
            bubble = ctk.CTkFrame(
                bubble_frame,
                fg_color=("#3B8ED0", "#1F6AA5"),
                corner_radius=20
            )
            bubble.pack(side="right", padx=5)
            
            # Sender and time
            header = ctk.CTkLabel(
                bubble,
                text=f"{sender} • {timestamp}",
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=("white", "white")
            )
            header.pack(anchor="e", padx=15, pady=(8, 2))
            
            # Message text
            msg_label = ctk.CTkLabel(
                bubble,
                text=message,
                font=ctk.CTkFont(size=13),
                text_color=("white", "white"),
                wraplength=500,
                justify="left"
            )
            msg_label.pack(anchor="w", padx=15, pady=(2, 10))
            
        elif sender == "Biralo":
            # AI message - left aligned, gray
            bubble_frame = ctk.CTkFrame(msg_container, fg_color="transparent")
            bubble_frame.grid(row=0, column=0, sticky="w")
            
            bubble = ctk.CTkFrame(
                bubble_frame,
                fg_color=("gray85", "gray20"),
                corner_radius=20
            )
            bubble.pack(side="left", padx=5)
            
            # Sender and time with icon
            header = ctk.CTkLabel(
                bubble,
                text=f"🐈 {sender} • {timestamp}",
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=("#3B8ED0", "#1F6AA5")
            )
            header.pack(anchor="w", padx=15, pady=(8, 2))
            
            # Message text
            msg_label = ctk.CTkLabel(
                bubble,
                text=message,
                font=ctk.CTkFont(size=13),
                text_color=("gray10", "gray90"),
                wraplength=500,
                justify="left"
            )
            msg_label.pack(anchor="w", padx=15, pady=(2, 10))
            
        else:
            # System message - centered, orange/yellow
            bubble_frame = ctk.CTkFrame(msg_container, fg_color="transparent")
            bubble_frame.grid(row=0, column=0)
            
            bubble = ctk.CTkFrame(
                bubble_frame,
                fg_color=("orange", "darkorange"),
                corner_radius=15
            )
            bubble.pack(padx=5)
            
            # System icon and message
            msg_label = ctk.CTkLabel(
                bubble,
                text=f"⚠️ {message}",
                font=ctk.CTkFont(size=12),
                text_color=("white", "white"),
                wraplength=600,
                justify="center"
            )
            msg_label.pack(padx=15, pady=8)
        
        self.message_row += 1
        
        # Auto-scroll to bottom
        self.chat_scroll._parent_canvas.yview_moveto(1.0)
        
    def clear_chat(self):
        # Remove all message widgets
        for widget in self.chat_scroll.winfo_children():
            widget.destroy()
        
        # Reset and add welcome message
        self.message_row = 0
        welcome_frame = ctk.CTkFrame(self.chat_scroll, fg_color="transparent")
        welcome_frame.grid(row=0, column=0, pady=20, sticky="ew")
        
        welcome_text = ctk.CTkLabel(
            welcome_frame,
            text="👋 Welcome to Biralo!\nAsk me anything...",
            font=ctk.CTkFont(size=16),
            text_color=("gray50", "gray60")
        )
        welcome_text.pack()
        
        self.message_row = 1
        
    def load_config_status(self):
        if self.config_path.exists():
            self.status_label.configure(text="● Configured", text_color="green")
        else:
            self.status_label.configure(text="● Not Configured", text_color="orange")
            
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
            self.config_display.insert("1.0", "Config file not found. Click 'Initialize Biralo' to create it.")
            
    def open_config_file(self):
        if self.config_path.exists():
            if sys.platform == "win32":
                os.startfile(self.config_path)
            elif sys.platform == "darwin":
                subprocess.run(["open", self.config_path])
            else:
                subprocess.run(["xdg-open", self.config_path])
        else:
            self.show_error("Config file not found")
            
    def initialize_biralo(self):
        def run_init():
            try:
                result = subprocess.run(
                    self.biralo_cmd + ["onboard"],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    self.after(0, lambda: self.show_success("Biralo initialized successfully!"))
                    self.after(0, self.load_config_status)
                    self.after(0, self.load_config_display)
                else:
                    self.after(0, lambda: self.show_error(f"Initialization failed: {result.stderr}"))
                    
            except FileNotFoundError:
                self.after(0, lambda: self.show_error("Biralo not found. Please install: pip install biralo-ai"))
            except Exception as e:
                self.after(0, lambda: self.show_error(f"Error: {str(e)}"))
                
        threading.Thread(target=run_init, daemon=True).start()
        
    def start_gateway(self):
        if self.gateway_process:
            self.gateway_log_message("Gateway already running")
            return
            
        def run_gateway():
            try:
                # Set UTF-8 encoding for Windows
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
                    errors='replace'  # Replace problematic characters
                )
                
                self.after(0, lambda: self.start_gateway_btn.configure(state="disabled"))
                self.after(0, lambda: self.stop_gateway_btn.configure(state="normal"))
                self.after(0, lambda: self.gateway_log_message("Gateway started"))
                
                # Read output
                for line in self.gateway_process.stdout:
                    self.after(0, lambda l=line: self.gateway_log_message(l.strip()))
                    
            except FileNotFoundError:
                self.after(0, lambda: self.gateway_log_message("Error: Biralo not found"))
            except Exception as e:
                self.after(0, lambda: self.gateway_log_message(f"Error: {str(e)}"))
            finally:
                self.gateway_process = None
                self.after(0, lambda: self.start_gateway_btn.configure(state="normal"))
                self.after(0, lambda: self.stop_gateway_btn.configure(state="disabled"))
                
        threading.Thread(target=run_gateway, daemon=True).start()
        
    def stop_gateway(self):
        if self.gateway_process:
            self.gateway_process.terminate()
            self.gateway_log_message("Gateway stopped")
            self.gateway_process = None
            self.start_gateway_btn.configure(state="normal")
            self.stop_gateway_btn.configure(state="disabled")
            
    def gateway_log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.gateway_log.insert("end", f"[{timestamp}] {message}\n")
        self.gateway_log.see("end")
        
    def show_success(self, message):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Success")
        dialog.geometry("400x150")
        
        label = ctk.CTkLabel(dialog, text=message, font=ctk.CTkFont(size=14))
        label.pack(pady=30)
        
        btn = ctk.CTkButton(dialog, text="OK", command=dialog.destroy, width=100)
        btn.pack(pady=10)
        
    def show_error(self, message):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Error")
        dialog.geometry("400x150")
        
        label = ctk.CTkLabel(dialog, text=message, font=ctk.CTkFont(size=14), text_color="red")
        label.pack(pady=30)
        
        btn = ctk.CTkButton(dialog, text="OK", command=dialog.destroy, width=100)
        btn.pack(pady=10)
        
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
