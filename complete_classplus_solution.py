#!/usr/bin/env python3
"""
Complete Classplus Solution using extracted patterns
"""

import requests
import json
import re
import asyncio
import aiohttp
import base64

class CompleteClassplusSolution:
    def __init__(self):
        self.classplus_apis = {
            "get_org_id": "https://api.classplusapp.com/v2/orgs/getOrgId",
            "send_otp": "https://api.classplusapp.com/v2/users/sendOtp", 
            "verify_otp": "https://api.classplusapp.com/v2/users/verify",
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

    async def get_hash_from_org_code(self, org_code):
        """Get hash from org code using extracted pattern"""
        url = f"https://{org_code}.courses.store"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.hash_headers) as response:
                    if response.status == 200:
                        html_text = await response.text()
                        hash_match = re.search(r'"hash":"(.*?)"', html_text)
                        
                        if hash_match:
                            token = hash_match.group(1)
                            print(f"   ✅ Hash extracted: {token[:20]}...")
                            return token
                        else:
                            print(f"   ❌ Hash not found in HTML")
                            return None
                    else:
                        print(f"   ❌ Failed to get HTML: {response.status}")
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

    def verify_otp_and_get_user_token(self, session_id, otp_code, org_id, email):
        """Verify OTP and get user token using extracted pattern"""
        url = self.classplus_apis["verify_otp"]
        payload = {
            "otp": otp_code,
            "countryExt": "91",
            "sessionId": session_id,
            "orgId": org_id,
            "fingerprintId": "dummy",
            "email": email
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
            
            if response.status_code == 201:
                try:
                    data = response.json()
                    print(f"   ✅ Success!")
                    
                    if "data" in data and "token" in data["data"]:
                        return data["data"]["token"]
                    else:
                        print(f"   ❌ Token not found in response")
                        return None
                        
                except json.JSONDecodeError:
                    print(f"   ❌ Error parsing JSON")
                    return None
            else:
                print(f"   ❌ Failed with status {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None

    def decode_user_token(self, token):
        """Decode and analyze user authentication token"""
        try:
            # Split the token
            parts = token.split('.')
            if len(parts) != 3:
                print("❌ Invalid JWT token format")
                return
            
            # Decode payload
            payload = parts[1]
            payload += '=' * (4 - len(payload) % 4)
            payload_decoded = base64.b64decode(payload).decode('utf-8')
            payload_json = json.loads(payload_decoded)
            
            print("\n🔍 **USER AUTHENTICATION TOKEN ANALYSIS:**")
            print("="*60)
            print(f"✅ Token Type: User Authentication Token")
            print(f"✅ User ID: {payload_json.get('id', 'N/A')}")
            print(f"✅ Org ID: {payload_json.get('orgID', 'N/A')}")
            print(f"✅ Email: {payload_json.get('email', 'N/A')}")
            print(f"✅ Name: {payload_json.get('name', 'N/A')}")
            print(f"✅ Mobile: {payload_json.get('mobile', 'N/A')}")
            print(f"✅ Type: {payload_json.get('type', 'N/A')}")
            print(f"✅ Is First Login: {payload_json.get('isFirstLogin', 'N/A')}")
            print(f"✅ Login Via: {payload_json.get('loginVia', 'N/A')}")
            print(f"✅ Country Code: {payload_json.get('countryCode', 'N/A')}")
            print(f"✅ Default Language: {payload_json.get('defaultLanguage', 'N/A')}")
            print(f"✅ Issued At: {payload_json.get('iat', 'N/A')}")
            print(f"✅ Expires At: {payload_json.get('exp', 'N/A')}")
            
            print(f"\n📊 Full Token Payload:")
            print(json.dumps(payload_json, indent=2))
            
        except Exception as e:
            print(f"❌ Error decoding token: {e}")

    async def test_complete_solution(self, org_code, email):
        """Test complete solution with both methods"""
        print(f"🚀 **COMPLETE CLASSPLUS SOLUTION**")
        print("="*60)
        print(f"📝 Testing with:")
        print(f"   • Org Code: {org_code}")
        print(f"   • Email: {email}")
        print()
        
        # Method 1: Hash extraction (works for Uievjh)
        print("🔍 **METHOD 1: Hash Extraction**")
        print("="*40)
        
        token = await self.get_hash_from_org_code(org_code)
        if token:
            courses = await self.get_courses_from_hash(token, org_code)
            if courses:
                print(f"   ✅ Found {len(courses)} courses via hash extraction")
                for i, course in enumerate(courses[:3]):
                    name = course.get('name', 'Unknown')
                    price = course.get('finalPrice', 0)
                    print(f"      {i+1}. {name} - ₹{price}")
                
                print(f"\n🎉 **HASH EXTRACTION SUCCESS!**")
                print(f"✅ Token: {token[:50]}...")
                print(f"✅ Courses: {len(courses)} found")
                return "HASH_SUCCESS", token, courses
            else:
                print(f"   ❌ No courses found via hash extraction")
        else:
            print(f"   ❌ Hash extraction failed")
        
        # Method 2: Traditional OTP flow
        print(f"\n🔍 **METHOD 2: Traditional OTP Flow**")
        print("="*40)
        
        org_id = self.get_org_id(org_code)
        if org_id:
            print(f"   ✅ Org ID: {org_id}")
            
            session_id = self.send_otp(email, org_code, org_id)
            if session_id and session_id != "RATE_LIMIT_EXCEEDED":
                print(f"   ✅ Session ID: {session_id}")
                print(f"   📝 Ready for OTP verification")
                return "OTP_READY", session_id, org_id
            elif session_id == "RATE_LIMIT_EXCEEDED":
                print(f"   ⚠️ Rate limit exceeded")
                return "RATE_LIMIT", None, None
            else:
                print(f"   ❌ Failed to send OTP")
                return "OTP_FAILED", None, None
        else:
            print(f"   ❌ Invalid org code")
            return "INVALID_ORG", None, None

def main():
    """Main function"""
    print("🚀 **COMPLETE CLASSPLUS SOLUTION**")
    print("="*60)
    print("🔍 Using extracted patterns from provided code...")
    
    solution = CompleteClassplusSolution()
    
    # Test with Uievjh
    org_code = "Uievjh"
    email = "makey75125@hostbyt.com"
    
    # Test complete solution
    result = asyncio.run(solution.test_complete_solution(org_code, email))
    
    method, data, extra = result
    
    if method == "HASH_SUCCESS":
        print(f"\n🎉 **SUCCESS! Hash extraction worked!**")
        print(f"✅ We can access courses without OTP!")
        print(f"✅ Token: {data[:50]}...")
        print(f"✅ Courses: {len(extra)} found")
        
    elif method == "OTP_READY":
        print(f"\n📝 **OTP FLOW READY!**")
        print(f"✅ Session ID: {data}")
        print(f"✅ Org ID: {extra}")
        print(f"📱 Please check your email and provide OTP!")
        
    elif method == "RATE_LIMIT":
        print(f"\n⚠️ **Rate limit exceeded**")
        print(f"💡 Try again after 6 hours")
        
    else:
        print(f"\n❌ **Method failed**")
        print(f"💡 Try a different org code")

if __name__ == "__main__":
    main()