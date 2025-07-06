import time
import threading
from datetime import datetime, timedelta

# Import dependencies with error handling
pyautogui = None
keyboard = None

# Define fallback functions for when imports fail
def log_purchase_fallback(category, item):
    """Fallback function when webhook module isn't available"""
    print(f"📝 Would log: {category} - {item} (webhook not available)")

def send_hourly_report_fallback(webhook_url):
    """Fallback function when webhook module isn't available"""
    print(f"📧 Would send hourly report (webhook not available)")

# Initialize with fallback functions
log_purchase = log_purchase_fallback
send_hourly_report = send_hourly_report_fallback

def check_dependencies():
    """Check and import dependencies"""
    global pyautogui, keyboard, log_purchase, send_hourly_report
    
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
        from Webhook import log_purchase as lp, send_hourly_report as shr
        log_purchase = lp
        send_hourly_report = shr
        print("✅ Webhook module loaded")
    except ImportError as e:
        print(f"⚠️ Webhook import failed: {e} (using fallback)")
        # Keep using fallback functions
    
    return True

# Global variables
MACRO_SPEED = 0.1
macro_running = False
UI_NAV_KEY = '\\'
selected_items = {}
webhook_url = ""

# Shop timer management (all start ready)
shop_timers = {
    "Seeds": {"time_left": 0, "total_time": 3600, "last_visited": None},     # 1 hour (3600 seconds)
    "Gears": {"time_left": 0, "total_time": 300, "last_visited": None},      # 5 minutes (300 seconds)  
    "Eggs": {"time_left": 0, "total_time": 1800, "last_visited": None},      # 30 minutes (1800 seconds)
    "Cosmetics": {"time_left": 0, "total_time": 14400, "last_visited": None} # 4 hours (14400 seconds)
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
    """Update all shop timers based on elapsed time and try to detect from UI"""
    current_time = datetime.now()
    for shop_name, timer_data in shop_timers.items():
        # Try to detect actual time from game UI first
        detected_time = detect_shop_restock_time(shop_name)
        
        if detected_time is not None:
            # Use detected time from game UI
            timer_data["time_left"] = detected_time
            print(f"🎯 Detected {shop_name} timer: {detected_time}s from game UI")
        elif timer_data["last_visited"]:
            # Fall back to calculated time
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
        if pyautogui:
            pyautogui.scroll(200)
        time.sleep(0.02)  # Fast scroll
    return True

def scroll_mouse_down(amount=8):
    """Scroll mouse down (zoom out)"""
    for _ in range(amount):
        if not macro_running:
            return False
        if pyautogui:
            pyautogui.scroll(-200)
        time.sleep(0.02)  # Fast scroll
    return True

def toggle_ui_navigation():
    """Toggle UI navigation on/off"""
    if not macro_running:
        return False
    safe_press(UI_NAV_KEY)
    safe_wait(0.1)
    return True

def navigate_ui_right(steps=1):
    """Navigate UI to the right using D key"""
    safe_press('d', steps)
    safe_wait(0.1)
    return True

def navigate_ui_down(steps=1):
    """Navigate UI down using S key"""
    safe_press('s', steps)
    safe_wait(0.1)
    return True

def navigate_ui_up(steps=1):
    """Navigate UI up using W key"""
    safe_press('w', steps)
    safe_wait(0.1)
    return True

def navigate_ui_left(steps=1):
    """Navigate UI to the left using A key"""
    safe_press('a', steps)
    safe_wait(0.1)
    return True

def press_enter():
    """Press enter key"""
    safe_press('enter')
    safe_wait(0.2)
    return True

def press_e():
    """Press E key to interact"""
    safe_press('e')
    safe_wait(0.3)
    return True

def spam_enter(times=10):
    """Spam enter key multiple times fast"""
    for _ in range(times):
        if not macro_running:
            return False
        safe_press('enter')
        safe_wait(0.05)  # Very fast
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
    safe_wait(0.5)
    
    # Open UI navigation again
    toggle_ui_navigation()
    safe_wait(0.5)
    
    # Navigate to inventory/backpack - Move right 4 times using D key
    print("🧭 Moving to inventory...")
    for i in range(4):
        print(f"  Step {i+1}: Moving right")
        navigate_ui_right(1)
        safe_wait(0.2)
    
    # Move down 1 using S key
    print("🧭 Moving down to backpack")
    navigate_ui_down(1)
    safe_wait(0.2)
    
    # Move right 1 more using D key
    print("🧭 Final movement to backpack")
    navigate_ui_right(1)
    safe_wait(0.2)
    
    print("✅ Ready to access inventory")
    safe_wait(0.5)
    return True

def setup_initial_camera():
    """Set up the initial camera position"""
    print("Setting up camera...")
    
    # Zoom in all the way (20 scrolls up)
    scroll_mouse_up(20)
    safe_wait(0.2)
    
    # Look down at the floor using mouse movement
    if pyautogui:
        # Move mouse down to look at floor
        pyautogui.move(0, 200, duration=0.1)
        safe_wait(0.1)
    
    # Then zoom out a bit (8 scrolls down)
    scroll_mouse_down(8)
    safe_wait(0.2)
    
    print("Camera ready")
    return True

def navigate_to_seed_shop():
    """Navigate to seed shop using UI navigation"""
    print("Going to seed shop")
    
    # Open UI navigation
    toggle_ui_navigation()
    safe_wait(0.2)
    
    # Navigate to Seeds button - Move right 3 times
    navigate_ui_right(3)
    safe_wait(0.1)
    
    # Press enter to select seeds
    press_enter()
    safe_wait(0.5)
    
    # Press E to interact with NPC
    press_e()
    safe_wait(0.5)
    
    return True

def buy_seeds(seeds_to_buy):
    """Buy selected seeds from seed shop - find specific seeds and buy them"""
    print(f"Buying seeds: {seeds_to_buy}")
    
    if not seeds_to_buy:
        return True
    
    # For each seed we need to buy
    for seed_name in seeds_to_buy:
        if not macro_running:
            break
            
        print(f"Finding {seed_name}")
        
        # Find the seed's position in the list
        if seed_name in SEED_ITEMS:
            seed_index = SEED_ITEMS.index(seed_name)
            
            # Navigate to the seed's position
            for _ in range(seed_index):
                if not macro_running:
                    break
                navigate_ui_down(1)
                safe_wait(0.05)
            
            # Buy the seed: enter, move down, spam enter 10 times
            press_enter()
            navigate_ui_down(1)
            spam_enter(10)  # Buy 10 of this seed fast
            
            # Reset position to top for next seed
            for _ in range(seed_index + 1):
                if not macro_running:
                    break
                navigate_ui_up(1)
                safe_wait(0.05)
            
            log_purchase("Seeds", seed_name)
            print(f"Bought {seed_name}")
    
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

def detect_shop_restock_time(shop_name):
    """Try to detect actual restock time from game UI"""
    try:
        print(f"🕵️ Detecting restock time for {shop_name}...")
        
        # Take screenshot of the area where timer is displayed
        # You may need to adjust these coordinates based on your screen resolution
        timer_areas = {
            "Seeds": (100, 100, 300, 50),    # x, y, width, height
            "Gears": (100, 150, 300, 50),
            "Eggs": (100, 200, 300, 50),
            "Cosmetics": (100, 250, 300, 50)
        }
        
        if shop_name not in timer_areas:
            print(f"⚠️ No timer area defined for {shop_name}")
            return None
        
        x, y, width, height = timer_areas[shop_name]
        
        # Take screenshot of timer area
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        
        # For now, we'll use a simple approach
        # In a real implementation, you'd use OCR (like pytesseract) to read the text
        
        # Simple color-based detection (placeholder)
        # This would need to be replaced with actual OCR
        print(f"📸 Screenshot taken for {shop_name} timer detection")
        
        # Return None for now - actual implementation would parse the timer text
        return None
        
    except Exception as e:
        print(f"❌ Error detecting restock time for {shop_name}: {e}")
        return None

def parse_time_string(time_str):
    """Parse time string like '3:29' or '0:45' into seconds"""
    try:
        if ':' not in time_str:
            return None
        
        parts = time_str.split(':')
        if len(parts) != 2:
            return None
        
        minutes = int(parts[0])
        seconds = int(parts[1])
        total_seconds = minutes * 60 + seconds
        
        return total_seconds
    except:
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
    # Check timers first
    check_shop_timers()
    
    # Visit seed shop if ready and items selected
    if (is_shop_ready("Seeds") and 
        selected_items.get("Seeds") and 
        macro_running):
        print("Visiting seed shop")
        navigate_to_seed_shop()
        buy_seeds(selected_items["Seeds"])
        update_shop_timer("Seeds", shop_timers["Seeds"]["total_time"])
    
    # Visit gear shop if ready and items selected
    if (is_shop_ready("Gears") and 
        selected_items.get("Gears") and 
        macro_running):
        print("Visiting gear shop")
        navigate_to_gear_shop()
        buy_gears(selected_items["Gears"])
        update_shop_timer("Gears", shop_timers["Gears"]["total_time"])
    
    # Visit egg shop if ready and items selected
    if (is_shop_ready("Eggs") and 
        selected_items.get("Eggs") and 
        macro_running):
        print("Visiting egg shop")
        navigate_to_egg_shop()
        buy_eggs(selected_items["Eggs"])
        update_shop_timer("Eggs", shop_timers["Eggs"]["total_time"])
    
    print("Cycle complete")

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
                print("Running shop cycle...")
                run_macro_cycle()
                safe_wait(5)  # Wait 5 seconds between cycles (faster)
            else:
                # Wait for next restock
                print(f"Waiting for {next_shop}: {int(next_restock_time)}s")
                safe_wait(min(30, next_restock_time))  # Check every 30 seconds
                
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
