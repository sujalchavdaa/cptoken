#!/usr/bin/env python3
"""
Simple Web Scraper for Classplus PDF Downloads
"""

import requests
import re
import os
import time
from urllib.parse import urljoin, urlparse
import json

class SimpleClassplusScraper:
    def __init__(self):
        self.download_folder = "simple_downloaded_pdfs"
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
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
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
            
            # Look for hash token in HTML
            hash_patterns = [
                r'"hash":"([^"]+)"',
                r'hash["\']?\s*:\s*["\']([^"\']+)["\']',
                r'data-hash=["\']([^"\']+)["\']',
                r'window\.hash\s*=\s*["\']([^"\']+)["\']'
            ]
            
            for pattern in hash_patterns:
                matches = re.findall(pattern, html_content)
                if matches:
                    token = matches[0]
                    print(f"✅ Found hash token: {token[:20]}...")
                    return token
            
            print("❌ Hash token not found")
            return None
            
        except Exception as e:
            print(f"❌ Error extracting hash token: {e}")
            return None

    def extract_json_data(self, html_content):
        """Extract JSON data from HTML"""
        try:
            print("🔍 Extracting JSON data...")
            
            # Look for JSON data in HTML
            json_patterns = [
                r'window\.__INITIAL_STATE__\s*=\s*({[^;]+});',
                r'window\.data\s*=\s*({[^;]+});',
                r'<script[^>]*>([^<]*window[^<]*)</script>',
                r'<script[^>]*>([^<]*courses[^<]*)</script>',
                r'<script[^>]*>([^<]*content[^<]*)</script>'
            ]
            
            json_data = []
            for pattern in json_patterns:
                matches = re.findall(pattern, html_content, re.IGNORECASE)
                for match in matches:
                    try:
                        # Try to extract JSON from the match
                        json_match = re.search(r'\{[^{}]*\}', match)
                        if json_match:
                            data = json.loads(json_match.group())
                            json_data.append(data)
                            print(f"✅ Found JSON data with {len(data)} keys")
                    except:
                        continue
            
            return json_data
            
        except Exception as e:
            print(f"❌ Error extracting JSON data: {e}")
            return []

    def extract_pdf_urls(self, html_content):
        """Extract PDF URLs from HTML content"""
        try:
            print("🔍 Extracting PDF URLs...")
            
            # PDF URL patterns
            pdf_patterns = [
                r'https?://[^"\s]*\.pdf[^"\s]*',
                r'https?://[^"\s]*document[^"\s]*',
                r'https?://[^"\s]*download[^"\s]*',
                r'"url":"([^"]*\.pdf[^"]*)"',
                r'"downloadUrl":"([^"]*)"',
                r'"fileUrl":"([^"]*)"',
                r'"pdfUrl":"([^"]*)"',
                r'href=["\']([^"\']*\.pdf[^"\']*)["\']',
                r'src=["\']([^"\']*\.pdf[^"\']*)["\']'
            ]
            
            pdf_urls = []
            for pattern in pdf_patterns:
                matches = re.findall(pattern, html_content, re.IGNORECASE)
                pdf_urls.extend(matches)
            
            # Remove duplicates and filter
            unique_urls = []
            seen_urls = set()
            
            for url in pdf_urls:
                if url and url not in seen_urls and ('pdf' in url.lower() or 'document' in url.lower()):
                    seen_urls.add(url)
                    unique_urls.append(url)
            
            print(f"✅ Found {len(unique_urls)} PDF URLs")
            return unique_urls
            
        except Exception as e:
            print(f"❌ Error extracting PDF URLs: {e}")
            return []

    def extract_course_links(self, html_content):
        """Extract course links from HTML"""
        try:
            print("🔍 Extracting course links...")
            
            # Course link patterns
            course_patterns = [
                r'href=["\']([^"\']*course[^"\']*)["\']',
                r'href=["\']([^"\']*courses[^"\']*)["\']',
                r'<a[^>]*href=["\']([^"\']*course[^"\']*)["\'][^>]*>([^<]*)</a>',
                r'<a[^>]*href=["\']([^"\']*courses[^"\']*)["\'][^>]*>([^<]*)</a>'
            ]
            
            course_links = []
            for pattern in course_patterns:
                matches = re.findall(pattern, html_content, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        url, title = match
                    else:
                        url = match
                        title = "Course"
                    
                    if url and 'course' in url.lower():
                        full_url = urljoin(self.base_url, url)
                        course_links.append({
                            'url': full_url,
                            'title': title.strip()
                        })
            
            # Remove duplicates
            unique_links = []
            seen_urls = set()
            
            for link in course_links:
                if link['url'] not in seen_urls:
                    seen_urls.add(link['url'])
                    unique_links.append(link)
            
            print(f"✅ Found {len(unique_links)} course links")
            return unique_links
            
        except Exception as e:
            print(f"❌ Error extracting course links: {e}")
            return []

    def find_ras_course(self, course_links):
        """Find RAS PRE course from links"""
        try:
            print("🔍 Looking for RAS PRE course...")
            
            for link in course_links:
                title = link['title'].lower()
                if 'ras' in title and ('pre' in title or 'prelims' in title):
                    print(f"🎯 Found RAS course: {link['title']}")
                    print(f"   URL: {link['url']}")
                    return link
            
            print("❌ RAS PRE course not found")
            return None
            
        except Exception as e:
            print(f"❌ Error finding RAS course: {e}")
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

    def download_pdfs_batch(self, pdf_urls):
        """Download multiple PDFs"""
        print(f"\n🚀 **BATCH PDF DOWNLOAD**")
        print("=" * 50)
        print(f"📁 Download folder: {self.download_folder}")
        print(f"📄 Total PDFs to download: {len(pdf_urls)}")
        
        successful_downloads = 0
        failed_downloads = 0
        
        for i, url in enumerate(pdf_urls, 1):
            print(f"\n📄 [{i}/{len(pdf_urls)}] Processing...")
            
            success = self.download_pdf(url)
            
            if success:
                successful_downloads += 1
            else:
                failed_downloads += 1
            
            # Small delay between downloads
            time.sleep(1)
        
        print(f"\n📊 **DOWNLOAD SUMMARY:**")
        print("=" * 40)
        print(f"✅ Successful downloads: {successful_downloads}")
        print(f"❌ Failed downloads: {failed_downloads}")
        print(f"📁 Files saved in: {self.download_folder}")
        
        return successful_downloads, failed_downloads

    def run_scraping(self):
        """Main scraping function"""
        print("🚀 **SIMPLE WEB SCRAPER**")
        print("=" * 60)
        
        # Get main page content
        main_content = self.get_page_content(self.base_url)
        if not main_content:
            print("❌ Failed to get main page content")
            return
        
        # Extract hash token
        hash_token = self.extract_hash_token(main_content)
        
        # Extract JSON data
        json_data = self.extract_json_data(main_content)
        
        # Extract course links
        course_links = self.extract_course_links(main_content)
        
        # Find RAS course
        ras_course = self.find_ras_course(course_links)
        
        # Extract PDF URLs from main page
        pdf_urls = self.extract_pdf_urls(main_content)
        
        # If RAS course found, get its content
        if ras_course:
            print(f"\n🔍 Getting RAS course content...")
            course_content = self.get_page_content(ras_course['url'])
            if course_content:
                course_pdf_urls = self.extract_pdf_urls(course_content)
                pdf_urls.extend(course_pdf_urls)
                print(f"✅ Added {len(course_pdf_urls)} PDFs from RAS course")
        
        # Remove duplicates
        unique_pdf_urls = list(set(pdf_urls))
        print(f"\n📄 Total unique PDF URLs found: {len(unique_pdf_urls)}")
        
        # Show first few URLs
        for i, url in enumerate(unique_pdf_urls[:5], 1):
            print(f"   {i}. {url[:80]}...")
        
        if len(unique_pdf_urls) > 5:
            print(f"   ... and {len(unique_pdf_urls) - 5} more")
        
        # Download PDFs
        if unique_pdf_urls:
            success, failed = self.download_pdfs_batch(unique_pdf_urls)
            
            print(f"\n🎉 **SCRAPING COMPLETE**")
            print("=" * 40)
            print(f"📁 Check folder: {self.download_folder}")
            print(f"✅ Successfully downloaded: {success} PDFs")
            print(f"❌ Failed downloads: {failed} PDFs")
        else:
            print("\n❌ No PDF URLs found")

def main():
    scraper = SimpleClassplusScraper()
    scraper.run_scraping()

if __name__ == "__main__":
    main()