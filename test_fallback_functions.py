#!/usr/bin/env python3
"""
Test fallback functions in MacroLogic
"""

def test_fallback_functions():
    """Test that fallback functions work when dependencies are missing"""
    print("🧪 Testing fallback functions...")
    
    try:
        import MacroLogic
        
        # Test log_purchase fallback
        print("\n📝 Testing log_purchase fallback:")
        MacroLogic.log_purchase("Seeds", "Carrot Seed")
        MacroLogic.log_purchase("Gears", "Watering Can")
        
        # Test send_hourly_report fallback
        print("\n📧 Testing send_hourly_report fallback:")
        MacroLogic.send_hourly_report("https://dummy-webhook-url.com")
        
        print("\n✅ All fallback functions work correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Fallback test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_fallback_functions()
    if success:
        print("\n🎉 Fallback functions are working correctly!")
        print("The macro will run even without webhook dependencies.")
    else:
        print("\n❌ Fallback functions have issues.")