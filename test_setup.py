#!/usr/bin/env python3
"""
Test script to verify the Grow a Garden macro setup
"""
import sys
import os

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ required")
        return False
    print("✅ Python version compatible")
    return True

def check_dependencies():
    """Check if required dependencies are available"""
    dependencies = [
        ('PyQt5', 'PyQt5.QtWidgets'),
        ('pyautogui', 'pyautogui'),
        ('keyboard', 'keyboard'),
        ('requests', 'requests'),
        ('PIL', 'PIL')
    ]
    
    missing = []
    for dep_name, import_name in dependencies:
        try:
            __import__(import_name)
            print(f"✅ {dep_name} available")
        except ImportError:
            print(f"❌ {dep_name} missing")
            missing.append(dep_name)
    
    if missing:
        print(f"\n📦 Install missing dependencies with:")
        print("pip install -r requirements.txt")
        return False
    
    return True

def check_files():
    """Check if all required files exist"""
    required_files = [
        'main.py',
        'MacroLogic.py',
        'Webhook.py',
        'requirements.txt',
        'Images/Close.png',
        'Images/Minimize.png'
    ]
    
    missing = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            missing.append(file_path)
    
    if missing:
        print(f"\n📁 Missing files: {missing}")
        return False
    
    return True

def test_imports():
    """Test if the main modules can be imported"""
    try:
        import main
        print("✅ main.py imports successfully")
    except Exception as e:
        print(f"❌ main.py import failed: {e}")
        return False
    
    try:
        import MacroLogic
        print("✅ MacroLogic.py imports successfully")
    except Exception as e:
        print(f"❌ MacroLogic.py import failed: {e}")
        return False
    
    try:
        import Webhook
        print("✅ Webhook.py imports successfully")
    except Exception as e:
        print(f"❌ Webhook.py import failed: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 Testing Grow a Garden Macro Setup")
    print("=" * 50)
    
    all_passed = True
    
    print("\n1. Checking Python version...")
    if not check_python_version():
        all_passed = False
    
    print("\n2. Checking required files...")
    if not check_files():
        all_passed = False
    
    print("\n3. Checking dependencies...")
    if not check_dependencies():
        all_passed = False
    
    print("\n4. Testing imports...")
    if not test_imports():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All tests passed! The macro is ready to use.")
        print("\nTo start the macro, run:")
        print("python3 main.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("\nIf you're missing dependencies, install them with:")
        print("pip install -r requirements.txt")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)