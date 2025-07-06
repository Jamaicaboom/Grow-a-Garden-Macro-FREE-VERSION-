import time
import pyautogui
import keyboard
import threading
from datetime import datetime, timedelta
from Webhook import log_purchase, send_hourly_report

# Global variables
MACRO_SPEED = 0.1  # Default speed for reliable operation
macro_running = False
UI_NAV_KEY = '\\'  # UI Navigation toggle key
selected_items = {
    "seeds": [],
    "gears": [],
    "eggs": [],
    "cosmetics": False
}

# Shop restock timers (in minutes)
SHOP_RESTOCK_TIMES = {
    "seeds": 60,    # 1 hour
    "gears": 60,    # 1 hour  
    "eggs": 60,     # 1 hour
    "cosmetics": 60  # 1 hour
}

# Shop navigation data
SHOP_LOCATIONS = {
    "seeds": {"name": "Seed Shop", "interaction": "e", "times": 1},
    "gears": {"name": "Gear Shop", "interaction": "e", "times": 1, "needs_zoom": True},
    "eggs": {"name": "Egg Shop", "interaction": "e", "times": 1, "spots": 3},
    "cosmetics": {"name": "Cosmetic Shop", "interaction": "e", "times": 1, "items": 9}
}

# Timer tracking
last_shop_visit = {
    "seeds": None,
    "gears": None,
    "eggs": None,
    "cosmetics": None
}

webhook_url = ""
discord_user_id = ""

def set_macro_speed(new_speed):
    """Set the macro execution speed"""
    global MACRO_SPEED
    MACRO_SPEED = new_speed
    print(f"🚀 Macro speed set to: {new_speed}")

def set_ui_nav_key(key):
    """Set the UI Navigation key"""
    global UI_NAV_KEY
    UI_NAV_KEY = key
    print(f"🎮 UI Navigation key set to: {key}")

def set_selected_items(items):
    """Set which items to buy from each shop"""
    global selected_items
    selected_items = items
    print(f"📝 Selected items updated: {items}")

def get_selected_items():
    """Get currently selected items"""
    return selected_items

def get_ui_nav_key():
    """Get current UI Navigation key"""
    return UI_NAV_KEY

def set_webhook_settings(url, user_id=""):
    """Set webhook settings"""
    global webhook_url, discord_user_id
    webhook_url = url
    discord_user_id = user_id

def stop_macro():
    """Stop the macro execution"""
    global macro_running
    macro_running = False
    print("⏹️ Macro stopped by user")

def test_webhook_func(url):
    """Test webhook functionality - compatibility function"""
    from Webhook import test_webhook
    return test_webhook(url)

def safe_press(key, times=1, delay=None):
    """Safely press a key with macro running check"""
    if delay is None:
        delay = MACRO_SPEED
    
    for _ in range(times):
        if not macro_running:
            return False
        keyboard.press_and_release(key)
        time.sleep(delay)
    return True

def safe_scroll(direction, amount=5):
    """Safely scroll with macro running check"""
    scroll_value = 200 if direction == "up" else -200
    
    for _ in range(amount):
        if not macro_running:
            return False
        pyautogui.scroll(scroll_value)
        time.sleep(min(MACRO_SPEED, 0.05))
    return True

def toggle_ui_navigation():
    """Toggle UI Navigation on/off"""
    if not macro_running:
        return False
    
    print(f"🎮 Toggling UI Navigation ({UI_NAV_KEY})")
    keyboard.press_and_release(UI_NAV_KEY)
    time.sleep(0.2)
    return True

def setup_camera():
    """Set up camera position for optimal macro performance"""
    if not macro_running:
        return False
    
    print("📷 Setting up camera position...")
    
    # Zoom in for better visibility
    if not safe_scroll("up", 20):
        return False
    
    # Adjust camera angle
    if not safe_scroll("down", 8):
        return False
    
    # Toggle UI Navigation to ensure it's in correct state
    toggle_ui_navigation()
    time.sleep(0.5)
    toggle_ui_navigation()
    
    print("📷 Camera setup completed")
    return True

def equip_recall_wrench():
    """Equip the recall wrench from inventory slot 2"""
    if not macro_running:
        return False
    
    print("🔧 Opening inventory...")
    
    # Open inventory (assuming Tab key)
    if not safe_press("tab"):
        return False
    
    time.sleep(0.5)
    
    # Type 'recall' to search for recall wrench
    if not macro_running:
        return False
    
    keyboard.write("recall")
    time.sleep(0.5)
    
    # Click on slot 2 (assuming it's the second slot)
    if not safe_press("2"):
        return False
    
    time.sleep(0.5)
    
    # Close inventory
    if not safe_press("tab"):
        return False
    
    print("🔧 Recall wrench equipped")
    return True

def use_recall_wrench():
    """Use the recall wrench to teleport"""
    if not macro_running:
        return False
    
    print("🔧 Using recall wrench...")
    
    # Assuming recall wrench is activated by clicking or pressing a key
    # You might need to adjust this based on how recall wrench works in the game
    if not safe_press("f"):  # Common interact key
        return False
    
    time.sleep(2)  # Wait for teleport animation
    
    print("🔧 Recall wrench used")
    return True

def navigate_to_shop(shop_type):
    """Navigate to a specific shop using UI Navigation"""
    if not macro_running:
        return False
    
    shop_info = SHOP_LOCATIONS.get(shop_type)
    if not shop_info:
        print(f"❌ Unknown shop type: {shop_type}")
        return False
    
    print(f"🏪 Navigating to {shop_info['name']}...")
    
    # Enable UI Navigation
    toggle_ui_navigation()
    time.sleep(0.5)
    
    # Navigate to shop (this might need adjustment based on actual game mechanics)
    if shop_type == "seeds":
        # Navigate to seed shop
        if not safe_press("w", 3):  # Move forward
            return False
        
    elif shop_type == "gears":
        # Use recall wrench to get to gear shop
        if not use_recall_wrench():
            return False
        
        # Zoom in close for gear shop
        if shop_info.get("needs_zoom"):
            if not safe_scroll("up", 10):
                return False
        
    elif shop_type == "eggs":
        # Navigate to egg area
        if not safe_press("w", 2):  # Move forward
            return False
        
    elif shop_type == "cosmetics":
        # Navigate to cosmetic shop
        if not safe_press("w", 4):  # Move forward
            return False
    
    # Disable UI Navigation
    toggle_ui_navigation()
    time.sleep(0.5)
    
    print(f"🏪 Arrived at {shop_info['name']}")
    return True

def interact_with_shop(shop_type):
    """Interact with a specific shop and buy selected items"""
    if not macro_running:
        return False
    
    shop_info = SHOP_LOCATIONS.get(shop_type)
    if not shop_info:
        return False
    
    print(f"🛒 Interacting with {shop_info['name']}...")
    
    # Press interaction key
    interaction_key = shop_info.get("interaction", "e")
    times = shop_info.get("times", 1)
    
    if not safe_press(interaction_key, times):
        return False
    
    time.sleep(1)  # Wait for shop to open
    
    # Handle different shop types
    if shop_type == "seeds":
        return buy_seeds()
    elif shop_type == "gears":
        return buy_gears()
    elif shop_type == "eggs":
        return buy_eggs()
    elif shop_type == "cosmetics":
        return buy_cosmetics()
    
    return False

def buy_seeds():
    """Buy selected seeds from the seed shop"""
    if not macro_running:
        return False
    
    selected_seeds = selected_items.get("seeds", [])
    if not selected_seeds:
        print("📦 No seeds selected for purchase")
        return True
    
    print(f"🌱 Buying seeds: {selected_seeds}")
    
    # Navigate through seed shop and buy items
    for i, seed in enumerate(selected_seeds):
        if not macro_running:
            return False
        
        print(f"🌱 Buying {seed}...")
        
        # Navigate to seed (assuming up/down arrows or number keys)
        if not safe_press("down", i):
            return False
        
        # Buy the seed (assuming Enter or specific buy key)
        if not safe_press("enter"):
            return False
        
        time.sleep(0.5)
        
        # Log purchase
        log_purchase("Seeds", seed)
    
    # Close shop
    if not safe_press("escape"):
        return False
    
    print("🌱 Seed purchases completed")
    return True

def buy_gears():
    """Buy selected gears from the gear shop"""
    if not macro_running:
        return False
    
    selected_gears = selected_items.get("gears", [])
    if not selected_gears:
        print("📦 No gears selected for purchase")
        return True
    
    print(f"�️ Buying gears: {selected_gears}")
    
    # First, click the first option to access gear shop
    if not safe_press("1"):
        return False
    
    time.sleep(1)
    
    # Navigate through gear shop and buy items
    for i, gear in enumerate(selected_gears):
        if not macro_running:
            return False
        
        print(f"🛠️ Buying {gear}...")
        
        # Navigate to gear
        if not safe_press("down", i):
            return False
        
        # Buy the gear
        if not safe_press("enter"):
            return False
        
        time.sleep(0.5)
        
        # Log purchase
        log_purchase("Gears", gear)
    
    # Close shop and return camera to normal
    if not safe_press("escape"):
        return False
    
    # Reset camera zoom
    if not safe_scroll("down", 5):
        return False
    
    print("🛠️ Gear purchases completed")
    return True

def buy_eggs():
    """Buy selected eggs from the egg shop"""
    if not macro_running:
        return False
    
    selected_eggs = selected_items.get("eggs", [])
    if not selected_eggs:
        print("📦 No eggs selected for purchase")
        return True
    
    print(f"🥚 Buying eggs: {selected_eggs}")
    
    # Navigate through 3 egg spots
    spots = SHOP_LOCATIONS["eggs"].get("spots", 3)
    
    for spot in range(spots):
        if not macro_running:
            return False
        
        print(f"🥚 Checking egg spot {spot + 1}...")
        
        # Move to egg spot
        if not safe_press("w", spot):
            return False
        
        # Interact with egg display
        if not safe_press("e"):
            return False
        
        time.sleep(0.5)
        
        # Check what egg type this is and buy if selected
        # This is a simplified version - you might need to add egg type detection
        for egg in selected_eggs:
            if not macro_running:
                return False
            
            print(f"🥚 Buying {egg}...")
            
            # Buy the egg
            if not safe_press("enter"):
                return False
            
            time.sleep(0.5)
            
            # Log purchase
            log_purchase("Eggs", egg)
        
        # Close current egg display
        if not safe_press("escape"):
            return False
        
        time.sleep(0.5)
    
    print("🥚 Egg purchases completed")
    return True

def buy_cosmetics():
    """Buy all cosmetics if selected"""
    if not macro_running:
        return False
    
    if not selected_items.get("cosmetics", False):
        print("📦 Cosmetics not selected for purchase")
        return True
    
    print("💄 Buying all cosmetics...")
    
    # Navigate through 9 cosmetic items
    cosmetic_count = SHOP_LOCATIONS["cosmetics"].get("items", 9)
    
    for i in range(cosmetic_count):
        if not macro_running:
            return False
        
        print(f"💄 Buying cosmetic item {i + 1}...")
        
        # Navigate to cosmetic item
        if not safe_press("down", i):
            return False
        
        # Spam buy button (in case of multiple quantities)
        for _ in range(5):  # Spam buy 5 times
            if not macro_running:
                return False
            
            if not safe_press("enter"):
                return False
            
            time.sleep(0.1)
        
        time.sleep(0.5)
        
        # Log purchase
        log_purchase("Cosmetics", f"Cosmetic Item {i + 1}")
    
    # Close shop
    if not safe_press("escape"):
        return False
    
    print("💄 Cosmetic purchases completed")
    return True

def calculate_next_restock_time(shop_type):
    """Calculate when the next restock will happen"""
    last_visit = last_shop_visit.get(shop_type)
    if not last_visit:
        return datetime.now()
    
    restock_minutes = SHOP_RESTOCK_TIMES.get(shop_type, 60)
    return last_visit + timedelta(minutes=restock_minutes)

def should_visit_shop(shop_type):
    """Check if we should visit a shop based on restock timer"""
    next_restock = calculate_next_restock_time(shop_type)
    return datetime.now() >= next_restock

def update_shop_visit_time(shop_type):
    """Update the last visit time for a shop"""
    last_shop_visit[shop_type] = datetime.now()

def print_shop_timers():
    """Print current shop restock timers"""
    print("\n⏰ Shop Restock Timers:")
    for shop_type in SHOP_LOCATIONS.keys():
        next_restock = calculate_next_restock_time(shop_type)
        time_left = next_restock - datetime.now()
        
        if time_left.total_seconds() <= 0:
            print(f"   {shop_type.capitalize()}: READY!")
        else:
            minutes_left = int(time_left.total_seconds() // 60)
            seconds_left = int(time_left.total_seconds() % 60)
            print(f"   {shop_type.capitalize()}: {minutes_left}m {seconds_left}s")

def run_macro():
    """Main macro execution loop"""
    global macro_running
    macro_running = True
    
    print("🚀 Starting King Clab's Grow a Garden Macro!")
    print("=" * 50)
    
    # Initial setup
    if not setup_camera():
        print("❌ Failed to set up camera")
        return
    
    if not equip_recall_wrench():
        print("❌ Failed to equip recall wrench")
        return
    
    print("✅ Initial setup completed")
    
    # Main macro loop
    while macro_running:
        try:
            print("\n🔄 Starting shop visit cycle...")
            
            # Check each shop
            for shop_type in SHOP_LOCATIONS.keys():
                if not macro_running:
                    break
                
                # Check if we have items selected for this shop
                if shop_type == "cosmetics":
                    has_items = selected_items.get("cosmetics", False)
                else:
                    has_items = len(selected_items.get(shop_type, [])) > 0
                
                if not has_items:
                    continue
                
                # Check if shop is ready for restock
                if should_visit_shop(shop_type):
                    print(f"\n🏪 Visiting {shop_type.capitalize()} Shop...")
                    
                    # Navigate to shop
                    if navigate_to_shop(shop_type):
                        # Interact with shop and buy items
                        if interact_with_shop(shop_type):
                            # Update visit time
                            update_shop_visit_time(shop_type)
                            print(f"✅ {shop_type.capitalize()} shop visit completed")
                        else:
                            print(f"❌ Failed to interact with {shop_type} shop")
                    else:
                        print(f"❌ Failed to navigate to {shop_type} shop")
                    
                    # Wait between shops
                    time.sleep(2)
                else:
                    print(f"⏰ {shop_type.capitalize()} shop not ready yet")
            
            # Print timer status
            print_shop_timers()
            
            # Wait before next cycle (check every 30 seconds)
            print(f"\n😴 Waiting 30 seconds before next cycle...")
            for _ in range(30):
                if not macro_running:
                    break
                time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error in macro execution: {e}")
            time.sleep(5)
    
    print("\n⏹️ Macro execution stopped")

def start_hourly_webhook_timer():
    """Start the hourly webhook reporting timer"""
    def send_hourly_reports():
        while macro_running:
            time.sleep(3600)  # Wait 1 hour
            if webhook_url:
                send_hourly_report(webhook_url)
    
    if webhook_url:
        webhook_thread = threading.Thread(target=send_hourly_reports, daemon=True)
        webhook_thread.start()

# Start webhook timer when module is imported
start_hourly_webhook_timer()
