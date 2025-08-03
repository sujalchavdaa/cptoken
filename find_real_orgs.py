#!/usr/bin/env python3
"""
Find Real Org Codes from Classplus
"""

import requests
import json
import re

def search_classplus_web():
    """Search Classplus web for real org codes"""
    print("🔍 Searching Classplus Web for Real Org Codes")
    print("="*60)
    
    # Try different web endpoints
    web_endpoints = [
        "https://web.classplusapp.com/",
        "https://web.classplusapp.com/api/v2/orgs",
        "https://web.classplusapp.com/api/v2/public/orgs",
        "https://web.classplusapp.com/api/v2/demo",
        "https://web.classplusapp.com/api/v2/sample",
        "https://web.classplusapp.com/api/v2/test"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    
    for url in web_endpoints:
        print(f"\n🔍 Trying: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                print(f"   ✅ Got content ({len(content)} chars)")
                
                # Look for org codes in HTML/JS
                org_patterns = [
                    r'"orgCode"\s*:\s*"([^"]+)"',
                    r'"code"\s*:\s*"([^"]+)"',
                    r'orgCode["\']?\s*:\s*["\']([^"\']+)["\']',
                    r'code["\']?\s*:\s*["\']([^"\']+)["\']',
                    r'org-code["\']?\s*:\s*["\']([^"\']+)["\']',
                    r'organization["\']?\s*:\s*["\']([^"\']+)["\']'
                ]
                
                found_codes = []
                for pattern in org_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    found_codes.extend(matches)
                
                if found_codes:
                    print(f"   🎯 Found potential org codes:")
                    for code in set(found_codes):
                        print(f"      • {code}")
                else:
                    print(f"   ❌ No org codes found in content")
                    
            else:
                print(f"   ❌ Failed with status {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def try_common_org_patterns():
    """Try common org code patterns"""
    print("\n🔍 Trying Common Org Code Patterns")
    print("="*60)
    
    # Common patterns that might be used
    patterns = [
        # Educational
        "edu", "school", "college", "university", "institute", "academy",
        "coaching", "tutorial", "training", "learning", "education",
        
        # Short codes
        "cp", "cl", "ed", "sc", "co", "un", "in", "ac", "tu", "le",
        
        # Demo/Test
        "demo", "test", "sample", "example", "trial", "free",
        
        # Real examples (if any)
        "classplus", "classplusapp", "classplusdemo", "classplustest",
        
        # Numbers
        "123", "456", "789", "001", "002", "003", "100", "200", "300",
        
        # Combinations
        "demo123", "test123", "class123", "school123", "edu123",
        "cp123", "cl123", "ed123", "sc123", "co123"
    ]
    
    valid_orgs = []
    
    for pattern in patterns:
        print(f"   🔍 Testing: {pattern}")
        
        url = "https://api.classplusapp.com/v2/orgs/getOrgId"
        payload = {"orgCode": pattern}
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "origin": "https://web.classplusapp.com",
            "referer": "https://web.classplusapp.com/",
            "user-agent": "Mozilla/5.0"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if "data" in data and "orgId" in data["data"]:
                    print(f"   ✅ VALID ORG FOUND: {pattern} -> {data['data']['orgId']}")
                    valid_orgs.append((pattern, data['data']['orgId']))
                else:
                    print(f"   ❌ Invalid response structure")
            else:
                print(f"   ❌ Status: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return valid_orgs

def try_documentation_search():
    """Search for org codes in documentation"""
    print("\n🔍 Searching Documentation for Org Codes")
    print("="*60)
    
    # Try to find documentation or examples
    doc_urls = [
        "https://docs.classplusapp.com/",
        "https://api.classplusapp.com/docs",
        "https://developer.classplusapp.com/",
        "https://help.classplusapp.com/"
    ]
    
    for url in doc_urls:
        print(f"   🔍 Trying: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                content = response.text
                print(f"   ✅ Got documentation content")
                
                # Look for example org codes
                examples = re.findall(r'["\']([a-zA-Z0-9]{3,10})["\']', content)
                print(f"   🎯 Found potential examples: {examples[:5]}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def main():
    """Main function"""
    print("🚀 **REAL ORG CODE FINDER**")
    print("="*60)
    print("🔍 Searching for real Classplus org codes...")
    
    # Search web interface
    search_classplus_web()
    
    # Try common patterns
    valid_orgs = try_common_org_patterns()
    
    # Search documentation
    try_documentation_search()
    
    if valid_orgs:
        print(f"\n🎉 **SUCCESS! Found Valid Orgs:**")
        for org_code, org_id in valid_orgs:
            print(f"✅ Org Code: {org_code} -> Org ID: {org_id}")
        print(f"✅ Ready to test with real data!")
    else:
        print(f"\n❌ **No valid org codes found**")
        print(f"💡 This suggests:")
        print(f"   • All org codes are private/restricted")
        print(f"   • Need real Classplus account")
        print(f"   • Need to register as organization")
        print(f"   • API might be blocking external access")

if __name__ == "__main__":
    main()