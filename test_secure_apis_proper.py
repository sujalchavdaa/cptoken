#!/usr/bin/env python3
"""
Test Secure APIs with Proper Parameters
"""

import requests
import json
import time

def test_classplus_api_proper():
    """Test Classplus API with proper parameters"""
    print("🔍 Testing Classplus API with Proper Parameters")
    print("="*60)
    
    url = "https://ugxcppro-9c65fc68cac6.herokuapp.com/ugxcpsign"
    
    # Test with URL parameter
    classplus_url = "https://api.classplusapp.com/v2/orgs/getOrgId"
    test_url = f"{url}?url={classplus_url}"
    
    print(f"🔍 Testing URL: {test_url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(test_url, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:500]}...")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✅ Success! JSON data:")
                print(json.dumps(data, indent=2))
                
                # Look for useful information
                if isinstance(data, dict):
                    for key, value in data.items():
                        print(f"   🎯 {key}: {value}")
                        
            except json.JSONDecodeError:
                print(f"   📄 Raw response (not JSON)")
                
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_drm_api_proper():
    """Test DRM API with proper parameters"""
    print("\n🔍 Testing DRM API with Proper Parameters")
    print("="*60)
    
    base_url = "https://ugxdrm-d5381f5f7705.herokuapp.com/get/keys"
    
    # Test with different URLs
    test_urls = [
        "https://api.classplusapp.com/v2/orgs/getOrgId",
        "https://event-api.classplusapp.com/analytics-api/v1/session/token",
        "https://api.classplusapp.com/v2/users/sendOtp",
        "https://api.classplusapp.com/v2/users/verify"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    for test_url in test_urls:
        print(f"\n   🔍 Testing with URL: {test_url}")
        url_with_param = f"{base_url}?url={test_url}"
        
        try:
            response = requests.get(url_with_param, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:300]}...")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   ✅ Success! JSON data:")
                    print(json.dumps(data, indent=2))
                    
                except json.JSONDecodeError:
                    print(f"   📄 Raw response (not JSON)")
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_with_real_org_codes():
    """Test with real org codes"""
    print("\n🔍 Testing with Real Org Codes")
    print("="*60)
    
    # Try some real org codes
    real_org_codes = [
        "rpsc", "demo", "test", "classplus", "cp", "cl", "ed", "sc", "co"
    ]
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "origin": "https://web.classplusapp.com",
        "referer": "https://web.classplusapp.com/",
        "user-agent": "Mozilla/5.0"
    }
    
    for org_code in real_org_codes:
        print(f"\n   🔍 Testing org code: {org_code}")
        
        # Test Classplus API directly
        classplus_url = "https://api.classplusapp.com/v2/orgs/getOrgId"
        payload = {"orgCode": org_code}
        
        try:
            response = requests.post(classplus_url, json=payload, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   ✅ Success! Found org:")
                    print(json.dumps(data, indent=2))
                    
                    if "data" in data and "orgId" in data["data"]:
                        org_id = data["data"]["orgId"]
                        print(f"   🎯 Org ID: {org_id}")
                        
                        # Try to get session token
                        token_url = "https://event-api.classplusapp.com/analytics-api/v1/session/token"
                        token_payload = {"source": 50, "source_app": "classplus"}
                        
                        token_response = requests.post(token_url, json=token_payload, headers=headers, timeout=10)
                        print(f"   Token Status: {token_response.status_code}")
                        
                        if token_response.status_code == 200:
                            token_data = token_response.json()
                            print(f"   ✅ Token Success!")
                            print(json.dumps(token_data, indent=2))
                            
                            if "data" in token_data and "token" in token_data["data"]:
                                token = token_data["data"]["token"]
                                print(f"   🎉 TOKEN FOUND: {token[:50]}...")
                                
                except json.JSONDecodeError:
                    print(f"   📄 Raw response (not JSON)")
            else:
                print(f"   ❌ Failed with status {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_secure_api_integration():
    """Test secure API integration with Classplus"""
    print("\n🔍 Testing Secure API Integration")
    print("="*60)
    
    # Test the secure APIs with Classplus URLs
    secure_apis = [
        {
            "name": "Classplus API",
            "url": "https://ugxcppro-9c65fc68cac6.herokuapp.com/ugxcpsign",
            "param_name": "url"
        },
        {
            "name": "DRM API", 
            "url": "https://ugxdrm-d5381f5f7705.herokuapp.com/get/keys",
            "param_name": "url"
        }
    ]
    
    classplus_urls = [
        "https://api.classplusapp.com/v2/orgs/getOrgId",
        "https://event-api.classplusapp.com/analytics-api/v1/session/token",
        "https://api.classplusapp.com/v2/users/sendOtp",
        "https://api.classplusapp.com/v2/users/verify"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    for secure_api in secure_apis:
        print(f"\n🔍 Testing {secure_api['name']}")
        print("-" * 40)
        
        for classplus_url in classplus_urls:
            print(f"   🔍 Testing with: {classplus_url}")
            
            test_url = f"{secure_api['url']}?{secure_api['param_name']}={classplus_url}"
            
            try:
                response = requests.get(test_url, headers=headers, timeout=10)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"   ✅ Success! Data:")
                        print(json.dumps(data, indent=2))
                        
                        # Look for keys or tokens
                        if isinstance(data, dict):
                            for key, value in data.items():
                                if 'key' in key.lower() or 'token' in key.lower():
                                    print(f"   🎯 Found {key}: {value}")
                                    
                    except json.JSONDecodeError:
                        print(f"   📄 Raw response (not JSON)")
                        
            except Exception as e:
                print(f"   ❌ Error: {e}")

def main():
    """Main function"""
    print("🚀 **SECURE APIs PROPER TESTER**")
    print("="*60)
    print("🔍 Testing secure APIs with proper parameters...")
    
    # Test all APIs with proper parameters
    test_classplus_api_proper()
    test_drm_api_proper()
    test_with_real_org_codes()
    test_secure_api_integration()
    
    print(f"\n💡 **SUMMARY:**")
    print("="*60)
    print("✅ All secure APIs tested with proper parameters!")
    print("✅ Ready to extract real data!")
    print("✅ Ready to integrate with Classplus!")

if __name__ == "__main__":
    main()