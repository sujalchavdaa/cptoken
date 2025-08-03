#!/usr/bin/env python3
"""
Explore Classplus API to get real information
"""

import requests
import json
import time

def explore_classplus_api():
    """Explore Classplus API endpoints"""
    print("🔍 Exploring Classplus API for Real Information")
    print("="*60)
    
    # Test different API endpoints
    endpoints_to_explore = [
        {
            "name": "Public Orgs List",
            "url": "https://api.classplusapp.com/v2/orgs/public",
            "method": "GET"
        },
        {
            "name": "Demo Orgs",
            "url": "https://api.classplusapp.com/v2/orgs/demo",
            "method": "GET"
        },
        {
            "name": "Popular Orgs",
            "url": "https://api.classplusapp.com/v2/orgs/popular",
            "method": "GET"
        },
        {
            "name": "Featured Orgs",
            "url": "https://api.classplusapp.com/v2/orgs/featured",
            "method": "GET"
        },
        {
            "name": "Search Orgs",
            "url": "https://api.classplusapp.com/v2/orgs/search",
            "method": "POST",
            "payload": {"query": "test"}
        },
        {
            "name": "Org Categories",
            "url": "https://api.classplusapp.com/v2/orgs/categories",
            "method": "GET"
        },
        {
            "name": "App Info",
            "url": "https://api.classplusapp.com/v2/app/info",
            "method": "GET"
        },
        {
            "name": "Public Info",
            "url": "https://api.classplusapp.com/v2/public/info",
            "method": "GET"
        }
    ]
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "origin": "https://web.classplusapp.com",
        "referer": "https://web.classplusapp.com/",
        "region": "IN",
        "user-agent": "Mozilla/5.0",
        "api-version": "52"
    }
    
    for endpoint in endpoints_to_explore:
        print(f"\n🔍 Trying: {endpoint['name']}")
        print(f"   URL: {endpoint['url']}")
        
        try:
            if endpoint['method'] == 'GET':
                response = requests.get(endpoint['url'], headers=headers, timeout=10)
            else:
                payload = endpoint.get('payload', {})
                response = requests.post(endpoint['url'], json=payload, headers=headers, timeout=10)
            
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:300]}...")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   ✅ Success! Found data:")
                    print(json.dumps(data, indent=2))
                    
                    # Look for org codes in response
                    if isinstance(data, dict):
                        if 'data' in data and isinstance(data['data'], list):
                            for item in data['data']:
                                if isinstance(item, dict) and 'orgCode' in item:
                                    print(f"   🎯 Found Org Code: {item['orgCode']}")
                                elif isinstance(item, dict) and 'code' in item:
                                    print(f"   🎯 Found Code: {item['code']}")
                        elif 'orgs' in data and isinstance(data['orgs'], list):
                            for org in data['orgs']:
                                if isinstance(org, dict) and 'orgCode' in org:
                                    print(f"   🎯 Found Org Code: {org['orgCode']}")
                    
                except Exception as e:
                    print(f"   ❌ Error parsing JSON: {e}")
            else:
                print(f"   ❌ Failed with status {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return None

def try_web_classplus_orgs():
    """Try to get orgs from web.classplusapp.com"""
    print("\n🔍 Trying Web Classplus for Real Orgs")
    print("="*60)
    
    try:
        # Try to get orgs from web interface
        url = "https://web.classplusapp.com/api/v2/orgs/public"
        headers = {
            "accept": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:300]}...")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✅ Found web orgs data:")
                print(json.dumps(data, indent=2))
            except Exception as e:
                print(f"   ❌ Error parsing: {e}")
        else:
            print(f"   ❌ Failed with status {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

def try_real_org_codes():
    """Try some real org codes that might exist"""
    print("\n🔍 Trying Real Org Codes")
    print("="*60)
    
    # Try some real org codes that might exist
    real_org_codes = [
        "classplus", "demo", "test", "sample", "example", "tutorial",
        "coaching", "academy", "institute", "school", "college", "university",
        "education", "learning", "training", "study", "course", "class",
        "teacher", "student", "admin", "user", "guest", "public"
    ]
    
    for org_code in real_org_codes:
        print(f"   🔍 Testing: {org_code}")
        
        url = "https://api.classplusapp.com/v2/orgs/getOrgId"
        payload = {"orgCode": org_code}
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
                    print(f"   ✅ VALID ORG FOUND: {org_code} -> {data['data']['orgId']}")
                    return org_code, data['data']['orgId']
                else:
                    print(f"   ❌ Invalid response structure")
            else:
                print(f"   ❌ Status: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return None, None

def main():
    """Main function"""
    print("🚀 **CLASSPLUS API EXPLORER**")
    print("="*60)
    print("🔍 Searching for real org codes and information...")
    
    # Explore API endpoints
    explore_classplus_api()
    
    # Try web interface
    try_web_classplus_orgs()
    
    # Try real org codes
    org_code, org_id = try_real_org_codes()
    
    if org_code and org_id:
        print(f"\n🎉 **SUCCESS! Found Real Org:**")
        print(f"✅ Org Code: {org_code}")
        print(f"✅ Org ID: {org_id}")
        print(f"✅ Ready to test with real data!")
    else:
        print(f"\n❌ **No valid org codes found**")
        print(f"💡 Need to find real org codes from Classplus")

if __name__ == "__main__":
    main()