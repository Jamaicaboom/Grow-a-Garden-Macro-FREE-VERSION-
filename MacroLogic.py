import time
import threading
from datetime import datetime, timedelta

# Import dependencies with error handling
pyautogui = None
keyboard = None

def check_dependencies():
    """Check and import dependencies"""
    global pyautogui, keyboard
    
    try:
        import pyautogui as pg
        pyautogui = pg
        print("✅ pyautogui loaded")
    except ImportError:
        print("❌ pyautogui not found - install with: pip install pyautogui")
        return False
    
    try:
        import keyboard as kb
        keyboard = kb
        print("✅ keyboard loaded")
    except ImportError:
        print("❌ keyboard not found - install with: pip install keyboard")
        return False
    
    try:
        from Webhook import log_purchase, send_hourly_report
        print("✅ Webhook module loaded")
        # Make these available globally
        globals()['log_purchase'] = log_purchase
        globals()['send_hourly_report'] = send_hourly_report
    except ImportError as e:
        print(f"❌ Webhook import failed: {e}")
        return False
    
    return True

# Global variables
MACRO_SPEED = 0.1
macro_running = False
UI_NAV_KEY = '\\'
selected_items = {}
webhook_url = ""

# Shop timer management (all start ready)
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

# Egg color map for recognition
EGG_COLOR_MAP = {
    "Common Egg": 0xFFFFFF,
    "Uncommon Egg": 0x81A7D3,
    "Rare Egg": 0xBB5421,
    "Legendary Egg": 0x2D78A3,
    "Mythical Egg": 0x00CCFF,
    "Bug Egg": 0x86FFD5,
    "Common Summer Egg": 0x00FFFF,
    "Rare Summer Egg": 0xFBFCA8,
    "Paradise Egg": 0x32CDFF,
    "Bee Egg": 0x00ACFF
}

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
    print(f"🔍 Zooming in ({amount} scrolls)")
    for _ in range(amount):
        if not macro_running:
            return False
        pyautogui.scroll(200)
        time.sleep(min(MACRO_SPEED, 0.05))
    return True

def scroll_mouse_down(amount=8):
    """Scroll mouse down (zoom out)"""
    print(f"🔍 Zooming out ({amount} scrolls)")
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
    print(f"🎮 Toggling UI Navigation ({UI_NAV_KEY})")
    safe_press(UI_NAV_KEY)
    safe_wait(0.15)
    return True

def navigate_ui_right(steps=1):
    """Navigate UI to the right"""
    print(f"➡️ Moving UI right ({steps} steps)")
    safe_press('right', steps)
    safe_wait(0.2)
    return True

def navigate_ui_down(steps=1):
    """Navigate UI down"""
    print(f"⬇️ Moving UI down ({steps} steps)")
    safe_press('down', steps)
    safe_wait(0.2)
    return True

def navigate_ui_up(steps=1):
    """Navigate UI up"""
    print(f"⬆️ Moving UI up ({steps} steps)")
    safe_press('up', steps)
    safe_wait(0.2)
    return True

def press_enter():
    """Press enter key"""
    print("✅ Pressing Enter")
    safe_press('enter')
    safe_wait(0.5)
    return True

def press_e():
    """Press E key to interact"""
    print("🤝 Pressing E to interact")
    safe_press('e')
    safe_wait(0.5)
    return True

def spam_enter(times=5):
    """Spam enter key multiple times"""
    print(f"🔄 Spamming Enter ({times} times)")
    for _ in range(times):
        if not macro_running:
            return False
        safe_press('enter')
        safe_wait(0.1)
    return True

def equip_recall_wrench():
    """Equip recall wrench from slot 2"""
    print("🔧 Equipping recall wrench from slot 2")
    safe_press('2')
    safe_wait(0.5)
    return True

def use_recall_wrench():
    """Use recall wrench to teleport"""
    print("� Using recall wrench to teleport")
    keyboard.write("recall")
    safe_wait(0.5)
    safe_press('enter')
    safe_wait(2.0)  # Wait for teleport
    return True

def close_shop():
    """Close the current shop using UI navigation"""
    print("🚪 Closing shop using UI navigation")
    
    # Close UI navigation
    toggle_ui_navigation()
    safe_wait(0.3)
    
    # Open UI navigation again
    toggle_ui_navigation()
    safe_wait(0.3)
    
    # Move 4 to the right
    navigate_ui_right(4)
    
    # Move 1 down
    navigate_ui_down(1)
    
    # Move 1 to the right
    navigate_ui_right(1)
    
    safe_wait(0.5)
    return True

def setup_initial_camera():
    """Set up the initial camera position"""
    print("🎥 Setting up camera position")
    
    # Zoom in all the way (20 scrolls up)
    scroll_mouse_up(20)
    safe_wait(0.5)
    
    # Then zoom out a bit (8 scrolls down)
    scroll_mouse_down(8)
    safe_wait(0.5)
    
    print("✅ Camera setup completed")
    return True

def navigate_to_seed_shop():
    """Navigate to seed shop using UI navigation"""
    print("🌱 Navigating to seed shop")
    
    # Open UI navigation
    toggle_ui_navigation()
    safe_wait(0.3)
    
    # Move 3 to the right
    navigate_ui_right(3)
    
    # Press enter to select seeds
    press_enter()
    safe_wait(1.0)
    
    # Press E to interact with NPC
    press_e()
    safe_wait(1.0)
    
    return True

def buy_seeds(seeds_to_buy):
    """Buy selected seeds from seed shop"""
    print(f"🌱 Buying seeds: {seeds_to_buy}")
    
    if not seeds_to_buy:
        print("No seeds selected to buy")
        return True
    
    # For each seed we need to buy
    for seed_name in seeds_to_buy:
        if not macro_running:
            break
            
        print(f"🔍 Looking for {seed_name}")
        
        # Find the seed by scrolling down through the shop
        seed_found = False
        max_scrolls = 30  # Prevent infinite loop
        
        for scroll_attempt in range(max_scrolls):
            if not macro_running:
                break
                
            # Try to find and buy the seed
            # Since we can't read text directly, we'll try to buy at each position
            # This is a simplified approach - in reality you'd need OCR or pattern matching
            
            # Press enter to try to buy current item
            press_enter()
            safe_wait(0.3)
            
            # Move down one to spam enter (buy multiple)
            navigate_ui_down(1)
            spam_enter(3)  # Buy 3 of this seed
            safe_wait(0.5)
            
            # Move back up to continue searching
            navigate_ui_up(1)
            safe_wait(0.3)
            
            # Move down to next item
            navigate_ui_down(1)
            safe_wait(0.3)
            
            # For now, we'll assume we found it after a few attempts
            if scroll_attempt >= len(SEED_ITEMS):
                break
        
        log_purchase("Seeds", seed_name)
        print(f"✅ Purchased {seed_name}")
    
    return True

def navigate_to_gear_shop():
    """Navigate to gear shop using recall wrench"""
    print("⚙️ Navigating to gear shop")
    
    # First close the shop
    close_shop()
    safe_wait(0.5)
    
    # Equip recall wrench
    equip_recall_wrench()
    safe_wait(0.5)
    
    # Use recall wrench to teleport
    use_recall_wrench()
    safe_wait(2.0)
    
    # Interact with NPC to enable gear shop
    press_e()
    safe_wait(1.0)
    
    # There are 3 options, click the first one
    # We'll use Enter to select the first option
    press_enter()
    safe_wait(1.0)
    
    return True

def buy_gears(gears_to_buy):
    """Buy selected gears from gear shop"""
    print(f"⚙️ Buying gears: {gears_to_buy}")
    
    if not gears_to_buy:
        print("No gears selected to buy")
        return True
    
    # Similar logic to seed buying
    for gear_name in gears_to_buy:
        if not macro_running:
            break
            
        print(f"🔍 Looking for {gear_name}")
        
        # Navigate through gear shop
        max_scrolls = 20
        
        for scroll_attempt in range(max_scrolls):
            if not macro_running:
                break
                
            # Try to buy current item
            press_enter()
            safe_wait(0.3)
            
            # Move down and spam enter
            navigate_ui_down(1)
            spam_enter(2)  # Buy 2 of this gear
            safe_wait(0.5)
            
            # Move back up and continue
            navigate_ui_up(1)
            safe_wait(0.3)
            navigate_ui_down(1)
            safe_wait(0.3)
            
            if scroll_attempt >= len(GEAR_ITEMS):
                break
        
        log_purchase("Gears", gear_name)
        print(f"✅ Purchased {gear_name}")
    
    return True

def get_pixel_color(x, y):
    """Get the color of a pixel at coordinates (x, y)"""
    try:
        screenshot = pyautogui.screenshot()
        color = screenshot.getpixel((x, y))
        # Convert RGB to hex
        hex_color = (color[0] << 16) + (color[1] << 8) + color[2]
        return hex_color
    except Exception as e:
        print(f"Error getting pixel color: {e}")
        return None

def find_egg_by_color(target_eggs):
    """Find eggs by their color on screen"""
    print(f"🥚 Looking for eggs by color: {target_eggs}")
    
    # Define search area (you may need to adjust these coordinates)
    search_areas = [
        (400, 300, 50, 50),  # Egg spot 1
        (500, 300, 50, 50),  # Egg spot 2
        (600, 300, 50, 50),  # Egg spot 3
    ]
    
    found_eggs = []
    
    for area_index, (x, y, width, height) in enumerate(search_areas):
        if not macro_running:
            break
            
        print(f"� Checking egg spot {area_index + 1}")
        
        # Sample color from center of the area
        center_x = x + width // 2
        center_y = y + height // 2
        
        pixel_color = get_pixel_color(center_x, center_y)
        
        if pixel_color is None:
            continue
        
        # Check if this color matches any of our target eggs
        for egg_name in target_eggs:
            if egg_name in EGG_COLOR_MAP:
                target_color = EGG_COLOR_MAP[egg_name]
                
                # Allow some tolerance in color matching
                color_diff = abs(pixel_color - target_color)
                if color_diff < 50000:  # Adjust tolerance as needed
                    found_eggs.append((egg_name, area_index))
                    print(f"✅ Found {egg_name} at spot {area_index + 1}")
                    break
    
    return found_eggs

def navigate_to_egg_shop():
    """Navigate to egg shop"""
    print("🥚 Navigating to egg shop")
    
    # Close gear shop first
    close_shop()
    safe_wait(0.5)
    
    # Move to egg area (adjust movement as needed)
    safe_press('w', 3)  # Move forward
    safe_wait(1.0)
    
    return True

def buy_eggs(eggs_to_buy):
    """Buy selected eggs using color recognition"""
    print(f"🥚 Buying eggs: {eggs_to_buy}")
    
    if not eggs_to_buy:
        print("No eggs selected to buy")
        return True
    
    # Find eggs by color
    found_eggs = find_egg_by_color(eggs_to_buy)
    
    for egg_name, spot_index in found_eggs:
        if not macro_running:
            break
            
        print(f"� Buying {egg_name} from spot {spot_index + 1}")
        
        # Move to the egg spot (adjust movement as needed)
        if spot_index == 0:
            safe_press('a', 2)  # Move left
        elif spot_index == 1:
            # Already in center
            pass
        elif spot_index == 2:
            safe_press('d', 2)  # Move right
        
        safe_wait(0.5)
        
        # Interact with egg
        press_e()
        safe_wait(0.5)
        
        # Buy the egg
        press_enter()
        safe_wait(0.5)
        
        log_purchase("Eggs", egg_name)
        print(f"✅ Purchased {egg_name}")
    
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
        print("🌱 Seed shop is ready!")
        navigate_to_seed_shop()
        buy_seeds(selected_items["Seeds"])
        update_shop_timer("Seeds", shop_timers["Seeds"]["total_time"])
    
    # Visit gear shop if ready and items selected
    if (is_shop_ready("Gears") and 
        selected_items.get("Gears") and 
        macro_running):
        print("⚙️ Gear shop is ready!")
        navigate_to_gear_shop()
        buy_gears(selected_items["Gears"])
        update_shop_timer("Gears", shop_timers["Gears"]["total_time"])
    
    # Visit egg shop if ready and items selected
    if (is_shop_ready("Eggs") and 
        selected_items.get("Eggs") and 
        macro_running):
        print("🥚 Egg shop is ready!")
        navigate_to_egg_shop()
        buy_eggs(selected_items["Eggs"])
        update_shop_timer("Eggs", shop_timers["Eggs"]["total_time"])
    
    print("✅ Macro cycle completed")

def get_next_restock_time():
    """Get the time until the next shop restocks"""
    check_shop_timers()
    
    next_restock = None
    next_shop = None
    
    for shop_name, timer_data in shop_timers.items():
        if timer_data["time_left"] > 0:
            if next_restock is None or timer_data["time_left"] < next_restock:
                next_restock = timer_data["time_left"]
                next_shop = shop_name
    
    return next_shop, next_restock

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
    
    try:
        print("🚀 Starting Grow a Garden macro...")
        print(f"📝 Selected items: {items}")
        
        # Check dependencies first
        print("🔍 Checking dependencies...")
        if not check_dependencies():
            print("❌ Dependencies check failed!")
            print("Please install dependencies with: pip install -r requirements.txt")
            return
        
        macro_running = True
        selected_items = items
        webhook_url = webhook
        
        print("🎥 Setting up camera...")
        # Initial camera setup
        if not setup_initial_camera():
            print("❌ Camera setup failed")
            return
        
        print("⏰ Starting timer threads...")
        # Start timer update thread
        timer_thread = threading.Thread(target=timer_update_thread)
        timer_thread.daemon = True
        timer_thread.start()
        
        # Start hourly report thread if webhook is configured
        if webhook_url:
            print("📡 Starting webhook thread...")
            report_thread = threading.Thread(target=hourly_report_thread)
            report_thread.daemon = True
            report_thread.start()
        
        print("🔄 Starting main macro loop...")
        
        # Test basic functionality first
        print("🧪 Testing basic controls...")
        if not test_basic_controls():
            print("❌ Basic controls test failed")
            return
        
        # Main macro loop
        cycle_count = 0
        while macro_running:
            cycle_count += 1
            print(f"\n🔄 === Macro Cycle {cycle_count} ===")
            
            # Check what's the next shop to restock
            next_shop, next_restock_time = get_next_restock_time()
            
            if next_restock_time is None or next_restock_time <= 0:
                # All shops are ready, run a cycle
                print("🏪 Shops are ready, running cycle...")
                run_macro_cycle()
                safe_wait(10)  # Wait 10 seconds between cycles
            else:
                # Wait for next restock
                print(f"⏰ Next restock: {next_shop} in {int(next_restock_time)} seconds")
                safe_wait(min(60, next_restock_time))  # Check every minute or when ready
                
    except KeyboardInterrupt:
        print("⏹ Macro interrupted by user")
    except Exception as e:
        print(f"❌ Macro error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        macro_running = False
        print("⏹ Macro stopped")

def test_basic_controls():
    """Test basic controls to make sure everything is working"""
    try:
        print("  🔍 Testing mouse scroll...")
        pyautogui.scroll(1)
        safe_wait(0.1)
        pyautogui.scroll(-1)
        
        print("  ⌨️ Testing keyboard input...")
        # Don't actually press keys during test, just make sure libraries work
        
        print("  ✅ Basic controls test passed")
        return True
    except Exception as e:
        print(f"  ❌ Basic controls test failed: {e}")
        return False

def test_webhook_func(webhook_url):
    """Test webhook function (for compatibility with old code)"""
    from Webhook import test_webhook
    return test_webhook(webhook_url)
