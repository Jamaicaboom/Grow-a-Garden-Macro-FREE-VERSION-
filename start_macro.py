#!/usr/bin/env python3
"""
Quick start script for the Grow a Garden Macro
This script will check dependencies and start the macro with better error handling.
"""
import sys
import os
import subprocess

def check_dependency(package_name, import_name):
    """Check if a dependency is installed"""
    try:
        __import__(import_name)
        return True
    except ImportError:
        return False

def install_dependencies():
    """Try to install missing dependencies"""
    print("📦 Installing dependencies...")
    
    # Try different pip commands
    pip_commands = ['pip', 'pip3', 'python -m pip', 'python3 -m pip']
    
    for cmd in pip_commands:
        try:
            print(f"Trying: {cmd} install -r requirements.txt")
            result = subprocess.run(
                f"{cmd} install -r requirements.txt", 
                shell=True, 
                capture_output=True, 
                text=True
            )
            
            if result.returncode == 0:
                print("✅ Dependencies installed successfully!")
                return True
            else:
                print(f"❌ Failed with {cmd}: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Error with {cmd}: {e}")
    
    print("\n❌ Could not install dependencies automatically.")
    print("Please install them manually using one of these commands:")
    print("  pip install -r requirements.txt")
    print("  pip3 install -r requirements.txt")
    print("  python -m pip install -r requirements.txt")
    print("  python3 -m pip install -r requirements.txt")
    
    return False

def check_all_dependencies():
    """Check if all required dependencies are available"""
    dependencies = [
        ('PyQt5', 'PyQt5.QtWidgets'),
        ('pyautogui', 'pyautogui'),
        ('keyboard', 'keyboard'),
        ('requests', 'requests'),
        ('Pillow', 'PIL')
    ]
    
    missing = []
    for dep_name, import_name in dependencies:
        if not check_dependency(dep_name, import_name):
            missing.append(dep_name)
    
    return missing

def main():
    """Main function to start the macro"""
    print("🌱 Grow a Garden Macro - Quick Start")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('main.py'):
        print("❌ main.py not found!")
        print("Please run this script from the macro directory.")
        return False
    
    # Check dependencies
    missing_deps = check_all_dependencies()
    
    if missing_deps:
        print(f"❌ Missing dependencies: {', '.join(missing_deps)}")
        
        # Ask user if they want to install dependencies
        try:
            response = input("\nWould you like to try installing them automatically? (y/n): ").lower()
            if response == 'y':
                if not install_dependencies():
                    return False
                
                # Check again after installation
                missing_deps = check_all_dependencies()
                if missing_deps:
                    print(f"❌ Still missing: {', '.join(missing_deps)}")
                    return False
            else:
                print("Please install the dependencies manually and try again.")
                return False
        except KeyboardInterrupt:
            print("\n❌ Installation cancelled.")
            return False
    
    print("✅ All dependencies are available!")
    print("🚀 Starting the macro...")
    
    # Try to start the macro
    try:
        import main
        # The main.py file should handle the GUI startup
        print("✅ Macro started successfully!")
        return True
    except Exception as e:
        print(f"❌ Error starting macro: {e}")
        print("\nTry running the macro manually with:")
        print("  python main.py")
        print("  or")
        print("  python3 main.py")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            input("\nPress Enter to exit...")
    except KeyboardInterrupt:
        print("\n❌ Startup cancelled.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        input("\nPress Enter to exit...")