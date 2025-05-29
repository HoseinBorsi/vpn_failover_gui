# 📁 File: ui/main_window.py
# 🔗 Project ID: VPNF-2025-001
# 🆔 File ID: 6834a7e24e348191b47388d4b9a70877
# 📃 Purpose: رابط گرافیکی اصلی برای مدیریت وضعیت VPN و نمایش لاگ
# 📅 Created on: 2025-05-26
# 📌 Edited on: 2025-05-27T21:00Z | Edit #2: بازگشت به نسخه پایه با ابعاد اولیه و بدون افکت گرافیکی اضافی
# 📌 Edited on: 2025-05-29 | Edit #3: افزودن دکمه روشن/خاموش و اسکرول خودکار لاگ به آخر

from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget,
    QTextEdit, QTabWidget, QSizePolicy, QSpacerItem, QStyle
)
from PyQt5.QtCore import QTimer, Qt, QSize
from PyQt5.QtGui import QFont
from core.vpn_manager import get_vpn_status, reset_metrics
from utils.logger import read_log, log_info
import subprocess
import sys
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VPN Failover Manager")
        self.resize(480, 320)
        self.setMinimumSize(400, 280)

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

        self.toggle_button = QPushButton("🟢 روشن")
        self.toggle_button.setFont(QFont("Segoe UI", 10))
        self.toggle_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.toggle_button.setIconSize(QSize(18, 18))
        self.toggle_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(True)
        self.toggle_button.clicked.connect(self.toggle_vpn_logic)

        status_layout = QVBoxLayout()
        status_layout.setContentsMargins(10, 10, 10, 10)
        status_layout.setSpacing(12)
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.toggle_button)
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
        if self.toggle_button.isChecked():
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
        self.log_text.verticalScrollBar().setValue(self.log_text.verticalScrollBar().maximum())

    def toggle_vpn_logic(self):
        if self.toggle_button.isChecked():
            self.toggle_button.setText("🟢 روشن")
            self.toggle_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            log_info("🔄 برنامه دوباره فعال شد.")
            self.refresh()
        else:
            self.toggle_button.setText("🔴 خاموش")
            self.toggle_button.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
            self.status_label.setText("⛔ بررسی اتصال متوقف شد.")
            self.status_label.setStyleSheet("color: gray;")
            log_info("⛔ بررسی وضعیت VPN غیرفعال شد.")
