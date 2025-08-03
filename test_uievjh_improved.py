#!/usr/bin/env python3
"""
Test Uievjh with improved bot
"""

import requests
import json
import re
import asyncio
import aiohttp
import base64

class ImprovedClassplusBot:
    def __init__(self):
        self.classplus_apis = {
            "get_org_id": "https://api.classplusapp.com/v2/orgs/getOrgId",
            "send_otp": "https://api.classplusapp.com/v2/users/sendOtp", 
            "verify_otp": "https://api.classplusapp.com/v2/users/verify",
            "get_access_token": "https://api.classplusapp.com/v2/users/get-access-token",
            "course_preview": "https://api.classplusapp.com/v2/course/preview/similar/{token}",
            "course_content": "https://api.classplusapp.com/v2/course/preview/content/list/{Batch_Token}",
            "signed_url": "https://api.classplusapp.com/cams/uploader/video/jw-signed-url",
            "org_info": "https://api.classplusapp.com/v2/course/preview/org/info"
        }
        
        self.classplus_headers = {
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
        }
        
        self.hash_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://qsvfn.courses.store/?mainCategory=0&subCatList=[130504,62442]',
            'Sec-CH-UA': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'Sec-CH-UA-Mobile': '?0',
            'Sec-CH-UA-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        }

    def get_org_id(self, org_code):
        """Get organization ID from org code using extracted pattern"""
        url = self.classplus_apis["get_org_id"]
        payload = {"orgCode": org_code}
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "origin": "https://web.classplusapp.com",
            "referer": "https://web.classplusapp.com/",
            "user-agent": "Mozilla/5.0"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
            if response.status_code == 200:
                data = response.json()
                if "data" in data and "orgId" in data["data"]:
                    return data["data"]["orgId"]
                else:
                    print(f"   ❌ Invalid response structure")
                    return None
            else:
                print(f"   ❌ Failed with status {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None

    def send_otp(self, email, org_code, org_id):
        """Send OTP using extracted pattern"""
        url = self.classplus_apis["send_otp"]
        payload = {
            "email": email,
            "countryExt": "91",
            "orgId": org_id,
            "fingerprintId": "dummy",
            "orgCode": org_code
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "origin": "https://web.classplusapp.com",
            "referer": "https://web.classplusapp.com/",
            "region": "IN",
            "user-agent": "Mozilla/5.0",
            "api-version": "52"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
            if response.status_code == 201:
                data = response.json()
                if "data" in data and "sessionId" in data["data"]:
                    return data["data"]["sessionId"]
                else:
                    print(f"   ❌ Invalid response structure")
                    return None
            elif response.status_code == 403 and "limit exceeded" in response.text.lower():
                return "RATE_LIMIT_EXCEEDED"
            else:
                print(f"   ❌ Failed with status {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None

    async def get_hash_from_org_code(self, org_code):
        """Get hash from org code using extracted pattern"""
        url = f"https://{org_code}.courses.store"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.hash_headers) as response:
                    html_text = await response.text()
                    hash_match = re.search(r'"hash":"(.*?)"', html_text)
                    
                    if hash_match:
                        token = hash_match.group(1)
                        print(f"   ✅ Hash extracted: {token[:20]}...")
                        return token
                    else:
                        print(f"   ❌ Hash not found in HTML")
                        return None
                        
        except Exception as e:
            print(f"   ❌ Error extracting hash: {e}")
            return None

    async def get_courses_from_hash(self, token, org_code):
        """Get courses from hash using extracted pattern"""
        url = f"https://api.classplusapp.com/v2/course/preview/similar/{token}?limit=20"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.classplus_headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        courses = data.get('data', {}).get('coursesData', [])
                        return courses
                    else:
                        print(f"   ❌ Failed to get courses: {response.status}")
                        return []
                        
        except Exception as e:
            print(f"   ❌ Error getting courses: {e}")
            return []

    def test_real_org_code(self, org_code, email):
        """Test with real org code using extracted patterns"""
        print(f"🚀 **TESTING UIEVJH WITH IMPROVED BOT**")
        print("="*60)
        print(f"📝 Testing with:")
        print(f"   • Org Code: {org_code}")
        print(f"   • Email: {email}")
        print()
        
        # Step 1: Get org ID
        print("🔍 Step 1: Getting Organization ID...")
        org_id = self.get_org_id(org_code)
        if not org_id:
            print("❌ Invalid org code or org not found")
            return None, None
        
        print(f"✅ Org ID: {org_id}")
        
        # Step 2: Send OTP
        print("\n🔍 Step 2: Sending OTP...")
        session_id = self.send_otp(email, org_code, org_id)
        
        if session_id == "RATE_LIMIT_EXCEEDED":
            print("⚠️ Rate limit exceeded. Cannot test further.")
            print("💡 Try again after 6 hours.")
            return None, None
        elif not session_id:
            print("❌ Failed to send OTP")
            return None, None
        
        print(f"✅ Session ID: {session_id}")
        
        return org_id, session_id

    async def test_hash_extraction(self, org_code):
        """Test hash extraction from org code"""
        print(f"\n🔍 **TESTING HASH EXTRACTION:**")
        print(f"   • Org Code: {org_code}")
        
        token = await self.get_hash_from_org_code(org_code)
        if token:
            courses = await self.get_courses_from_hash(token, org_code)
            if courses:
                print(f"   ✅ Found {len(courses)} courses")
                for i, course in enumerate(courses[:3]):  # Show first 3
                    print(f"      {i+1}. {course.get('name', 'Unknown')} - ₹{course.get('finalPrice', 0)}")
            else:
                print(f"   ❌ No courses found")
        else:
            print(f"   ❌ Hash extraction failed")

def main():
    """Main function"""
    print("🚀 **UIEVJH IMPROVED BOT TEST**")
    print("="*60)
    print("🔍 Testing Uievjh with extracted patterns...")
    
    bot = ImprovedClassplusBot()
    
    # Test with Uievjh
    org_code = "Uievjh"
    email = "makey75125@hostbyt.com"
    
    # Test org code
    org_id, session_id = bot.test_real_org_code(org_code, email)
    
    if org_id and session_id:
        print(f"\n🎉 **SUCCESS! Ready for OTP verification!**")
        print(f"✅ Org ID: {org_id}")
        print(f"✅ Session ID: {session_id}")
        print(f"✅ Email: {email}")
        
        # Test hash extraction
        asyncio.run(bot.test_hash_extraction(org_code))
        
        print(f"\n📝 **NEXT STEP:**")
        print(f"Please check your email and provide the OTP!")
        print(f"Then I'll verify the OTP and extract the user authentication token!")
        
    else:
        print(f"\n❌ **Failed to get org ID or session ID**")
        print(f"💡 Please check the org code and try again")

if __name__ == "__main__":
    main()