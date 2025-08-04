#!/usr/bin/env python3
"""
Advanced Online Agriculture API Scraper
Target: https://onlineagricultureapi.classx.co.in
"""

import requests
import re
import json
import os
import time
from urllib.parse import urljoin, urlparse
from datetime import datetime

class AdvancedAgricultureScraper:
    def __init__(self):
        self.base_url = "https://onlineagricultureapi.classx.co.in"
        self.download_folder = "advanced_agriculture_downloads"
        
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

    def test_different_approaches(self):
        """Test different approaches to access the API"""
        print("🔍 **TESTING DIFFERENT APPROACHES**")
        print("=" * 50)
        
        # Test different HTTP methods
        methods = ['GET', 'POST', 'PUT', 'DELETE']
        for method in methods:
            try:
                print(f"🔍 Testing {method} request")
                if method == 'GET':
                    response = requests.get(self.base_url, headers=self.headers, timeout=10)
                elif method == 'POST':
                    response = requests.post(self.base_url, headers=self.headers, timeout=10)
                elif method == 'PUT':
                    response = requests.put(self.base_url, headers=self.headers, timeout=10)
                elif method == 'DELETE':
                    response = requests.delete(self.base_url, headers=self.headers, timeout=10)
                
                print(f"   Status: {response.status_code}")
                print(f"   Response: {response.text[:100]}...")
                
            except Exception as e:
                print(f"   Error: {e}")

    def test_with_parameters(self):
        """Test API with different parameters"""
        print("\n🔍 **TESTING WITH PARAMETERS**")
        print("=" * 50)
        
        # Test with different query parameters
        test_params = [
            {'action': 'get_courses'},
            {'method': 'courses'},
            {'api': 'courses'},
            {'type': 'courses'},
            {'data': 'courses'},
            {'action': 'get_pdfs'},
            {'method': 'pdfs'},
            {'api': 'pdfs'},
            {'type': 'pdfs'},
            {'data': 'pdfs'},
            {'action': 'get_videos'},
            {'method': 'videos'},
            {'api': 'videos'},
            {'type': 'videos'},
            {'data': 'videos'}
        ]
        
        for params in test_params:
            try:
                print(f"🔍 Testing with params: {params}")
                response = requests.get(self.base_url, params=params, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    print(f"   ✅ Success with params: {params}")
                    print(f"   📄 Response: {response.text[:200]}...")
                    
                    # Save response
                    filename = f"{self.download_folder}/html/params_{'_'.join([f'{k}_{v}' for k, v in params.items()])}.html"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(response.text)
                    print(f"   💾 Saved to: {filename}")
                    
                else:
                    print(f"   ❌ Failed: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")

    def test_with_json_payload(self):
        """Test API with JSON payloads"""
        print("\n🔍 **TESTING WITH JSON PAYLOADS**")
        print("=" * 50)
        
        # Test with different JSON payloads
        test_payloads = [
            {'action': 'get_courses'},
            {'method': 'courses'},
            {'api': 'courses'},
            {'type': 'courses'},
            {'data': 'courses'},
            {'action': 'get_pdfs'},
            {'method': 'pdfs'},
            {'api': 'pdfs'},
            {'type': 'pdfs'},
            {'data': 'pdfs'},
            {'action': 'get_videos'},
            {'method': 'videos'},
            {'api': 'videos'},
            {'type': 'videos'},
            {'data': 'videos'},
            {'request': 'courses'},
            {'request': 'pdfs'},
            {'request': 'videos'},
            {'query': 'courses'},
            {'query': 'pdfs'},
            {'query': 'videos'}
        ]
        
        for payload in test_payloads:
            try:
                print(f"🔍 Testing with payload: {payload}")
                response = requests.post(self.base_url, json=payload, headers=self.api_headers, timeout=10)
                
                if response.status_code == 200:
                    print(f"   ✅ Success with payload: {payload}")
                    print(f"   📄 Response: {response.text[:200]}...")
                    
                    # Save response
                    filename = f"{self.download_folder}/html/payload_{'_'.join([f'{k}_{v}' for k, v in payload.items()])}.html"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(response.text)
                    print(f"   💾 Saved to: {filename}")
                    
                else:
                    print(f"   ❌ Failed: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")

    def test_with_authentication_headers(self):
        """Test with different authentication headers"""
        print("\n🔍 **TESTING WITH AUTH HEADERS**")
        print("=" * 50)
        
        # Test with different auth headers
        auth_headers = [
            {'Authorization': 'Bearer test'},
            {'X-API-Key': 'test'},
            {'X-Auth-Token': 'test'},
            {'Authorization': 'Basic dGVzdDp0ZXN0'},
            {'X-Requested-With': 'XMLHttpRequest'},
            {'Content-Type': 'application/x-www-form-urlencoded'},
            {'Accept': 'application/xml'},
            {'Accept': 'text/plain'}
        ]
        
        for auth_header in auth_headers:
            try:
                headers = self.headers.copy()
                headers.update(auth_header)
                
                print(f"🔍 Testing with auth header: {list(auth_header.keys())[0]}")
                response = requests.get(self.base_url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    print(f"   ✅ Success with auth header")
                    print(f"   📄 Response: {response.text[:200]}...")
                    
                    # Save response
                    filename = f"{self.download_folder}/html/auth_{list(auth_header.keys())[0].lower().replace('-', '_')}.html"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(response.text)
                    print(f"   💾 Saved to: {filename}")
                    
                else:
                    print(f"   ❌ Failed: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")

    def test_subdomain_variations(self):
        """Test different subdomain variations"""
        print("\n🔍 **TESTING SUBDOMAIN VARIATIONS**")
        print("=" * 50)
        
        # Test different subdomain patterns
        subdomains = [
            "api.onlineagricultureapi.classx.co.in",
            "www.onlineagricultureapi.classx.co.in",
            "mobile.onlineagricultureapi.classx.co.in",
            "app.onlineagricultureapi.classx.co.in",
            "admin.onlineagricultureapi.classx.co.in",
            "web.onlineagricultureapi.classx.co.in"
        ]
        
        for subdomain in subdomains:
            try:
                url = f"https://{subdomain}"
                print(f"🔍 Testing subdomain: {subdomain}")
                response = requests.get(url, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    print(f"   ✅ Success: {subdomain}")
                    print(f"   📄 Response: {response.text[:200]}...")
                    
                    # Save response
                    filename = f"{self.download_folder}/html/subdomain_{subdomain.split('.')[0]}.html"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(response.text)
                    print(f"   💾 Saved to: {filename}")
                    
                else:
                    print(f"   ❌ Failed: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")

    def test_path_variations(self):
        """Test different path variations"""
        print("\n🔍 **TESTING PATH VARIATIONS**")
        print("=" * 50)
        
        # Test different path patterns
        paths = [
            "/index.php",
            "/api.php",
            "/data.php",
            "/courses.php",
            "/content.php",
            "/materials.php",
            "/videos.php",
            "/pdfs.php",
            "/documents.php",
            "/test.php",
            "/info.php",
            "/status.php",
            "/health.php",
            "/ping.php"
        ]
        
        for path in paths:
            try:
                url = f"{self.base_url}{path}"
                print(f"🔍 Testing path: {path}")
                response = requests.get(url, headers=self.headers, timeout=10)
                
                if response.status_code == 200:
                    print(f"   ✅ Success: {path}")
                    print(f"   📄 Response: {response.text[:200]}...")
                    
                    # Save response
                    filename = f"{self.download_folder}/html/path_{path.replace('/', '_')}.html"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(response.text)
                    print(f"   💾 Saved to: {filename}")
                    
                else:
                    print(f"   ❌ Failed: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")

    def analyze_saved_files(self):
        """Analyze all saved files for content"""
        print("\n🔍 **ANALYZING SAVED FILES**")
        print("=" * 50)
        
        html_folder = f"{self.download_folder}/html"
        if os.path.exists(html_folder):
            files = os.listdir(html_folder)
            
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(html_folder, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        print(f"📄 Analyzing: {file}")
                        print(f"   📏 Length: {len(content)} characters")
                        
                        # Look for interesting content
                        if 'course' in content.lower():
                            print(f"   🎓 Found course-related content")
                        if 'pdf' in content.lower():
                            print(f"   📄 Found PDF-related content")
                        if 'video' in content.lower():
                            print(f"   🎥 Found video-related content")
                        if 'json' in content.lower():
                            print(f"   📊 Found JSON content")
                        if 'error' in content.lower():
                            print(f"   ❌ Found error content")
                        
                        # Show first 200 characters
                        print(f"   📝 Preview: {content[:200]}...")
                        
                    except Exception as e:
                        print(f"   ❌ Error reading {file}: {e}")

    def run_advanced_analysis(self):
        """Run advanced analysis"""
        print("🚀 **ADVANCED ONLINE AGRICULTURE API ANALYSIS**")
        print("=" * 60)
        print(f"🎯 Target: {self.base_url}")
        print(f"📅 Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Test different approaches
        self.test_different_approaches()
        
        # Test with parameters
        self.test_with_parameters()
        
        # Test with JSON payloads
        self.test_with_json_payload()
        
        # Test with auth headers
        self.test_with_authentication_headers()
        
        # Test subdomain variations
        self.test_subdomain_variations()
        
        # Test path variations
        self.test_path_variations()
        
        # Analyze saved files
        self.analyze_saved_files()
        
        print(f"\n📊 **ADVANCED ANALYSIS SUMMARY:**")
        print("=" * 40)
        print("✅ Multiple approaches tested")
        print("✅ Various parameters tested")
        print("✅ JSON payloads tested")
        print("✅ Authentication headers tested")
        print("✅ Subdomain variations tested")
        print("✅ Path variations tested")
        print("✅ All saved files analyzed")
        
        print(f"\n💡 **NEXT STEPS:**")
        print("   1. Review all saved HTML files")
        print("   2. Check for any working endpoints")
        print("   3. Analyze response patterns")
        print("   4. Try manual API exploration")

def main():
    scraper = AdvancedAgricultureScraper()
    scraper.run_advanced_analysis()

if __name__ == "__main__":
    main()