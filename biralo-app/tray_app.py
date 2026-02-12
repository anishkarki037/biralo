"""
Biralo Desktop App with System Tray Support
Optional enhanced version with system tray icon
"""
import customtkinter as ctk
from main import BiraloApp
import sys

try:
    from pystray import Icon, Menu, MenuItem
    from PIL import Image, ImageDraw
    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False
    print("⚠️  System tray support not available")
    print("   Install with: pip install pystray pillow")


def create_icon_image():
    """Create a simple icon for the system tray"""
    # Create a 64x64 image with a cat emoji representation
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), 'black')
    dc = ImageDraw.Draw(image)
    
    # Draw a simple cat face
    # Ears
    dc.polygon([(10, 20), (20, 10), (25, 20)], fill='orange')
    dc.polygon([(54, 20), (44, 10), (39, 20)], fill='orange')
    
    # Face
    dc.ellipse([15, 20, 49, 54], fill='orange', outline='white')
    
    # Eyes
    dc.ellipse([22, 28, 28, 34], fill='white')
    dc.ellipse([36, 28, 42, 34], fill='white')
    dc.ellipse([24, 30, 26, 32], fill='black')
    dc.ellipse([38, 30, 40, 32], fill='black')
    
    # Nose
    dc.polygon([(32, 38), (30, 42), (34, 42)], fill='pink')
    
    # Mouth
    dc.arc([28, 40, 36, 46], 0, 180, fill='black')
    
    return image


class TrayBiraloApp(BiraloApp):
    """Enhanced Biralo app with system tray support"""
    
    def __init__(self):
        super().__init__()
        
        if TRAY_AVAILABLE:
            self.setup_tray()
        
        # Override close behavior
        self.protocol("WM_DELETE_WINDOW", self.hide_window)
        
    def setup_tray(self):
        """Setup system tray icon"""
        icon_image = create_icon_image()
        
        menu = Menu(
            MenuItem('Show', self.show_window),
            MenuItem('Hide', self.hide_window),
            Menu.SEPARATOR,
            MenuItem('Chat', lambda: self.show_and_focus('chat')),
            MenuItem('Gateway', lambda: self.show_and_focus('gateway')),
            MenuItem('Config', lambda: self.show_and_focus('config')),
            Menu.SEPARATOR,
            MenuItem('Exit', self.quit_app)
        )
        
        self.tray_icon = Icon("Biralo", icon_image, "Biralo AI Assistant", menu)
        
        # Run tray icon in separate thread
        import threading
        threading.Thread(target=self.tray_icon.run, daemon=True).start()
        
    def show_window(self, icon=None, item=None):
        """Show the main window"""
        self.deiconify()
        self.lift()
        self.focus_force()
        
    def hide_window(self):
        """Hide window to tray"""
        if TRAY_AVAILABLE:
            self.withdraw()
        else:
            self.quit_app()
            
    def show_and_focus(self, view):
        """Show window and switch to specific view"""
        self.show_window()
        if view == 'chat':
            self.show_chat()
        elif view == 'gateway':
            self.show_gateway()
        elif view == 'config':
            self.show_config()
            
    def quit_app(self, icon=None, item=None):
        """Completely quit the application"""
        if self.gateway_process:
            self.gateway_process.terminate()
        
        if TRAY_AVAILABLE and hasattr(self, 'tray_icon'):
            self.tray_icon.stop()
        
        self.destroy()
        sys.exit(0)


def main():
    if TRAY_AVAILABLE:
        print("🐈 Starting Biralo Desktop App with system tray support...")
        app = TrayBiraloApp()
    else:
        print("🐈 Starting Biralo Desktop App...")
        app = BiraloApp()
        app.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    app.mainloop()


if __name__ == "__main__":
    main()
