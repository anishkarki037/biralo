"""
Test script for Biralo Desktop App
Run this to verify installation and basic functionality
"""
import sys
import subprocess
from pathlib import Path


def test_python_version():
    """Test Python version"""
    print("Testing Python version...")
    if sys.version_info >= (3, 11):
        print(f"✅ Python {sys.version.split()[0]} - OK")
        return True
    else:
        print(f"❌ Python {sys.version.split()[0]} - Need 3.11+")
        return False


def test_import(module_name):
    """Test if a module can be imported"""
    try:
        __import__(module_name)
        print(f"✅ {module_name} - OK")
        return True
    except ImportError:
        print(f"❌ {module_name} - Not found")
        return False


def test_biralo_cli():
    """Test if Biralo CLI is available"""
    print("Testing Biralo CLI...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "biralo", "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✅ Biralo CLI - OK")
            return True
        else:
            print("❌ Biralo CLI - Error")
            return False
    except FileNotFoundError:
        print("❌ Biralo CLI - Not found")
        return False
    except Exception as e:
        print(f"❌ Biralo CLI - Error: {e}")
        return False


def test_config_path():
    """Test if config directory exists"""
    print("Testing config path...")
    config_path = Path.home() / ".biralo"
    if config_path.exists():
        print(f"✅ Config directory - OK ({config_path})")
        
        config_file = config_path / "config.json"
        if config_file.exists():
            print(f"✅ Config file - OK")
        else:
            print(f"⚠️  Config file - Not found (run 'biralo onboard')")
        return True
    else:
        print(f"⚠️  Config directory - Not found ({config_path})")
        print("   Run 'biralo onboard' to initialize")
        return True  # Not a failure, just not initialized


def test_app_files():
    """Test if app files exist"""
    print("Testing app files...")
    files = [
        "main.py",
        "requirements.txt",
        "README.md",
        "QUICKSTART.md"
    ]
    
    all_ok = True
    for file in files:
        if Path(file).exists():
            print(f"✅ {file} - OK")
        else:
            print(f"❌ {file} - Not found")
            all_ok = False
    
    return all_ok


def test_optional_features():
    """Test optional features"""
    print("\nTesting optional features...")
    
    # System tray
    try:
        import pystray
        import PIL
        print("✅ System tray support - Available")
    except ImportError:
        print("⚠️  System tray support - Not available (optional)")
    
    # Windows shortcuts
    if sys.platform == "win32":
        try:
            import winshell
            import win32com
            print("✅ Desktop shortcuts - Available")
        except ImportError:
            print("⚠️  Desktop shortcuts - Not available (optional)")


def main():
    print("=" * 60)
    print("🐈 Biralo Desktop App - Test Suite")
    print("=" * 60)
    print()
    
    results = []
    
    # Core tests
    results.append(("Python Version", test_python_version()))
    results.append(("customtkinter", test_import("customtkinter")))
    results.append(("Biralo CLI", test_biralo_cli()))
    results.append(("Config Path", test_config_path()))
    results.append(("App Files", test_app_files()))
    
    # Optional tests
    test_optional_features()
    
    # Summary
    print()
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print()
        print("🎉 All tests passed! You're ready to run the app.")
        print()
        print("To launch:")
        print("  python main.py")
        print()
        print("Or with system tray:")
        print("  python tray_app.py")
        return 0
    else:
        print()
        print("⚠️  Some tests failed. Please check the errors above.")
        print()
        print("To fix:")
        print("  pip install -r requirements.txt")
        print("  biralo onboard")
        return 1


if __name__ == "__main__":
    sys.exit(main())
