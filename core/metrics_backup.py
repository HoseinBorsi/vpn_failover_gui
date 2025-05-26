# 📁 File: core/metrics_backup.py
# 🔗 Project ID: VPNF-2025-001
# 🆔 File ID: 6834a9bf8dd88191abe31fe7f7cc66f6
# 📃 Purpose: ذخیره‌سازی و بازیابی متریک آداپتورهای شبکه از فایل پشتیبان
# 📅 Created on: 2025-05-26

import json
import os
import subprocess
import platform

# 🔖 مسیر فایل پشتیبان در Temp ویندوز
BACKUP_FILE = os.path.join(os.environ['TEMP'], 'vpn_metrics_backup.json')

# 🎯 تابع ذخیره‌سازی متریک‌های فعلی
# این تابع از PowerShell برای گرفتن متریک‌های آداپتورها استفاده می‌کند
def save_current_metrics(interfaces):
    backup = {}
    for iface in interfaces:
        try:
            output = subprocess.check_output([
                "powershell",
                f"(Get-NetIPInterface -InterfaceAlias '{iface}' -AddressFamily IPv4).InterfaceMetric"
            ], text=True)
            backup[iface] = int(output.strip())
        except subprocess.CalledProcessError:
            print(f"❌ خطا در دریافت متریک برای: {iface}")
    try:
        with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
            json.dump(backup, f, indent=2)
    except Exception as e:
        print(f"❌ خطا در ذخیره فایل پشتیبان: {e}")

# 🎯 تابع بازیابی متریک‌ها از فایل
# متریک ذخیره‌شده برای هر آداپتور دوباره اعمال می‌شود
def restore_metrics():
    if not os.path.exists(BACKUP_FILE):
        print("⚠️ فایل پشتیبان وجود ندارد.")
        return

    try:
        with open(BACKUP_FILE, 'r', encoding='utf-8') as f:
            backup = json.load(f)

        for iface, metric in backup.items():
            subprocess.run([
                "powershell",
                f"Set-NetIPInterface -InterfaceAlias '{iface}' -InterfaceMetric {metric}"
            ], check=True)

        print("✅ متریک‌ها بازیابی شدند.")
    except Exception as e:
        print(f"❌ خطا در بازیابی متریک‌ها: {e}")
