#!/usr/bin/env python3
"""
Simple macro test without GUI dependencies
This helps debug macro startup issues
"""

def test_macro_import():
    """Test if we can import the macro logic"""
    try:
        print("🧪 Testing macro imports...")
        
        # Test MacroLogic import
        try:
            import MacroLogic
            print("✅ MacroLogic imported successfully")
        except Exception as e:
            print(f"❌ MacroLogic import failed: {e}")
            return False
        
        # Test basic functions
        try:
            MacroLogic.set_macro_speed(0.1)
            print("✅ set_macro_speed works")
        except Exception as e:
            print(f"❌ set_macro_speed failed: {e}")
            return False
        
        # Test timer functions
        try:
            timers = MacroLogic.get_shop_timers()
            print(f"✅ get_shop_timers works: {timers}")
        except Exception as e:
            print(f"❌ get_shop_timers failed: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_macro_with_dummy_data():
    """Test macro with dummy data (no actual key presses)"""
    try:
        print("🧪 Testing macro with dummy data...")
        
        import MacroLogic
        
        # Test data
        test_items = {
            "Seeds": ["Carrot Seed", "Strawberry Seed"],
            "Gears": ["Watering Can"],
            "Eggs": ["Common Egg"],
            "Cosmetics": []
        }
        
        print(f"📝 Test items: {test_items}")
        
        # Test various functions
        MacroLogic.selected_items = test_items
        selected = MacroLogic.get_selected_items()
        print(f"✅ Selected items test: {selected}")
        
        # Test timer functions
        MacroLogic.check_shop_timers()
        next_shop, next_time = MacroLogic.get_next_restock_time()
        print(f"✅ Timer test - Next: {next_shop}, Time: {next_time}")
        
        print("✅ All basic tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Dummy data test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dependencies():
    """Test if dependencies are available"""
    deps_available = True
    
    try:
        import pyautogui
        print("✅ pyautogui available")
    except ImportError:
        print("❌ pyautogui missing")
        deps_available = False
    
    try:
        import keyboard
        print("✅ keyboard available")
    except ImportError:
        print("❌ keyboard missing")
        deps_available = False
    
    try:
        import requests
        print("✅ requests available")
    except ImportError:
        print("❌ requests missing")
        deps_available = False
    
    return deps_available

def main():
    """Run all tests"""
    print("🧪 Simple Macro Test")
    print("=" * 50)
    
    # Test 1: Dependencies
    print("\n1. Testing dependencies...")
    deps_ok = test_dependencies()
    
    # Test 2: Imports
    print("\n2. Testing imports...")
    import_ok = test_macro_import()
    
    # Test 3: Basic functionality
    print("\n3. Testing basic functionality...")
    basic_ok = test_macro_with_dummy_data()
    
    # Summary
    print("\n" + "=" * 50)
    if deps_ok and import_ok and basic_ok:
        print("🎉 All tests passed! The macro should work.")
        print("\nTo start the full macro:")
        print("1. Select some items in the GUI")
        print("2. Press F1 or click Start Macro")
        print("3. Make sure Roblox is running and focused")
    else:
        print("❌ Some tests failed:")
        if not deps_ok:
            print("  - Install dependencies: pip install -r requirements.txt")
        if not import_ok:
            print("  - Check MacroLogic.py for errors")
        if not basic_ok:
            print("  - Check macro logic for issues")

if __name__ == "__main__":
    main()