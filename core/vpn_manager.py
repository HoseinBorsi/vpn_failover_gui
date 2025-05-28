# 📁 File: core/vpn_manager.py
# 🔗 Project ID: VPNF-2025-001
# 🆔 File ID: 6834a7ece6a08191bc2ba9c94266a160
# 📃 Purpose: بررسی اتصال VPNها (Nord و WARP) و تنظیم متریک آداپتورها
# 📅 Created on: 2025-05-26
# 📌 Edited on: 2025-05-27T23:20Z | Edit #3: افزودن تابع check_active_route برای شناسایی مسیر فعال اینترنتی سیستم

import subprocess
import platform
from utils.logger import log_info, log_warning, log_error

# آداپتورهای پیش‌فرض
IFACE_NORD = "NordLynx"
IFACE_WARP = "Cloudflare WARP"
IFACE_MAIN = "Wi-Fi"

# بررسی اتصال NordVPN
def is_nord_connected():
    try:
        output = subprocess.check_output(["nordvpn", "status"], stderr=subprocess.STDOUT, text=True)
        if "Connected" in output:
            log_info("✅ NordVPN وصل است.")
            return True
        else:
            log_warning("⚠️ NordVPN نصب است ولی وصل نیست.")
            return False
    except Exception as e:
        log_warning(f"❌ خطا در بررسی NordVPN: {e}")
        return False

# بررسی اتصال WARP
def is_warp_connected():
    try:
        output = subprocess.check_output(["warp-cli", "status"], stderr=subprocess.STDOUT, text=True)
        if "Connected" in output:
            log_info("✅ WARP وصل است.")
            return True
        else:
            log_warning("⚠️ WARP نصب است ولی وصل نیست.")
            return False
    except Exception as e:
        log_warning(f"❌ خطا در بررسی WARP: {e}")
        return False

# وضعیت کلی VPN
def get_vpn_status():
    if is_nord_connected():
        return "nord"
    elif is_warp_connected():
        return "warp"
    else:
        log_warning("❌ هیچ VPN فعالی یافت نشد. اینترنت خام در حال استفاده است.")
        return "none"

# بازنشانی متریک آداپتورها (اجباری)
def reset_metrics():
    if platform.system() == "Windows":
        try:
            subprocess.run(["powershell", f"Set-NetIPInterface -InterfaceAlias '{IFACE_MAIN}' -InterfaceMetric 10"], check=True)
            subprocess.run(["powershell", f"Set-NetIPInterface -InterfaceAlias '{IFACE_WARP}' -InterfaceMetric 20"], check=True)
            subprocess.run(["powershell", f"Set-NetIPInterface -InterfaceAlias '{IFACE_NORD}' -InterfaceMetric 30"], check=True)
            log_info("✅ متریک‌های آداپتورها با موفقیت ریست شدند.")
        except subprocess.CalledProcessError as e:
            log_error(f"❌ خطا در بازنشانی متریک‌ها: {e}")

# 🔄 اعمال راهبرد failover بر اساس اتصال واقعی
_previous_status = None

def apply_failover_strategy():
    global _previous_status
    status = get_vpn_status()

    if status == _previous_status:
        log_info(f"⏳ وضعیت اتصال تغییر نکرد: {status}")
        return

    try:
        if status == "nord":
            subprocess.run(["powershell", f"Set-NetIPInterface -InterfaceAlias '{IFACE_NORD}' -InterfaceMetric 10"], check=True)
            subprocess.run(["powershell", f"Set-NetIPInterface -InterfaceAlias '{IFACE_WARP}' -InterfaceMetric 20"], check=True)
            subprocess.run(["powershell", f"Set-NetIPInterface -InterfaceAlias '{IFACE_MAIN}' -InterfaceMetric 30"], check=True)
            log_info("🔁 سوییچ به NordVPN انجام شد.")

        elif status == "warp":
            subprocess.run(["powershell", f"Set-NetIPInterface -InterfaceAlias '{IFACE_WARP}' -InterfaceMetric 10"], check=True)
            subprocess.run(["powershell", f"Set-NetIPInterface -InterfaceAlias '{IFACE_NORD}' -InterfaceMetric 20"], check=True)
            subprocess.run(["powershell", f"Set-NetIPInterface -InterfaceAlias '{IFACE_MAIN}' -InterfaceMetric 30"], check=True)
            log_info("🔁 سوییچ به WARP انجام شد.")

        else:
            subprocess.run(["powershell", f"Set-NetIPInterface -InterfaceAlias '{IFACE_MAIN}' -InterfaceMetric 10"], check=True)
            subprocess.run(["powershell", f"Set-NetIPInterface -InterfaceAlias '{IFACE_NORD}' -InterfaceMetric 20"], check=True)
            subprocess.run(["powershell", f"Set-NetIPInterface -InterfaceAlias '{IFACE_WARP}' -InterfaceMetric 30"], check=True)
            log_info("⚠️ هیچ VPN فعال نبود؛ استفاده از اینترنت معمولی")

        _previous_status = status

    except subprocess.CalledProcessError as e:
        log_error(f"❌ خطا در اجرای راهبرد failover: {e}")

# 🔍 بررسی مسیر فعال بر اساس کم‌ترین متریک واقعی در حال استفاده

def check_active_route():
    try:
        output = subprocess.check_output([
            "powershell",
            "Get-NetRoute -DestinationPrefix '0.0.0.0/0' | Sort-Object RouteMetric | Select-Object -First 1 -ExpandProperty InterfaceAlias"
        ], text=True).strip()
        return output if output else "(مشخص نشد)"
    except Exception as e:
        log_error(f"❌ خطا در بررسی مسیر فعال: {e}")
        return "(خطا در دریافت مسیر)"
