#!/usr/bin/env python3
"""
Test hash extraction from Uievjh
"""

import requests
import json
import re
import asyncio
import aiohttp

async def test_hash_extraction():
    """Test hash extraction from Uievjh"""
    print("🚀 **TESTING HASH EXTRACTION**")
    print("="*60)
    
    org_code = "Uievjh"
    
    # Hash headers from extracted code
    hash_headers = {
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
    
    # Classplus headers from extracted code
    classplus_headers = {
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
    
    print(f"📝 Testing with:")
    print(f"   • Org Code: {org_code}")
    print()
    
    # Step 1: Try to get hash from courses.store
    print("🔍 Step 1: Getting hash from courses.store...")
    url = f"https://{org_code}.courses.store"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=hash_headers) as response:
                print(f"   Status: {response.status}")
                
                if response.status == 200:
                    html_text = await response.text()
                    print(f"   ✅ Got HTML response")
                    
                    # Look for hash in HTML
                    hash_match = re.search(r'"hash":"(.*?)"', html_text)
                    
                    if hash_match:
                        token = hash_match.group(1)
                        print(f"   ✅ Hash extracted: {token[:20]}...")
                        
                        # Step 2: Try to get courses from hash
                        print(f"\n🔍 Step 2: Getting courses from hash...")
                        courses_url = f"https://api.classplusapp.com/v2/course/preview/similar/{token}?limit=20"
                        
                        async with session.get(courses_url, headers=classplus_headers) as courses_response:
                            print(f"   Status: {courses_response.status}")
                            
                            if courses_response.status == 200:
                                data = await courses_response.json()
                                courses = data.get('data', {}).get('coursesData', [])
                                
                                if courses:
                                    print(f"   ✅ Found {len(courses)} courses")
                                    for i, course in enumerate(courses[:5]):  # Show first 5
                                        name = course.get('name', 'Unknown')
                                        price = course.get('finalPrice', 0)
                                        print(f"      {i+1}. {name} - ₹{price}")
                                else:
                                    print(f"   ❌ No courses found in response")
                            else:
                                print(f"   ❌ Failed to get courses: {courses_response.status}")
                                print(f"   Response: {await courses_response.text()[:200]}...")
                    else:
                        print(f"   ❌ Hash not found in HTML")
                        print(f"   HTML preview: {html_text[:500]}...")
                else:
                    print(f"   ❌ Failed to get HTML: {response.status}")
                    print(f"   Response: {await response.text()[:200]}...")
                    
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    """Main function"""
    print("🔍 Testing hash extraction from Uievjh...")
    
    # Run the async function
    asyncio.run(test_hash_extraction())
    
    print(f"\n💡 **Note:** If hash extraction works, we can bypass org ID requirement!")

if __name__ == "__main__":
    main()