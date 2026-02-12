"""
Installation helper for Biralo Desktop App
"""
import subprocess
import sys
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.11+"""
    if sys.version_info < (3, 11):
        print("❌ Python 3.11 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def install_dependencies():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False


    def check_biralo():
    """Check if Biralo is installed"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "biralo", "--help"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ Biralo is installed")
            return True
    except FileNotFoundError:
        pass
    
    print("⚠️  Biralo not found")
    print("   Installing Biralo...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "biralo-ai"])
        print("✅ Biralo installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Biralo")
        return False


def create_desktop_shortcut():
    """Create desktop shortcut (Windows only)"""
    if sys.platform != "win32":
        return
    
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = Path(desktop) / "Biralo.lnk"
        target = str(Path(__file__).parent / "main.py")
        icon = str(Path(__file__).parent / "main.py")
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(str(path))
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{target}"'
        shortcut.WorkingDirectory = str(Path(__file__).parent)
        shortcut.IconLocation = icon
        shortcut.save()
        
        print("✅ Desktop shortcut created")
    except ImportError:
        print("⚠️  Could not create desktop shortcut (pywin32 not installed)")
    except Exception as e:
        print(f"⚠️  Could not create desktop shortcut: {e}")


def main():
    print("🐈 Biralo Desktop App - Installation")
    print("=" * 50)
    
    if not check_python_version():
        sys.exit(1)
    
    if not install_dependencies():
        sys.exit(1)
    
    if not check_biralo():
        sys.exit(1)
    
    create_desktop_shortcut()
    
    print("\n" + "=" * 50)
    print("✅ Installation complete!")
    print("\nTo launch the app:")
    print("  python main.py")
    print("\nOr use the launcher:")
    if sys.platform == "win32":
        print("  launch.bat")
    else:
        print("  ./launch.sh")
    print("=" * 50)


if __name__ == "__main__":
    main()
