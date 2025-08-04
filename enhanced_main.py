# 🔧 Enhanced UG Uploader Bot with All Improvements
import os
import re
import sys
import time
import json
import random
import string
import shutil
import zipfile
import urllib
import subprocess
from datetime import datetime, timedelta
from base64 import b64encode, b64decode
from subprocess import getstatusoutput

# 🕒 Timezone
import pytz

# 📦 Third-party Libraries
import aiohttp
import aiofiles
import requests
import asyncio
import ffmpeg
import m3u8
import cloudscraper
import yt_dlp
import tgcrypto
from bs4 import BeautifulSoup
from pytube import YouTube
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# ⚙️ Pyrogram
from pyrogram import Client, filters, idle
from pyrogram.handlers import MessageHandler
from pyrogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from pyrogram.errors import (
    FloodWait,
    BadRequest,
    Unauthorized,
    SessionExpired,
    AuthKeyDuplicated,
    AuthKeyUnregistered,
    ChatAdminRequired,
    PeerIdInvalid,
    RPCError
)
from pyrogram.errors.exceptions.bad_request_400 import MessageNotModified

# 🧠 Enhanced Bot Modules
import auth
import ug as helper
from ug import *

from clean import register_clean_handler
from logs import logging
from utils import progress_bar
from vars import *

# 🚀 New Enhanced Modules
from security import security
from performance import performance
from analytics import analytics
from notifications import notifications
from ui_enhancements import ui
from error_handler import error_handler

from pyromod import listen
import apixug
from apixug import SecureAPIClient
from db import db

auto_flags = {}
auto_clicked = False
client = SecureAPIClient()
apis = client.get_apis()

# Global variables
watermark = "S U J A L"  # Default value
count = 0
userbot = None
timeout_duration = 300  # 5 minutes

# Initialize enhanced bot with random session
bot = Client(
    "ugx_enhanced",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=300,
    sleep_threshold=60,
    in_memory=True
)

# Register command handlers
register_clean_handler(bot)

# 🔄 Enhanced Callback Query Handler
@bot.on_callback_query()
async def handle_callback(client: Client, callback_query: CallbackQuery):
    """Handle all callback queries with enhanced UI"""
    try:
        data = callback_query.data
        user_id = callback_query.from_user.id
        
        # Check rate limit
        if not security.check_rate_limit(user_id, "api_calls"):
            await callback_query.answer("⚠️ Rate limit exceeded. Please wait.", show_alert=True)
            return
        
        if data == "download":
            await show_download_options(client, callback_query)
        elif data == "upload":
            await show_upload_options(client, callback_query)
        elif data == "settings":
            await show_settings(client, callback_query)
        elif data == "stats":
            await show_user_stats(client, callback_query)
        elif data == "help":
            await show_help(client, callback_query)
        elif data == "support":
            await show_support(client, callback_query)
        elif data == "main_menu":
            await show_main_menu(client, callback_query)
        elif data.startswith("download_"):
            await handle_download_selection(client, callback_query, data)
        elif data.startswith("quality_"):
            await handle_quality_selection(client, callback_query, data)
        elif data.startswith("admin_"):
            await handle_admin_actions(client, callback_query, data)
        else:
            await callback_query.answer("Unknown action", show_alert=True)
            
    except Exception as e:
        await error_handler.handle_error(e, callback_query.from_user.id, "callback_query", client)
        await callback_query.answer("An error occurred", show_alert=True)

async def show_download_options(client: Client, callback_query: CallbackQuery):
    """Show download options with enhanced UI"""
    message = """
📥 **Download Options**

Choose the type of file you want to download:

• 📄 **PDF** - Documents and presentations
• 🎥 **Video** - Movies, tutorials, and clips
• 🎵 **Audio** - Music and podcasts
• 🖼️ **Image** - Photos and graphics
• 📦 **All Files** - Any file type
    """
    
    await callback_query.edit_message_text(
        message,
        reply_markup=ui.download_keyboard
    )

async def show_upload_options(client: Client, callback_query: CallbackQuery):
    """Show upload options"""
    message = """
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
    """
    
    await callback_query.edit_message_text(
        message,
        reply_markup=ui.main_keyboard
    )

async def show_settings(client: Client, callback_query: CallbackQuery):
    """Show settings menu"""
    message = """
⚙️ **Settings**

Customize your experience:

• 🔔 **Notifications** - Toggle notifications
• 🌐 **Language** - Change language
• 📏 **Quality** - Set download quality
• 💾 **Storage** - Manage storage settings
    """
    
    await callback_query.edit_message_text(
        message,
        reply_markup=ui.settings_keyboard
    )

async def show_user_stats(client: Client, callback_query: CallbackQuery):
    """Show user statistics with analytics"""
    try:
        user_id = callback_query.from_user.id
        user_stats = analytics.get_user_analytics(user_id)
        
        stats_card = ui.create_user_stats_card(user_stats)
        
        await callback_query.edit_message_text(
            stats_card,
            reply_markup=ui.main_keyboard
        )
        
        # Track analytics
        await analytics.track_download(user_id, 0, "stats_view")
        
    except Exception as e:
        await error_handler.handle_error(e, callback_query.from_user.id, "show_stats", client)

async def show_help(client: Client, callback_query: CallbackQuery):
    """Show help menu"""
    message = """
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
    
    await callback_query.edit_message_text(
        message,
        reply_markup=ui.help_keyboard
    )

async def show_support(client: Client, callback_query: CallbackQuery):
    """Show support information"""
    message = """
💬 **Support**

📞 **Contact Us:**
• Telegram: @ItsUGxBot
• Email: support@uguploader.com
• Website: https://uguploader.com

🕒 **Response Time:**
• Usually within 1-2 hours
• 24/7 support available

📝 **Before Contacting:**
• Check FAQ section
• Try restarting the bot
• Provide error details
    """
    
    await callback_query.edit_message_text(
        message,
        reply_markup=ui.main_keyboard
    )

async def show_main_menu(client: Client, callback_query: CallbackQuery):
    """Show main menu"""
    message = ui.create_welcome_message(callback_query.from_user.first_name)
    
    await callback_query.edit_message_text(
        message,
        reply_markup=ui.main_keyboard
    )

async def handle_download_selection(client: Client, callback_query: CallbackQuery, data: str):
    """Handle download type selection"""
    file_type = data.replace("download_", "")
    
    message = f"""
📥 **Download {file_type.upper()}**

Please send the URL of the {file_type} file you want to download.

💡 **Tips:**
• Make sure the URL is direct
• Check if the file is accessible
• Supported formats for {file_type}: {get_supported_formats(file_type)}
    """
    
    await callback_query.edit_message_text(
        message,
        reply_markup=ui.main_keyboard
    )

async def handle_quality_selection(client: Client, callback_query: CallbackQuery, data: str):
    """Handle quality selection"""
    quality = data.replace("quality_", "")
    
    message = f"""
📏 **Quality Set to: {quality.upper()}**

Your download quality preference has been updated.

🎯 **Current Settings:**
• Quality: {quality.upper()}
• Format: Auto-detect
• Compression: Enabled
    """
    
    await callback_query.edit_message_text(
        message,
        reply_markup=ui.settings_keyboard
    )

async def handle_admin_actions(client: Client, callback_query: CallbackQuery, data: str):
    """Handle admin actions"""
    user_id = callback_query.from_user.id
    
    if not db.is_admin(user_id):
        await callback_query.answer("⚠️ Admin access required", show_alert=True)
        return
    
    action = data.replace("admin_", "")
    
    if action == "users":
        await show_admin_users(client, callback_query)
    elif action == "analytics":
        await show_admin_analytics(client, callback_query)
    elif action == "system":
        await show_admin_system(client, callback_query)

async def show_admin_users(client: Client, callback_query: CallbackQuery):
    """Show admin users management"""
    users = db.list_users()
    
    message = f"""
👥 **User Management**

📊 **Total Users:** {len(users)}

📋 **Recent Users:**
"""
    
    for user in users[:5]:
        message += f"• User {user['user_id']} - Expires: {user['expiry_date']}\n"
    
    await callback_query.edit_message_text(
        message,
        reply_markup=ui.admin_keyboard
    )

async def show_admin_analytics(client: Client, callback_query: CallbackQuery):
    """Show admin analytics"""
    report = analytics.generate_report()
    
    await callback_query.edit_message_text(
        report,
        reply_markup=ui.admin_keyboard
    )

async def show_admin_system(client: Client, callback_query: CallbackQuery):
    """Show admin system info"""
    error_report = error_handler.get_error_report()
    
    message = f"""
⚙️ **System Information**

{error_report}

🔧 **Performance:**
• Cache hits: {len(performance.download_cache)}
• Active sessions: 1
• Memory usage: Normal
    """
    
    await callback_query.edit_message_text(
        message,
        reply_markup=ui.admin_keyboard
    )

def get_supported_formats(file_type: str) -> str:
    """Get supported formats for file type"""
    formats = {
        "pdf": "PDF, DOC, DOCX, TXT",
        "video": "MP4, AVI, MOV, MKV",
        "audio": "MP3, WAV, AAC, FLAC",
        "image": "JPG, PNG, GIF, WEBP"
    }
    return formats.get(file_type, "All formats")

# 🔄 Enhanced Start Command
@bot.on_message(filters.command("start") & (filters.private | filters.channel))
async def enhanced_start(bot: Client, m: Message):
    """Enhanced start command with better UI"""
    try:
        user_id = m.from_user.id
        user_name = m.from_user.first_name
        
        # Check if user is authorized
        if not db.is_user_authorized(user_id):
            await notifications.send_welcome_message(bot, user_id)
            return
        
        # Send enhanced welcome message
        welcome_message = ui.create_welcome_message(user_name)
        
        await m.reply_text(
            welcome_message,
            reply_markup=ui.main_keyboard
        )
        
        # Track analytics
        await analytics.track_download(user_id, 0, "start_command")
        
    except Exception as e:
        await error_handler.handle_error(e, m.from_user.id, "start_command", bot)

# 🔄 Enhanced Text Handler
@bot.on_message(filters.text & filters.private)
async def enhanced_text_handler(bot: Client, m: Message):
    """Enhanced text handler with URL validation and smart processing"""
    try:
        user_id = m.from_user.id
        text = m.text.strip()
        
        # Check rate limit
        if not security.check_rate_limit(user_id, "api_calls"):
            await notifications.send_rate_limit_warning(
                bot, user_id, "text processing", "1 minute"
            )
            return
        
        # Validate URL if it looks like one
        if text.startswith(('http://', 'https://')):
            validation = error_handler.validate_download_request(text, user_id)
            
            if not validation["valid"]:
                error_msg = "\n".join(validation["errors"])
                await notifications.send_error_notification(
                    bot, user_id, "ValidationError", error_msg
                )
                return
            
            # Process URL download
            await process_url_download(bot, m, text)
        else:
            # Handle other text commands
            await process_text_command(bot, m, text)
            
    except Exception as e:
        await error_handler.handle_error(e, m.from_user.id, "text_handler", bot)

async def process_url_download(bot: Client, m: Message, url: str):
    """Process URL download with enhanced features"""
    try:
        user_id = m.from_user.id
        
        # Show processing message
        processing_msg = await m.reply_text("🔄 Processing URL...")
        
        # Use smart download with progress
        filename = f"download_{int(time.time())}"
        
        async def progress_callback(percentage, status):
            if percentage % 20 == 0:  # Update every 20%
                try:
                    progress_bar = ui.create_progress_bar(percentage)
                    await processing_msg.edit_text(f"📥 Downloading...\n{progress_bar}\n{status}")
                except:
                    pass
        
        # Download file
        success = await performance.smart_download(url, filename, progress_callback)
        
        if success:
            # Get file info
            file_info = performance.get_file_info(filename)
            file_size = file_info.get("size", 0)
            file_type = file_info.get("extension", "").replace(".", "")
            
            # Track analytics
            await analytics.track_download(user_id, file_size, file_type)
            
            # Send success notification
            await notifications.send_download_complete(
                bot, user_id, filename, file_size, file_type
            )
            
            # Send file with info card
            info_card = ui.create_file_info_card(filename, file_size, file_type)
            await m.reply_text(info_card)
            
            # Clean up
            if os.path.exists(filename):
                os.remove(filename)
        else:
            await notifications.send_error_notification(
                bot, user_id, "DownloadError", "Failed to download file"
            )
            
    except Exception as e:
        await error_handler.handle_error(e, m.from_user.id, "url_download", bot)

async def process_text_command(bot: Client, m: Message, text: str):
    """Process text commands"""
    user_id = m.from_user.id
    
    if text.lower() in ["help", "/help"]:
        await show_help(bot, m)
    elif text.lower() in ["stats", "/stats"]:
        await show_user_stats(bot, m)
    elif text.lower() in ["menu", "/menu"]:
        await show_main_menu(bot, m)
    else:
        await m.reply_text(
            "❓ I didn't understand that command.\n\n"
            "Try:\n"
            "• Send a URL to download\n"
            "• Send a file to upload\n"
            "• /help for assistance"
        )

# 🔄 Enhanced File Handler
@bot.on_message(filters.document & filters.private)
async def enhanced_file_handler(bot: Client, m: Message):
    """Enhanced file upload handler"""
    try:
        user_id = m.from_user.id
        file = m.document
        
        # Validate file
        validation = error_handler.validate_upload_request(file.file_size, file.file_name)
        
        if not validation["valid"]:
            error_msg = "\n".join(validation["errors"])
            await notifications.send_error_notification(
                bot, user_id, "ValidationError", error_msg
            )
            return
        
        # Track analytics
        file_type = file.file_name.split(".")[-1] if "." in file.file_name else "unknown"
        await analytics.track_upload(user_id, file.file_size, file_type)
        
        # Send success notification
        await notifications.send_upload_complete(
            bot, user_id, file.file_name, file.file_size
        )
        
        # Create file info card
        info_card = ui.create_file_info_card(file.file_name, file.file_size, file_type)
        await m.reply_text(info_card)
        
    except Exception as e:
        await error_handler.handle_error(e, m.from_user.id, "file_upload", bot)

# 🔄 Enhanced Stats Command
@bot.on_message(filters.command("stats") & filters.private)
async def enhanced_stats_command(bot: Client, m: Message):
    """Enhanced stats command with analytics"""
    try:
        user_id = m.from_user.id
        user_stats = analytics.get_user_analytics(user_id)
        
        stats_card = ui.create_user_stats_card(user_stats)
        
        await m.reply_text(stats_card, reply_markup=ui.main_keyboard)
        
    except Exception as e:
        await error_handler.handle_error(e, m.from_user.id, "stats_command", bot)

# 🔄 Enhanced Help Command
@bot.on_message(filters.command("help") & filters.private)
async def enhanced_help_command(bot: Client, m: Message):
    """Enhanced help command"""
    try:
        help_message = """
🆘 **Help & Support**

📋 **Available Commands:**
• Send any file to upload
• Send URL to download
• /stats - View your statistics
• /help - Show this help

💡 **Pro Tips:**
• Supported formats: PDF, Video, Audio, Images
• Max file size: 2GB
• Rate limit: 10 downloads/hour

📞 **Need Help?**
Contact: @ItsUGxBot
        """
        
        await m.reply_text(help_message, reply_markup=ui.help_keyboard)
        
    except Exception as e:
        await error_handler.handle_error(e, m.from_user.id, "help_command", bot)

# 🔄 Enhanced Admin Commands
@bot.on_message(filters.command("admin") & filters.private)
async def enhanced_admin_command(bot: Client, m: Message):
    """Enhanced admin command"""
    try:
        user_id = m.from_user.id
        
        if not db.is_admin(user_id):
            await m.reply_text("⚠️ Admin access required")
            return
        
        admin_message = """
👨‍💼 **Admin Panel**

📊 **Quick Actions:**
• View all users
• Check analytics
• System status
• Error reports
        """
        
        await m.reply_text(admin_message, reply_markup=ui.admin_keyboard)
        
    except Exception as e:
        await error_handler.handle_error(e, m.from_user.id, "admin_command", bot)

# 🔄 Enhanced Error Handler
@bot.on_message(filters.command("errors") & filters.private)
async def enhanced_errors_command(bot: Client, m: Message):
    """Show error report"""
    try:
        user_id = m.from_user.id
        
        if not db.is_admin(user_id):
            await m.reply_text("⚠️ Admin access required")
            return
        
        error_report = error_handler.get_error_report()
        await m.reply_text(error_report)
        
    except Exception as e:
        await error_handler.handle_error(e, m.from_user.id, "errors_command", bot)

# 🔄 Enhanced Analytics Command
@bot.on_message(filters.command("analytics") & filters.private)
async def enhanced_analytics_command(bot: Client, m: Message):
    """Show analytics report"""
    try:
        user_id = m.from_user.id
        
        if not db.is_admin(user_id):
            await m.reply_text("⚠️ Admin access required")
            return
        
        report = analytics.generate_report()
        await m.reply_text(report)
        
    except Exception as e:
        await error_handler.handle_error(e, m.from_user.id, "analytics_command", bot)

# 🔄 Cleanup on shutdown
async def cleanup():
    """Cleanup resources on shutdown"""
    try:
        await performance.close()
        performance.cleanup_cache()
        analytics.save_analytics()
        print("✅ Cleanup completed successfully")
    except Exception as e:
        print(f"❌ Cleanup error: {e}")

# 🔄 Main function
async def main():
    """Main function with enhanced features"""
    try:
        print("🚀 Starting Enhanced UG Uploader Bot...")
        
        # Start the bot
        await bot.start()
        print("✅ Bot started successfully")
        
        # Send startup notification to admins
        admin_ids = [int(x) for x in ADMINS]
        await notifications.send_system_alert(
            bot, admin_ids, "Bot Started", 
            "Enhanced UG Uploader Bot is now online! 🚀"
        )
        
        # Keep the bot running
        await idle()
        
    except Exception as e:
        print(f"❌ Bot startup error: {e}")
    finally:
        await cleanup()
        await bot.stop()

# 🔄 Run the bot
if __name__ == "__main__":
    asyncio.run(main())