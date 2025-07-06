import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QTabWidget, QCheckBox, QScrollArea, QLineEdit, QFrame
)
from PyQt5.QtCore import Qt, QEvent, QTimer
from PyQt5.QtGui import QPixmap, QIcon
from MacroLogic import run_macro, stop_macro, set_macro_speed, get_selected_items, set_selected_items, get_ui_nav_key, set_ui_nav_key
from Webhook import test_webhook
from TimerWidget import TimerWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove title bar
        self.setFixedSize(800, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: black;
                color: white;
                font-weight: bold;
            }
            QTabWidget::pane {
                border: 2px solid purple;
            }
            QTabBar::tab {
                background: black;
                border: 1px solid purple;
                padding: 8px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: purple;
            }
            QPushButton {
                background-color: purple;
                color: white;
                font-weight: bold;
                padding: 8px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #9b59b6;
            }
            QComboBox {
                background-color: black;
                color: white;
                font-weight: bold;
                border: 1px solid purple;
                padding: 4px;
            }
            QLineEdit {
                background-color: #222222;
                color: white;
                font-weight: bold;
                border: 1px solid purple;
                padding: 4px;
            }
            QLabel {
                font-weight: bold;
            }
            QCheckBox {
                color: white;
                font-weight: bold;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid purple;
                background-color: black;
            }
            QCheckBox::indicator:checked {
                border: 2px solid purple;
                background-color: purple;
            }
        """)

        self.init_ui()
        self.old_pos = None
        
        # Store checkbox references for getting selected items
        self.seeds_checkboxes = {}
        self.gears_checkboxes = {}
        self.eggs_checkboxes = {}
        self.cosmetics_checkbox = None

        # Install event filter to capture keypresses for hotkeys
        self.installEventFilter(self)

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Custom title bar
        title_bar = self.create_title_bar()
        main_layout.addWidget(title_bar)
        
        # Main content
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(10, 10, 10, 10)
        
        # Title label
        title_label = QLabel("King Clab Macro")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white; margin-bottom: 10px;")
        title_label.setAlignment(Qt.AlignLeft)
        content_layout.addWidget(title_label)

        # Tabs
        self.tabs = QTabWidget()
        content_layout.addWidget(self.tabs)

        # Add tabs
        self.seeds_tab = self.create_scrollable_tab(self.get_seeds_content())
        self.gears_tab = self.create_scrollable_tab(self.get_gears_content())
        self.eggs_tab = self.create_scrollable_tab(self.get_eggs_content())
        self.cosmetics_tab = self.create_cosmetics_tab()
        self.settings_tab = self.create_settings_tab()
        self.credits_tab = self.create_credits_tab()

        self.tabs.addTab(self.seeds_tab, "Seeds")
        self.tabs.addTab(self.gears_tab, "Gears")
        self.tabs.addTab(self.eggs_tab, "Eggs")
        self.tabs.addTab(self.cosmetics_tab, "Cosmetics")
        self.tabs.addTab(self.settings_tab, "Settings")
        self.tabs.addTab(self.credits_tab, "Credits")

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def create_title_bar(self):
        title_bar = QFrame()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("background-color: #2d2d2d; border-bottom: 1px solid purple;")
        
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)
        
        # Title
        title = QLabel("King Clab Macro")
        title.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # Spacer
        layout.addStretch()
        
        # Minimize button
        minimize_btn = QPushButton()
        minimize_btn.setFixedSize(30, 30)
        minimize_btn.setStyleSheet("background-color: transparent; border: none;")
        if os.path.exists("Images/Minimize.png"):
            minimize_btn.setIcon(QIcon("Images/Minimize.png"))
        else:
            minimize_btn.setText("−")
        minimize_btn.clicked.connect(self.showMinimized)
        layout.addWidget(minimize_btn)
        
        # Close button
        close_btn = QPushButton()
        close_btn.setFixedSize(30, 30)
        close_btn.setStyleSheet("background-color: transparent; border: none;")
        if os.path.exists("Images/Close.png"):
            close_btn.setIcon(QIcon("Images/Close.png"))
        else:
            close_btn.setText("×")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        title_bar.setLayout(layout)
        return title_bar

    def create_scrollable_tab(self, content_widget):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content_widget)
        scroll.setStyleSheet("background-color: black; border: none;")
        return scroll

    def get_seeds_content(self):
        seeds = ["Carrot Seed", "Strawberry Seed", "Blueberry Seed", "Orange Tulip",
                 "Tomato Seed", "Daffodil Seed", "Watermelon Seed", "Pumpkin Seed",
                 "Apple Seed", "Bamboo Seed", "Coconut Seed", "Cactus Seed",
                 "Dragon Fruit Seed", "Mango Seed", "Grape Seed", "Mushroom Seed",
                 "Pepper Seed", "Cacao Seed", "Beanstalk Seed", "Ember Lily",
                 "Sugar Apple", "Burning Bud"]
        return self.create_checkbox_list(seeds, "seeds")

    def get_gears_content(self):
        gears = ["Watering Can", "Trowel", "Recall Wrench", "Basic Sprinkler",
                 "Advanced Sprinkler", "Godly Sprinkler", "Magnifying Glass", "Tanning Mirror",
                 "Master Sprinkler", "Cleaning Spray", "Favorite Tool", "Harvest Tool", "Friendship Pot"]
        return self.create_checkbox_list(gears, "gears")

    def get_eggs_content(self):
        eggs = ["Common Egg", "Common Summer Egg", "Rare Summer Egg",
                "Mythical Egg", "Paradise Egg", "Bee Egg", "Bug Egg"]
        return self.create_checkbox_list(eggs, "eggs")

    def create_cosmetics_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        info_label = QLabel("Note: Cosmetics shop has 9 different items.\nSelecting 'All cosmetics' will buy all available items.")
        info_label.setStyleSheet("color: #cccccc; font-size: 12px; margin-bottom: 10px;")
        layout.addWidget(info_label)
        
        self.cosmetics_checkbox = QCheckBox("All cosmetics")
        self.cosmetics_checkbox.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        layout.addWidget(self.cosmetics_checkbox)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_checkbox_list(self, items, category):
        widget = QWidget()
        layout = QVBoxLayout()
        
        checkboxes = {}
        for item in items:
            cb = QCheckBox(item)
            cb.setStyleSheet("color: white; font-weight: bold; margin: 2px;")
            layout.addWidget(cb)
            checkboxes[item] = cb
        
        # Store checkbox references
        if category == "seeds":
            self.seeds_checkboxes = checkboxes
        elif category == "gears":
            self.gears_checkboxes = checkboxes
        elif category == "eggs":
            self.eggs_checkboxes = checkboxes
            
        widget.setLayout(layout)
        return widget

    def create_settings_tab(self):
        widget = QWidget()
        main_layout = QHBoxLayout()
        
        # Left side - Settings
        left_layout = QVBoxLayout()

        # Webhook settings
        webhook_frame = QFrame()
        webhook_frame.setStyleSheet("border: 1px solid purple; padding: 10px; margin: 5px;")
        webhook_layout = QVBoxLayout()
        
        webhook_layout.addWidget(QLabel("Webhook URL:"))
        self.webhook_input = QLineEdit()
        self.webhook_input.setPlaceholderText("Enter your Discord webhook URL here")
        webhook_layout.addWidget(self.webhook_input)

        webhook_layout.addWidget(QLabel("Discord User ID:"))
        self.discord_id_input = QLineEdit()
        self.discord_id_input.setPlaceholderText("Enter your Discord user ID (optional)")
        webhook_layout.addWidget(self.discord_id_input)
        
        webhook_frame.setLayout(webhook_layout)
        left_layout.addWidget(webhook_frame)

        # Macro settings
        macro_frame = QFrame()
        macro_frame.setStyleSheet("border: 1px solid purple; padding: 10px; margin: 5px;")
        macro_layout = QVBoxLayout()
        
        macro_layout.addWidget(QLabel("UI Navigation Keybind:"))
        self.ui_nav_input = QLineEdit()
        self.ui_nav_input.setPlaceholderText("Enter your UI Navigation key (default: \\)")
        self.ui_nav_input.setText("\\")
        macro_layout.addWidget(self.ui_nav_input)

        macro_layout.addWidget(QLabel("Macro Speed:"))
        self.speed_dropdown = QComboBox()
        self.speed_dropdown.addItems(["Neutral", "Fast", "Ultra", "Max"])
        macro_layout.addWidget(self.speed_dropdown)

        self.warning_label = QLabel("")
        self.warning_label.setStyleSheet("color: red; font-weight: bold; font-size: 12px;")
        macro_layout.addWidget(self.warning_label)
        self.speed_dropdown.currentTextChanged.connect(self.speed_changed)
        
        macro_frame.setLayout(macro_layout)
        left_layout.addWidget(macro_frame)

        # Control buttons
        buttons_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Macro (F1)")
        self.start_button.clicked.connect(self.start_macro)
        buttons_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Macro (F2)")
        self.stop_button.clicked.connect(self.stop_macro)
        buttons_layout.addWidget(self.stop_button)

        self.test_webhook_button = QPushButton("Test Webhook")
        self.test_webhook_button.clicked.connect(self.test_webhook)
        buttons_layout.addWidget(self.test_webhook_button)

        left_layout.addLayout(buttons_layout)
        
        # Status label
        self.status_label = QLabel("Status: Ready")
        self.status_label.setStyleSheet("color: #00ff00; font-weight: bold; margin-top: 10px;")
        left_layout.addWidget(self.status_label)
        
        left_layout.addStretch()
        
        # Right side - Timer widget
        self.timer_widget = TimerWidget()
        
        # Add both sides to main layout
        main_layout.addLayout(left_layout)
        main_layout.addWidget(self.timer_widget)
        
        widget.setLayout(main_layout)
        return widget

    def create_credits_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        credits_label = QLabel("Made by King Clab, and King Julian")
        credits_label.setStyleSheet("font-weight: bold; font-size: 28px; color: white;")
        layout.addWidget(credits_label, alignment=Qt.AlignCenter)
        
        info_label = QLabel("Grow a Garden Macro\nFor educational purposes only")
        info_label.setStyleSheet("color: #cccccc; font-size: 14px; margin-top: 20px;")
        layout.addWidget(info_label, alignment=Qt.AlignCenter)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def speed_changed(self, text):
        if text == "Max":
            self.warning_label.setText("⚠️ Warning: Max speed requires very good FPS!")
        elif text == "Ultra":
            self.warning_label.setText("⚠️ Warning: Ultra speed may cause issues on slower computers!")
        else:
            self.warning_label.setText("")

    def get_selected_items(self):
        """Get all selected items from checkboxes"""
        selected = {
            "seeds": [name for name, cb in self.seeds_checkboxes.items() if cb.isChecked()],
            "gears": [name for name, cb in self.gears_checkboxes.items() if cb.isChecked()],
            "eggs": [name for name, cb in self.eggs_checkboxes.items() if cb.isChecked()],
            "cosmetics": self.cosmetics_checkbox.isChecked() if self.cosmetics_checkbox else False
        }
        return selected

    def start_macro(self):
        """Start the macro with current settings"""
        self.status_label.setText("Status: Starting macro...")
        self.status_label.setStyleSheet("color: #ffff00; font-weight: bold; margin-top: 10px;")
        
        # Get speed setting
        speed_map = {
            "Neutral": 0.05,
            "Fast": 0.03,
            "Ultra": 0.015,
            "Max": 0.005
        }
        chosen_speed = speed_map.get(self.speed_dropdown.currentText(), 0.05)
        set_macro_speed(chosen_speed)
        
        # Set UI navigation key
        ui_nav_key = self.ui_nav_input.text().strip() or "\\"
        set_ui_nav_key(ui_nav_key)
        
        # Get selected items
        selected_items = self.get_selected_items()
        set_selected_items(selected_items)
        
        # Start macro
        run_macro()
        
        self.status_label.setText("Status: Macro running...")
        self.status_label.setStyleSheet("color: #00ff00; font-weight: bold; margin-top: 10px;")

    def stop_macro(self):
        """Stop the macro"""
        stop_macro()
        self.status_label.setText("Status: Macro stopped")
        self.status_label.setStyleSheet("color: #ff0000; font-weight: bold; margin-top: 10px;")

    def test_webhook(self):
        """Test webhook functionality"""
        url = self.webhook_input.text().strip()
        if not url:
            self.status_label.setText("Status: Please enter a webhook URL")
            self.status_label.setStyleSheet("color: #ff0000; font-weight: bold; margin-top: 10px;")
            return
            
        success, message = test_webhook(url)
        if success:
            self.status_label.setText("Status: Webhook test successful!")
            self.status_label.setStyleSheet("color: #00ff00; font-weight: bold; margin-top: 10px;")
        else:
            self.status_label.setText(f"Status: Webhook failed - {message}")
            self.status_label.setStyleSheet("color: #ff0000; font-weight: bold; margin-top: 10px;")

    # Window dragging functionality
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPos() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

    # Hotkey handling
    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_F1:
                self.start_macro()
                return True
            elif event.key() == Qt.Key_F2:
                self.stop_macro()
                return True
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
