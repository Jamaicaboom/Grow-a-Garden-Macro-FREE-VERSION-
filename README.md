# 🌱 King Clab's Grow a Garden Macro

A comprehensive Python macro for automating shop purchases in Roblox's "Grow a Garden" game.

## ⚠️ Important Disclaimer

This macro is for **educational purposes only**. Use at your own risk. The developers are not responsible for any consequences of using this macro, including but not limited to account bans or other penalties.

## ✨ Features

- **Automated Shop Navigation**: Automatically navigates to Seeds, Gears, Eggs, and Cosmetics shops
- **Smart Timer System**: Tracks shop restock times and only visits when items are available
- **Custom UI**: Purple and black themed interface with custom window controls
- **Webhook Integration**: Discord webhook support for purchase notifications
- **Recall Wrench Support**: Uses recall wrench to teleport between shops
- **Speed Controls**: Multiple speed settings (Neutral, Fast, Ultra, Max)
- **Real-time Timers**: Live display of shop restock countdowns

## 🛠️ Installation

### Prerequisites

- Python 3.7 or higher
- Roblox account with access to "Grow a Garden"
- Basic understanding of running Python scripts

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Set Up Game Requirements

1. **Get a Recall Wrench**: You need a recall wrench in your inventory slot 2
2. **Set UI Navigation Key**: Make sure your UI Navigation key is set (default: `\`)
3. **Position Your Character**: Start near the seed shop area

### Step 3: Configure Settings

1. Run the macro:
   ```bash
   python main.py
   ```

2. Go to the **Settings** tab and configure:
   - **Webhook URL**: (Optional) Your Discord webhook URL for notifications
   - **Discord User ID**: (Optional) Your Discord user ID
   - **UI Navigation Key**: The key you use for UI Navigation (default: `\`)
   - **Macro Speed**: Choose your preferred speed

## 📖 How to Use

### Basic Usage

1. **Select Items**: Go to each tab (Seeds, Gears, Eggs, Cosmetics) and check the items you want to buy
2. **Configure Settings**: Set your preferred speed and UI Navigation key
3. **Start Macro**: Click "Start Macro" or press F1
4. **Stop Macro**: Click "Stop Macro" or press F2

### Shop Types

#### 🌱 Seeds Shop
- Select individual seeds you want to purchase
- Macro will navigate to seed shop and buy selected items
- Items available: Carrot Seed, Strawberry Seed, Blueberry Seed, and more

#### 🛠️ Gears Shop
- Select individual gears you want to purchase
- Uses recall wrench to teleport to gear shop
- Zooms in close to access the first option
- Items available: Watering Can, Trowel, Recall Wrench, and more

#### 🥚 Eggs Shop
- Select individual eggs you want to purchase
- Checks 3 different egg spots
- Items available: Common Egg, Rare Summer Egg, Mythical Egg, and more

#### 💄 Cosmetics Shop
- Simple checkbox for "All cosmetics"
- Navigates through all 9 cosmetic items
- Spams buy button for each item

### Timer System

The macro includes a smart timer system that:
- Tracks the last visit time for each shop
- Calculates when shops will restock (default: 1 hour)
- Only visits shops when they're ready for restock
- Displays countdown timers in the GUI

## ⚙️ Speed Settings

- **Neutral**: Safest speed, good for slower computers (0.05s delay)
- **Fast**: Faster execution, requires decent performance (0.03s delay)
- **Ultra**: Very fast, may cause issues on slower computers (0.015s delay)
- **Max**: Maximum speed, requires excellent FPS (0.005s delay)

⚠️ **Warning**: Higher speeds require better computer performance and may cause issues if your game runs at low FPS.

## 🔧 Advanced Configuration

### Webhook Setup

1. Create a Discord webhook in your Discord server
2. Copy the webhook URL
3. Paste it in the "Webhook URL" field in settings
4. Test the webhook using the "Test Webhook" button

### Custom UI Navigation Key

If you use a different key for UI Navigation:
1. Go to Settings tab
2. Enter your custom key in the "UI Navigation Keybind" field
3. The macro will use your custom key instead of the default `\`

## 🎮 Game Setup Tips

1. **Inventory Management**: Keep your recall wrench in slot 2
2. **Camera Position**: The macro will automatically adjust camera settings
3. **Character Position**: Start near the seed shop area for best results
4. **UI Navigation**: Make sure UI Navigation is working properly in your game

## 📊 Understanding the Interface

### Main Tabs

- **Seeds**: Select individual seeds to purchase
- **Gears**: Select individual gears to purchase  
- **Eggs**: Select individual eggs to purchase
- **Cosmetics**: Toggle all cosmetics on/off
- **Settings**: Configure macro settings and view timers
- **Credits**: Information about the developers

### Timer Display

The timer widget shows:
- Current restock status for each shop
- Countdown timers until next restock
- Green text = Ready to visit
- Yellow text = Time remaining until restock

## 🚨 Troubleshooting

### Common Issues

1. **Macro Not Working**: 
   - Check that your UI Navigation key is correct
   - Ensure you have a recall wrench in slot 2
   - Make sure Roblox is the active window

2. **Speed Issues**:
   - Lower the speed setting if actions are too fast
   - Increase the speed if actions are too slow

3. **Shop Navigation Problems**:
   - Verify your character is positioned correctly
   - Check that UI Navigation is working in game

4. **Webhook Not Working**:
   - Verify the webhook URL is correct
   - Test the webhook using the test button

### Performance Tips

- Close unnecessary programs to improve FPS
- Use windowed mode for better performance
- Start with "Neutral" speed and increase gradually
- Monitor your system performance while running

## 📝 File Structure

```
grow-a-garden-macro/
├── main.py              # Main GUI application
├── MacroLogic.py        # Core macro functionality
├── Webhook.py           # Discord webhook integration
├── TimerWidget.py       # Timer display widget
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── Images/             # UI images
    ├── Close.png       # Close button image
    └── Minimize.png    # Minimize button image
```

## 🤝 Contributing

This project is created by King Clab and King Julian. If you find bugs or have suggestions:

1. Test thoroughly before reporting
2. Provide detailed information about issues
3. Include your system specifications
4. Describe exact steps to reproduce problems

## 📄 License

This project is for educational purposes only. Use at your own risk.

## 🙏 Acknowledgments

- Created by King Clab and King Julian
- Built for the Roblox "Grow a Garden" community
- Thanks to all testers and contributors

---

**Remember**: This is an educational project. Always follow Roblox's Terms of Service and play responsibly!