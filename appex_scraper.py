#!/usr/bin/env python3
"""
Appex Platform Scraper
"""

import requests
import re
import json
import os
import time
from urllib.parse import urljoin, urlparse

class AppexScraper:
    def __init__(self):
        self.download_folder = "appex_downloaded_pdfs"
        
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
        
        # Appex API headers
        self.api_headers = {
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        }

    def search_appex_organizations(self):
        """Search for Appex organizations"""
        print("🔍 **SEARCHING APPEX ORGANIZATIONS**")
        print("=" * 50)
        
        # Common Appex organization patterns
        org_patterns = [
            "appex.co",
            "appex.in", 
            "appexapp.com",
            "appexapp.in"
        ]
        
        # Try to find Appex organizations
        found_orgs = []
        
        # Search for RAS/UPSC related organizations
        search_keywords = [
            "ras",
            "upsc", 
            "prelims",
            "civil services",
            "government exam"
        ]
        
        print("🔍 Searching for Appex organizations...")
        
        # Try some common Appex URLs
        test_urls = [
            "https://appex.co",
            "https://appex.in",
            "https://appexapp.com",
            "https://appexapp.in"
        ]
        
        for url in test_urls:
            try:
                print(f"🌐 Testing: {url}")
                response = requests.get(url, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ Found working Appex URL: {url}")
                    found_orgs.append({
                        'url': url,
                        'status': 'active',
                        'title': response.text[:100] if response.text else 'Unknown'
                    })
                else:
                    print(f"❌ Failed: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
        
        return found_orgs

    def search_ras_courses_on_appex(self):
        """Search for RAS courses on Appex"""
        print("\n🔍 **SEARCHING RAS COURSES ON APPEX**")
        print("=" * 50)
        
        # Try to find RAS courses on Appex
        search_urls = [
            "https://appex.co/search?q=ras",
            "https://appex.in/search?q=ras",
            "https://appexapp.com/search?q=ras",
            "https://appexapp.in/search?q=ras"
        ]
        
        found_courses = []
        
        for url in search_urls:
            try:
                print(f"🔍 Searching: {url}")
                response = requests.get(url, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ Found search results")
                    
                    # Extract course information
                    courses = self.extract_courses_from_page(response.text)
                    found_courses.extend(courses)
                    
                else:
                    print(f"❌ Search failed: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error searching: {e}")
        
        return found_courses

    def extract_courses_from_page(self, html_content):
        """Extract course information from page"""
        courses = []
        
        try:
            # Look for course patterns
            course_patterns = [
                r'<div[^>]*class="[^"]*course[^"]*"[^>]*>([^<]*)</div>',
                r'<a[^>]*href="[^"]*course[^"]*"[^>]*>([^<]*)</a>',
                r'"title":"([^"]*ras[^"]*)"',
                r'"name":"([^"]*ras[^"]*)"',
                r'"courseName":"([^"]*)"'
            ]
            
            for pattern in course_patterns:
                matches = re.findall(pattern, html_content, re.IGNORECASE)
                for match in matches:
                    if 'ras' in match.lower() or 'prelims' in match.lower():
                        courses.append({
                            'name': match.strip(),
                            'source': 'page_extraction'
                        })
            
            print(f"✅ Extracted {len(courses)} courses from page")
            
        except Exception as e:
            print(f"❌ Error extracting courses: {e}")
        
        return courses

    def test_appex_api_endpoints(self):
        """Test Appex API endpoints"""
        print("\n🔍 **TESTING APPEX API ENDPOINTS**")
        print("=" * 50)
        
        # Common Appex API endpoints
        api_endpoints = [
            "https://api.appex.co/v1/courses",
            "https://api.appex.in/v1/courses", 
            "https://api.appexapp.com/v1/courses",
            "https://api.appexapp.in/v1/courses",
            "https://appex.co/api/courses",
            "https://appex.in/api/courses",
            "https://appexapp.com/api/courses",
            "https://appexapp.in/api/courses"
        ]
        
        working_endpoints = []
        
        for endpoint in api_endpoints:
            try:
                print(f"🔍 Testing: {endpoint}")
                response = requests.get(endpoint, headers=self.api_headers, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ Working endpoint: {endpoint}")
                    working_endpoints.append(endpoint)
                    
                    # Try to parse JSON response
                    try:
                        data = response.json()
                        print(f"   📊 Response keys: {list(data.keys())}")
                    except:
                        print(f"   📄 Response: {response.text[:200]}...")
                        
                else:
                    print(f"❌ Failed: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
        
        return working_endpoints

    def search_appex_mobile_app(self):
        """Search for Appex mobile app patterns"""
        print("\n🔍 **SEARCHING APPEX MOBILE APP**")
        print("=" * 50)
        
        # Mobile app API patterns
        mobile_patterns = [
            "https://mobile.appex.co",
            "https://mobile.appex.in",
            "https://app.appex.co",
            "https://app.appex.in"
        ]
        
        mobile_endpoints = []
        
        for pattern in mobile_patterns:
            try:
                print(f"🔍 Testing mobile: {pattern}")
                response = requests.get(pattern, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ Mobile endpoint working: {pattern}")
                    mobile_endpoints.append(pattern)
                else:
                    print(f"❌ Mobile endpoint failed: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Mobile error: {e}")
        
        return mobile_endpoints

    def search_appex_web_interface(self):
        """Search for Appex web interface"""
        print("\n🔍 **SEARCHING APPEX WEB INTERFACE**")
        print("=" * 50)
        
        # Web interface URLs
        web_urls = [
            "https://web.appex.co",
            "https://web.appex.in",
            "https://dashboard.appex.co",
            "https://dashboard.appex.in",
            "https://admin.appex.co",
            "https://admin.appex.in"
        ]
        
        working_web_urls = []
        
        for url in web_urls:
            try:
                print(f"🔍 Testing web: {url}")
                response = requests.get(url, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ Web interface working: {url}")
                    working_web_urls.append(url)
                    
                    # Save page content for analysis
                    filename = f"appex_web_{len(working_web_urls)}.html"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(response.text)
                    print(f"   💾 Saved to: {filename}")
                    
                else:
                    print(f"❌ Web interface failed: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Web error: {e}")
        
        return working_web_urls

    def analyze_appex_structure(self):
        """Analyze Appex platform structure"""
        print("\n🔍 **ANALYZING APPEX STRUCTURE**")
        print("=" * 50)
        
        # Try to understand Appex platform structure
        analysis_results = {
            'platform_type': 'Educational/Coaching',
            'common_features': [
                'Course Management',
                'Video Streaming',
                'PDF Downloads',
                'Live Classes',
                'Test Series',
                'Study Material'
            ],
            'possible_endpoints': [
                '/api/courses',
                '/api/lessons',
                '/api/documents',
                '/api/videos',
                '/api/tests',
                '/api/users'
            ],
            'authentication_methods': [
                'JWT Tokens',
                'Session Cookies',
                'API Keys',
                'OAuth'
            ]
        }
        
        print("📊 **APPEX PLATFORM ANALYSIS:**")
        print(f"   Platform Type: {analysis_results['platform_type']}")
        print(f"   Common Features: {', '.join(analysis_results['common_features'])}")
        print(f"   Possible Endpoints: {', '.join(analysis_results['possible_endpoints'])}")
        print(f"   Auth Methods: {', '.join(analysis_results['authentication_methods'])}")
        
        return analysis_results

    def create_appex_scraping_strategy(self):
        """Create strategy for Appex scraping"""
        print("\n💡 **APPEX SCRAPING STRATEGY**")
        print("=" * 50)
        
        strategy = {
            'phase_1': {
                'name': 'Platform Discovery',
                'steps': [
                    'Find working Appex URLs',
                    'Identify API endpoints',
                    'Understand authentication',
                    'Map course structure'
                ]
            },
            'phase_2': {
                'name': 'Course Discovery',
                'steps': [
                    'Search for RAS courses',
                    'Extract course IDs',
                    'Get course metadata',
                    'Find content structure'
                ]
            },
            'phase_3': {
                'name': 'Content Extraction',
                'steps': [
                    'Get PDF URLs',
                    'Download documents',
                    'Extract videos',
                    'Get study material'
                ]
            }
        }
        
        print("📋 **SCRAPING STRATEGY:**")
        for phase_name, phase_data in strategy.items():
            print(f"\n📊 {phase_data['name']}:")
            for step in phase_data['steps']:
                print(f"   • {step}")
        
        return strategy

    def run_appex_analysis(self):
        """Main Appex analysis function"""
        print("🚀 **APPEX PLATFORM ANALYSIS**")
        print("=" * 60)
        
        # Phase 1: Platform Discovery
        print("\n🔍 **PHASE 1: PLATFORM DISCOVERY**")
        print("=" * 40)
        
        # Search for organizations
        orgs = self.search_appex_organizations()
        print(f"📊 Found {len(orgs)} working Appex organizations")
        
        # Test API endpoints
        api_endpoints = self.test_appex_api_endpoints()
        print(f"📊 Found {len(api_endpoints)} working API endpoints")
        
        # Search mobile app
        mobile_endpoints = self.search_appex_mobile_app()
        print(f"📊 Found {len(mobile_endpoints)} mobile endpoints")
        
        # Search web interface
        web_urls = self.search_appex_web_interface()
        print(f"📊 Found {len(web_urls)} web interfaces")
        
        # Phase 2: Course Discovery
        print("\n🔍 **PHASE 2: COURSE DISCOVERY**")
        print("=" * 40)
        
        # Search for RAS courses
        courses = self.search_ras_courses_on_appex()
        print(f"📊 Found {len(courses)} RAS courses")
        
        # Phase 3: Analysis
        print("\n🔍 **PHASE 3: PLATFORM ANALYSIS**")
        print("=" * 40)
        
        # Analyze structure
        structure = self.analyze_appex_structure()
        
        # Create strategy
        strategy = self.create_appex_scraping_strategy()
        
        # Summary
        print(f"\n📊 **ANALYSIS SUMMARY:**")
        print("=" * 40)
        print(f"✅ Organizations found: {len(orgs)}")
        print(f"✅ API endpoints found: {len(api_endpoints)}")
        print(f"✅ Mobile endpoints found: {len(mobile_endpoints)}")
        print(f"✅ Web interfaces found: {len(web_urls)}")
        print(f"✅ RAS courses found: {len(courses)}")
        
        if courses:
            print(f"\n📚 **RAS COURSES FOUND:**")
            for i, course in enumerate(courses, 1):
                print(f"   {i}. {course['name']}")
        
        print(f"\n💡 **NEXT STEPS:**")
        print("   1. Analyze saved HTML files")
        print("   2. Test API endpoints with authentication")
        print("   3. Create specific scraper for working endpoints")
        print("   4. Implement PDF download functionality")

def main():
    scraper = AppexScraper()
    scraper.run_appex_analysis()

if __name__ == "__main__":
    main()