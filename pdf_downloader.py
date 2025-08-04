#!/usr/bin/env python3
"""
PDF Downloader - Actually download PDFs from Classplus
"""

import requests
import json
import asyncio
import aiohttp
import os
import time
from urllib.parse import urlparse
import re

class PDFDownloader:
    def __init__(self):
        self.download_folder = "downloaded_pdfs"
        self.session_token = "eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJzb3VyY2UiOjUwLCJzb3VyY2VfYXBwIjoiY2xhc3NwbHVzIiwic2Vzc2lvbl9pZCI6IjhkZTBmZTcyLTQ1NjEtNGNiYy04NjZhLTYzMjUyMTkwMTg2MyIsInZpc2l0b3JfaWQiOiJjMWFhM2IwNS03ZjlhLTRlZjktOTI1My0zNzRhM2RjMmYxZWYiLCJjcmVhdGVkX2F0IjoxNzU0MjI4MjIwNTQzLCJpYXQiOjE3NTQyMjgyMjAsImV4cCI6MTc1NTUyNDIyMH0.eKG1pqT0Ws6Dbb7LUzpHRjevH4Wi33Si-H2zLyEyuXCdhTc5kcK8cNnjm4XPSlaT"
        
        # Headers for API requests
        self.api_headers = {
            'accept': 'application/json',
            'authorization': f'Bearer {self.session_token}',
            'origin': 'https://web.classplusapp.com',
            'referer': 'https://web.classplusapp.com/',
            'region': 'IN',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'api-version': '52'
        }
        
        # Headers for file downloads
        self.download_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # Create download folder
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
            print(f"📁 Created download folder: {self.download_folder}")

    def sanitize_filename(self, filename):
        """Sanitize filename for safe saving"""
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Remove extra spaces
        filename = re.sub(r'\s+', ' ', filename).strip()
        # Limit length
        if len(filename) > 100:
            filename = filename[:100]
        return filename

    async def get_download_url(self, content_id):
        """Get actual download URL for a content ID"""
        url = f"https://api.classplusapp.com/v2/course/preview/document/download/{content_id}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.api_headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        download_url = data.get('data', {}).get('url')
                        if download_url:
                            print(f"✅ Got download URL for ID {content_id}: {download_url[:50]}...")
                            return download_url
                        else:
                            print(f"❌ No download URL in response for ID {content_id}")
                            return None
                    else:
                        print(f"❌ Failed to get download URL for ID {content_id}: {response.status}")
                        return None
                        
        except Exception as e:
            print(f"❌ Error getting download URL for ID {content_id}: {e}")
            return None

    async def download_pdf(self, content_id, filename, download_url=None):
        """Download a single PDF"""
        try:
            # If no download URL provided, get it
            if not download_url:
                download_url = await self.get_download_url(content_id)
                if not download_url:
                    print(f"❌ Could not get download URL for: {filename}")
                    return False
            
            # Sanitize filename
            safe_filename = self.sanitize_filename(filename)
            if not safe_filename.endswith('.pdf'):
                safe_filename += '.pdf'
            
            filepath = os.path.join(self.download_folder, safe_filename)
            
            # Check if file already exists
            if os.path.exists(filepath):
                print(f"⏭️  File already exists: {safe_filename}")
                return True
            
            print(f"📥 Downloading: {safe_filename}")
            print(f"   URL: {download_url[:50]}...")
            
            # Download the file
            async with aiohttp.ClientSession() as session:
                async with session.get(download_url, headers=self.download_headers) as response:
                    if response.status == 200:
                        # Get file size
                        content_length = response.headers.get('content-length')
                        if content_length:
                            size_mb = int(content_length) / (1024 * 1024)
                            print(f"   📊 File size: {size_mb:.2f} MB")
                        
                        # Download and save
                        with open(filepath, 'wb') as f:
                            async for chunk in response.content.iter_chunked(8192):
                                f.write(chunk)
                        
                        print(f"✅ Downloaded: {safe_filename}")
                        return True
                    else:
                        print(f"❌ Download failed for {filename}: {response.status}")
                        return False
                        
        except Exception as e:
            print(f"❌ Error downloading {filename}: {e}")
            return False

    async def download_pdfs_from_list(self, pdf_list):
        """Download PDFs from a list"""
        print(f"\n🚀 **PDF DOWNLOADER**")
        print("=" * 60)
        print(f"📁 Download folder: {self.download_folder}")
        print(f"📄 Total PDFs to download: {len(pdf_list)}")
        
        successful_downloads = 0
        failed_downloads = 0
        
        for i, pdf in enumerate(pdf_list, 1):
            content_id = pdf.get('id')
            name = pdf.get('name', f'PDF_{i}')
            url = pdf.get('url')
            
            print(f"\n📄 [{i}/{len(pdf_list)}] Processing: {name}")
            print(f"   ID: {content_id}")
            
            # Try to download
            success = await self.download_pdf(content_id, name, url)
            
            if success:
                successful_downloads += 1
            else:
                failed_downloads += 1
            
            # Small delay to avoid overwhelming the server
            await asyncio.sleep(1)
        
        print(f"\n📊 **DOWNLOAD SUMMARY:**")
        print("=" * 40)
        print(f"✅ Successful downloads: {successful_downloads}")
        print(f"❌ Failed downloads: {failed_downloads}")
        print(f"📁 Files saved in: {self.download_folder}")
        
        return successful_downloads, failed_downloads

    async def download_sample_pdfs(self):
        """Download a few sample PDFs for testing"""
        # Sample PDFs from our extracted list
        sample_pdfs = [
            {"id": "64802601", "name": "Rajasthan History Part 1", "url": None},
            {"id": "64802602", "name": "Rajasthan History Part 2", "url": None},
            {"id": "65257383", "name": "Polity Hindi Notes", "url": None},
            {"id": "65257384", "name": "Polity English Notes", "url": None},
            {"id": "64497224", "name": "Art & Culture Notes", "url": None}
        ]
        
        print("🧪 **TESTING PDF DOWNLOAD**")
        print("=" * 40)
        print("Downloading 5 sample PDFs to test the system...")
        
        return await self.download_pdfs_from_list(sample_pdfs)

async def main():
    downloader = PDFDownloader()
    
    # Test with sample PDFs first
    print("🔍 Testing PDF download functionality...")
    success, failed = await downloader.download_sample_pdfs()
    
    if success > 0:
        print(f"\n🎉 Successfully downloaded {success} PDFs!")
        print("✅ PDF download system is working!")
    else:
        print("\n❌ No PDFs were downloaded. There might be an issue with:")
        print("   - Authentication token")
        print("   - Download URLs")
        print("   - API permissions")
        print("   - Network connectivity")

if __name__ == "__main__":
    asyncio.run(main())