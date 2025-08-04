#!/usr/bin/env python3
"""
Online Agriculture API Scraper
Target: https://onlineagricultureapi.classx.co.in
"""

import requests
import re
import json
import os
import time
from urllib.parse import urljoin, urlparse
from datetime import datetime

class OnlineAgricultureScraper:
    def __init__(self):
        self.base_url = "https://onlineagricultureapi.classx.co.in"
        self.download_folder = "online_agriculture_downloads"
        
        # Create download folders
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
        if not os.path.exists(f"{self.download_folder}/pdfs"):
            os.makedirs(f"{self.download_folder}/pdfs")
        if not os.path.exists(f"{self.download_folder}/videos"):
            os.makedirs(f"{self.download_folder}/videos")
        if not os.path.exists(f"{self.download_folder}/html"):
            os.makedirs(f"{self.download_folder}/html")
            
        print(f"📁 Created download folders: {self.download_folder}")
        
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
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        }

    def test_api_connectivity(self):
        """Test basic API connectivity"""
        print("🔍 **TESTING API CONNECTIVITY**")
        print("=" * 50)
        
        try:
            print(f"🌐 Testing: {self.base_url}")
            response = requests.get(self.base_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                print("✅ API is accessible")
                print(f"📄 Response length: {len(response.text)} characters")
                
                # Save main response
                with open(f"{self.download_folder}/html/main_api_response.html", "w", encoding="utf-8") as f:
                    f.write(response.text)
                print("💾 Saved main API response")
                
                return response.text
            else:
                print(f"❌ API failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error connecting to API: {e}")
            return None

    def discover_api_endpoints(self):
        """Discover available API endpoints"""
        print("\n🔍 **DISCOVERING API ENDPOINTS**")
        print("=" * 50)
        
        # Common API endpoints to test
        endpoints = [
            "/",
            "/api",
            "/api/v1",
            "/api/v2",
            "/courses",
            "/api/courses",
            "/v1/courses",
            "/v2/courses",
            "/lessons",
            "/api/lessons",
            "/v1/lessons",
            "/v2/lessons",
            "/documents",
            "/api/documents",
            "/v1/documents",
            "/v2/documents",
            "/videos",
            "/api/videos",
            "/v1/videos",
            "/v2/videos",
            "/tests",
            "/api/tests",
            "/v1/tests",
            "/v2/tests",
            "/users",
            "/api/users",
            "/v1/users",
            "/v2/users",
            "/content",
            "/api/content",
            "/v1/content",
            "/v2/content",
            "/materials",
            "/api/materials",
            "/v1/materials",
            "/v2/materials"
        ]
        
        working_endpoints = []
        
        for endpoint in endpoints:
            url = f"{self.base_url}{endpoint}"
            try:
                print(f"🔍 Testing: {endpoint}")
                response = requests.get(url, headers=self.api_headers, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ Working endpoint: {endpoint}")
                    working_endpoints.append({
                        'endpoint': endpoint,
                        'url': url,
                        'status': response.status_code,
                        'content_type': response.headers.get('content-type', 'unknown'),
                        'response_length': len(response.text)
                    })
                    
                    # Try to parse JSON
                    try:
                        data = response.json()
                        print(f"   📊 JSON response with {len(data)} keys")
                        if isinstance(data, dict):
                            print(f"   📋 Keys: {list(data.keys())}")
                    except:
                        print(f"   📄 HTML/Text response: {response.text[:200]}...")
                        
                elif response.status_code == 401:
                    print(f"🔐 Authentication required: {endpoint}")
                elif response.status_code == 403:
                    print(f"🚫 Access forbidden: {endpoint}")
                elif response.status_code == 404:
                    print(f"❌ Not found: {endpoint}")
                else:
                    print(f"⚠️  Other status: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
        
        return working_endpoints

    def search_for_courses(self):
        """Search for courses on the API"""
        print("\n🔍 **SEARCHING FOR COURSES**")
        print("=" * 50)
        
        # Try different course search endpoints
        course_endpoints = [
            "/courses",
            "/api/courses",
            "/v1/courses",
            "/v2/courses",
            "/content",
            "/api/content",
            "/v1/content",
            "/v2/content"
        ]
        
        found_courses = []
        
        for endpoint in course_endpoints:
            url = f"{self.base_url}{endpoint}"
            try:
                print(f"🔍 Searching courses: {endpoint}")
                response = requests.get(url, headers=self.api_headers, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ Found course data")
                    
                    # Save course response
                    filename = f"{self.download_folder}/html/courses_{endpoint.replace('/', '_')}.html"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(response.text)
                    print(f"💾 Saved course data to: {filename}")
                    
                    # Try to extract course information
                    courses = self.extract_course_data(response.text)
                    found_courses.extend(courses)
                    
                else:
                    print(f"❌ Course search failed: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error searching courses: {e}")
        
        return found_courses

    def extract_course_data(self, content):
        """Extract course data from response"""
        courses = []
        
        try:
            # Try to parse as JSON first
            try:
                data = json.loads(content)
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            courses.append({
                                'id': item.get('id', 'unknown'),
                                'name': item.get('name', item.get('title', 'unknown')),
                                'type': 'json_list_item',
                                'data': item
                            })
                elif isinstance(data, dict):
                    if 'courses' in data:
                        for course in data['courses']:
                            courses.append({
                                'id': course.get('id', 'unknown'),
                                'name': course.get('name', course.get('title', 'unknown')),
                                'type': 'json_courses',
                                'data': course
                            })
                    else:
                        courses.append({
                            'id': data.get('id', 'unknown'),
                            'name': data.get('name', data.get('title', 'unknown')),
                            'type': 'json_single',
                            'data': data
                        })
            except:
                # If not JSON, try to extract from HTML
                course_patterns = [
                    r'<div[^>]*class="[^"]*course[^"]*"[^>]*>([^<]*)</div>',
                    r'<a[^>]*href="[^"]*course[^"]*"[^>]*>([^<]*)</a>',
                    r'"title":"([^"]*)"',
                    r'"name":"([^"]*)"',
                    r'"courseName":"([^"]*)"',
                    r'<h[1-6][^>]*>([^<]*course[^<]*)</h[1-6]>'
                ]
                
                for pattern in course_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    for match in matches:
                        if len(match.strip()) > 5:
                            courses.append({
                                'id': f"html_{len(courses)}",
                                'name': match.strip(),
                                'type': 'html_extraction',
                                'data': {'name': match.strip()}
                            })
            
            print(f"✅ Extracted {len(courses)} courses")
            
        except Exception as e:
            print(f"❌ Error extracting course data: {e}")
        
        return courses

    def search_for_pdfs(self):
        """Search for PDF files"""
        print("\n🔍 **SEARCHING FOR PDFS**")
        print("=" * 50)
        
        # Try different PDF endpoints
        pdf_endpoints = [
            "/documents",
            "/api/documents",
            "/v1/documents",
            "/v2/documents",
            "/pdfs",
            "/api/pdfs",
            "/v1/pdfs",
            "/v2/pdfs",
            "/materials",
            "/api/materials",
            "/v1/materials",
            "/v2/materials"
        ]
        
        found_pdfs = []
        
        for endpoint in pdf_endpoints:
            url = f"{self.base_url}{endpoint}"
            try:
                print(f"🔍 Searching PDFs: {endpoint}")
                response = requests.get(url, headers=self.api_headers, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ Found PDF data")
                    
                    # Save PDF response
                    filename = f"{self.download_folder}/html/pdfs_{endpoint.replace('/', '_')}.html"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(response.text)
                    print(f"💾 Saved PDF data to: {filename}")
                    
                    # Extract PDF URLs
                    pdfs = self.extract_pdf_urls(response.text)
                    found_pdfs.extend(pdfs)
                    
                else:
                    print(f"❌ PDF search failed: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error searching PDFs: {e}")
        
        return found_pdfs

    def extract_pdf_urls(self, content):
        """Extract PDF URLs from content"""
        pdfs = []
        
        try:
            # Look for PDF URLs
            pdf_patterns = [
                r'https?://[^"\s]+\.pdf',
                r'"url":"([^"]*\.pdf)"',
                r'"pdf_url":"([^"]*)"',
                r'"document_url":"([^"]*\.pdf)"',
                r'href="([^"]*\.pdf)"',
                r'src="([^"]*\.pdf)"'
            ]
            
            for pattern in pdf_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    if match.startswith('http'):
                        pdfs.append({
                            'url': match,
                            'filename': os.path.basename(match),
                            'type': 'direct_url'
                        })
                    else:
                        # Relative URL
                        full_url = urljoin(self.base_url, match)
                        pdfs.append({
                            'url': full_url,
                            'filename': os.path.basename(match),
                            'type': 'relative_url'
                        })
            
            print(f"✅ Found {len(pdfs)} PDF URLs")
            
        except Exception as e:
            print(f"❌ Error extracting PDF URLs: {e}")
        
        return pdfs

    def search_for_videos(self):
        """Search for video files"""
        print("\n🔍 **SEARCHING FOR VIDEOS**")
        print("=" * 50)
        
        # Try different video endpoints
        video_endpoints = [
            "/videos",
            "/api/videos",
            "/v1/videos",
            "/v2/videos",
            "/content",
            "/api/content",
            "/v1/content",
            "/v2/content"
        ]
        
        found_videos = []
        
        for endpoint in video_endpoints:
            url = f"{self.base_url}{endpoint}"
            try:
                print(f"🔍 Searching videos: {endpoint}")
                response = requests.get(url, headers=self.api_headers, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ Found video data")
                    
                    # Save video response
                    filename = f"{self.download_folder}/html/videos_{endpoint.replace('/', '_')}.html"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(response.text)
                    print(f"💾 Saved video data to: {filename}")
                    
                    # Extract video URLs
                    videos = self.extract_video_urls(response.text)
                    found_videos.extend(videos)
                    
                else:
                    print(f"❌ Video search failed: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error searching videos: {e}")
        
        return found_videos

    def extract_video_urls(self, content):
        """Extract video URLs from content"""
        videos = []
        
        try:
            # Look for video URLs
            video_patterns = [
                r'https?://[^"\s]+\.(mp4|avi|mov|wmv|flv|webm)',
                r'"url":"([^"]*\.(mp4|avi|mov|wmv|flv|webm))"',
                r'"video_url":"([^"]*)"',
                r'"stream_url":"([^"]*)"',
                r'href="([^"]*\.(mp4|avi|mov|wmv|flv|webm))"',
                r'src="([^"]*\.(mp4|avi|mov|wmv|flv|webm))"'
            ]
            
            for pattern in video_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        url = match[0]
                        ext = match[1]
                    else:
                        url = match
                        ext = 'mp4'
                    
                    if url.startswith('http'):
                        videos.append({
                            'url': url,
                            'filename': os.path.basename(url),
                            'type': 'direct_url',
                            'extension': ext
                        })
                    else:
                        # Relative URL
                        full_url = urljoin(self.base_url, url)
                        videos.append({
                            'url': full_url,
                            'filename': os.path.basename(url),
                            'type': 'relative_url',
                            'extension': ext
                        })
            
            print(f"✅ Found {len(videos)} video URLs")
            
        except Exception as e:
            print(f"❌ Error extracting video URLs: {e}")
        
        return videos

    def download_files(self, files, file_type):
        """Download files (PDFs or videos)"""
        print(f"\n📥 **DOWNLOADING {file_type.upper()}S**")
        print("=" * 50)
        
        downloaded_count = 0
        
        for i, file_info in enumerate(files, 1):
            try:
                url = file_info['url']
                filename = file_info['filename']
                
                print(f"📥 Downloading {i}/{len(files)}: {filename}")
                
                response = requests.get(url, headers=self.headers, timeout=30, stream=True)
                
                if response.status_code == 200:
                    # Save file
                    file_path = f"{self.download_folder}/{file_type}s/{filename}"
                    with open(file_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    print(f"✅ Downloaded: {filename}")
                    downloaded_count += 1
                    
                else:
                    print(f"❌ Failed to download {filename}: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error downloading {filename}: {e}")
        
        print(f"📊 Downloaded {downloaded_count}/{len(files)} {file_type}s")
        return downloaded_count

    def run_comprehensive_analysis(self):
        """Run comprehensive analysis of the API"""
        print("🚀 **ONLINE AGRICULTURE API ANALYSIS**")
        print("=" * 60)
        print(f"🎯 Target: {self.base_url}")
        print(f"📅 Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Test connectivity
        main_response = self.test_api_connectivity()
        
        # Discover endpoints
        working_endpoints = self.discover_api_endpoints()
        
        # Search for courses
        courses = self.search_for_courses()
        
        # Search for PDFs
        pdfs = self.search_for_pdfs()
        
        # Search for videos
        videos = self.search_for_videos()
        
        # Download PDFs if found
        if pdfs:
            downloaded_pdfs = self.download_files(pdfs, 'pdf')
        else:
            downloaded_pdfs = 0
        
        # Download videos if found
        if videos:
            downloaded_videos = self.download_files(videos, 'video')
        else:
            downloaded_videos = 0
        
        # Summary
        print(f"\n📊 **ANALYSIS SUMMARY:**")
        print("=" * 40)
        print(f"✅ API Connectivity: {'Working' if main_response else 'Failed'}")
        print(f"✅ Working Endpoints: {len(working_endpoints)}")
        print(f"✅ Courses Found: {len(courses)}")
        print(f"✅ PDFs Found: {len(pdfs)}")
        print(f"✅ Videos Found: {len(videos)}")
        print(f"✅ PDFs Downloaded: {downloaded_pdfs}")
        print(f"✅ Videos Downloaded: {downloaded_videos}")
        
        if courses:
            print(f"\n📚 **COURSES FOUND:**")
            for i, course in enumerate(courses[:10], 1):
                print(f"   {i}. {course['name']} (ID: {course['id']})")
        
        if pdfs:
            print(f"\n📄 **PDFS FOUND:**")
            for i, pdf in enumerate(pdfs[:10], 1):
                print(f"   {i}. {pdf['filename']}")
        
        if videos:
            print(f"\n🎥 **VIDEOS FOUND:**")
            for i, video in enumerate(videos[:10], 1):
                print(f"   {i}. {video['filename']}")
        
        print(f"\n💡 **NEXT STEPS:**")
        print("   1. Analyze downloaded files")
        print("   2. Test authentication if needed")
        print("   3. Explore course-specific content")
        print("   4. Implement automated downloads")

def main():
    scraper = OnlineAgricultureScraper()
    scraper.run_comprehensive_analysis()

if __name__ == "__main__":
    main()