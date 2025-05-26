# 📁 File: main.py
# 🔗 Project ID: VPNF-2025-001
# 🆔 File ID: 6834a54280ec819195d871a2a81dd5e4
# 📃 Purpose: نقطه شروع اجرای برنامه PyQt
# 📅 Created on: 2025-05-26

from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
