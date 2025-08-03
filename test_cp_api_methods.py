#!/usr/bin/env python3
"""
Test CP API with different methods
"""

import requests
import json
import time

def test_cp_api_methods():
    """Test CP API with different HTTP methods"""
    print("🔍 Testing CP API with Different Methods")
    print("="*60)
    
    url = "https://cpapi-rjbs-1l0p.onrender.com/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Test different endpoints
    endpoints = [
        "/",
        "/api",
        "/token",
        "/org",
        "/user",
        "/otp",
        "/verify",
        "/session",
        "/keys",
        "/auth"
    ]
    
    for endpoint in endpoints:
        test_url = url.rstrip('/') + endpoint
        print(f"\n🔍 Testing endpoint: {test_url}")
        
        # Test GET
        try:
            response = requests.get(test_url, headers=headers, timeout=10)
            print(f"   GET Status: {response.status_code}")
            print(f"   GET Response: {response.text[:200]}...")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   ✅ GET Success! Data:")
                    print(json.dumps(data, indent=2))
                except json.JSONDecodeError:
                    print(f"   📄 GET Raw response (not JSON)")
        except Exception as e:
            print(f"   ❌ GET Error: {e}")
        
        # Test POST
        try:
            payload = {
                "orgCode": "test",
                "email": "test@example.com"
            }
            response = requests.post(test_url, json=payload, headers=headers, timeout=10)
            print(f"   POST Status: {response.status_code}")
            print(f"   POST Response: {response.text[:200]}...")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   ✅ POST Success! Data:")
                    print(json.dumps(data, indent=2))
                except json.JSONDecodeError:
                    print(f"   📄 POST Raw response (not JSON)")
        except Exception as e:
            print(f"   ❌ POST Error: {e}")

def test_cp_api_with_parameters():
    """Test CP API with URL parameters"""
    print("\n🔍 Testing CP API with URL Parameters")
    print("="*60)
    
    base_url = "https://cpapi-rjbs-1l0p.onrender.com/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    # Test different parameters
    parameters = [
        "?orgCode=test",
        "?email=test@example.com",
        "?action=get_token",
        "?action=get_org",
        "?action=send_otp",
        "?action=verify_otp",
        "?orgCode=test&email=test@example.com",
        "?action=get_token&orgCode=test",
        "?action=get_org&orgCode=test",
        "?action=send_otp&email=test@example.com"
    ]
    
    for param in parameters:
        test_url = base_url + param
        print(f"\n🔍 Testing URL: {test_url}")
        
        try:
            response = requests.get(test_url, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:300]}...")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   ✅ Success! Data:")
                    print(json.dumps(data, indent=2))
                    
                    # Look for useful information
                    if isinstance(data, dict):
                        for key, value in data.items():
                            if 'token' in key.lower() or 'orgId' in key.lower() or 'key' in key.lower():
                                print(f"   🎯 Found {key}: {value}")
                                
                except json.JSONDecodeError:
                    print(f"   📄 Raw response (not JSON)")
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_cp_api_with_real_data():
    """Test CP API with real data"""
    print("\n🔍 Testing CP API with Real Data")
    print("="*60)
    
    base_url = "https://cpapi-rjbs-1l0p.onrender.com/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    # Test with different org codes
    org_codes = ["rpsc", "demo", "test", "classplus", "cp", "cl", "ed", "sc", "co"]
    
    for org_code in org_codes:
        print(f"\n🔍 Testing org code: {org_code}")
        
        # Test with GET parameters
        test_url = f"{base_url}?orgCode={org_code}&email=test@example.com"
        
        try:
            response = requests.get(test_url, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   ✅ Success! Data:")
                    print(json.dumps(data, indent=2))
                    
                    # Look for org ID or token
                    if isinstance(data, dict):
                        for key, value in data.items():
                            if 'orgId' in key.lower() or 'token' in key.lower():
                                print(f"   🎯 Found {key}: {value}")
                                
                except json.JSONDecodeError:
                    print(f"   📄 Raw response (not JSON)")
            else:
                print(f"   ❌ Failed with status {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_cp_api_actions():
    """Test CP API with different actions"""
    print("\n🔍 Testing CP API with Different Actions")
    print("="*60)
    
    base_url = "https://cpapi-rjbs-1l0p.onrender.com/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    # Test different actions
    actions = [
        "get_token",
        "get_org",
        "send_otp", 
        "verify_otp",
        "get_session",
        "get_keys",
        "get_auth",
        "get_user",
        "get_info",
        "get_data"
    ]
    
    for action in actions:
        print(f"\n🔍 Testing action: {action}")
        
        # Test with GET
        test_url = f"{base_url}?action={action}&orgCode=test&email=test@example.com"
        
        try:
            response = requests.get(test_url, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:300]}...")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   ✅ Success! Data:")
                    print(json.dumps(data, indent=2))
                    
                    # Look for useful information
                    if isinstance(data, dict):
                        for key, value in data.items():
                            if 'token' in key.lower() or 'orgId' in key.lower() or 'key' in key.lower():
                                print(f"   🎯 Found {key}: {value}")
                                
                except json.JSONDecodeError:
                    print(f"   📄 Raw response (not JSON)")
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")

def main():
    """Main function"""
    print("🚀 **CP API METHODS TESTER**")
    print("="*60)
    print("🔍 Testing CP API with different methods...")
    
    # Test all methods
    test_cp_api_methods()
    test_cp_api_with_parameters()
    test_cp_api_with_real_data()
    test_cp_api_actions()
    
    print(f"\n💡 **SUMMARY:**")
    print("="*60)
    print("✅ All CP API methods tested!")
    print("✅ Ready to extract real data!")
    print("✅ Ready to get real tokens!")

if __name__ == "__main__":
    main()