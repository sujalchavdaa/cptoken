import traceback
import asyncio
from typing import Dict, Optional, Callable
from datetime import datetime
import logging

class ErrorHandler:
    def __init__(self):
        self.error_log = []
        self.error_solutions = {
            "ConnectionError": {
                "message": "🌐 Network connection issue",
                "solution": "Check your internet connection and try again",
                "retry_after": 30
            },
            "TimeoutError": {
                "message": "⏰ Request timed out",
                "solution": "The request took too long. Please try again",
                "retry_after": 60
            },
            "FileNotFoundError": {
                "message": "📁 File not found",
                "solution": "The file or URL doesn't exist. Please check the link",
                "retry_after": 0
            },
            "PermissionError": {
                "message": "🔒 Permission denied",
                "solution": "You don't have permission to access this file",
                "retry_after": 0
            },
            "ValueError": {
                "message": "⚠️ Invalid input",
                "solution": "Please check your input and try again",
                "retry_after": 0
            },
            "KeyError": {
                "message": "🔑 Missing data",
                "solution": "Required information is missing. Please try again",
                "retry_after": 0
            },
            "MemoryError": {
                "message": "💾 Out of memory",
                "solution": "File is too large. Try a smaller file",
                "retry_after": 0
            },
            "OSError": {
                "message": "💻 System error",
                "solution": "System error occurred. Please try again",
                "retry_after": 30
            },
            "default": {
                "message": "❌ Unexpected error",
                "solution": "An unexpected error occurred. Please try again",
                "retry_after": 60
            }
        }
    
    async def handle_error(self, error: Exception, user_id: int, 
                          context: str = "", client=None) -> Dict:
        """Handle errors comprehensively"""
        error_type = type(error).__name__
        error_info = self.error_solutions.get(error_type, self.error_solutions["default"])
        
        # Log error
        self.log_error(error, user_id, context)
        
        # Create error response
        error_response = {
            "error_type": error_type,
            "message": error_info["message"],
            "solution": error_info["solution"],
            "retry_after": error_info["retry_after"],
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "user_id": user_id
        }
        
        # Send notification if client is available
        if client:
            await self.send_error_notification(client, user_id, error_response)
        
        return error_response
    
    def log_error(self, error: Exception, user_id: int, context: str = ""):
        """Log error details"""
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "user_id": user_id,
            "context": context,
            "traceback": traceback.format_exc()
        }
        
        self.error_log.append(error_entry)
        
        # Keep only last 100 errors
        if len(self.error_log) > 100:
            self.error_log = self.error_log[-100:]
    
    async def send_error_notification(self, client, user_id: int, error_response: Dict):
        """Send user-friendly error notification"""
        try:
            message = f"""
{error_response['message']}

🔍 **Details:** {error_response['error_type']}
💡 **Solution:** {error_response['solution']}

⏰ **Time:** {error_response['timestamp']}
            """
            
            await client.send_message(user_id, message)
            
        except Exception as e:
            print(f"Failed to send error notification: {e}")
    
    def get_error_stats(self) -> Dict:
        """Get error statistics"""
        error_counts = {}
        for entry in self.error_log:
            error_type = entry["error_type"]
            error_counts[error_type] = error_counts.get(error_type, 0) + 1
        
        return {
            "total_errors": len(self.error_log),
            "error_types": error_counts,
            "recent_errors": self.error_log[-10:] if self.error_log else []
        }
    
    def should_retry(self, error_type: str) -> bool:
        """Check if operation should be retried"""
        error_info = self.error_solutions.get(error_type, self.error_solutions["default"])
        return error_info["retry_after"] > 0
    
    async def retry_operation(self, operation: Callable, max_retries: int = 3, 
                            delay: int = 5, *args, **kwargs):
        """Retry operation with exponential backoff"""
        for attempt in range(max_retries):
            try:
                return await operation(*args, **kwargs)
            except Exception as e:
                error_type = type(e).__name__
                
                if attempt == max_retries - 1:
                    raise e
                
                if not self.should_retry(error_type):
                    raise e
                
                # Wait before retry
                wait_time = delay * (2 ** attempt)
                await asyncio.sleep(wait_time)
    
    def validate_download_request(self, url: str, user_id: int) -> Dict:
        """Validate download request before processing"""
        errors = []
        
        # Check URL format
        if not url or not url.startswith(('http://', 'https://')):
            errors.append("Invalid URL format")
        
        # Check URL length
        if len(url) > 2048:
            errors.append("URL too long")
        
        # Check for suspicious patterns
        suspicious_patterns = [
            "javascript:", "data:", "file://", "ftp://"
        ]
        
        for pattern in suspicious_patterns:
            if pattern in url.lower():
                errors.append(f"Suspicious URL pattern: {pattern}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def validate_upload_request(self, file_size: int, file_type: str) -> Dict:
        """Validate upload request"""
        errors = []
        
        # Check file size (2GB limit)
        max_size = 2 * 1024 * 1024 * 1024
        if file_size > max_size:
            errors.append(f"File too large. Max size: 2GB")
        
        # Check file type
        allowed_types = [
            "pdf", "doc", "docx", "txt",
            "mp4", "avi", "mov", "mkv",
            "mp3", "wav", "aac",
            "jpg", "jpeg", "png", "gif"
        ]
        
        if file_type.lower() not in allowed_types:
            errors.append(f"File type not supported: {file_type}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def get_error_report(self) -> str:
        """Generate error report"""
        stats = self.get_error_stats()
        
        report = f"""
🚨 **Error Report**

📊 **Statistics:**
• Total Errors: {stats['total_errors']}
• Error Types: {len(stats['error_types'])}

🔍 **Most Common Errors:**
"""
        
        # Sort by frequency
        sorted_errors = sorted(stats['error_types'].items(), 
                             key=lambda x: x[1], reverse=True)
        
        for error_type, count in sorted_errors[:5]:
            report += f"• {error_type}: {count}\n"
        
        if stats['recent_errors']:
            report += "\n⏰ **Recent Errors:**\n"
            for error in stats['recent_errors'][-3:]:
                report += f"• {error['error_type']}: {error['error_message'][:50]}...\n"
        
        return report

# Global error handler instance
error_handler = ErrorHandler()