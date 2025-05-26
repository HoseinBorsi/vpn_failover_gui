# 📁 File: ui/main_window.py
# 🔗 Project ID: VPNF-2025-001
# 🆔 File ID: 6834a7e24e348191b47388d4b9a70877
# 📃 Purpose: رابط گرافیکی اصلی برای نمایش وضعیت VPN و لاگ‌ها
# 📅 Created on: 2025-05-26
# 📌 Edited on: 2025-05-26 | Edit #1: افزودن نمایش لاگ در تب جداگانه

from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QTextEdit, QTabWidget
from PyQt5.QtCore import QTimer
from core.vpn_manager import get_vpn_status, reset_metrics
from utils.logger import read_log

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VPN Failover Manager")
        self.setFixedSize(400, 300)

        self.tabs = QTabWidget()

        # --- تب وضعیت VPN ---
        self.status_tab = QWidget()
        self.status_label = QLabel("🔄 بررسی وضعیت...")
        self.status_label.setStyleSheet("font-size: 16px; text-align: center;")

        self.reset_button = QPushButton("🔁 بازنشانی متریک‌ها")
        self.reset_button.clicked.connect(self.handle_reset)

        status_layout = QVBoxLayout()
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.reset_button)
        self.status_tab.setLayout(status_layout)

        # --- تب لاگ‌ها ---
        self.log_tab = QWidget()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)

        log_layout = QVBoxLayout()
        log_layout.addWidget(self.log_text)
        self.log_tab.setLayout(log_layout)

        # --- افزودن تب‌ها به تب‌ویجت ---
        self.tabs.addTab(self.status_tab, "وضعیت اتصال")
        self.tabs.addTab(self.log_tab, "لاگ سیستم")

        self.setCentralWidget(self.tabs)

        # تایمر برای آپدیت خودکار وضعیت و لاگ
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(15000)

        self.refresh()

    def refresh(self):
        self.update_status()
        self.update_log()

    def update_status(self):
        status = get_vpn_status()
        if status == "nord":
            self.status_label.setText("✅ اتصال از طریق NordVPN")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
        elif status == "warp":
            self.status_label.setText("🟡 اتصال از طریق WARP")
            self.status_label.setStyleSheet("color: orange; font-weight: bold;")
        else:
            self.status_label.setText("⚠️ بدون VPN - استفاده از اینترنت عادی")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")

    def update_log(self):
        logs = read_log()
        self.log_text.setText(logs)

    def handle_reset(self):
        reset_metrics()
        self.status_label.setText("🔁 متریک‌ها ریست شدند.")
