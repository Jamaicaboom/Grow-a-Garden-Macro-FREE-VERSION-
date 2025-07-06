import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QTabWidget, QCheckBox, QScrollArea, QLineEdit
)
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QKeySequence
from MacroLogic import run_macro, stop_macro, set_macro_speed, test_webhook_func

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
        """)

        self.init_ui()
        self.old_pos = None

        # Install event filter to capture keypresses for hotkeys
        self.installEventFilter(self)

    def init_ui(self):
        main_layout = QVBoxLayout()
        # Title label top-left
        title_label = QLabel("King Clab Macro")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        title_label.setAlignment(Qt.AlignLeft)
        main_layout.addWidget(title_label)

        # Tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

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

        self.setLayout(main_layout)

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
        return self.create_checkbox_list(seeds)

    def get_gears_content(self):
        gears = ["Watering Can", "Trowel", "Recall Wrench", "Basic Sprinkler",
                 "Advanced Sprinkler", "Godly Sprinkler", "Magnifying Glass", "Tanning Mirror",
                 "Master Sprinkler", "Cleaning Spray", "Favorite Tool", "Harvest Tool", "Friendship Pot"]
        return self.create_checkbox_list(gears)

    def get_eggs_content(self):
        eggs = ["Common Egg", "Common Summer Egg", "Rare Summer Egg",
                "Mythical Egg", "Paradise Egg", "Bee Egg", "Bug Egg"]
        return self.create_checkbox_list(eggs)

    def create_cosmetics_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        all_cosmetics_checkbox = QCheckBox("All cosmetics")
        all_cosmetics_checkbox.setStyleSheet("color: white; font-weight: bold;")
        layout.addWidget(all_cosmetics_checkbox)
        widget.setLayout(layout)
        return widget

    def create_checkbox_list(self, items):
        widget = QWidget()
        layout = QVBoxLayout()
        for item in items:
            cb = QCheckBox(item)
            cb.setStyleSheet("color: white; font-weight: bold;")
            layout.addWidget(cb)
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
        layout.addWidget(self.discord_id_input)

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

    def speed_changed(self, text):
        if text == "Max":
            self.warning_label.setText("Warning: Max speed requires very good FPS!")
        else:
            self.warning_label.setText("")

    def start_macro(self):
        speed_map = {
            "Neutral": 0.05,
            "Fast": 0.03,
            "Ultra": 0.015,
            "Max": 0.005
        }
        chosen_speed = speed_map.get(self.speed_dropdown.currentText(), 0.05)
        set_macro_speed(chosen_speed)
        run_macro()

    def stop_macro(self):
        stop_macro()

    def test_webhook(self):
        url = self.webhook_input.text().strip()
        success, message = test_webhook_func(url)
        if success:
            print("Webhook test succeeded!")
        else:
            print(f"Webhook test failed: {message}")

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
