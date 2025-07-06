import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QTabWidget, QCheckBox, QScrollArea, QLineEdit, QGridLayout,
    QProgressBar, QFrame
)
from PyQt5.QtCore import Qt, QEvent, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QIcon, QPalette, QColor
from MacroLogic import run_macro, stop_macro, set_macro_speed, get_selected_items, set_ui_nav_key, get_shop_timers
from Webhook import test_webhook

class TimerThread(QThread):
    timer_updated = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.running = True
        
    def run(self):
        while self.running:
            timers = get_shop_timers()
            self.timer_updated.emit(timers)
            self.msleep(1000)  # Update every second
    
    def stop(self):
        self.running = False
        self.quit()
        self.wait()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove default title bar
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
            QProgressBar {
                border: 1px solid purple;
                border-radius: 4px;
                text-align: center;
                color: white;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: purple;
                border-radius: 3px;
            }
        """)

        # Store checkbox references for easy access (initialize before UI)
        self.seed_checkboxes = {}
        self.gear_checkboxes = {}
        self.egg_checkboxes = {}
        self.cosmetics_checkbox = None
        
        self.init_ui()
        self.old_pos = None
        
        # Timer thread for shop restock timers
        self.timer_thread = TimerThread()
        self.timer_thread.timer_updated.connect(self.update_timers)
        self.timer_thread.start()

        # Install event filter to capture keypresses for hotkeys
        self.installEventFilter(self)

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Custom title bar
        title_bar = self.create_title_bar()
        main_layout.addWidget(title_bar)
        
        # Content area
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(10, 10, 10, 10)
        
        # Shop timers display
        self.timer_display = self.create_timer_display()
        content_layout.addWidget(self.timer_display)

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
        title_bar.setStyleSheet("background-color: #1a1a1a; border-bottom: 2px solid purple;")
        
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Title
        title_label = QLabel("King Clab Macro")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        layout.addWidget(title_label)
        
        # Spacer
        layout.addStretch()
        
        # Minimize button
        minimize_btn = QPushButton()
        minimize_btn.setFixedSize(30, 30)
        minimize_btn.setStyleSheet("background-color: transparent; border: none;")
        if os.path.exists("Images/Minimize.png"):
            minimize_btn.setIcon(QIcon("Images/Minimize.png"))
        else:
            minimize_btn.setText("_")
        minimize_btn.clicked.connect(self.showMinimized)
        layout.addWidget(minimize_btn)
        
        # Close button
        close_btn = QPushButton()
        close_btn.setFixedSize(30, 30)
        close_btn.setStyleSheet("background-color: transparent; border: none;")
        if os.path.exists("Images/Close.png"):
            close_btn.setIcon(QIcon("Images/Close.png"))
        else:
            close_btn.setText("X")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        title_bar.setLayout(layout)
        return title_bar
    
    def create_timer_display(self):
        timer_frame = QFrame()
        timer_frame.setStyleSheet("border: 1px solid purple; border-radius: 4px; padding: 5px;")
        
        layout = QGridLayout()
        
        # Timer labels and progress bars
        self.seed_timer_label = QLabel("Seed Shop: Ready")
        self.seed_timer_bar = QProgressBar()
        self.seed_timer_bar.setVisible(False)
        
        self.gear_timer_label = QLabel("Gear Shop: Ready")
        self.gear_timer_bar = QProgressBar()
        self.gear_timer_bar.setVisible(False)
        
        self.egg_timer_label = QLabel("Egg Shop: Ready")
        self.egg_timer_bar = QProgressBar()
        self.egg_timer_bar.setVisible(False)
        
        self.cosmetic_timer_label = QLabel("Cosmetic Shop: Ready")
        self.cosmetic_timer_bar = QProgressBar()
        self.cosmetic_timer_bar.setVisible(False)
        
        layout.addWidget(QLabel("Shop Restock Timers:"), 0, 0, 1, 2)
        layout.addWidget(self.seed_timer_label, 1, 0)
        layout.addWidget(self.seed_timer_bar, 1, 1)
        layout.addWidget(self.gear_timer_label, 2, 0)
        layout.addWidget(self.gear_timer_bar, 2, 1)
        layout.addWidget(self.egg_timer_label, 3, 0)
        layout.addWidget(self.egg_timer_bar, 3, 1)
        layout.addWidget(self.cosmetic_timer_label, 4, 0)
        layout.addWidget(self.cosmetic_timer_bar, 4, 1)
        
        timer_frame.setLayout(layout)
        return timer_frame
    
    def update_timers(self, timers):
        """Update the timer display with current shop restock times"""
        for shop, data in timers.items():
            if shop == "Seeds":
                if data['time_left'] > 0:
                    self.seed_timer_label.setText(f"Seed Shop: {data['time_left']}s")
                    self.seed_timer_bar.setVisible(True)
                    self.seed_timer_bar.setMaximum(data['total_time'])
                    self.seed_timer_bar.setValue(data['total_time'] - data['time_left'])
                else:
                    self.seed_timer_label.setText("Seed Shop: Ready")
                    self.seed_timer_bar.setVisible(False)
            elif shop == "Gears":
                if data['time_left'] > 0:
                    self.gear_timer_label.setText(f"Gear Shop: {data['time_left']}s")
                    self.gear_timer_bar.setVisible(True)
                    self.gear_timer_bar.setMaximum(data['total_time'])
                    self.gear_timer_bar.setValue(data['total_time'] - data['time_left'])
                else:
                    self.gear_timer_label.setText("Gear Shop: Ready")
                    self.gear_timer_bar.setVisible(False)
            elif shop == "Eggs":
                if data['time_left'] > 0:
                    self.egg_timer_label.setText(f"Egg Shop: {data['time_left']}s")
                    self.egg_timer_bar.setVisible(True)
                    self.egg_timer_bar.setMaximum(data['total_time'])
                    self.egg_timer_bar.setValue(data['total_time'] - data['time_left'])
                else:
                    self.egg_timer_label.setText("Egg Shop: Ready")
                    self.egg_timer_bar.setVisible(False)
            elif shop == "Cosmetics":
                if data['time_left'] > 0:
                    self.cosmetic_timer_label.setText(f"Cosmetic Shop: {data['time_left']}s")
                    self.cosmetic_timer_bar.setVisible(True)
                    self.cosmetic_timer_bar.setMaximum(data['total_time'])
                    self.cosmetic_timer_bar.setValue(data['total_time'] - data['time_left'])
                else:
                    self.cosmetic_timer_label.setText("Cosmetic Shop: Ready")
                    self.cosmetic_timer_bar.setVisible(False)

    def create_scrollable_tab(self, content_widget):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(content_widget)
        scroll.setStyleSheet("background-color: black;")
        return scroll

    def get_seeds_content(self):
        seeds = ["Carrot Seed", "Strawberry Seed", "Blueberry Seed", "Orange Tulip",
                 "Tomato Seed", "Daffodil Seed", "Watermelon Seed", "Pumpkin Seed",
                 "Apple Seed", "Bamboo Seed", "Coconut Seed", "Cactus Seed",
                 "Dragon Fruit Seed", "Mango Seed", "Grape Seed", "Mushroom Seed",
                 "Pepper Seed", "Cacao Seed", "Beanstalk Seed", "Ember Lily",
                 "Sugar Apple", "Burning Bud"]
        return self.create_checkbox_list(seeds, "Seeds")

    def get_gears_content(self):
        gears = ["Watering Can", "Trowel", "Recall Wrench", "Basic Sprinkler",
                 "Advanced Sprinkler", "Godly Sprinkler", "Magnifying Glass", "Tanning Mirror",
                 "Master Sprinkler", "Cleaning Spray", "Favorite Tool", "Harvest Tool", "Friendship Pot"]
        return self.create_checkbox_list(gears, "Gears")

    def get_eggs_content(self):
        eggs = ["Common Egg", "Common Summer Egg", "Rare Summer Egg",
                "Mythical Egg", "Paradise Egg", "Bee Egg", "Bug Egg"]
        return self.create_checkbox_list(eggs, "Eggs")

    def create_cosmetics_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        self.cosmetics_checkbox = QCheckBox("All cosmetics")
        self.cosmetics_checkbox.setStyleSheet("color: white; font-weight: bold;")
        layout.addWidget(self.cosmetics_checkbox)
        
        # Add info label
        info_label = QLabel("Note: This will purchase all 9 cosmetic items")
        info_label.setStyleSheet("color: #888888; font-size: 11px;")
        layout.addWidget(info_label)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_checkbox_list(self, items, category):
        widget = QWidget()
        layout = QVBoxLayout()
        
        for item in items:
            cb = QCheckBox(item)
            cb.setStyleSheet("color: white; font-weight: bold;")
            layout.addWidget(cb)
            
            # Store checkbox reference
            if category == "Seeds":
                self.seed_checkboxes[item] = cb
            elif category == "Gears":
                self.gear_checkboxes[item] = cb
            elif category == "Eggs":
                self.egg_checkboxes[item] = cb
                
        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_settings_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Webhook URL:"))
        self.webhook_input = QLineEdit()
        self.webhook_input.setPlaceholderText("Enter your webhook URL here")
        layout.addWidget(self.webhook_input)

        layout.addWidget(QLabel("Discord User ID:"))
        self.discord_id_input = QLineEdit()
        self.discord_id_input.setPlaceholderText("Enter your Discord User ID")
        layout.addWidget(self.discord_id_input)
        
        layout.addWidget(QLabel("UI Navigation Keybind:"))
        self.ui_nav_input = QLineEdit()
        self.ui_nav_input.setPlaceholderText("Enter keybind (e.g., \\)")
        self.ui_nav_input.setText("\\")  # Default value
        self.ui_nav_input.textChanged.connect(self.update_ui_nav_key)
        layout.addWidget(self.ui_nav_input)

        layout.addWidget(QLabel("Macro Speed:"))
        self.speed_dropdown = QComboBox()
        self.speed_dropdown.addItems(["Neutral", "Fast", "Ultra", "Max"])
        layout.addWidget(self.speed_dropdown)

        self.warning_label = QLabel("")
        self.warning_label.setStyleSheet("color: red; font-weight: bold;")
        layout.addWidget(self.warning_label)
        self.speed_dropdown.currentTextChanged.connect(self.speed_changed)

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

        layout.addLayout(buttons_layout)
        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_credits_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        credits_label = QLabel("Made by King Clab, and King Julian")
        credits_label.setStyleSheet("font-weight: bold; font-size: 28px; color: white;")
        layout.addWidget(credits_label, alignment=Qt.AlignCenter)
        widget.setLayout(layout)
        return widget

    def update_ui_nav_key(self, text):
        """Update the UI navigation key in the macro logic"""
        if text:
            set_ui_nav_key(text)

    def speed_changed(self, text):
        if text == "Max":
            self.warning_label.setText("Warning: Max speed requires very good FPS!")
        else:
            self.warning_label.setText("")

    def get_selected_items(self):
        """Get all selected items from checkboxes"""
        selected = {
            "Seeds": [],
            "Gears": [],
            "Eggs": [],
            "Cosmetics": []
        }
        
        # Get selected seeds
        for item, checkbox in self.seed_checkboxes.items():
            if checkbox.isChecked():
                selected["Seeds"].append(item)
        
        # Get selected gears
        for item, checkbox in self.gear_checkboxes.items():
            if checkbox.isChecked():
                selected["Gears"].append(item)
        
        # Get selected eggs
        for item, checkbox in self.egg_checkboxes.items():
            if checkbox.isChecked():
                selected["Eggs"].append(item)
        
        # Get cosmetics selection
        if self.cosmetics_checkbox and self.cosmetics_checkbox.isChecked():
            selected["Cosmetics"] = ["All"]
        
        return selected

    def start_macro(self):
        # Get selected items
        selected_items = self.get_selected_items()
        
        # Check if any items are selected
        if not any(selected_items.values()):
            print("No items selected! Please select items to purchase.")
            return
        
        # Set macro speed
        speed_map = {
            "Neutral": 0.05,
            "Fast": 0.03,
            "Ultra": 0.015,
            "Max": 0.005
        }
        chosen_speed = speed_map.get(self.speed_dropdown.currentText(), 0.05)
        set_macro_speed(chosen_speed)
        
        # Get webhook URL
        webhook_url = self.webhook_input.text().strip()
        
        # Start macro with selected items
        run_macro(selected_items, webhook_url)

    def stop_macro(self):
        stop_macro()

    def test_webhook(self):
        url = self.webhook_input.text().strip()
        success, message = test_webhook(url)
        if success:
            print("Webhook test succeeded!")
        else:
            print(f"Webhook test failed: {message}")

    def closeEvent(self, event):
        """Clean up when closing the application"""
        self.timer_thread.stop()
        event.accept()

    # Draggable window override
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

    # Event filter to capture F1/F2 key presses globally within the window
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
