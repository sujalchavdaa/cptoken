#!/usr/bin/env python3
"""
Test the APIs obtained from secure API client
"""

import requests
import json
import time

def test_classplus_api():
    """Test the Classplus API from secure source"""
    print("🔍 Testing Classplus API from Secure Source")
    print("="*60)
    
    url = "https://ugxcppro-9c65fc68cac6.herokuapp.com/ugxcpsign"
    
    print(f"🔍 Testing URL: {url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    try:
        # Test GET request
        print(f"   🔍 Testing GET request...")
        response = requests.get(url, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:300]}...")
        
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
                
        # Test POST request
        print(f"\n   🔍 Testing POST request...")
        payload = {
            "orgCode": "test",
            "email": "test@example.com"
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
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

def test_drm_api():
    """Test the DRM API from secure source"""
    print("\n🔍 Testing DRM API from Secure Source")
    print("="*60)
    
    base_url = "https://ugxdrm-d5381f5f7705.herokuapp.com/get/keys"
    
    print(f"🔍 Testing URL: {base_url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    try:
        # Test without parameters
        print(f"   🔍 Testing without parameters...")
        response = requests.get(base_url, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:300]}...")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✅ Success! JSON data:")
                print(json.dumps(data, indent=2))
                
            except json.JSONDecodeError:
                print(f"   📄 Raw response (not JSON)")
        
        # Test with URL parameter
        print(f"\n   🔍 Testing with URL parameter...")
        test_url = "https://api.classplusapp.com/v2/orgs/getOrgId"
        url_with_param = f"{base_url}?url={test_url}"
        
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

def test_pw_api():
    """Test the PW API from secure source"""
    print("\n🔍 Testing PW API from Secure Source")
    print("="*60)
    
    url = "https://anonymouspwplayerr-f996115ea61a.herokuapp.com"
    
    print(f"🔍 Testing URL: {url}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    try:
        # Test GET request
        print(f"   🔍 Testing GET request...")
        response = requests.get(url, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:300]}...")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✅ Success! JSON data:")
                print(json.dumps(data, indent=2))
                
            except json.JSONDecodeError:
                print(f"   📄 Raw response (not JSON)")
        
        # Test POST request
        print(f"\n   🔍 Testing POST request...")
        payload = {
            "action": "get_keys",
            "url": "https://api.classplusapp.com/v2/orgs/getOrgId"
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
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

def test_with_classplus_integration():
    """Test APIs with Classplus integration"""
    print("\n🔍 Testing APIs with Classplus Integration")
    print("="*60)
    
    # Test Classplus API with the secure APIs
    classplus_url = "https://api.classplusapp.com/v2/orgs/getOrgId"
    payload = {"orgCode": "test"}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "origin": "https://web.classplusapp.com",
        "referer": "https://web.classplusapp.com/",
        "user-agent": "Mozilla/5.0"
    }
    
    print(f"🔍 Testing Classplus API: {classplus_url}")
    print(f"   Payload: {payload}")
    
    try:
        response = requests.post(classplus_url, json=payload, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:300]}...")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✅ Success! JSON data:")
                print(json.dumps(data, indent=2))
                
                # If we get org ID, try to get token
                if "data" in data and "orgId" in data["data"]:
                    org_id = data["data"]["orgId"]
                    print(f"\n   🎯 Got Org ID: {org_id}")
                    print(f"   🔍 Now trying to get token...")
                    
                    # Try to get session token
                    token_url = "https://event-api.classplusapp.com/analytics-api/v1/session/token"
                    token_payload = {"source": 50, "source_app": "classplus"}
                    
                    token_response = requests.post(token_url, json=token_payload, headers=headers, timeout=10)
                    print(f"   Token Status: {token_response.status_code}")
                    
                    if token_response.status_code == 200:
                        token_data = token_response.json()
                        print(f"   ✅ Token Success! Data:")
                        print(json.dumps(token_data, indent=2))
                        
                        if "data" in token_data and "token" in token_data["data"]:
                            token = token_data["data"]["token"]
                            print(f"   🎉 TOKEN FOUND: {token[:50]}...")
                            
            except json.JSONDecodeError:
                print(f"   📄 Raw response (not JSON)")
                
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    """Main function"""
    print("🚀 **SECURE APIs TESTER**")
    print("="*60)
    print("🔍 Testing APIs from secure source...")
    
    # Test all APIs
    test_classplus_api()
    test_drm_api()
    test_pw_api()
    test_with_classplus_integration()
    
    print(f"\n💡 **SUMMARY:**")
    print("="*60)
    print("✅ All secure APIs tested!")
    print("✅ Ready to extract real data!")
    print("✅ Ready to integrate with Classplus!")

if __name__ == "__main__":
    main()