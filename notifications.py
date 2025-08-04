import asyncio
from datetime import datetime
from typing import Optional, Dict, List
from pyrogram import Client
from pyrogram.types import Message

class NotificationService:
    def __init__(self):
        self.notification_templates = {
            "download_complete": {
                "title": "✅ Download Complete!",
                "message": """
📁 **File:** `{filename}`
📏 **Size:** {size}
⏰ **Time:** {time}
🎯 **Format:** {format}
                """
            },
            "upload_complete": {
                "title": "✅ Upload Complete!",
                "message": """
📤 **File Uploaded Successfully!**
📁 **File:** `{filename}`
📏 **Size:** {size}
⏰ **Time:** {time}
                """
            },
            "error_notification": {
                "title": "❌ Error Occurred",
                "message": """
⚠️ **Error Type:** {error_type}
🔍 **Description:** {description}
💡 **Solution:** {solution}
                """
            },
            "rate_limit_warning": {
                "title": "⚠️ Rate Limit Warning",
                "message": """
🚫 **Rate Limit Exceeded**
⏳ **Action:** {action}
⏰ **Reset Time:** {reset_time}
💡 **Tip:** Please wait before trying again
                """
            },
            "subscription_expiring": {
                "title": "⚠️ Subscription Expiring Soon",
                "message": """
⏰ **Subscription Expires:** {expiry_date}
📅 **Days Remaining:** {days_left}
💳 **Renew:** Contact admin to extend subscription
                """
            },
            "welcome_message": {
                "title": "🎉 Welcome to UG Uploader!",
                "message": """
🚀 **Welcome aboard!**

📋 **Available Commands:**
• Send any file to upload
• Send URL to download
• /stats - View your statistics
• /help - Get help

💡 **Tips:**
• Supported formats: PDF, Video, Audio, Images
• Max file size: 2GB
• Rate limit: 10 downloads/hour
                """
            }
        }
        
        self.error_solutions = {
            "ConnectionError": "Check your internet connection and try again",
            "TimeoutError": "Request timed out. Please try again",
            "FileNotFoundError": "File not found. Please check the URL",
            "PermissionError": "Permission denied. Contact admin",
            "ValueError": "Invalid input. Please check your request",
            "KeyError": "Missing required data. Please try again",
            "default": "An unexpected error occurred. Please try again"
        }
    
    async def send_download_complete(self, client: Client, user_id: int, 
                                   filename: str, file_size: int, file_type: str):
        """Send download completion notification"""
        template = self.notification_templates["download_complete"]
        
        # Format file size
        if file_size > 1024 * 1024:
            size_str = f"{file_size / (1024 * 1024):.2f} MB"
        else:
            size_str = f"{file_size / 1024:.2f} KB"
        
        message = template["message"].format(
            filename=filename,
            size=size_str,
            time=datetime.now().strftime("%H:%M:%S"),
            format=file_type
        )
        
        await self.send_rich_message(client, user_id, template["title"], message)
    
    async def send_upload_complete(self, client: Client, user_id: int, 
                                 filename: str, file_size: int):
        """Send upload completion notification"""
        template = self.notification_templates["upload_complete"]
        
        # Format file size
        if file_size > 1024 * 1024:
            size_str = f"{file_size / (1024 * 1024):.2f} MB"
        else:
            size_str = f"{file_size / 1024:.2f} KB"
        
        message = template["message"].format(
            filename=filename,
            size=size_str,
            time=datetime.now().strftime("%H:%M:%S")
        )
        
        await self.send_rich_message(client, user_id, template["title"], message)
    
    async def send_error_notification(self, client: Client, user_id: int, 
                                    error_type: str, error_description: str):
        """Send error notification with solution"""
        template = self.notification_templates["error_notification"]
        
        solution = self.error_solutions.get(error_type, self.error_solutions["default"])
        
        message = template["message"].format(
            error_type=error_type,
            description=error_description,
            solution=solution
        )
        
        await self.send_rich_message(client, user_id, template["title"], message)
    
    async def send_rate_limit_warning(self, client: Client, user_id: int, 
                                    action: str, reset_time: str):
        """Send rate limit warning"""
        template = self.notification_templates["rate_limit_warning"]
        
        message = template["message"].format(
            action=action,
            reset_time=reset_time
        )
        
        await self.send_rich_message(client, user_id, template["title"], message)
    
    async def send_subscription_expiring(self, client: Client, user_id: int, 
                                       expiry_date: str, days_left: int):
        """Send subscription expiring warning"""
        template = self.notification_templates["subscription_expiring"]
        
        message = template["message"].format(
            expiry_date=expiry_date,
            days_left=days_left
        )
        
        await self.send_rich_message(client, user_id, template["title"], message)
    
    async def send_welcome_message(self, client: Client, user_id: int):
        """Send welcome message to new users"""
        template = self.notification_templates["welcome_message"]
        
        await self.send_rich_message(client, user_id, template["title"], template["message"])
    
    async def send_rich_message(self, client: Client, chat_id: int, 
                              title: str, description: str, buttons=None):
        """Send beautifully formatted message"""
        text = f"""
{title}

{description}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        
        try:
            await client.send_message(chat_id, text, reply_markup=buttons)
        except Exception as e:
            print(f"Failed to send notification to {chat_id}: {e}")
    
    async def send_bulk_notification(self, client: Client, user_ids: List[int], 
                                   title: str, message: str):
        """Send notification to multiple users"""
        tasks = []
        for user_id in user_ids:
            task = self.send_rich_message(client, user_id, title, message)
            tasks.append(task)
        
        # Send with delay to avoid rate limits
        for i, task in enumerate(tasks):
            await task
            if i % 10 == 0:  # Delay every 10 messages
                await asyncio.sleep(1)
    
    async def send_analytics_report(self, client: Client, user_id: int, report: str):
        """Send analytics report to user"""
        title = "📊 Your Analytics Report"
        await self.send_rich_message(client, user_id, title, report)
    
    async def send_system_alert(self, client: Client, admin_ids: List[int], 
                              alert_type: str, message: str):
        """Send system alert to admins"""
        title = f"🚨 System Alert: {alert_type}"
        await self.send_bulk_notification(client, admin_ids, title, message)

# Global notification instance
notifications = NotificationService()