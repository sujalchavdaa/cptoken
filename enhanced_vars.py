import os
from os import environ

# 🔐 API Configuration
API_ID = int(os.environ.get("API_ID", ""))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# 👤 User Configuration
CREDIT = os.environ.get("CREDIT", "𓍯𝙎𝙪𝙟𝙖𝙡⚝")

# 🗄️ MongoDB Configuration
DATABASE_NAME = os.environ.get("DATABASE_NAME", "UGxPRO")
DATABASE_URL = os.environ.get("DATABASE_URL", "")
MONGO_URL = DATABASE_URL  # For auth system

# 👨‍💼 Owner and Admin Configuration
OWNER_ID = int(os.environ.get("OWNER_ID", "7114926879"))
ADMINS = [int(x) for x in os.environ.get("ADMINS", "7114926879").split()]  # Default to owner ID

# 📢 Channel Configuration
PREMIUM_CHANNEL = "https://t.me/+W-Q51EuLf2QwYTl"

# 🖼️ Thumbnail Configuration
THUMBNAILS = list(map(str, os.environ.get("THUMBNAILS", "https://i.fbcd.co/products/original/ug-logo-designs-2-acbfbf7b80e16df4c902a34d1caf148e7e1feca736e21075114990e62294f3ac.jpg").split()))

# 🌐 Web Server Configuration
WEB_SERVER = os.environ.get("WEB_SERVER", "False").lower() == "true"
WEBHOOK = True  # Don't change this
PORT = int(os.environ.get("PORT", 8000))

# 🚀 Enhanced Features Configuration
ENHANCED_FEATURES = {
    # 🔐 Security Settings
    "rate_limiting": {
        "downloads_per_hour": 10,
        "uploads_per_hour": 5,
        "api_calls_per_minute": 30
    },
    
    # ⚡ Performance Settings
    "download": {
        "chunk_size": 8192,
        "max_concurrent": 3,
        "timeout": 300,
        "cache_duration": 3600  # 1 hour
    },
    
    # 📊 Analytics Settings
    "analytics": {
        "track_user_activity": True,
        "track_file_types": True,
        "track_errors": True,
        "save_interval": 300  # 5 minutes
    },
    
    # 🔔 Notification Settings
    "notifications": {
        "download_complete": True,
        "upload_complete": True,
        "error_notifications": True,
        "rate_limit_warnings": True,
        "subscription_reminders": True
    },
    
    # 🎨 UI Settings
    "ui": {
        "show_progress_bars": True,
        "show_file_info_cards": True,
        "show_user_stats": True,
        "enable_quick_actions": True
    },
    
    # 🛠️ Error Handling Settings
    "error_handling": {
        "log_errors": True,
        "retry_failed_operations": True,
        "max_retries": 3,
        "retry_delay": 5
    },
    
    # 📁 File Processing Settings
    "file_processing": {
        "max_file_size": 2 * 1024 * 1024 * 1024,  # 2GB
        "allowed_formats": [
            "pdf", "doc", "docx", "txt",
            "mp4", "avi", "mov", "mkv",
            "mp3", "wav", "aac", "flac",
            "jpg", "jpeg", "png", "gif", "webp"
        ],
        "auto_compress": True,
        "compression_quality": 85
    },
    
    # 🔍 Validation Settings
    "validation": {
        "validate_urls": True,
        "validate_file_types": True,
        "validate_file_sizes": True,
        "check_suspicious_patterns": True
    }
}

# 📱 Mobile Optimization Settings
MOBILE_OPTIMIZATIONS = {
    "max_file_size": 50 * 1024 * 1024,  # 50MB for mobile
    "auto_compress": True,
    "quick_upload": True,
    "touch_friendly_buttons": True,
    "simplified_ui": True
}

# 🎯 Quality Settings
QUALITY_SETTINGS = {
    "video": {
        "high": "1080p",
        "medium": "720p", 
        "low": "480p"
    },
    "audio": {
        "high": "320kbps",
        "medium": "192kbps",
        "low": "128kbps"
    },
    "image": {
        "high": "100%",
        "medium": "85%",
        "low": "70%"
    }
}

# 🔄 Message Templates
AUTH_MESSAGES = {
    "subscription_active": """<b>🎉 Subscription Activated!</b>

<blockquote>Your subscription has been activated and will expire on {expiry_date}.
You can now use the bot!</blockquote>\n\n Type /start to start uploading """,

    "subscription_expired": """<b>⚠️ Your Subscription Has Ended</b>

<blockquote>Your access to the bot has been revoked as your subscription period has expired.
Please contact the admin to renew your subscription.</blockquote>""",

    "user_added": """<b>✅ User Added Successfully!</b>

<blockquote>👤 Name: {name}
🆔 User ID: {user_id}
📅 Expiry: {expiry_date}</blockquote>""",

    "user_removed": """<b>✅ User Removed Successfully!</b>

<blockquote>User ID {user_id} has been removed from authorized users.</blockquote>""",

    "access_denied": """<b>⚠️ Access Denied!</b>

<blockquote>You are not authorized to use this bot.
Please contact the admin @ItsUGBot to get access.</blockquote>""",

    "not_admin": "⚠️ You are not authorized to use this command!",
    
    "invalid_format": """❌ <b>Invalid Format!</b>

<blockquote>Use format: {format}</blockquote>"""
}

# 🎨 UI Messages
UI_MESSAGES = {
    "welcome": """
🎉 **Welcome to UG Uploader!**

🚀 **Your ultimate file management solution.**

📋 **Quick Start:**
• Send any file to upload
• Send URL to download
• Use /stats to view your activity
• Use /help for assistance

💡 **Pro Tips:**
• Supported: PDF, Video, Audio, Images
• Max size: 2GB per file
• Rate limit: 10 downloads/hour

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """,
    
    "download_options": """
📥 **Download Options**

Choose the type of file you want to download:

• 📄 **PDF** - Documents and presentations
• 🎥 **Video** - Movies, tutorials, and clips
• 🎵 **Audio** - Music and podcasts
• 🖼️ **Image** - Photos and graphics
• 📦 **All Files** - Any file type
    """,
    
    "upload_options": """
📤 **Upload Options**

Send any file to upload it to our servers:

• 📄 **Documents** - PDF, DOC, TXT
• 🎥 **Videos** - MP4, AVI, MOV
• 🎵 **Audio** - MP3, WAV, AAC
• 🖼️ **Images** - JPG, PNG, GIF

💡 **Tips:**
• Max file size: 2GB
• Supported formats listed above
• Files are processed automatically
    """,
    
    "help": """
🆘 **Help & Support**

📋 **Commands:**
• Send any file to upload
• Send URL to download
• /stats - View your statistics
• /help - Show this help

❓ **FAQ:**
• How to upload files?
• How to download from URLs?
• What file types are supported?
• How to contact support?

💡 **Need more help?**
Contact our support team!
    """
}

# 🔧 System Settings
SYSTEM_SETTINGS = {
    "debug_mode": os.environ.get("DEBUG_MODE", "False").lower() == "true",
    "log_level": os.environ.get("LOG_LEVEL", "INFO"),
    "auto_cleanup": True,
    "cleanup_interval": 3600,  # 1 hour
    "max_log_size": 10 * 1024 * 1024,  # 10MB
    "backup_enabled": True,
    "backup_interval": 86400  # 24 hours
}

# 🎯 Feature Flags
FEATURE_FLAGS = {
    "enhanced_ui": True,
    "analytics_tracking": True,
    "smart_downloads": True,
    "error_handling": True,
    "rate_limiting": True,
    "notifications": True,
    "mobile_optimization": True,
    "admin_panel": True,
    "file_validation": True,
    "progress_tracking": True
}

# 📊 Analytics Configuration
ANALYTICS_CONFIG = {
    "track_user_behavior": True,
    "track_file_types": True,
    "track_download_sources": True,
    "track_error_patterns": True,
    "generate_reports": True,
    "save_to_database": True,
    "export_format": "json"
}

# 🔐 Security Configuration
SECURITY_CONFIG = {
    "validate_urls": True,
    "sanitize_filenames": True,
    "check_file_types": True,
    "rate_limiting": True,
    "input_validation": True,
    "error_logging": True,
    "suspicious_pattern_detection": True
}

# ⚡ Performance Configuration
PERFORMANCE_CONFIG = {
    "enable_caching": True,
    "cache_duration": 3600,
    "parallel_downloads": True,
    "max_concurrent": 3,
    "chunk_size": 8192,
    "timeout": 300,
    "retry_failed": True,
    "compression": True
}