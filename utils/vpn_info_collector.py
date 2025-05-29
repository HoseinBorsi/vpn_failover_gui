# 📁 File: utils/vpn_info_collector.py
# 🔗 Project ID: VPNF-2025-001
# 🆔 File ID: 68385b7f8dd88191a1fa7e3011cc9b90
# 📃 Purpose: جمع‌آوری و ذخیره اطلاعات شبکه برای تحلیل وضعیت اتصال VPN
# 📅 Created on: 2025-05-29
# 📌 Edited on: 2025-05-29 | Edit #1: افزودن اطلاعات بیشتر و ساختار دقیق‌تر برای ذخیره‌سازی و تحلیل متریک اتصال VPN
# 📌 Edited on: 2025-05-29 | Edit #2: رفع خطاهای احتمالی اجرای مستقیم (status 2) و کنترل استثناها

import psutil
import socket
import subprocess
import json
import os

OUTPUT_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'local_logs', 'vpn_connection_info.json')
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

def get_process_info():
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name']):
            if 'vpn' in proc.info['name'].lower():
                processes.append(proc.info)
        return processes
    except Exception as e:
        return [f"❌ خطا در process info: {e}"]

def get_connections():
    try:
        conns = []
        for conn in psutil.net_connections():
            if conn.status and conn.laddr:
                item = {
                    'pid': conn.pid,
                    'status': conn.status,
                    'local_ip': conn.laddr.ip,
                    'local_port': conn.laddr.port,
                    'remote_ip': conn.raddr.ip if conn.raddr else None,
                    'remote_port': conn.raddr.port if conn.raddr else None
                }
                conns.append(item)
        return conns
    except Exception as e:
        return [f"❌ خطا در connections: {e}"]

def get_default_gateway():
    try:
        result = subprocess.run("powershell Get-NetRoute | Where { $_.DestinationPrefix -eq '0.0.0.0/0' }", 
                                shell=True, text=True, capture_output=True)
        return result.stdout
    except Exception as e:
        return f"❌ خطا در gateway: {e}"

def get_ip_info():
    try:
        return {
            'hostname': socket.gethostname(),
            'local_ip': socket.gethostbyname(socket.gethostname())
        }
    except Exception as e:
        return {"error": f"❌ خطا در ip_info: {e}"}

def get_active_adapters():
    try:
        result = subprocess.run("powershell Get-NetAdapter | Where {$_.Status -eq 'Up'} | Format-Table -AutoSize", 
                                shell=True, text=True, capture_output=True)
        return result.stdout
    except Exception as e:
        return f"❌ خطا در adapters: {e}"

def get_proxy_settings():
    try:
        result = subprocess.run("netsh winhttp show proxy", shell=True, text=True, capture_output=True)
        return result.stdout
    except Exception as e:
        return f"❌ خطا در proxy: {e}"

def get_portproxy_settings():
    try:
        result = subprocess.run("netsh interface portproxy show all", shell=True, text=True, capture_output=True)
        return result.stdout
    except Exception as e:
        return f"❌ خطا در portproxy: {e}"

def get_dns_info():
    try:
        result = subprocess.run("ipconfig /all", shell=True, text=True, capture_output=True)
        return result.stdout
    except Exception as e:
        return f"❌ خطا در dns_info: {e}"

def get_latency(host='8.8.8.8'):
    try:
        result = subprocess.run(["ping", host, "-n", "3"], text=True, capture_output=True)
        return result.stdout
    except Exception as e:
        return f"❌ خطا در ping: {e}"

def collect_all_info():
    info = {
        'processes': get_process_info(),
        'connections': get_connections(),
        'default_gateway': get_default_gateway(),
        'ip_info': get_ip_info(),
        'active_adapters': get_active_adapters(),
        'proxy_settings': get_proxy_settings(),
        'port_proxy': get_portproxy_settings(),
        'dns_info': get_dns_info(),
        'latency_test': get_latency(),
    }
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(info, f, indent=2, ensure_ascii=False)
        print(f"✅ اطلاعات اتصال VPN ذخیره شد: {OUTPUT_FILE}")
    except Exception as e:
        print(f"❌ خطا در ذخیره‌سازی فایل: {e}")

if __name__ == '__main__':
    collect_all_info()
