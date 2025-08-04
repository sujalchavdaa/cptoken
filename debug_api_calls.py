#!/usr/bin/env python3
"""
Debug API calls to understand why PDFs aren't downloading
"""

import requests
import json
import asyncio
import aiohttp

class APIDebugger:
    def __init__(self):
        self.session_token = "eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJzb3VyY2UiOjUwLCJzb3VyY2VfYXBwIjoiY2xhc3NwbHVzIiwic2Vzc2lvbl9pZCI6IjhkZTBmZTcyLTQ1NjEtNGNiYy04NjZhLTYzMjUyMTkwMTg2MyIsInZpc2l0b3JfaWQiOiJjMWFhM2IwNS03ZjlhLTRlZjktOTI1My0zNzRhM2RjMmYxZWYiLCJjcmVhdGVkX2F0IjoxNzU0MjI4MjIwNTQzLCJpYXQiOjE3NTQyMjgyMjAsImV4cCI6MTc1NTUyNDIyMH0.eKG1pqT0Ws6Dbb7LUzpHRjevH4Wi33Si-H2zLyEyuXCdhTc5kcK8cNnjm4XPSlaT"
        
        # Different header configurations to test
        self.headers_configs = {
            "web_headers": {
                'accept': 'application/json',
                'authorization': f'Bearer {self.session_token}',
                'origin': 'https://web.classplusapp.com',
                'referer': 'https://web.classplusapp.com/',
                'region': 'IN',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
                'api-version': '52'
            },
            "mobile_headers": {
                'accept-encoding': 'gzip',
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
            },
            "simple_headers": {
                'accept': 'application/json',
                'authorization': f'Bearer {self.session_token}',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        }

    async def test_api_endpoint(self, url, headers, name):
        """Test an API endpoint"""
        print(f"\n🔍 Testing: {name}")
        print(f"   URL: {url}")
        print(f"   Headers: {list(headers.keys())}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    print(f"   Status: {response.status}")
                    print(f"   Response Headers: {dict(response.headers)}")
                    
                    if response.status == 200:
                        try:
                            data = await response.json()
                            print(f"   ✅ Success! Response keys: {list(data.keys())}")
                            if 'data' in data:
                                print(f"   Data keys: {list(data['data'].keys())}")
                        except:
                            text = await response.text()
                            print(f"   Response (first 200 chars): {text[:200]}...")
                    else:
                        try:
                            error_data = await response.json()
                            print(f"   ❌ Error response: {error_data}")
                        except:
                            text = await response.text()
                            print(f"   ❌ Error text: {text[:200]}...")
                            
        except Exception as e:
            print(f"   ❌ Exception: {e}")

    async def test_different_endpoints(self):
        """Test different API endpoints"""
        print("🚀 **API DEBUG TESTING**")
        print("=" * 60)
        
        content_id = "64802601"  # Test with one content ID
        
        # Different API endpoints to test
        endpoints = [
            {
                "name": "Document Download API",
                "url": f"https://api.classplusapp.com/v2/course/preview/document/download/{content_id}"
            },
            {
                "name": "Content Details API",
                "url": f"https://api.classplusapp.com/v2/course/preview/content/details/{content_id}"
            },
            {
                "name": "Document Info API",
                "url": f"https://api.classplusapp.com/v2/course/preview/document/info/{content_id}"
            },
            {
                "name": "Content Download API",
                "url": f"https://api.classplusapp.com/v2/course/preview/content/download/{content_id}"
            },
            {
                "name": "File Download API",
                "url": f"https://api.classplusapp.com/v2/course/preview/file/download/{content_id}"
            }
        ]
        
        # Test each endpoint with different headers
        for endpoint in endpoints:
            for header_name, headers in self.headers_configs.items():
                await self.test_api_endpoint(endpoint["url"], headers, f"{endpoint['name']} ({header_name})")

    async def test_authentication(self):
        """Test if our token is working"""
        print("\n🔐 **AUTHENTICATION TEST**")
        print("=" * 40)
        
        # Test user profile endpoint
        profile_url = "https://api.classplusapp.com/v2/users/profile"
        
        for header_name, headers in self.headers_configs.items():
            await self.test_api_endpoint(profile_url, headers, f"User Profile ({header_name})")

    async def test_course_access(self):
        """Test course access"""
        print("\n📚 **COURSE ACCESS TEST**")
        print("=" * 40)
        
        # Test with the batch token we extracted
        batch_token = "eyJjb3Vyc2VJZCI6IjY5NzE5NzIiLCJ0dXRvcklkIjpudWxsLCJvcmdJZCI6NzYzMzIwLCJjYXRlZ2orySWQiOm51bGx9"
        
        course_url = f"https://api.classplusapp.com/v2/course/preview/content/list/{batch_token}"
        
        for header_name, headers in self.headers_configs.items():
            await self.test_api_endpoint(course_url, headers, f"Course Content ({header_name})")

async def main():
    debugger = APIDebugger()
    
    # Test authentication first
    await debugger.test_authentication()
    
    # Test course access
    await debugger.test_course_access()
    
    # Test different download endpoints
    await debugger.test_different_endpoints()

if __name__ == "__main__":
    asyncio.run(main())