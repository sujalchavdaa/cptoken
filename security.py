import hashlib
import time
import re
from typing import Dict, Optional
from collections import defaultdict
import asyncio
from datetime import datetime, timedelta

class SecurityManager:
    def __init__(self):
        self.rate_limits = {
            "downloads_per_hour": 10,
            "uploads_per_hour": 5,
            "api_calls_per_minute": 30
        }
        self.user_activity = defaultdict(lambda: {
            "downloads": [],
            "uploads": [],
            "api_calls": []
        })
    
    def validate_url(self, url: str) -> bool:
        """Validate and sanitize URLs"""
        if not url or not isinstance(url, str):
            return False
        
        # Basic URL validation
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return bool(url_pattern.match(url))
    
    def encrypt_api_key(self, key: str) -> str:
        """Encrypt sensitive API keys"""
        if not key:
            return ""
        return hashlib.sha256(key.encode()).hexdigest()
    
    def check_rate_limit(self, user_id: int, action: str) -> bool:
        """Check if user has exceeded rate limits"""
        now = datetime.now()
        user_data = self.user_activity[user_id]
        
        if action not in user_data:
            return True
        
        # Clean old entries
        if action == "downloads":
            user_data[action] = [t for t in user_data[action] 
                               if now - t < timedelta(hours=1)]
            limit = self.rate_limits["downloads_per_hour"]
        elif action == "uploads":
            user_data[action] = [t for t in user_data[action] 
                               if now - t < timedelta(hours=1)]
            limit = self.rate_limits["uploads_per_hour"]
        elif action == "api_calls":
            user_data[action] = [t for t in user_data[action] 
                               if now - t < timedelta(minutes=1)]
            limit = self.rate_limits["api_calls_per_minute"]
        else:
            return True
        
        if len(user_data[action]) >= limit:
            return False
        
        user_data[action].append(now)
        return True
    
    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for safe storage"""
        # Remove dangerous characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Limit length
        if len(filename) > 255:
            name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
            filename = name[:255-len(ext)-1] + '.' + ext
        return filename
    
    def validate_file_size(self, size_bytes: int, max_size_mb: int = 100) -> bool:
        """Validate file size"""
        max_size_bytes = max_size_mb * 1024 * 1024
        return size_bytes <= max_size_bytes

# Global security instance
security = SecurityManager()