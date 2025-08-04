#!/usr/bin/env python3
"""
Targeted Appex Scraper - Focus on working endpoints
"""

import requests
import re
import json
import os
import time
from urllib.parse import urljoin, urlparse

class AppexTargetedScraper:
    def __init__(self):
        self.download_folder = "appex_targeted_pdfs"
        
        # Create download folder
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
            print(f"📁 Created download folder: {self.download_folder}")
        
        # Working Appex endpoints we found
        self.working_endpoints = {
            'main': 'https://appex.in',
            'api': 'https://api.appex.in',
            'mobile': 'https://mobile.appex.in',
            'app': 'https://app.appex.in',
            'admin': 'https://admin.appex.in'
        }
        
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

    def explore_main_site(self):
        """Explore the main Appex site"""
        print("🔍 **EXPLORING MAIN APPEX SITE**")
        print("=" * 50)
        
        try:
            print(f"🌐 Exploring: {self.working_endpoints['main']}")
            response = requests.get(self.working_endpoints['main'], headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                print("✅ Main site accessible")
                
                # Save main page
                with open("appex_main.html", "w", encoding="utf-8") as f:
                    f.write(response.text)
                print("💾 Saved main page to: appex_main.html")
                
                # Look for links and structure
                links = re.findall(r'href=["\']([^"\']+)["\']', response.text)
                unique_links = list(set(links))
                
                print(f"📊 Found {len(unique_links)} links on main page")
                
                # Look for interesting links
                interesting_links = []
                for link in unique_links:
                    if any(keyword in link.lower() for keyword in ['course', 'api', 'login', 'register', 'dashboard']):
                        interesting_links.append(link)
                
                print(f"📊 Found {len(interesting_links)} interesting links:")
                for link in interesting_links[:10]:
                    print(f"   • {link}")
                
                return response.text
            else:
                print(f"❌ Main site failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error exploring main site: {e}")
            return None

    def test_api_endpoints(self):
        """Test specific API endpoints"""
        print("\n🔍 **TESTING API ENDPOINTS**")
        print("=" * 50)
        
        # Common API endpoints to test
        api_endpoints = [
            '/v1/courses',
            '/api/courses',
            '/v1/lessons',
            '/api/lessons',
            '/v1/documents',
            '/api/documents',
            '/v1/videos',
            '/api/videos',
            '/v1/tests',
            '/api/tests',
            '/v1/users',
            '/api/users'
        ]
        
        working_apis = []
        
        for endpoint in api_endpoints:
            url = f"{self.working_endpoints['api']}{endpoint}"
            try:
                print(f"🔍 Testing: {url}")
                response = requests.get(url, headers=self.api_headers, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ Working API: {endpoint}")
                    working_apis.append(endpoint)
                    
                    # Try to parse JSON
                    try:
                        data = response.json()
                        print(f"   📊 JSON response with {len(data)} keys")
                    except:
                        print(f"   📄 HTML response: {response.text[:200]}...")
                        
                elif response.status_code == 401:
                    print(f"🔐 Authentication required: {endpoint}")
                elif response.status_code == 403:
                    print(f"🚫 Access forbidden: {endpoint}")
                else:
                    print(f"❌ Failed: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
        
        return working_apis

    def search_for_courses(self):
        """Search for courses on Appex"""
        print("\n🔍 **SEARCHING FOR COURSES**")
        print("=" * 50)
        
        # Try different search approaches
        search_urls = [
            f"{self.working_endpoints['main']}/search?q=ras",
            f"{self.working_endpoints['main']}/search?q=upsc",
            f"{self.working_endpoints['main']}/search?q=prelims",
            f"{self.working_endpoints['main']}/courses",
            f"{self.working_endpoints['main']}/course",
            f"{self.working_endpoints['main']}/programs"
        ]
        
        found_courses = []
        
        for url in search_urls:
            try:
                print(f"🔍 Searching: {url}")
                response = requests.get(url, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ Found search results")
                    
                    # Extract course information
                    courses = self.extract_course_info(response.text)
                    found_courses.extend(courses)
                    
                    # Save search results
                    filename = f"appex_search_{len(found_courses)}.html"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(response.text)
                    print(f"💾 Saved search results to: {filename}")
                    
                else:
                    print(f"❌ Search failed: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error searching: {e}")
        
        return found_courses

    def extract_course_info(self, html_content):
        """Extract course information from HTML"""
        courses = []
        
        try:
            # Look for course patterns
            course_patterns = [
                r'<div[^>]*class="[^"]*course[^"]*"[^>]*>([^<]*)</div>',
                r'<a[^>]*href="[^"]*course[^"]*"[^>]*>([^<]*)</a>',
                r'"title":"([^"]*)"',
                r'"name":"([^"]*)"',
                r'"courseName":"([^"]*)"',
                r'<h[1-6][^>]*>([^<]*course[^<]*)</h[1-6]>',
                r'<span[^>]*>([^<]*course[^<]*)</span>'
            ]
            
            for pattern in course_patterns:
                matches = re.findall(pattern, html_content, re.IGNORECASE)
                for match in matches:
                    if len(match.strip()) > 5:  # Filter out very short matches
                        courses.append({
                            'name': match.strip(),
                            'source': 'html_extraction'
                        })
            
            print(f"✅ Extracted {len(courses)} potential courses")
            
        except Exception as e:
            print(f"❌ Error extracting courses: {e}")
        
        return courses

    def test_mobile_endpoints(self):
        """Test mobile app endpoints"""
        print("\n🔍 **TESTING MOBILE ENDPOINTS**")
        print("=" * 50)
        
        mobile_endpoints = [
            '/api/v1/courses',
            '/api/v1/lessons',
            '/api/v1/documents',
            '/api/v1/videos',
            '/api/v1/tests'
        ]
        
        working_mobile_apis = []
        
        for endpoint in mobile_endpoints:
            url = f"{self.working_endpoints['mobile']}{endpoint}"
            try:
                print(f"🔍 Testing mobile: {url}")
                response = requests.get(url, headers=self.api_headers, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ Working mobile API: {endpoint}")
                    working_mobile_apis.append(endpoint)
                else:
                    print(f"❌ Mobile API failed: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Mobile API error: {e}")
        
        return working_mobile_apis

    def explore_admin_interface(self):
        """Explore admin interface"""
        print("\n🔍 **EXPLORING ADMIN INTERFACE**")
        print("=" * 50)
        
        try:
            print(f"🌐 Exploring: {self.working_endpoints['admin']}")
            response = requests.get(self.working_endpoints['admin'], headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                print("✅ Admin interface accessible")
                
                # Save admin page
                with open("appex_admin.html", "w", encoding="utf-8") as f:
                    f.write(response.text)
                print("💾 Saved admin page to: appex_admin.html")
                
                # Look for login forms or API endpoints
                login_forms = re.findall(r'<form[^>]*>', response.text)
                api_links = re.findall(r'href=["\']([^"\']*api[^"\']*)["\']', response.text)
                
                print(f"📊 Found {len(login_forms)} forms")
                print(f"📊 Found {len(api_links)} API links")
                
                return response.text
            else:
                print(f"❌ Admin interface failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error exploring admin interface: {e}")
            return None

    def create_appex_scraper(self):
        """Create a comprehensive Appex scraper"""
        print("\n💡 **CREATING APPEX SCRAPER**")
        print("=" * 50)
        
        # Based on our findings, create a scraper
        scraper_code = '''
class AppexComprehensiveScraper:
    def __init__(self):
        self.base_url = "https://appex.in"
        self.api_url = "https://api.appex.in"
        self.mobile_url = "https://mobile.appex.in"
        
    def authenticate(self):
        """Authenticate with Appex"""
        # Implementation needed
        pass
        
    def get_courses(self):
        """Get courses from Appex"""
        # Implementation needed
        pass
        
    def get_course_content(self, course_id):
        """Get content for a specific course"""
        # Implementation needed
        pass
        
    def download_pdfs(self, course_id):
        """Download PDFs for a course"""
        # Implementation needed
        pass
'''
        
        print("📝 **SCRAPER TEMPLATE CREATED**")
        print("Next steps:")
        print("1. Implement authentication")
        print("2. Add course discovery")
        print("3. Add content extraction")
        print("4. Add PDF download functionality")
        
        return scraper_code

    def run_comprehensive_analysis(self):
        """Run comprehensive Appex analysis"""
        print("🚀 **COMPREHENSIVE APPEX ANALYSIS**")
        print("=" * 60)
        
        # Explore main site
        main_content = self.explore_main_site()
        
        # Test API endpoints
        working_apis = self.test_api_endpoints()
        
        # Search for courses
        courses = self.search_for_courses()
        
        # Test mobile endpoints
        mobile_apis = self.test_mobile_endpoints()
        
        # Explore admin interface
        admin_content = self.explore_admin_interface()
        
        # Create scraper
        scraper_template = self.create_appex_scraper()
        
        # Summary
        print(f"\n📊 **ANALYSIS SUMMARY:**")
        print("=" * 40)
        print(f"✅ Main site: {'Working' if main_content else 'Failed'}")
        print(f"✅ Working APIs: {len(working_apis)}")
        print(f"✅ Courses found: {len(courses)}")
        print(f"✅ Mobile APIs: {len(mobile_apis)}")
        print(f"✅ Admin interface: {'Working' if admin_content else 'Failed'}")
        
        if courses:
            print(f"\n📚 **COURSES FOUND:**")
            for i, course in enumerate(courses[:10], 1):
                print(f"   {i}. {course['name']}")
        
        print(f"\n💡 **NEXT STEPS:**")
        print("   1. Analyze saved HTML files for structure")
        print("   2. Implement authentication mechanism")
        print("   3. Create specific API calls")
        print("   4. Build PDF download functionality")
        print("   5. Test with real course data")

def main():
    scraper = AppexTargetedScraper()
    scraper.run_comprehensive_analysis()

if __name__ == "__main__":
    main()