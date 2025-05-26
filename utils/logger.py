# 📁 File: utils/logger.py
# 🔗 Project ID: VPNF-2025-001
# 🆔 File ID: 6834aa5b7ad8819194fc0713517f2d67
# 📃 Purpose: ثبت لاگ‌های سیستم و ارائه آن‌ها برای نمایش در GUI
# 📅 Created on: 2025-05-26

import logging
import os

# 🔖 مسیر لاگ فایل در دایرکتوری Temp سیستم
LOG_PATH = os.path.join(os.environ['TEMP'], 'vpn_failover.log')

# 🎯 پیکربندی لاگر با سطح INFO و فرمت زمان‌دار
logger = logging.getLogger("vpn_logger")
logger.setLevel(logging.INFO)

# فقط یک بار هندلر اضافه شود
if not logger.handlers:
    file_handler = logging.FileHandler(LOG_PATH, encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

# 🎯 تابع ثبت لاگ با سطح info
def log_info(message):
    logger.info(message)

# 🎯 تابع ثبت لاگ با سطح warning
def log_warning(message):
    logger.warning(message)

# 🎯 تابع ثبت لاگ با سطح error
def log_error(message):
    logger.error(message)

# 🎯 تابع خواندن لاگ (برای نمایش در GUI در آینده)
def read_log():
    try:
        with open(LOG_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "(لاگی یافت نشد)"
