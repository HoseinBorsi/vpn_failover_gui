# 📁 File: README.md  
# 🔗 Project ID: VPNF-2025-001  
# 🆔 File ID: 6834ae6d519c8191aaf6124887da0d85  
# 📃 Purpose: معرفی پروژه VPNFailoverManager و توضیح اجرای آن برای GitHub  
# 📅 Created on: 2025-05-26

# VPNFailoverManager

**یک برنامه گرافیکی هوشمند برای مدیریت اولویت اتصال به VPN در ویندوز.**

این پروژه به شما اجازه می‌دهد اولویت اتصال را بین NordVPN، Cloudflare WARP و اینترنت عادی مدیریت کنید. همچنین وضعیت اتصال را با رابط گرافیکی نشان می‌دهد و لاگ سیستم را در تب جداگانه ثبت و نمایش می‌دهد.

---

## 🚀 امکانات اصلی
- شناسایی خودکار اتصال به NordVPN و WARP
- تنظیم متریک آداپتورها با PowerShell برای مدیریت اولویت اتصال
- رابط گرافیکی ساده با PyQt5
- نمایش لحظه‌ای وضعیت اتصال
- نمایش لاگ سیستم
- دکمه بازنشانی متریک‌ها

---

## 🧱 ساختار پروژه
```
vpn_failover_gui/
├── main.py                   # نقطه شروع برنامه
├── core/
│   ├── vpn_manager.py        # بررسی اتصال و تنظیم متریک‌ها
│   └── metrics_backup.py     # ذخیره و بازیابی متریک‌ها
├── ui/
│   └── main_window.py        # رابط گرافیکی برنامه
├── utils/
│   └── logger.py             # مدیریت لاگ
├── requirements.txt          # وابستگی‌ها
├── README.md
└── project_info/
    ├── filemap.json
    └── project.meta.json
```

---

## ⚙️ نحوه اجرا
```bash
pip install -r requirements.txt
python main.py
```

📌 فقط روی سیستم‌عامل ویندوز کار می‌کند.

---

## 🧩 وابستگی‌ها
- Python 3.8+
- PyQt5
- NordVPN CLI
- Cloudflare WARP CLI

---

## 📄 مجوز
MIT License
