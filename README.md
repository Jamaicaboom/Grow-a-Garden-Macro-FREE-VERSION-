# 🌱 Grow a Garden Macro

A comprehensive macro for automating shop purchases in Roblox's "Grow a Garden" game.

## ✨ Features

- **Multi-Shop Support**: Automatically visits Seed Shop, Gear Shop, Egg Shop, and Cosmetic Shop
- **Smart Timer Management**: Tracks shop restock times and only visits when ready
- **Custom GUI**: Purple and black themed interface with custom title bar
- **Webhook Integration**: Sends hourly reports to Discord via webhook
- **Flexible Speed Settings**: Choose from Neutral, Fast, Ultra, or Max speed
- **Item Selection**: Choose exactly which items to buy from each shop

## � Project Structure

```
Grow-a-Garden-Macro/
├── main.py                 # Main GUI application with console output
├── MacroLogic.py           # Macro automation logic with color recognition
├── Webhook.py              # Discord webhook functionality
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── start_macro.py         # Smart start script with dependency checking
├── start_macro.bat        # Windows quick start script
├── start_macro.sh         # Linux/macOS quick start script
├── test_setup.py          # Setup verification script
├── test_macro_simple.py   # Simple dependency test (no GUI needed)
└── Images/
    ├── Close.png          # Custom close button image
    └── Minimize.png       # Custom minimize button image
```

## �🚀 Quick Start

### Prerequisites

1. **Python 3.7+** installed on your system
2. **Roblox** game running
3. **Admin privileges** (required for keyboard automation)

### Installation

1. **Clone or download** this repository
2. **Open terminal/command prompt** in the project folder
3. **Install dependencies**:

   **Option 1: Using pip (Windows/most systems)**
   ```bash
   pip install -r requirements.txt
   ```

   **Option 2: Using pip3 (Linux/macOS)**
   ```bash
   pip3 install -r requirements.txt
   ```

   **Option 3: Using virtual environment (recommended)**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   pip install -r requirements.txt
   ```

   **Option 4: If you get permission errors**
   ```bash
   pip install -r requirements.txt --user
   ```

### First Time Setup

1. **Run the macro**:

   **Easy Start (Recommended)**:
   - **Windows**: Double-click `start_macro.bat`
   - **Linux/macOS**: Double-click `start_macro.sh` or run `./start_macro.sh`

   **Manual Start**:
   ```bash
   python main.py
   ```
   
   **Or if using python3:**
   ```bash
   python3 main.py
   ```

   **Advanced Start (with dependency checking)**:
   ```bash
   python start_macro.py
   ```

2. **Configure Settings**:
   - Go to the **Settings** tab
   - Set your **Discord Webhook URL** (optional)
   - Set your **Discord User ID** (optional)
   - Choose your **UI Navigation Keybind** (default: `\`)
   - Select your **Macro Speed** (start with Neutral)

3. **Select Items**:
   - Go to **Seeds**, **Gears**, **Eggs**, or **Cosmetics** tabs
   - Check the boxes for items you want to buy
   - For cosmetics, just check "All cosmetics" to buy all 9 items

## 🎮 How to Use

### Before Starting the Macro

1. **Join Grow a Garden** in Roblox
2. **Position yourself** at the spawn area
3. **Make sure you have a Recall Wrench** in your inventory slot 2
4. **Have enough in-game currency** to buy selected items

### Running the Macro

1. **Select items** you want to buy in each tab
2. **Press F1** or click "Start Macro" button
3. **The macro will**:
   - Set up initial camera position
   - Equip your recall wrench
   - Visit each shop when ready
   - Buy your selected items
   - Track restock timers
   - Send hourly reports (if webhook configured)

### Stopping the Macro

- **Press F2** or click "Stop Macro" button
- **Close the GUI** to stop everything

## 🏪 Shop Information

### Seed Shop (Restocks every 1 hour)
- **22 different seeds** available
- **Single interaction** needed with NPC
- **Navigation**: Uses UI Navigation to find Seeds button

### Gear Shop (Restocks every 2 hours)
- **13 different tools** available
- **Uses Recall Wrench** to teleport to location
- **Zooms in close** for precise interaction

### Egg Shop (Restocks every 30 minutes)
- **10 different eggs** available with color recognition
- **3 egg spots** to check
- **Color-based detection** to identify specific eggs
- **Automatic movement** between egg spots

### Cosmetic Shop (Restocks every 4 hours)
- **9 cosmetic items** available
- **Cycles through all items** when "All cosmetics" is selected

## ⚙️ Settings Guide

### Macro Speed Settings
- **Neutral (0.05s)**: Safe and reliable, good for beginners
- **Fast (0.03s)**: Faster execution, requires stable connection
- **Ultra (0.015s)**: Very fast, needs good performance
- **Max (0.005s)**: ⚠️ **WARNING**: Requires excellent FPS and connection

### UI Navigation Keybind
- **Default**: `\` (backslash)
- **Change if needed**: Some users prefer different keys
- **Make sure it matches** your in-game UI Navigation keybind

### New Navigation Workflow
- **Automatic camera setup**: 20 scrolls up, then 8 scrolls down
- **Smart UI navigation**: Moves precisely to shop buttons
- **Intelligent item finding**: Scrolls through shops to find your items
- **Efficient shop closing**: Automated navigation to inventory and recall wrench

### Webhook Configuration
- **Optional**: Only needed if you want Discord notifications
- **Get webhook URL** from your Discord server settings
- **Test webhook** using the "Test Webhook" button

## 🔧 Important Setup Notes

### Recall Wrench Setup
- **Must be in inventory slot 2**
- **Equip it manually** before starting the macro
- **The macro will type "recall"** to use it

### Camera and Position
- **Start at spawn area** of the game
- **Macro will adjust camera** automatically
- **Don't move manually** while macro is running

### Game Requirements
- **UI Navigation** must be enabled in game settings
- **Keybind must match** the one in macro settings
- **Stable internet connection** recommended

## 📊 Timer System

The macro tracks when each shop was last visited and their restock times:

- **Green "Ready"**: Shop is available for purchase
- **Progress bar**: Shows time until next restock
- **Automatic checking**: Updates every second

## 🔔 Webhook Reports

If configured, the macro sends hourly reports showing:
- Items purchased from each shop
- Total items bought
- Time stamps

## ⚠️ Warnings and Tips

### Performance Warnings
- **Max speed requires 60+ FPS** consistently
- **Ultra speed needs stable connection**
- **Start with Neutral speed** to test

### Safety Tips
- **Don't leave macro running unattended** for extended periods
- **Monitor your game** for any issues
- **Keep backup of important items**

### Troubleshooting

#### 🚨 **Macro Won't Start (Most Common Issue)**
If the macro doesn't start when you press F1:

1. **Check the console output** (green text area at bottom of GUI)
2. **Most likely cause**: Missing dependencies
   ```
   ❌ pyautogui not found - install with: pip install pyautogui
   ❌ keyboard not found - install with: pip install keyboard
   ```
3. **Solution**: Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Or individually:
   ```bash
   pip install pyautogui keyboard requests pillow
   ```

#### 🔧 **Other Common Issues**
- **No items selected**: Check boxes in Seeds/Gears/Eggs tabs first
- **Macro not moving**: Check your UI Navigation keybind matches game settings
- **Wrong items bought**: Verify your item selections match what you want
- **Timer issues**: Restart the macro to reset all timers
- **Webhook not sending**: Test webhook URL in settings tab

#### 📱 **GUI Console Output**
The new console at the bottom shows real-time status:
- `🚀 Starting macro...` - Macro is initializing
- `❌ Dependencies check failed!` - Install missing packages
- `✅ Dependencies loaded successfully` - Ready to run
- `📝 Selected items: {...}` - Shows what will be purchased

## 🎨 GUI Features

### Custom Title Bar
- **Purple and black theme**
- **Custom minimize/close buttons** (Images/Minimize.png, Images/Close.png)
- **Draggable window**

### Real-time Timers
- **Visual progress bars** for each shop
- **Countdown timers** showing seconds until restock
- **Color-coded status** (Ready vs. Waiting)

### Hotkeys
- **F1**: Start macro
- **F2**: Stop macro
- **Works globally** within the application

## 🥚 Egg Color Recognition

The macro uses advanced color detection to identify specific eggs at each egg spot:

### Supported Egg Colors:
- **Common Egg**: White (0xFFFFFF)
- **Uncommon Egg**: Light Blue (0x81A7D3)
- **Rare Egg**: Brown (0xBB5421)
- **Legendary Egg**: Dark Blue (0x2D78A3)
- **Mythical Egg**: Cyan (0x00CCFF)
- **Bug Egg**: Light Green (0x86FFD5)
- **Common Summer Egg**: Bright Cyan (0x00FFFF)
- **Rare Summer Egg**: Light Yellow (0xFBFCA8)
- **Paradise Egg**: Sky Blue (0x32CDFF)
- **Bee Egg**: Blue (0x00ACFF)

### How It Works:
1. **Scans 3 egg spots** automatically
2. **Captures screen colors** at each spot
3. **Matches colors** to your selected eggs
4. **Moves to correct spot** and purchases automatically

## 📝 Customization

### Modifying Shop Items
Edit the lists in `MacroLogic.py`:
- `SEED_ITEMS`: List of all seeds
- `GEAR_ITEMS`: List of all tools
- `EGG_ITEMS`: List of all eggs

### Adjusting Timers
Modify `shop_timers` in `MacroLogic.py`:
- Change restock times (in seconds)
- Add new shops if needed

### Speed Adjustment
Modify speed values in `main.py`:
- Change the speed mappings
- Add new speed options

## 🔄 Updates and Maintenance

### Regular Updates
- **Game updates** may require macro adjustments
- **Check item lists** if new items are added
- **Update shop timers** if restock times change

### Backup Your Settings
- **Save your webhook URL** and settings
- **Keep track of your preferred configurations**
- **Export settings** if needed for sharing

## 📞 Support

### Common Issues
1. **Macro not moving**: Check UI Navigation keybind
2. **Items not buying**: Verify item names and shop navigation
3. **Timer problems**: Restart macro to reset all timers
4. **Webhook errors**: Check Discord webhook URL

### Getting Help
- **Test each feature** individually
- **Check console output** for error messages
- **Verify game settings** match macro requirements
- **Start with simple configurations** and build up

## 🎯 Best Practices

1. **Start with few items** to test the macro
2. **Use Neutral speed** until you're comfortable
3. **Monitor the first few cycles** to ensure everything works
4. **Keep the game window active** and focused
5. **Don't run other automation** simultaneously

## 📋 Credits

**Made by King Clab and King Julian**

Enjoy your automated garden growing! 🌱✨