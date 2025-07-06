# 🚀 Quick Installation Guide

## Step 1: Check Python

Open a terminal/command prompt and run:
```bash
python --version
```
or
```bash
python3 --version
```

**Need Python 3.7+**. If you don't have it, download from [python.org](https://python.org)

## Step 2: Install Dependencies

Choose the method that works for your system:

### 🪟 **Windows**
```cmd
pip install -r requirements.txt
```

### 🐧 **Linux/Ubuntu**
```bash
pip3 install -r requirements.txt
```

### 🍎 **macOS**
```bash
pip3 install -r requirements.txt
```

### 🔒 **If you get permission errors:**
```bash
pip install -r requirements.txt --user
```

### 🐍 **If pip is not found:**
```bash
python -m pip install -r requirements.txt
```

## Step 3: Test Installation

Run the simple test (no GUI needed):
```bash
python test_macro_simple.py
```

**Expected output:**
```
✅ MacroLogic imported successfully
✅ All basic tests passed!
```

## Step 4: Start the Macro

### Easy Way:
- **Windows**: Double-click `start_macro.bat`
- **Linux/macOS**: Double-click `start_macro.sh`

### Manual Way:
```bash
python main.py
```

## 🚨 Common Issues & Fixes

### Issue: "No module named 'PyQt5'"
```bash
pip install PyQt5
```

### Issue: "No module named 'pyautogui'"
```bash
pip install pyautogui
```

### Issue: "No module named 'keyboard'"
```bash
pip install keyboard
```

### Issue: Macro button doesn't work
1. Check the **green console** at the bottom of the GUI
2. Look for error messages
3. Install any missing dependencies shown

### Issue: "pip: command not found"
- **Windows**: Reinstall Python and check "Add to PATH"
- **Linux**: `sudo apt install python3-pip`
- **macOS**: Install using [Homebrew](https://brew.sh): `brew install python`

## ✅ Success Checklist

After installation, you should see:
- [ ] GUI opens without errors
- [ ] Green console shows "Console Ready"
- [ ] All tabs (Seeds, Gears, Eggs) load properly
- [ ] Checkboxes are clickable
- [ ] Start button changes to "Starting..." when clicked

## 🆘 Still Having Issues?

1. **Run the simple test:**
   ```bash
   python test_macro_simple.py
   ```

2. **Check what the console says** when you try to start the macro

3. **Common dependency install:**
   ```bash
   pip install PyQt5 pyautogui keyboard requests pillow
   ```

4. **Try with python3 instead of python**:
   ```bash
   python3 main.py
   ```

## 🎮 Ready to Use!

Once installed successfully:
1. **Select items** in Seeds/Gears/Eggs tabs
2. **Configure settings** (optional webhook)
3. **Open Roblox** and join "Grow a Garden"
4. **Press F1** to start the macro

The macro will show detailed progress in the green console! 🌱✨