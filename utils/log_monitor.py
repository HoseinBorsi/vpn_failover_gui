# 📁 File: utils/log_monitor.py
# 🔗 Project ID: VPNF-2025-001
# 🆔 File ID: 6838639505948191ad59c3f83f5a6587
# 📃 Purpose: مانیتور زنده لاگ‌ها برای شناسایی خطاهای بحرانی و واکنش خودکار و نمایشی در رابط گرافیکی
# 📅 Created on: 2025-05-29
# 📌 Edited on: 2025-05-29 | Edit #1: نمایش پیغام هشدار در رابط گرافیکی هنگام بروز خطای بحرانی

import os
import time
import subprocess
import threading
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSignal, QObject

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, 'local_logs', 'vpn_failover.log')

CRITICAL_ERRORS = [
    'WinError 2',
    'returned non-zero exit status',
    'هیچ VPN فعالی یافت نشد',
    'WARP نصب است ولی وصل نیست'
]

class LogAlertEmitter(QObject):
    alert = pyqtSignal(str)

emitter = LogAlertEmitter()

def attempt_recovery():
    try:
        subprocess.run(["warp-cli", "connect"], check=True)
    except Exception as e:
        emitter.alert.emit(f"خطا در اتصال مجدد WARP: {e}")

# مانیتور اصلی که توسط ترد در main.py اجرا می‌شود
def monitor_log_gui():
    last_size = 0
    while True:
        try:
            current_size = os.path.getsize(LOG_FILE)
            if current_size > last_size:
                with open(LOG_FILE, 'r', encoding='utf-8') as f:
                    f.seek(last_size)
                    new_lines = f.readlines()
                    for line in new_lines:
                        for keyword in CRITICAL_ERRORS:
                            if keyword in line:
                                emitter.alert.emit(f"⚠️ خطای بحرانی: {keyword}")
                                attempt_recovery()
                                break
                last_size = current_size
            time.sleep(5)
        except Exception as e:
            emitter.alert.emit(f"⚠️ خطا در مانیتورینگ لاگ: {e}")
            time.sleep(10)

# تابعی برای اتصال به GUI

def bind_gui_alert(window):
    def show_alert(message):
        QMessageBox.warning(window, "هشدار بحرانی از لاگ‌ها", message)
    emitter.alert.connect(show_alert)

# برای اجرای مستقل تستی بدون GUI
if __name__ == '__main__':
    print("📡 اجرای مانیتور مستقل لاگ...")
    monitor_log_gui()
