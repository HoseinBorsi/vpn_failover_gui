# 📁 File: core/vpn_manager.py
# 🔗 Project ID: VPNF-2025-001
# 🆔 File ID: 6834a7ece6a08191bc2ba9c94266a160
# 📃 Purpose: بررسی اتصال VPNها (Nord و WARP) و تنظیم متریک آداپتورها
# 📅 Created on: 2025-05-26

import subprocess
import platform

# آداپتورهای پیش‌فرض
IFACE_NORD = "NordLynx"
IFACE_WARP = "CloudflareWARP"
IFACE_MAIN = "Wi-Fi"

# بررسی اتصال NordVPN
def is_nord_connected():
    try:
        output = subprocess.check_output(["nordvpn", "status"], stderr=subprocess.STDOUT, text=True)
        return "Connected" in output
    except:
        return False

# بررسی اتصال WARP
def is_warp_connected():
    try:
        output = subprocess.check_output(["warp-cli", "status"], stderr=subprocess.STDOUT, text=True)
        return "Connected" in output
    except:
        return False

# وضعیت کلی VPN
def get_vpn_status():
    if is_nord_connected():
        return "nord"
    elif is_warp_connected():
        return "warp"
    else:
        return "none"

# بازنشانی متریک آداپتورها
def reset_metrics():
    if platform.system() == "Windows":
        try:
            subprocess.run(["powershell", f"Set-NetIPInterface -InterfaceAlias '{IFACE_MAIN}' -InterfaceMetric 10"], check=True)
            subprocess.run(["powershell", f"Set-NetIPInterface -InterfaceAlias '{IFACE_WARP}' -InterfaceMetric 20"], check=True)
            subprocess.run(["powershell", f"Set-NetIPInterface -InterfaceAlias '{IFACE_NORD}' -InterfaceMetric 30"], check=True)
        except subprocess.CalledProcessError:
            print("خطا در بازنشانی متریک‌ها")
