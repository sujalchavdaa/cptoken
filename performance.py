import aiohttp
import aiofiles
import asyncio
import os
import time
from typing import Optional, Callable
from pathlib import Path
import hashlib
from datetime import datetime, timedelta

class PerformanceManager:
    def __init__(self):
        self.cache_dir = Path("cache")
        self.cache_dir.mkdir(exist_ok=True)
        self.download_cache = {}
        self.session = None
    
    async def get_session(self):
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=300)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session
    
    async def smart_download(self, url: str, filename: str, 
                           progress_callback: Optional[Callable] = None,
                           chunk_size: int = 8192) -> bool:
        """Optimized download with progress tracking and caching"""
        try:
            session = await self.get_session()
            
            # Check cache first
            cache_key = hashlib.md5(url.encode()).hexdigest()
            cache_file = self.cache_dir / f"{cache_key}.cache"
            
            if cache_file.exists():
                # Use cached file if it's less than 1 hour old
                if time.time() - cache_file.stat().st_mtime < 3600:
                    shutil.copy2(cache_file, filename)
                    if progress_callback:
                        await progress_callback(100, "Using cached file")
                    return True
            
            async with session.get(url) as response:
                if response.status != 200:
                    return False
                
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                with open(filename, 'wb') as f:
                    async for chunk in response.content.iter_chunked(chunk_size):
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0 and progress_callback:
                            progress = (downloaded / total_size) * 100
                            await progress_callback(progress, f"Downloading... {downloaded}/{total_size} bytes")
                
                # Cache the downloaded file
                shutil.copy2(filename, cache_file)
                return True
                
        except Exception as e:
            print(f"Download error: {e}")
            return False
    
    async def parallel_downloads(self, urls: list, max_concurrent: int = 3):
        """Download multiple files in parallel"""
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def download_with_semaphore(url):
            async with semaphore:
                return await self.smart_download(url, f"download_{hashlib.md5(url.encode()).hexdigest()}")
        
        tasks = [download_with_semaphore(url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)
    
    def get_file_info(self, file_path: str) -> dict:
        """Get detailed file information"""
        try:
            stat = os.stat(file_path)
            return {
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_ctime),
                "modified": datetime.fromtimestamp(stat.st_mtime),
                "extension": Path(file_path).suffix,
                "name": Path(file_path).name
            }
        except Exception:
            return {}
    
    async def compress_file(self, input_path: str, output_path: str, quality: int = 85):
        """Compress file to reduce size"""
        try:
            import subprocess
            
            if input_path.endswith(('.jpg', '.jpeg', '.png')):
                # Compress image
                cmd = ['convert', input_path, '-quality', str(quality), output_path]
            elif input_path.endswith(('.mp4', '.avi', '.mov')):
                # Compress video
                cmd = ['ffmpeg', '-i', input_path, '-c:v', 'libx264', '-crf', str(quality), output_path]
            else:
                # Just copy for other files
                shutil.copy2(input_path, output_path)
                return True
            
            process = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            return process.returncode == 0
            
        except Exception as e:
            print(f"Compression error: {e}")
            return False
    
    def cleanup_cache(self, max_age_hours: int = 24):
        """Clean up old cache files"""
        cutoff_time = time.time() - (max_age_hours * 3600)
        
        for cache_file in self.cache_dir.glob("*.cache"):
            if cache_file.stat().st_mtime < cutoff_time:
                cache_file.unlink()
    
    async def close(self):
        """Close session and cleanup"""
        if self.session and not self.session.closed:
            await self.session.close()

# Global performance instance
performance = PerformanceManager()