import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
from datetime import datetime, timedelta

class TimerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
        # Timer to update display every second
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_display)
        self.update_timer.start(1000)  # Update every second
        
        # Shop restock times (same as MacroLogic)
        self.shop_restock_times = {
            "seeds": 60,      # 1 hour
            "gears": 60,      # 1 hour
            "eggs": 60,       # 1 hour
            "cosmetics": 60   # 1 hour
        }
        
        # Last visit times (will be updated by macro)
        self.last_shop_visit = {
            "seeds": None,
            "gears": None,
            "eggs": None,
            "cosmetics": None
        }
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Shop Restock Timers")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: white; margin-bottom: 10px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Timer frame
        timer_frame = QFrame()
        timer_frame.setStyleSheet("border: 1px solid purple; padding: 10px; margin: 5px;")
        timer_layout = QVBoxLayout()
        
        # Shop timer labels
        self.shop_labels = {}
        for shop_type in ["seeds", "gears", "eggs", "cosmetics"]:
            label = QLabel(f"{shop_type.capitalize()}: Ready!")
            label.setStyleSheet("color: #00ff00; font-weight: bold; margin: 2px;")
            timer_layout.addWidget(label)
            self.shop_labels[shop_type] = label
        
        timer_frame.setLayout(timer_layout)
        layout.addWidget(timer_frame)
        
        # Status label
        self.status_label = QLabel("Waiting for macro to start...")
        self.status_label.setStyleSheet("color: #cccccc; font-size: 12px; margin-top: 10px;")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def update_shop_visit_time(self, shop_type):
        """Update the last visit time for a shop"""
        self.last_shop_visit[shop_type] = datetime.now()
    
    def calculate_next_restock_time(self, shop_type):
        """Calculate when the next restock will happen"""
        last_visit = self.last_shop_visit.get(shop_type)
        if not last_visit:
            return datetime.now()
        
        restock_minutes = self.shop_restock_times.get(shop_type, 60)
        return last_visit + timedelta(minutes=restock_minutes)
    
    def update_display(self):
        """Update the timer display"""
        try:
            for shop_type, label in self.shop_labels.items():
                next_restock = self.calculate_next_restock_time(shop_type)
                time_left = next_restock - datetime.now()
                
                if time_left.total_seconds() <= 0:
                    label.setText(f"{shop_type.capitalize()}: READY!")
                    label.setStyleSheet("color: #00ff00; font-weight: bold; margin: 2px;")
                else:
                    minutes_left = int(time_left.total_seconds() // 60)
                    seconds_left = int(time_left.total_seconds() % 60)
                    label.setText(f"{shop_type.capitalize()}: {minutes_left}m {seconds_left}s")
                    label.setStyleSheet("color: #ffff00; font-weight: bold; margin: 2px;")
        except Exception as e:
            print(f"Error updating timer display: {e}")
    
    def set_macro_status(self, status):
        """Set the macro status message"""
        self.status_label.setText(status)