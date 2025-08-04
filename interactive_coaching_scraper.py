#!/usr/bin/env python3
"""
Interactive Appex Coaching API Scraper
Asks user for coaching institute API URL and tests it
"""

import requests
import re
import json
import os
import time
from urllib.parse import urljoin, urlparse
from datetime import datetime

class InteractiveCoachingScraper:
    def __init__(self):
        self.download_folder = "interactive_coaching_downloads"
        
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

    def get_coaching_url(self):
        """Get coaching institute URL from user"""
        print("🎯 **APPEX COACHING API SCRAPER**")
        print("=" * 60)
        print("This scraper can test any Appex coaching institute API!")
        print("Just provide the coaching institute API URL.")
        print()
        print("Example URLs:")
        print("  • https://onlineagricultureapi.classx.co.in")
        print("  • https://rascoachingapi.classx.co.in")
        print("  • https://upsccoachingapi.classx.co.in")
        print("  • https://yourcoachingapi.classx.co.in")
        print()
        
        while True:
            coaching_url = input("🔗 Enter coaching institute API URL: ").strip()
            
            if not coaching_url:
                print("❌ Please enter a valid URL")
                continue
                
            if not coaching_url.startswith(('http://', 'https://')):
                coaching_url = 'https://' + coaching_url
                
            print(f"✅ Testing: {coaching_url}")
            return coaching_url

    def test_coaching_api(self, coaching_url):
        """Test a specific coaching institute API"""
        print(f"\n🔍 **TESTING COACHING API: {coaching_url}**")
        print("=" * 60)
        
        try:
            print(f"🌐 Testing: {coaching_url}")
            response = requests.get(coaching_url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                print("✅ Coaching API is accessible")
                print(f"📄 Response length: {len(response.text)} characters")
                print(f"📄 Response: {response.text[:200]}...")
                
                # Save response
                coaching_name = coaching_url.split('//')[1].split('.')[0] if '//' in coaching_url else 'unknown'
                filename = f"{self.download_folder}/html/{coaching_name}_main_response.html"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(response.text)
                print(f"💾 Saved coaching response to: {filename}")
                
                return response.text
            else:
                print(f"❌ Coaching API failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error connecting to coaching API: {e}")
            return None

    def discover_coaching_endpoints(self, coaching_url):
        """Discover endpoints for a specific coaching institute"""
        print(f"\n🔍 **DISCOVERING ENDPOINTS FOR: {coaching_url}**")
        print("=" * 60)
        
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
            url = f"{coaching_url.rstrip('/')}{endpoint}"
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
                else:
                    print(f"❌ Failed: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
        
        return working_endpoints

    def search_coaching_courses(self, coaching_url):
        """Search for courses in a specific coaching institute"""
        print(f"\n🔍 **SEARCHING COURSES IN: {coaching_url}**")
        print("=" * 60)
        
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
            url = f"{coaching_url.rstrip('/')}{endpoint}"
            try:
                print(f"🔍 Searching courses: {endpoint}")
                response = requests.get(url, headers=self.api_headers, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ Found course data")
                    
                    # Save course response
                    coaching_name = coaching_url.split('//')[1].split('.')[0] if '//' in coaching_url else 'unknown'
                    filename = f"{self.download_folder}/html/{coaching_name}_courses_{endpoint.replace('/', '_')}.html"
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

    def search_coaching_pdfs(self, coaching_url):
        """Search for PDFs in a specific coaching institute"""
        print(f"\n🔍 **SEARCHING PDFS IN: {coaching_url}**")
        print("=" * 60)
        
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
            url = f"{coaching_url.rstrip('/')}{endpoint}"
            try:
                print(f"🔍 Searching PDFs: {endpoint}")
                response = requests.get(url, headers=self.api_headers, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ Found PDF data")
                    
                    # Save PDF response
                    coaching_name = coaching_url.split('//')[1].split('.')[0] if '//' in coaching_url else 'unknown'
                    filename = f"{self.download_folder}/html/{coaching_name}_pdfs_{endpoint.replace('/', '_')}.html"
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

    def search_coaching_videos(self, coaching_url):
        """Search for videos in a specific coaching institute"""
        print(f"\n🔍 **SEARCHING VIDEOS IN: {coaching_url}**")
        print("=" * 60)
        
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
            url = f"{coaching_url.rstrip('/')}{endpoint}"
            try:
                print(f"🔍 Searching videos: {endpoint}")
                response = requests.get(url, headers=self.api_headers, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ Found video data")
                    
                    # Save video response
                    coaching_name = coaching_url.split('//')[1].split('.')[0] if '//' in coaching_url else 'unknown'
                    filename = f"{self.download_folder}/html/{coaching_name}_videos_{endpoint.replace('/', '_')}.html"
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

    def download_files(self, files, file_type, coaching_name):
        """Download files (PDFs or videos)"""
        print(f"\n📥 **DOWNLOADING {file_type.upper()}S FOR {coaching_name}**")
        print("=" * 60)
        
        downloaded_count = 0
        
        for i, file_info in enumerate(files, 1):
            try:
                url = file_info['url']
                filename = file_info['filename']
                
                print(f"📥 Downloading {i}/{len(files)}: {filename}")
                
                response = requests.get(url, headers=self.headers, timeout=30, stream=True)
                
                if response.status_code == 200:
                    # Save file
                    file_path = f"{self.download_folder}/{file_type}s/{coaching_name}_{filename}"
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

    def analyze_coaching_institute(self, coaching_url):
        """Analyze a specific coaching institute"""
        print(f"🚀 **ANALYZING COACHING INSTITUTE: {coaching_url}**")
        print("=" * 60)
        print(f"📅 Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Extract coaching name from URL
        coaching_name = coaching_url.split('//')[1].split('.')[0] if '//' in coaching_url else 'unknown'
        
        # Test connectivity
        main_response = self.test_coaching_api(coaching_url)
        
        # Discover endpoints
        working_endpoints = self.discover_coaching_endpoints(coaching_url)
        
        # Search for courses
        courses = self.search_coaching_courses(coaching_url)
        
        # Search for PDFs
        pdfs = self.search_coaching_pdfs(coaching_url)
        
        # Search for videos
        videos = self.search_coaching_videos(coaching_url)
        
        # Download PDFs if found
        if pdfs:
            downloaded_pdfs = self.download_files(pdfs, 'pdf', coaching_name)
        else:
            downloaded_pdfs = 0
        
        # Download videos if found
        if videos:
            downloaded_videos = self.download_files(videos, 'video', coaching_name)
        else:
            downloaded_videos = 0
        
        # Summary
        print(f"\n📊 **ANALYSIS SUMMARY FOR {coaching_name.upper()}:**")
        print("=" * 50)
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
        
        return {
            'coaching_name': coaching_name,
            'coaching_url': coaching_url,
            'connectivity': 'Working' if main_response else 'Failed',
            'working_endpoints': len(working_endpoints),
            'courses_found': len(courses),
            'pdfs_found': len(pdfs),
            'videos_found': len(videos),
            'pdfs_downloaded': downloaded_pdfs,
            'videos_downloaded': downloaded_videos
        }

def main():
    scraper = InteractiveCoachingScraper()
    
    while True:
        # Get coaching URL from user
        coaching_url = scraper.get_coaching_url()
        
        # Analyze the coaching institute
        result = scraper.analyze_coaching_institute(coaching_url)
        
        # Ask if user wants to test another coaching institute
        print(f"\n💡 **ANALYSIS COMPLETE!**")
        print("=" * 40)
        print(f"🏫 Coaching: {result['coaching_name']}")
        print(f"🔗 URL: {result['coaching_url']}")
        print(f"📊 Status: {result['connectivity']}")
        print(f"📊 Working APIs: {result['working_endpoints']}")
        print(f"📊 Courses: {result['courses_found']}")
        print(f"📊 PDFs: {result['pdfs_found']} (Downloaded: {result['pdfs_downloaded']})")
        print(f"📊 Videos: {result['videos_found']} (Downloaded: {result['videos_downloaded']})")
        
        # Ask if user wants to continue
        continue_testing = input("\n🔍 Test another coaching institute? (y/n): ").strip().lower()
        if continue_testing not in ['y', 'yes', '1']:
            break
    
    print("\n🎉 **THANK YOU FOR USING APPEX COACHING SCRAPER!**")
    print("=" * 60)

if __name__ == "__main__":
    main()