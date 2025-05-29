# 📁 File: core/vpn_auto_router.py
# 🔗 Project ID: VPNF-2025-001
# 🆔 File ID: 68385d9e1bc481919b88a46908407d9c
# 📃 Purpose: تحلیل اطلاعات ذخیره‌شده برای تنظیم خودکار اولویت اتصال VPN (Nord, WARP, Internet)
# 📅 Created on: 2025-05-29

import json
import os
import subprocess

# 🔖 مسیر فایل JSON خروجی از vpn_info_collector
INFO_FILE = os.path.join(os.environ['TEMP'], 'vpn_connection_info.json')

# 📌 اولویت پیش‌فرض: Nord > WARP > Direct
PRIORITY_ORDER = {
    'nord': 10,
    'warp': 20,
    'default': 30
}

# 📛 آداپتورهایی که باید شناخته شوند (بر اساس فایل‌های دیگر پروژه)
IFACES = {
    'nord': 'NordLynx',
    'warp': 'CloudflareWARP',
    'default': 'Wi-Fi'
}

def detect_active_vpn(info):
    conns = info.get("connections", [])
    for conn in conns:
        if conn['status'] == 'ESTABLISHED':
            if 'nord' in str(conn['pid']).lower():
                return 'nord'
            if 'warp' in str(conn['pid']).lower():
                return 'warp'
    return 'default'

def set_interface_metric(alias, metric):
    try:
        subprocess.run([
            "powershell",
            f"Set-NetIPInterface -InterfaceAlias '{alias}' -InterfaceMetric {metric}"
        ], check=True)
        print(f"✅ تنظیم متریک برای {alias} با اولویت {metric}")
    except subprocess.CalledProcessError:
        print(f"❌ خطا در تنظیم متریک برای {alias}")

def apply_routing():
    if not os.path.exists(INFO_FILE):
        print("⚠️ فایل اطلاعات پیدا نشد. لطفاً ابتدا vpn_info_collector را اجرا کنید.")
        return

    with open(INFO_FILE, 'r', encoding='utf-8') as f:
        info = json.load(f)

    selected = detect_active_vpn(info)
    print(f"🔍 VPN فعال شناسایی‌شده: {selected}")

    for key, iface in IFACES.items():
        metric = PRIORITY_ORDER[key]
        set_interface_metric(iface, metric if key != selected else 5)

    print("✅ تنظیم مسیرها و اولویت‌ها با موفقیت انجام شد.")

if __name__ == '__main__':
    apply_routing()
