# 📁 File: ui/main_window.py
# 🔗 Project ID: VPNF-2025-001
# 🆔 File ID: 6834a7e24e348191b47388d4b9a70877
# 📃 Purpose: رابط گرافیکی اصلی برای مدیریت وضعیت VPN و نمایش لاگ
# 📅 Created on: 2025-05-26
# 📌 Edited on: 2025-05-27T23:15Z | Edit #4: افزودن دکمه بررسی مسیر فعال اینترنت بر اساس متریک سیستم

from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget,
    QTextEdit, QTabWidget, QSizePolicy, QStyle, QHBoxLayout
)
from PyQt5.QtCore import QTimer, Qt, QSize
from PyQt5.QtGui import QFont
from core.vpn_manager import get_vpn_status, reset_metrics, check_active_route
from core.metrics_backup import save_current_metrics, restore_metrics
from utils.logger import read_log

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VPN Failover Manager")
        self.resize(480, 360)
        self.setMinimumSize(400, 280)

        # --- تب‌ها ---
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("QTabBar::tab { padding: 8px 16px; font-size: 13px; }")

        # --- تب لاگ سیستم ---
        self.log_tab = QWidget()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 10))

        log_layout = QVBoxLayout()
        log_layout.setContentsMargins(10, 10, 10, 10)
        log_layout.addWidget(self.log_text)
        self.log_tab.setLayout(log_layout)

        # --- تب وضعیت اتصال ---
        self.status_tab = QWidget()
        self.status_label = QLabel("🔄 بررسی وضعیت...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Segoe UI", 12))
        self.status_label.setWordWrap(True)

        # دکمه‌های متریک
        self.reset_button = QPushButton("🔁 بازنشانی متریک‌ها")
        self.reset_button.setFont(QFont("Segoe UI", 10))
        self.reset_button.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        self.reset_button.setIconSize(QSize(18, 18))
        self.reset_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.reset_button.clicked.connect(self.handle_reset)

        self.save_button = QPushButton("🧷 ذخیره متریک‌ها")
        self.save_button.setFont(QFont("Segoe UI", 10))
        self.save_button.clicked.connect(self.handle_save)

        self.restore_button = QPushButton("♻️ بازیابی متریک‌ها")
        self.restore_button.setFont(QFont("Segoe UI", 10))
        self.restore_button.clicked.connect(self.handle_restore)

        self.route_button = QPushButton("🔎 بررسی مسیر فعال")
        self.route_button.setFont(QFont("Segoe UI", 10))
        self.route_button.clicked.connect(self.handle_route_check)

        # لایه افقی دکمه‌ها
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.restore_button)
        button_layout.addWidget(self.route_button)

        status_layout = QVBoxLayout()
        status_layout.setContentsMargins(10, 10, 10, 10)
        status_layout.setSpacing(12)
        status_layout.addWidget(self.status_label)
        status_layout.addLayout(button_layout)
        status_layout.addStretch()
        self.status_tab.setLayout(status_layout)

        # --- افزودن تب‌ها ---
        self.tabs.addTab(self.log_tab, "لاگ سیستم")
        self.tabs.addTab(self.status_tab, "وضعیت اتصال")

        # --- تنظیم چیدمان کلی ---
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.addWidget(self.tabs)
        self.setCentralWidget(container)

        # --- تایمر به‌روزرسانی ---
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
            self.status_label.setText("✅ اتصال از طریق NordVPN فعال است.")
            self.status_label.setStyleSheet("color: green; font-weight: bold;")
        elif status == "warp":
            self.status_label.setText("🟡 فقط WARP فعال است. استفاده از WARP.")
            self.status_label.setStyleSheet("color: orange; font-weight: bold;")
        else:
            self.status_label.setText("⚠️ هیچ VPN فعال نیست. استفاده از اینترنت عادی!")
            self.status_label.setStyleSheet("color: red; font-weight: bold;")

    def update_log(self):
        logs = read_log()
        self.log_text.setText(logs)

    def handle_reset(self):
        reset_metrics()
        self.status_label.setText("🔁 متریک‌ها ریست شدند.")

    def handle_save(self):
        interfaces = ["Wi-Fi", "Cloudflare WARP", "NordLynx"]
        save_current_metrics(interfaces)
        self.status_label.setText("🧷 متریک‌ها ذخیره شدند.")

    def handle_restore(self):
        restore_metrics()
        self.status_label.setText("♻️ متریک‌ها بازیابی شدند.")

    def handle_route_check(self):
        route_info = check_active_route()
        self.status_label.setText(f"🔎 مسیر فعال: {route_info}")
