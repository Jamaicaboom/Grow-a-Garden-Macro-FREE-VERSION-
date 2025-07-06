import time
import pyautogui
import keyboard
import threading
from datetime import datetime, timedelta
from Webhook import log_purchase, send_hourly_report

# Global variables
MACRO_SPEED = 0.1
macro_running = False
UI_NAV_KEY = '\\'
selected_items = {}
webhook_url = ""

# Shop timer management
shop_timers = {
    "Seeds": {"time_left": 0, "total_time": 3600, "last_visited": None},     # 1 hour
    "Gears": {"time_left": 0, "total_time": 7200, "last_visited": None},     # 2 hours  
    "Eggs": {"time_left": 0, "total_time": 1800, "last_visited": None},      # 30 minutes
    "Cosmetics": {"time_left": 0, "total_time": 14400, "last_visited": None} # 4 hours
}

# Item indexes in shops (order matters for navigation)
SEED_ITEMS = [
    "Carrot Seed", "Strawberry Seed", "Blueberry Seed", "Orange Tulip",
    "Tomato Seed", "Daffodil Seed", "Watermelon Seed", "Pumpkin Seed",
    "Apple Seed", "Bamboo Seed", "Coconut Seed", "Cactus Seed",
    "Dragon Fruit Seed", "Mango Seed", "Grape Seed", "Mushroom Seed",
    "Pepper Seed", "Cacao Seed", "Beanstalk Seed", "Ember Lily",
    "Sugar Apple", "Burning Bud"
]

GEAR_ITEMS = [
    "Watering Can", "Trowel", "Recall Wrench", "Basic Sprinkler",
    "Advanced Sprinkler", "Godly Sprinkler", "Magnifying Glass", "Tanning Mirror",
    "Master Sprinkler", "Cleaning Spray", "Favorite Tool", "Harvest Tool", "Friendship Pot"
]

EGG_ITEMS = [
    "Common Egg", "Common Summer Egg", "Rare Summer Egg",
    "Mythical Egg", "Paradise Egg", "Bee Egg", "Bug Egg"
]

def set_macro_speed(new_speed):
    """Set the macro execution speed"""
    global MACRO_SPEED
    MACRO_SPEED = new_speed

def set_ui_nav_key(key):
    """Set the UI navigation key"""
    global UI_NAV_KEY
    UI_NAV_KEY = key

def stop_macro():
    """Stop the macro execution"""
    global macro_running
    macro_running = False

def get_selected_items():
    """Get the currently selected items"""
    return selected_items

def get_shop_timers():
    """Get current shop timer status"""
    return shop_timers

def update_shop_timer(shop_name, duration):
    """Update a shop's timer after visiting"""
    shop_timers[shop_name]["time_left"] = duration
    shop_timers[shop_name]["last_visited"] = datetime.now()

def check_shop_timers():
    """Update all shop timers based on elapsed time"""
    current_time = datetime.now()
    for shop_name, timer_data in shop_timers.items():
        if timer_data["last_visited"]:
            elapsed = (current_time - timer_data["last_visited"]).total_seconds()
            timer_data["time_left"] = max(0, timer_data["total_time"] - elapsed)

def is_shop_ready(shop_name):
    """Check if a shop is ready for purchase"""
    return shop_timers[shop_name]["time_left"] <= 0

def safe_press(key, times=1):
    """Safely press a key with macro speed delay"""
    for _ in range(times):
        if not macro_running:
            return False
        keyboard.press_and_release(key)
        time.sleep(MACRO_SPEED)
    return True

def safe_wait(duration):
    """Wait for a duration while checking if macro is still running"""
    end_time = time.time() + duration
    while time.time() < end_time:
        if not macro_running:
            return False
        time.sleep(0.1)
    return True

def scroll_mouse_up(amount=20):
    """Scroll mouse up (zoom in)"""
    for _ in range(amount):
        if not macro_running:
            return False
        pyautogui.scroll(200)
        time.sleep(min(MACRO_SPEED, 0.05))
    return True

def scroll_mouse_down(amount=8):
    """Scroll mouse down (zoom out)"""
    for _ in range(amount):
        if not macro_running:
            return False
        pyautogui.scroll(-200)
        time.sleep(min(MACRO_SPEED, 0.05))
    return True

def toggle_ui_navigation():
    """Toggle UI navigation on/off"""
    if not macro_running:
        return False
    safe_press(UI_NAV_KEY)
    safe_wait(0.15)
    return True

def open_inventory():
    """Open the inventory"""
    print("🎒 Opening inventory...")
    safe_press('tab')
    safe_wait(0.5)
    return True

def equip_recall_wrench():
    """Equip the recall wrench from inventory slot 2"""
    print("🔧 Equipping recall wrench...")
    open_inventory()
    safe_press('2')  # Press 2 to equip item in slot 2
    safe_wait(0.5)
    safe_press('tab')  # Close inventory
    safe_wait(0.5)
    return True

def use_recall_wrench():
    """Use the recall wrench to teleport"""
    print("🔧 Using recall wrench...")
    # Type "recall" to teleport
    keyboard.write("recall")
    safe_wait(0.5)
    safe_press('enter')
    safe_wait(2.0)  # Wait for teleport
    return True

def navigate_to_seed_shop():
    """Navigate to the seed shop"""
    print("🌱 Navigating to seed shop...")
    toggle_ui_navigation()
    
    # Navigate to Seeds button and press it
    safe_press('tab', 3)  # Navigate to Seeds button (adjust as needed)
    safe_press('enter')
    safe_wait(1.0)
    
    return True

def navigate_to_gear_shop():
    """Navigate to the gear shop using recall wrench"""
    print("⚙️ Navigating to gear shop...")
    use_recall_wrench()
    
    # Navigate to gear shop location
    safe_press('w', 5)  # Move forward (adjust as needed)
    safe_wait(0.5)
    
    # Zoom in close for gear shop interaction
    scroll_mouse_up(10)
    safe_wait(0.5)
    
    # Click to access gear shop
    safe_press('e')
    safe_wait(1.0)
    
    return True

def navigate_to_egg_shop():
    """Navigate to the egg shop"""
    print("🥚 Navigating to egg shop...")
    # Return camera to normal first
    scroll_mouse_down(10)
    safe_wait(0.5)
    
    # Walk forward to egg area
    safe_press('w', 3)
    safe_wait(1.0)
    
    return True

def navigate_to_cosmetic_shop():
    """Navigate to the cosmetic shop"""
    print("💄 Navigating to cosmetic shop...")
    # Navigate to cosmetic shop area
    safe_press('w', 2)
    safe_wait(1.0)
    
    return True

def buy_from_seed_shop(items_to_buy):
    """Buy selected items from seed shop"""
    print(f"🌱 Buying seeds: {items_to_buy}")
    
    # Interact with seed shop NPC
    safe_press('e')
    safe_wait(1.0)
    
    for item in items_to_buy:
        if item in SEED_ITEMS and macro_running:
            item_index = SEED_ITEMS.index(item)
            print(f"  💰 Buying {item} (index {item_index})")
            
            # Navigate to item and buy it
            # This is a simplified version - you may need to adjust navigation
            safe_press('tab', item_index + 1)  # Navigate to item
            safe_press('enter')  # Buy item
            safe_wait(0.5)
            
            log_purchase("Seeds", item)
    
    # Close shop
    safe_press('esc')
    safe_wait(0.5)
    
    # Update shop timer
    update_shop_timer("Seeds", shop_timers["Seeds"]["total_time"])
    
    return True

def buy_from_gear_shop(items_to_buy):
    """Buy selected items from gear shop"""
    print(f"⚙️ Buying gears: {items_to_buy}")
    
    for item in items_to_buy:
        if item in GEAR_ITEMS and macro_running:
            item_index = GEAR_ITEMS.index(item)
            print(f"  💰 Buying {item} (index {item_index})")
            
            # Navigate to item and buy it
            safe_press('tab', item_index + 1)  # Navigate to item
            safe_press('enter')  # Buy item
            safe_wait(0.5)
            
            log_purchase("Gears", item)
    
    # Close shop
    safe_press('esc')
    safe_wait(0.5)
    
    # Update shop timer
    update_shop_timer("Gears", shop_timers["Gears"]["total_time"])
    
    return True

def buy_from_egg_shop(items_to_buy):
    """Buy selected items from egg shop"""
    print(f"🥚 Buying eggs: {items_to_buy}")
    
    # There are 3 egg spots, we need to check each one
    for i in range(3):
        if not macro_running:
            break
            
        print(f"  🔍 Checking egg spot {i+1}")
        
        # Move to egg spot
        safe_press('a' if i == 0 else 'd', 2)  # Move left/right between spots
        safe_wait(0.5)
        
        # Check what egg is available
        safe_press('e')
        safe_wait(0.5)
        
        # For simplicity, we'll try to buy any selected egg
        # In reality, you'd need to identify which egg is at this spot
        for item in items_to_buy:
            if item in EGG_ITEMS and macro_running:
                print(f"  💰 Attempting to buy {item}")
                safe_press('enter')  # Buy egg
                safe_wait(0.5)
                log_purchase("Eggs", item)
                break
    
    # Update shop timer
    update_shop_timer("Eggs", shop_timers["Eggs"]["total_time"])
    
    return True

def buy_from_cosmetic_shop():
    """Buy all cosmetics from cosmetic shop"""
    print("💄 Buying all cosmetics...")
    
    # Navigate through all 9 cosmetic items
    for i in range(9):
        if not macro_running:
            break
            
        print(f"  💰 Buying cosmetic item {i+1}")
        
        # Navigate to cosmetic and buy it
        safe_press('tab', i + 1)  # Navigate to cosmetic
        safe_press('enter')  # Buy cosmetic
        safe_wait(0.5)
        
        log_purchase("Cosmetics", f"Cosmetic {i+1}")
    
    # Update shop timer
    update_shop_timer("Cosmetics", shop_timers["Cosmetics"]["total_time"])
    
    return True

def setup_initial_position():
    """Set up the initial camera position and UI state"""
    print("🔄 Setting up initial position...")
    
    # Adjust camera position
    scroll_mouse_up(20)      # Zoom in
    safe_wait(0.5)
    scroll_mouse_down(8)     # Zoom out slightly
    safe_wait(0.5)
    
    # Toggle UI navigation to reset state
    toggle_ui_navigation()
    safe_wait(0.2)
    toggle_ui_navigation()
    safe_wait(0.2)
    
    # Equip recall wrench
    equip_recall_wrench()
    
    print("✅ Initial setup completed.")
    return True

def run_macro_cycle():
    """Run one complete macro cycle through all shops"""
    print("🔄 Starting macro cycle...")
    
    # Check timers first
    check_shop_timers()
    
    # Visit seed shop if ready and items selected
    if (is_shop_ready("Seeds") and 
        selected_items.get("Seeds") and 
        macro_running):
        navigate_to_seed_shop()
        buy_from_seed_shop(selected_items["Seeds"])
    
    # Visit gear shop if ready and items selected
    if (is_shop_ready("Gears") and 
        selected_items.get("Gears") and 
        macro_running):
        navigate_to_gear_shop()
        buy_from_gear_shop(selected_items["Gears"])
    
    # Visit egg shop if ready and items selected
    if (is_shop_ready("Eggs") and 
        selected_items.get("Eggs") and 
        macro_running):
        navigate_to_egg_shop()
        buy_from_egg_shop(selected_items["Eggs"])
    
    # Visit cosmetic shop if ready and selected
    if (is_shop_ready("Cosmetics") and 
        selected_items.get("Cosmetics") and 
        macro_running):
        navigate_to_cosmetic_shop()
        buy_from_cosmetic_shop()
    
    print("✅ Macro cycle completed.")

def timer_update_thread():
    """Thread function to continuously update shop timers"""
    while macro_running:
        check_shop_timers()
        time.sleep(1)  # Update every second

def hourly_report_thread():
    """Thread function to send hourly webhook reports"""
    while macro_running:
        time.sleep(3600)  # Wait 1 hour
        if webhook_url and macro_running:
            send_hourly_report(webhook_url)

def run_macro(items, webhook):
    """Main macro execution function"""
    global macro_running, selected_items, webhook_url
    
    macro_running = True
    selected_items = items
    webhook_url = webhook
    
    print("🚀 Starting Grow a Garden macro...")
    print(f"📝 Selected items: {items}")
    
    # Initial setup
    if not setup_initial_position():
        return
    
    # Start timer update thread
    timer_thread = threading.Thread(target=timer_update_thread)
    timer_thread.daemon = True
    timer_thread.start()
    
    # Start hourly report thread if webhook is configured
    if webhook_url:
        report_thread = threading.Thread(target=hourly_report_thread)
        report_thread.daemon = True
        report_thread.start()
    
    # Main macro loop
    try:
        while macro_running:
            run_macro_cycle()
            
            # Wait a bit before next cycle
            if not safe_wait(10):  # 10 second wait between cycles
                break
                
    except KeyboardInterrupt:
        print("⏹ Macro interrupted by user.")
    except Exception as e:
        print(f"❌ Macro error: {e}")
    finally:
        macro_running = False
        print("⏹ Macro stopped.")

def test_webhook_func(webhook_url):
    """Test webhook function (for compatibility with old code)"""
    from Webhook import test_webhook
    return test_webhook(webhook_url)
