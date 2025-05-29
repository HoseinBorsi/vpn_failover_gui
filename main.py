# 📁 File: main.py
# 🔗 Project ID: VPNF-2025-001
# 🆔 File ID: 6834a54280ec819195d871a2a81dd5e4
# 📃 Purpose: نقطه شروع اجرای برنامه PyQt
# 📅 Created on: 2025-05-26
# 📌 Edited on: 2025-05-29 | Edit #1: اجرای خودکار vpn_info_collector و vpn_auto_router قبل از اجرای GUI
# 📌 Edited on: 2025-05-29 | Edit #2: اضافه کردن ذخیره لاگ ورود و خروج برنامه برای تحلیل بهینه‌سازی آینده
# 📌 Edited on: 2025-05-29 | Edit #3: اجرای هم‌زمان لاگ مانیتور هنگام اجرای GUI + اتصال هشدار گرافیکی

from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
import sys
import subprocess
import os
import threading
from utils.logger import log_info
from utils.log_monitor import bind_gui_alert, monitor_log_gui

def run_background_scripts():
    try:
        subprocess.run([sys.executable, os.path.join("utils", "vpn_info_collector.py")], check=True)
        subprocess.run([sys.executable, os.path.join("core", "vpn_auto_router.py")], check=True)
    except Exception as e:
        log_info(f"⚠️ خطا در اجرای اسکریپت‌های اولیه: {e}")

def start_log_monitor():
    def monitor():
        monitor_log_gui()
    threading.Thread(target=monitor, daemon=True).start()

if __name__ == '__main__':
    log_info("🟢 برنامه اجرا شد")
    run_background_scripts()
    app = QApplication(sys.argv)
    window = MainWindow()
    bind_gui_alert(window)  # اتصال هشدار لاگ مانیتور به GUI
    start_log_monitor()
    window.show()
    exit_code = app.exec_()
    log_info("🔴 برنامه بسته شد")
    sys.exit(exit_code)
