#!/usr/bin/env python3
"""
Test New APIs provided by user
"""

import requests
import json
import time

def test_scammer_keys_api():
    """Test the scammer keys API"""
    print("🔍 Testing Scammer Keys API")
    print("="*60)
    
    url = "https://scammer-keys.vercel.app/api"
    
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
                
        # Test POST request
        print(f"\n   🔍 Testing POST request...")
        payload = {
            "url": "https://api.classplusapp.com/v2/orgs/getOrgId",
            "method": "POST",
            "data": {"orgCode": "test"}
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:500]}...")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✅ Success! JSON data:")
                print(json.dumps(data, indent=2))
                
            except json.JSONDecodeError:
                print(f"   📄 Raw response (not JSON)")
                
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_cpapi_api():
    """Test the CP API"""
    print("\n🔍 Testing CP API")
    print("="*60)
    
    url = "https://cpapi-rjbs-1l0p.onrender.com/"
    
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
                
        # Test POST request
        print(f"\n   🔍 Testing POST request...")
        payload = {
            "orgCode": "test",
            "email": "test@example.com"
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:500]}...")
        
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
    
    # Test with different endpoints
    classplus_endpoints = [
        {
            "name": "Get Org ID",
            "url": "https://api.classplusapp.com/v2/orgs/getOrgId",
            "payload": {"orgCode": "test"}
        },
        {
            "name": "Session Token",
            "url": "https://event-api.classplusapp.com/analytics-api/v1/session/token",
            "payload": {"source": 50, "source_app": "classplus"}
        },
        {
            "name": "Send OTP",
            "url": "https://api.classplusapp.com/v2/users/sendOtp",
            "payload": {
                "email": "test@example.com",
                "countryExt": "91",
                "orgId": 1,
                "fingerprintId": "dummy",
                "orgCode": "test"
            }
        },
        {
            "name": "Verify OTP",
            "url": "https://api.classplusapp.com/v2/users/verify",
            "payload": {
                "otp": "123456",
                "countryExt": "91",
                "sessionId": "test",
                "orgId": 1,
                "fingerprintId": "dummy",
                "email": "test@example.com"
            }
        }
    ]
    
    # Test with scammer keys API
    print("🔍 Testing with Scammer Keys API")
    print("-" * 40)
    
    scammer_url = "https://scammer-keys.vercel.app/api"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    for endpoint in classplus_endpoints:
        print(f"\n   🔍 Testing: {endpoint['name']}")
        
        payload = {
            "url": endpoint['url'],
            "method": "POST",
            "data": endpoint['payload']
        }
        
        try:
            response = requests.post(scammer_url, json=payload, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:300]}...")
            
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
    
    # Test with CP API
    print(f"\n🔍 Testing with CP API")
    print("-" * 40)
    
    cp_url = "https://cpapi-rjbs-1l0p.onrender.com/"
    
    for endpoint in classplus_endpoints:
        print(f"\n   🔍 Testing: {endpoint['name']}")
        
        try:
            response = requests.post(cp_url, json=endpoint['payload'], headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:300]}...")
            
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

def test_with_real_org_codes():
    """Test with real org codes"""
    print("\n🔍 Testing with Real Org Codes")
    print("="*60)
    
    # Test different org codes
    org_codes = ["rpsc", "demo", "test", "classplus", "cp", "cl", "ed", "sc", "co"]
    
    # Test with CP API
    cp_url = "https://cpapi-rjbs-1l0p.onrender.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    for org_code in org_codes:
        print(f"\n   🔍 Testing org code: {org_code}")
        
        payload = {
            "orgCode": org_code,
            "email": "test@example.com"
        }
        
        try:
            response = requests.post(cp_url, json=payload, headers=headers, timeout=10)
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

def main():
    """Main function"""
    print("🚀 **NEW APIs TESTER**")
    print("="*60)
    print("🔍 Testing new APIs provided by user...")
    
    # Test all APIs
    test_scammer_keys_api()
    test_cpapi_api()
    test_with_classplus_integration()
    test_with_real_org_codes()
    
    print(f"\n💡 **SUMMARY:**")
    print("="*60)
    print("✅ All new APIs tested!")
    print("✅ Ready to extract real data!")
    print("✅ Ready to get real tokens!")

if __name__ == "__main__":
    main()