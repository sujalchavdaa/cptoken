import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict
import os

class Analytics:
    def __init__(self):
        self.stats = {
            "downloads": 0,
            "uploads": 0,
            "errors": 0,
            "users": set(),
            "file_types": defaultdict(int),
            "hourly_activity": defaultdict(int),
            "daily_activity": defaultdict(int)
        }
        self.user_stats = defaultdict(lambda: {
            "downloads": 0,
            "uploads": 0,
            "last_activity": None,
            "favorite_formats": defaultdict(int),
            "total_size": 0
        })
        self.analytics_file = "analytics.json"
        self.load_analytics()
    
    def load_analytics(self):
        """Load analytics from file"""
        try:
            if os.path.exists(self.analytics_file):
                with open(self.analytics_file, 'r') as f:
                    data = json.load(f)
                    self.stats.update(data.get('global_stats', {}))
                    # Convert user_ids back to integers
                    for user_id_str, user_data in data.get('user_stats', {}).items():
                        self.user_stats[int(user_id_str)] = user_data
        except Exception as e:
            print(f"Error loading analytics: {e}")
    
    def save_analytics(self):
        """Save analytics to file"""
        try:
            data = {
                'global_stats': self.stats,
                'user_stats': {str(k): v for k, v in self.user_stats.items()},
                'last_updated': datetime.now().isoformat()
            }
            with open(self.analytics_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving analytics: {e}")
    
    async def track_download(self, user_id: int, file_size: int, file_type: str):
        """Track download statistics"""
        now = datetime.now()
        
        # Global stats
        self.stats["downloads"] += 1
        self.stats["users"].add(user_id)
        self.stats["file_types"][file_type] += 1
        self.stats["hourly_activity"][now.hour] += 1
        self.stats["daily_activity"][now.strftime("%Y-%m-%d")] += 1
        
        # User stats
        self.user_stats[user_id]["downloads"] += 1
        self.user_stats[user_id]["last_activity"] = now.isoformat()
        self.user_stats[user_id]["favorite_formats"][file_type] += 1
        self.user_stats[user_id]["total_size"] += file_size
        
        await self.save_analytics_async()
    
    async def track_upload(self, user_id: int, file_size: int, file_type: str):
        """Track upload statistics"""
        now = datetime.now()
        
        # Global stats
        self.stats["uploads"] += 1
        self.stats["users"].add(user_id)
        self.stats["file_types"][file_type] += 1
        self.stats["hourly_activity"][now.hour] += 1
        self.stats["daily_activity"][now.strftime("%Y-%m-%d")] += 1
        
        # User stats
        self.user_stats[user_id]["uploads"] += 1
        self.user_stats[user_id]["last_activity"] = now.isoformat()
        self.user_stats[user_id]["favorite_formats"][file_type] += 1
        self.user_stats[user_id]["total_size"] += file_size
        
        await self.save_analytics_async()
    
    async def track_error(self, user_id: int, error_type: str):
        """Track error statistics"""
        self.stats["errors"] += 1
        self.user_stats[user_id]["last_activity"] = datetime.now().isoformat()
        await self.save_analytics_async()
    
    async def save_analytics_async(self):
        """Save analytics asynchronously"""
        await asyncio.get_event_loop().run_in_executor(None, self.save_analytics)
    
    def get_user_analytics(self, user_id: int) -> Dict:
        """Get detailed user analytics"""
        user_data = self.user_stats.get(user_id, {})
        
        # Get favorite format
        favorite_format = max(user_data.get("favorite_formats", {}).items(), 
                            key=lambda x: x[1], default=("None", 0))[0]
        
        return {
            "total_downloads": user_data.get("downloads", 0),
            "total_uploads": user_data.get("uploads", 0),
            "favorite_format": favorite_format,
            "total_size_mb": round(user_data.get("total_size", 0) / (1024 * 1024), 2),
            "last_activity": user_data.get("last_activity"),
            "formats_used": dict(user_data.get("favorite_formats", {}))
        }
    
    def get_global_stats(self) -> Dict:
        """Get global statistics"""
        now = datetime.now()
        today = now.strftime("%Y-%m-%d")
        
        return {
            "total_downloads": self.stats["downloads"],
            "total_uploads": self.stats["uploads"],
            "total_errors": self.stats["errors"],
            "unique_users": len(self.stats["users"]),
            "today_downloads": self.stats["daily_activity"].get(today, 0),
            "popular_formats": dict(sorted(self.stats["file_types"].items(), 
                                         key=lambda x: x[1], reverse=True)[:5]),
            "busiest_hour": max(self.stats["hourly_activity"].items(), 
                              key=lambda x: x[1], default=(0, 0))[0]
        }
    
    def get_trends(self, days: int = 7) -> Dict:
        """Get activity trends for the last N days"""
        trends = {}
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            trends[date] = self.stats["daily_activity"].get(date, 0)
        
        return dict(sorted(trends.items(), reverse=True))
    
    def get_top_users(self, limit: int = 10) -> List[Dict]:
        """Get top users by activity"""
        users = []
        for user_id, data in self.user_stats.items():
            total_activity = data.get("downloads", 0) + data.get("uploads", 0)
            if total_activity > 0:
                users.append({
                    "user_id": user_id,
                    "downloads": data.get("downloads", 0),
                    "uploads": data.get("uploads", 0),
                    "total_activity": total_activity,
                    "last_activity": data.get("last_activity")
                })
        
        return sorted(users, key=lambda x: x["total_activity"], reverse=True)[:limit]
    
    def generate_report(self) -> str:
        """Generate a comprehensive analytics report"""
        global_stats = self.get_global_stats()
        trends = self.get_trends()
        top_users = self.get_top_users(5)
        
        report = f"""
📊 **Analytics Report**

📈 **Global Statistics:**
• Total Downloads: {global_stats['total_downloads']}
• Total Uploads: {global_stats['total_uploads']}
• Total Errors: {global_stats['total_errors']}
• Unique Users: {global_stats['unique_users']}
• Today's Activity: {global_stats['today_downloads']}

🎯 **Popular Formats:**
"""
        for format_name, count in global_stats['popular_formats'].items():
            report += f"• {format_name}: {count}\n"
        
        report += f"\n⏰ **Busiest Hour:** {global_stats['busiest_hour']}:00\n"
        
        report += "\n👥 **Top Users:**\n"
        for i, user in enumerate(top_users, 1):
            report += f"{i}. User {user['user_id']}: {user['total_activity']} activities\n"
        
        return report

# Global analytics instance
analytics = Analytics()