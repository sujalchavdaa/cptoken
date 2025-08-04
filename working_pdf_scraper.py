#!/usr/bin/env python3
"""
Working PDF Scraper using hash token and JSON data
"""

import requests
import re
import json
import os
import time
from urllib.parse import urljoin, urlparse

class WorkingPDFScraper:
    def __init__(self):
        self.download_folder = "working_downloaded_pdfs"
        self.org_code = "Uievjh"
        self.base_url = f"https://{self.org_code}.courses.store"
        
        # Create download folder
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
            print(f"📁 Created download folder: {self.download_folder}")
        
        # Headers for requests
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # API headers
        self.api_headers = {
            'accept': 'application/json',
            'accept-language': 'EN',
            'api-version': '35',
            'app-version': '1.4.73.2',
            'build-number': '35',
            'connection': 'Keep-Alive',
            'content-type': 'application/json',
            'device-details': 'Xiaomi_Redmi 7_SDK-32',
            'device-id': 'c28d3cb16bbdac01',
            'host': 'api.classplusapp.com',
            'region': 'IN',
            'user-agent': 'Mobile-Android',
            'webengage-luid': '00000187-6fe4-5d41-a530-26186858be4c'
        }

    def get_page_content(self, url):
        """Get page content"""
        try:
            print(f"🌐 Fetching: {url}")
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Successfully fetched page")
                return response.text
            else:
                print(f"❌ Failed to fetch page: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error fetching page: {e}")
            return None

    def extract_hash_token(self, html_content):
        """Extract hash token from HTML"""
        try:
            print("🔍 Extracting hash token...")
            
            # Look for hash token in JSON data
            hash_pattern = r'"hash":"([^"]+)"'
            matches = re.findall(hash_pattern, html_content)
            
            if matches:
                token = matches[0]
                print(f"✅ Found hash token: {token[:20]}...")
                return token
            
            print("❌ Hash token not found")
            return None
            
        except Exception as e:
            print(f"❌ Error extracting hash token: {e}")
            return None

    def get_courses_from_hash(self, hash_token):
        """Get courses using hash token"""
        try:
            print("🔍 Getting courses from hash token...")
            
            url = f"https://api.classplusapp.com/v2/course/preview/similar/{hash_token}?limit=50"
            
            response = requests.get(url, headers=self.api_headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                courses = data.get('data', {}).get('coursesData', [])
                print(f"✅ Found {len(courses)} courses")
                return courses
            else:
                print(f"❌ Failed to get courses: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error getting courses: {e}")
            return []

    def find_ras_course(self, courses):
        """Find RAS PRE course"""
        try:
            print("🔍 Looking for RAS PRE course...")
            
            for course in courses:
                name = course.get('name', '').lower()
                if 'ras' in name and ('pre' in name or 'prelims' in name):
                    print(f"🎯 Found RAS course: {course.get('name')}")
                    print(f"   ID: {course.get('id')}")
                    print(f"   Price: ₹{course.get('finalPrice', 0)}")
                    return course
            
            print("❌ RAS PRE course not found")
            return None
            
        except Exception as e:
            print(f"❌ Error finding RAS course: {e}")
            return None

    def get_course_content(self, course_id):
        """Get course content using course ID"""
        try:
            print(f"🔍 Getting content for course ID: {course_id}")
            
            # First get batch token
            batch_url = "https://api.classplusapp.com/v2/course/preview/org/info"
            params = {'courseId': str(course_id)}
            
            response = requests.get(batch_url, params=params, headers=self.api_headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                batch_token = data.get('data', {}).get('hash')
                
                if batch_token:
                    print(f"✅ Got batch token: {batch_token[:20]}...")
                    
                    # Get course content
                    content_url = f"https://api.classplusapp.com/v2/course/preview/content/list/{batch_token}"
                    params = {'folderId': 0, 'limit': 9999999999}
                    
                    content_response = requests.get(content_url, params=params, headers=self.api_headers, timeout=10)
                    
                    if content_response.status_code == 200:
                        content_data = content_response.json()
                        contents = content_data.get('data', [])
                        print(f"✅ Found {len(contents)} content items")
                        return contents
                    else:
                        print(f"❌ Failed to get content: {content_response.status_code}")
                        return []
                else:
                    print("❌ No batch token found")
                    return []
            else:
                print(f"❌ Failed to get batch token: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error getting course content: {e}")
            return []

    def extract_pdfs_from_content(self, contents, folder_id=0, depth=0):
        """Recursively extract PDFs from content"""
        pdfs = []
        indent = "  " * depth
        
        try:
            for content in contents:
                content_type = content.get('contentType')
                name = content.get('name', '')
                content_id = content.get('id')
                
                # Type 3 = PDF/Document
                if content_type == 3:
                    pdfs.append({
                        'name': name,
                        'id': content_id,
                        'folder_depth': depth,
                        'content_type': content_type,
                        'format': content.get('format', ''),
                        'url': content.get('url') or content.get('thumbnailUrl')
                    })
                    print(f"{indent}📄 PDF Found: {name} (ID: {content_id})")
                
                # Check if it's a folder (contentType == 1)
                elif content_type == 1:
                    folder_id = content.get('id')
                    if folder_id:
                        print(f"{indent}📁 Entering folder: {name} (ID: {folder_id})")
                        
                        # Get folder contents
                        folder_url = f"https://api.classplusapp.com/v2/course/preview/content/list/{batch_token}"
                        folder_params = {'folderId': folder_id, 'limit': 9999999999}
                        
                        folder_response = requests.get(folder_url, params=folder_params, headers=self.api_headers, timeout=10)
                        
                        if folder_response.status_code == 200:
                            folder_data = folder_response.json()
                            folder_contents = folder_data.get('data', [])
                            
                            # Recursively get folder contents
                            folder_pdfs = self.extract_pdfs_from_content(folder_contents, folder_id, depth + 1)
                            pdfs.extend(folder_pdfs)
                            print(f"{indent}📁 Exiting folder: {name}")
                
                # Check for other document types (Type 4 = Test/Quiz)
                elif content_type == 4:
                    pdfs.append({
                        'name': name,
                        'id': content_id,
                        'folder_depth': depth,
                        'content_type': content_type,
                        'url': content.get('url') or content.get('thumbnailUrl')
                    })
                    print(f"{indent}📝 Test Found: {name} (ID: {content_id})")
            
        except Exception as e:
            print(f"{indent}❌ Error in folder {folder_id}: {e}")
        
        return pdfs

    def get_download_url(self, content_id):
        """Get download URL for content ID"""
        try:
            url = f"https://api.classplusapp.com/v2/course/preview/document/download/{content_id}"
            
            response = requests.get(url, headers=self.api_headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                download_url = data.get('data', {}).get('url')
                if download_url:
                    print(f"✅ Got download URL for ID {content_id}")
                    return download_url
                else:
                    print(f"❌ No download URL in response for ID {content_id}")
                    return None
            else:
                print(f"❌ Failed to get download URL for ID {content_id}: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error getting download URL for ID {content_id}: {e}")
            return None

    def download_pdf(self, url, filename=None):
        """Download a single PDF"""
        try:
            if not filename:
                # Extract filename from URL
                filename = os.path.basename(urlparse(url).path)
                if not filename.endswith('.pdf'):
                    filename = f"pdf_{int(time.time())}.pdf"
            
            filepath = os.path.join(self.download_folder, filename)
            
            # Check if file already exists
            if os.path.exists(filepath):
                print(f"⏭️  File already exists: {filename}")
                return True
            
            print(f"📥 Downloading: {filename}")
            print(f"   URL: {url[:80]}...")
            
            # Download file
            response = requests.get(url, headers=self.headers, stream=True, timeout=30)
            
            if response.status_code == 200:
                # Get file size
                content_length = response.headers.get('content-length')
                if content_length:
                    size_mb = int(content_length) / (1024 * 1024)
                    print(f"   📊 File size: {size_mb:.2f} MB")
                
                # Save file
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f"✅ Downloaded: {filename}")
                return True
            else:
                print(f"❌ Download failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error downloading {url}: {e}")
            return False

    def run_scraping(self):
        """Main scraping function"""
        print("🚀 **WORKING PDF SCRAPER**")
        print("=" * 60)
        
        # Get main page content
        main_content = self.get_page_content(self.base_url)
        if not main_content:
            print("❌ Failed to get main page content")
            return
        
        # Extract hash token
        hash_token = self.extract_hash_token(main_content)
        if not hash_token:
            print("❌ No hash token found")
            return
        
        # Get courses from hash token
        courses = self.get_courses_from_hash(hash_token)
        if not courses:
            print("❌ No courses found")
            return
        
        # Find RAS course
        ras_course = self.find_ras_course(courses)
        if not ras_course:
            print("❌ RAS course not found")
            return
        
        # Get course content
        course_id = ras_course.get('id')
        contents = self.get_course_content(course_id)
        
        if not contents:
            print("❌ No content found for RAS course")
            return
        
        # Extract PDFs from content
        pdfs = self.extract_pdfs_from_content(contents)
        
        if not pdfs:
            print("❌ No PDFs found in course content")
            return
        
        print(f"\n📄 **FOUND {len(pdfs)} PDFs/DOCUMENTS:**")
        print("=" * 60)
        
        # Show PDFs found
        for i, pdf in enumerate(pdfs, 1):
            content_type_text = "PDF" if pdf['content_type'] == 3 else "Test"
            print(f"{i}. {pdf['name']} ({content_type_text})")
            print(f"   ID: {pdf['id']}")
            if pdf.get('url'):
                print(f"   URL: {pdf['url'][:80]}...")
        
        # Download PDFs
        print(f"\n🚀 **DOWNLOADING PDFs**")
        print("=" * 50)
        
        successful_downloads = 0
        failed_downloads = 0
        
        for i, pdf in enumerate(pdfs, 1):
            print(f"\n📄 [{i}/{len(pdfs)}] Processing: {pdf['name']}")
            
            # Get download URL
            download_url = self.get_download_url(pdf['id'])
            
            if download_url:
                # Download PDF
                success = self.download_pdf(download_url, f"{pdf['name']}.pdf")
                
                if success:
                    successful_downloads += 1
                else:
                    failed_downloads += 1
            else:
                print(f"❌ Could not get download URL")
                failed_downloads += 1
            
            # Small delay between downloads
            time.sleep(1)
        
        print(f"\n📊 **DOWNLOAD SUMMARY:**")
        print("=" * 40)
        print(f"✅ Successful downloads: {successful_downloads}")
        print(f"❌ Failed downloads: {failed_downloads}")
        print(f"📁 Files saved in: {self.download_folder}")
        
        if successful_downloads > 0:
            print(f"\n🎉 **SUCCESS!** Downloaded {successful_downloads} PDFs!")
        else:
            print(f"\n❌ **FAILED!** No PDFs were downloaded.")

def main():
    scraper = WorkingPDFScraper()
    scraper.run_scraping()

if __name__ == "__main__":
    main()