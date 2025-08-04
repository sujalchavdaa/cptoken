from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from typing import List, Dict, Optional
import asyncio

class UIEnhancements:
    def __init__(self):
        self.setup_keyboards()
    
    def setup_keyboards(self):
        """Setup all keyboard layouts"""
        # Main menu keyboard
        self.main_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📥 Download", callback_data="download"),
                InlineKeyboardButton("📤 Upload", callback_data="upload")
            ],
            [
                InlineKeyboardButton("⚙️ Settings", callback_data="settings"),
                InlineKeyboardButton("📊 Stats", callback_data="stats")
            ],
            [
                InlineKeyboardButton("🆘 Help", callback_data="help"),
                InlineKeyboardButton("💬 Support", callback_data="support")
            ]
        ])
        
        # Download options keyboard
        self.download_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📄 PDF", callback_data="download_pdf"),
                InlineKeyboardButton("🎥 Video", callback_data="download_video")
            ],
            [
                InlineKeyboardButton("🎵 Audio", callback_data="download_audio"),
                InlineKeyboardButton("🖼️ Image", callback_data="download_image")
            ],
            [
                InlineKeyboardButton("📦 All Files", callback_data="download_all"),
                InlineKeyboardButton("🔙 Back", callback_data="main_menu")
            ]
        ])
        
        # Settings keyboard
        self.settings_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🔔 Notifications", callback_data="toggle_notifications"),
                InlineKeyboardButton("🌐 Language", callback_data="change_language")
            ],
            [
                InlineKeyboardButton("📏 Quality", callback_data="change_quality"),
                InlineKeyboardButton("💾 Storage", callback_data="storage_settings")
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data="main_menu")
            ]
        ])
        
        # Quality selection keyboard
        self.quality_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🎯 High (1080p)", callback_data="quality_high"),
                InlineKeyboardButton("📱 Medium (720p)", callback_data="quality_medium")
            ],
            [
                InlineKeyboardButton("⚡ Low (480p)", callback_data="quality_low"),
                InlineKeyboardButton("🔙 Back", callback_data="settings")
            ]
        ])
        
        # Help keyboard
        self.help_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📋 Commands", callback_data="help_commands"),
                InlineKeyboardButton("❓ FAQ", callback_data="help_faq")
            ],
            [
                InlineKeyboardButton("📞 Contact", callback_data="contact_support"),
                InlineKeyboardButton("🔙 Back", callback_data="main_menu")
            ]
        ])
        
        # Admin keyboard
        self.admin_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("👥 Users", callback_data="admin_users"),
                InlineKeyboardButton("📊 Analytics", callback_data="admin_analytics")
            ],
            [
                InlineKeyboardButton("⚙️ System", callback_data="admin_system"),
                InlineKeyboardButton("🔙 Back", callback_data="main_menu")
            ]
        ])
    
    def create_progress_bar(self, percentage: float, width: int = 20) -> str:
        """Create a visual progress bar"""
        filled = int(width * percentage / 100)
        empty = width - filled
        
        bar = "█" * filled + "░" * empty
        return f"[{bar}] {percentage:.1f}%"
    
    def create_file_info_card(self, filename: str, size: int, file_type: str) -> str:
        """Create a beautiful file info card"""
        # Format size
        if size > 1024 * 1024 * 1024:
            size_str = f"{size / (1024 * 1024 * 1024):.2f} GB"
        elif size > 1024 * 1024:
            size_str = f"{size / (1024 * 1024):.2f} MB"
        else:
            size_str = f"{size / 1024:.2f} KB"
        
        # Get file icon
        file_icons = {
            "pdf": "📄", "doc": "📄", "docx": "📄",
            "mp4": "🎥", "avi": "🎥", "mov": "🎥",
            "mp3": "🎵", "wav": "🎵", "aac": "🎵",
            "jpg": "🖼️", "jpeg": "🖼️", "png": "🖼️", "gif": "🖼️"
        }
        
        icon = file_icons.get(file_type.lower(), "📁")
        
        return f"""
{icon} **File Information**

📁 **Name:** `{filename}`
📏 **Size:** {size_str}
🎯 **Type:** {file_type.upper()}
        """
    
    def create_user_stats_card(self, user_stats: Dict) -> str:
        """Create a beautiful user statistics card"""
        return f"""
📊 **Your Statistics**

📥 **Downloads:** {user_stats.get('total_downloads', 0)}
📤 **Uploads:** {user_stats.get('total_uploads', 0)}
🎯 **Favorite Format:** {user_stats.get('favorite_format', 'None')}
💾 **Total Size:** {user_stats.get('total_size_mb', 0)} MB
⏰ **Last Activity:** {user_stats.get('last_activity', 'Never')}
        """
    
    def create_welcome_message(self, user_name: str) -> str:
        """Create a personalized welcome message"""
        return f"""
🎉 **Welcome, {user_name}!**

🚀 **UG Uploader** is your ultimate file management solution.

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
        """
    
    def create_error_message(self, error_type: str, error_msg: str) -> str:
        """Create a user-friendly error message"""
        error_icons = {
            "ConnectionError": "🌐",
            "TimeoutError": "⏰",
            "FileNotFoundError": "📁",
            "PermissionError": "🔒",
            "ValueError": "⚠️",
            "default": "❌"
        }
        
        icon = error_icons.get(error_type, error_icons["default"])
        
        return f"""
{icon} **Error Occurred**

🔍 **Type:** {error_type}
📝 **Details:** {error_msg}

💡 **What to do:**
• Check your internet connection
• Verify the file/URL is correct
• Try again in a few minutes
• Contact support if problem persists

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
    
    def create_success_message(self, action: str, filename: str, size: str) -> str:
        """Create a success message"""
        action_icons = {
            "download": "📥",
            "upload": "📤",
            "process": "⚙️",
            "convert": "🔄"
        }
        
        icon = action_icons.get(action, "✅")
        
        return f"""
{icon} **{action.title()} Successful!**

📁 **File:** `{filename}`
📏 **Size:** {size}
⏰ **Time:** {self.get_current_time()}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
    
    def get_current_time(self) -> str:
        """Get current time in readable format"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
    
    def create_quick_actions_keyboard(self, file_type: str) -> InlineKeyboardMarkup:
        """Create context-aware quick actions keyboard"""
        if file_type in ["pdf", "doc", "docx"]:
            return InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("📄 View", callback_data=f"view_{file_type}"),
                    InlineKeyboardButton("📥 Download", callback_data=f"download_{file_type}")
                ],
                [
                    InlineKeyboardButton("🔄 Convert", callback_data=f"convert_{file_type}"),
                    InlineKeyboardButton("📤 Share", callback_data=f"share_{file_type}")
                ]
            ])
        elif file_type in ["mp4", "avi", "mov"]:
            return InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🎥 Play", callback_data=f"play_{file_type}"),
                    InlineKeyboardButton("📥 Download", callback_data=f"download_{file_type}")
                ],
                [
                    InlineKeyboardButton("🎬 Compress", callback_data=f"compress_{file_type}"),
                    InlineKeyboardButton("📤 Share", callback_data=f"share_{file_type}")
                ]
            ])
        else:
            return InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("📥 Download", callback_data=f"download_{file_type}"),
                    InlineKeyboardButton("📤 Share", callback_data=f"share_{file_type}")
                ]
            ])

# Global UI instance
ui = UIEnhancements()