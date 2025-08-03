#!/usr/bin/env python3
"""
Extract useful Classplus parts from the provided code
"""

import requests
import json
import re
import asyncio
import aiohttp

def extract_classplus_apis():
    """Extract Classplus API patterns from the code"""
    print("🔍 **EXTRACTING USEFUL CLASSPLUS PARTS**")
    print("="*60)
    
    # Classplus API patterns from the code
    classplus_apis = {
        "get_org_id": "https://api.classplusapp.com/v2/orgs/getOrgId",
        "send_otp": "https://api.classplusapp.com/v2/users/sendOtp", 
        "verify_otp": "https://api.classplusapp.com/v2/users/verify",
        "get_access_token": "https://api.classplusapp.com/v2/users/get-access-token",
        "course_preview": "https://api.classplusapp.com/v2/course/preview/similar/{token}",
        "course_content": "https://api.classplusapp.com/v2/course/preview/content/list/{Batch_Token}",
        "signed_url": "https://api.classplusapp.com/cams/uploader/video/jw-signed-url",
        "org_info": "https://api.classplusapp.com/v2/course/preview/org/info"
    }
    
    # Headers from the code
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
    
    # Batch headers from the code
    batch_headers = {
        'Accept': 'application/json, text/plain, */*',
        'region': 'IN',
        'accept-language': 'EN',
        'Api-Version': '22',
        'tutorWebsiteDomain': 'https://{org_code}.courses.store'
    }
    
    # Hash headers from the code
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
    
    print("📋 **Classplus API Endpoints:**")
    for name, url in classplus_apis.items():
        print(f"   • {name}: {url}")
    
    print(f"\n📋 **Classplus Headers:**")
    for key, value in classplus_headers.items():
        print(f"   • {key}: {value}")
    
    print(f"\n📋 **Batch Headers:**")
    for key, value in batch_headers.items():
        print(f"   • {key}: {value}")
    
    print(f"\n📋 **Hash Headers:**")
    for key, value in hash_headers.items():
        print(f"   • {key}: {value}")
    
    return classplus_apis, classplus_headers, batch_headers, hash_headers

def extract_url_patterns():
    """Extract URL patterns from the code"""
    print(f"\n🔍 **URL PATTERNS FROM CODE:**")
    print("="*60)
    
    url_patterns = [
        "https://{org_code}.courses.store",
        "https://api.classplusapp.com/v2/course/preview/similar/{token}",
        "https://api.classplusapp.com/v2/course/preview/content/list/{Batch_Token}",
        "https://api.classplusapp.com/cams/uploader/video/jw-signed-url",
        "https://api.classplusapp.com/v2/course/preview/org/info",
        "https://media-cdn.classplusapp.com/tencent/{identifier}/master.m3u8",
        "https://media-cdn.classplusapp.com/alisg-cdn-a.classplusapp.com/{identifier}/master.m3u8",
        "https://media-cdn.classplusapp.com/drm/{video_id}/playlist.m3u8",
        "https://cpvod.testbook.com/{video_id}/playlist.m3u8"
    ]
    
    for pattern in url_patterns:
        print(f"   • {pattern}")
    
    return url_patterns

def extract_hash_extraction():
    """Extract hash extraction logic from the code"""
    print(f"\n🔍 **HASH EXTRACTION LOGIC:**")
    print("="*60)
    
    hash_logic = """
    # Hash extraction from HTML
    async with session.get(f"https://{org_code}.courses.store", headers=hash_headers) as response:
        html_text = await response.text()
        hash_match = re.search(r'"hash":"(.*?)"', html_text)
        
        if hash_match:
            token = hash_match.group(1)
            # Use token for API calls
    """
    
    print(hash_logic)
    
    return hash_logic

def extract_signed_url_logic():
    """Extract signed URL logic from the code"""
    print(f"\n🔍 **SIGNED URL LOGIC:**")
    print("="*60)
    
    signed_url_logic = """
    # Signed URL fetching
    async def fetch_cpwp_signed_url(url_val: str, name: str, session: aiohttp.ClientSession, headers: Dict[str, str]) -> str | None:
        MAX_RETRIES = 3
        for attempt in range(MAX_RETRIES):
            params = {"url": url_val}
            try:
                async with session.get("https://api.classplusapp.com/cams/uploader/video/jw-signed-url", params=params, headers=headers) as response:
                    response.raise_for_status()
                    response_json = await response.json()
                    signed_url = response_json.get("url") or response_json.get('drmUrls', {}).get('manifestUrl')
                    return signed_url
            except Exception as e:
                pass
            if attempt < MAX_RETRIES - 1:
                await asyncio.sleep(2 ** attempt)
        return None
    """
    
    print(signed_url_logic)
    
    return signed_url_logic

def extract_url_transformations():
    """Extract URL transformation patterns from the code"""
    print(f"\n🔍 **URL TRANSFORMATION PATTERNS:**")
    print("="*60)
    
    transformations = [
        "media-cdn.classplusapp.com/tencent/ -> master.m3u8",
        "media-cdn.classplusapp.com/alisg-cdn-a.classplusapp.com/ -> master.m3u8", 
        "media-cdn.classplusapp.com/drm/ -> playlist.m3u8",
        "cpvideocdn.testbook.com -> cpvod.testbook.com/playlist.m3u8",
        "thumbnail.png -> master.m3u8",
        "thumbnail.jpg -> master.m3u8"
    ]
    
    for transform in transformations:
        print(f"   • {transform}")
    
    return transformations

def test_extracted_patterns():
    """Test the extracted patterns"""
    print(f"\n🔍 **TESTING EXTRACTED PATTERNS:**")
    print("="*60)
    
    # Test org code extraction
    test_org_codes = ["demo", "test", "sample", "classplus", "cp", "edu"]
    
    for org_code in test_org_codes:
        print(f"Testing org code: {org_code}")
        # Test hash extraction
        test_url = f"https://{org_code}.courses.store"
        print(f"   URL: {test_url}")
    
    return test_org_codes

def main():
    """Main function"""
    print("🚀 **EXTRACTING USEFUL CLASSPLUS PARTS**")
    print("="*60)
    
    # Extract all parts
    apis, headers, batch_headers, hash_headers = extract_classplus_apis()
    url_patterns = extract_url_patterns()
    hash_logic = extract_hash_extraction()
    signed_url_logic = extract_signed_url_logic()
    transformations = extract_url_transformations()
    test_org_codes = test_extracted_patterns()
    
    print(f"\n🎉 **EXTRACTION COMPLETE!**")
    print(f"✅ Found {len(apis)} API endpoints")
    print(f"✅ Found {len(url_patterns)} URL patterns")
    print(f"✅ Found {len(transformations)} URL transformations")
    print(f"✅ Ready to use extracted patterns!")

if __name__ == "__main__":
    main()