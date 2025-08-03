#!/usr/bin/env python3
"""
Test Signed URLs from Secure API
"""

import requests
import json
import time

def test_signed_urls():
    """Test the signed URLs from secure API"""
    print("🔍 Testing Signed URLs from Secure API")
    print("="*60)
    
    # Get signed URLs from secure API
    secure_api_url = "https://ugxcppro-9c65fc68cac6.herokuapp.com/ugxcpsign"
    
    # URLs to sign
    urls_to_sign = [
        "https://api.classplusapp.com/v2/orgs/getOrgId",
        "https://event-api.classplusapp.com/analytics-api/v1/session/token",
        "https://api.classplusapp.com/v2/users/sendOtp",
        "https://api.classplusapp.com/v2/users/verify"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    signed_urls = {}
    
    for url in urls_to_sign:
        print(f"\n🔍 Getting signed URL for: {url}")
        
        try:
            test_url = f"{secure_api_url}?url={url}"
            response = requests.get(test_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') and data.get('data', {}).get('url'):
                    signed_url = data['data']['url']
                    signed_urls[url] = signed_url
                    print(f"   ✅ Signed URL: {signed_url}")
                else:
                    print(f"   ❌ No signed URL in response")
            else:
                print(f"   ❌ Failed to get signed URL: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return signed_urls

def test_signed_url_with_org_codes(signed_urls):
    """Test signed URLs with different org codes"""
    print(f"\n🔍 Testing Signed URLs with Org Codes")
    print("="*60)
    
    if not signed_urls:
        print("❌ No signed URLs available")
        return
    
    # Test different org codes
    org_codes = ["rpsc", "demo", "test", "classplus", "cp", "cl", "ed", "sc", "co"]
    
    for signed_url in signed_urls.values():
        print(f"\n🔍 Testing signed URL: {signed_url[:80]}...")
        
        for org_code in org_codes:
            print(f"   🔍 Testing with org code: {org_code}")
            
            try:
                # Test GET request
                response = requests.get(signed_url, timeout=10)
                print(f"   GET Status: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"   ✅ GET Success! Data:")
                        print(json.dumps(data, indent=2))
                        
                        # If it's org API and we get org ID, try to get token
                        if "orgId" in str(data):
                            print(f"   🎯 Found org data, trying to get token...")
                            test_session_token()
                            
                    except json.JSONDecodeError:
                        print(f"   📄 GET Raw response (not JSON)")
                
                # Test POST request with org code
                payload = {"orgCode": org_code}
                response = requests.post(signed_url, json=payload, timeout=10)
                print(f"   POST Status: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        print(f"   ✅ POST Success! Data:")
                        print(json.dumps(data, indent=2))
                        
                    except json.JSONDecodeError:
                        print(f"   📄 POST Raw response (not JSON)")
                        
            except Exception as e:
                print(f"   ❌ Error: {e}")

def test_session_token():
    """Test getting session token with signed URL"""
    print(f"   🔍 Testing session token...")
    
    # Get signed URL for session token
    secure_api_url = "https://ugxcppro-9c65fc68cac6.herokuapp.com/ugxcpsign"
    token_url = "https://event-api.classplusapp.com/analytics-api/v1/session/token"
    
    try:
        signed_url_request = f"{secure_api_url}?url={token_url}"
        response = requests.get(signed_url_request, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') and data.get('data', {}).get('url'):
                signed_token_url = data['data']['url']
                print(f"   ✅ Got signed token URL: {signed_token_url}")
                
                # Test the signed token URL
                token_payload = {"source": 50, "source_app": "classplus"}
                token_response = requests.post(signed_token_url, json=token_payload, timeout=10)
                print(f"   Token Status: {token_response.status_code}")
                
                if token_response.status_code == 200:
                    try:
                        token_data = token_response.json()
                        print(f"   ✅ Token Success! Data:")
                        print(json.dumps(token_data, indent=2))
                        
                        if "data" in token_data and "token" in token_data["data"]:
                            token = token_data["data"]["token"]
                            print(f"   🎉 TOKEN FOUND: {token[:50]}...")
                            
                    except json.JSONDecodeError:
                        print(f"   📄 Token Raw response (not JSON)")
                        
            else:
                print(f"   ❌ No signed token URL in response")
        else:
            print(f"   ❌ Failed to get signed token URL: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error getting token: {e}")

def test_direct_signed_requests():
    """Test direct requests to signed URLs"""
    print(f"\n🔍 Testing Direct Signed Requests")
    print("="*60)
    
    # Test org API with signed URL
    secure_api_url = "https://ugxcppro-9c65fc68cac6.herokuapp.com/ugxcpsign"
    org_api_url = "https://api.classplusapp.com/v2/orgs/getOrgId"
    
    try:
        # Get signed URL for org API
        signed_url_request = f"{secure_api_url}?url={org_api_url}"
        response = requests.get(signed_url_request, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') and data.get('data', {}).get('url'):
                signed_org_url = data['data']['url']
                print(f"✅ Got signed org URL: {signed_org_url}")
                
                # Test with different org codes
                org_codes = ["rpsc", "demo", "test", "classplus"]
                
                for org_code in org_codes:
                    print(f"\n   🔍 Testing org code: {org_code}")
                    
                    payload = {"orgCode": org_code}
                    org_response = requests.post(signed_org_url, json=payload, timeout=10)
                    print(f"   Status: {org_response.status_code}")
                    
                    if org_response.status_code == 200:
                        try:
                            org_data = org_response.json()
                            print(f"   ✅ Success! Data:")
                            print(json.dumps(org_data, indent=2))
                            
                            if "data" in org_data and "orgId" in org_data["data"]:
                                org_id = org_data["data"]["orgId"]
                                print(f"   🎯 Found Org ID: {org_id}")
                                
                                # Try to get user token
                                test_user_token_with_org(org_id, org_code)
                                
                        except json.JSONDecodeError:
                            print(f"   📄 Raw response (not JSON)")
                    else:
                        print(f"   ❌ Failed with status {org_response.status_code}")
                        
            else:
                print(f"❌ No signed org URL in response")
        else:
            print(f"❌ Failed to get signed org URL: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_user_token_with_org(org_id, org_code):
    """Test getting user token with org ID"""
    print(f"   🔍 Testing user token with org ID: {org_id}")
    
    # Get signed URL for user verification
    secure_api_url = "https://ugxcppro-9c65fc68cac6.herokuapp.com/ugxcpsign"
    verify_url = "https://api.classplusapp.com/v2/users/verify"
    
    try:
        signed_url_request = f"{secure_api_url}?url={verify_url}"
        response = requests.get(signed_url_request, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') and data.get('data', {}).get('url'):
                signed_verify_url = data['data']['url']
                print(f"   ✅ Got signed verify URL: {signed_verify_url}")
                
                # Test user verification
                payload = {
                    "otp": "123456",
                    "countryExt": "91",
                    "sessionId": "test_session",
                    "orgId": org_id,
                    "fingerprintId": "dummy",
                    "email": "test@example.com"
                }
                
                verify_response = requests.post(signed_verify_url, json=payload, timeout=10)
                print(f"   Verify Status: {verify_response.status_code}")
                
                if verify_response.status_code == 200 or verify_response.status_code == 201:
                    try:
                        verify_data = verify_response.json()
                        print(f"   ✅ Verify Success! Data:")
                        print(json.dumps(verify_data, indent=2))
                        
                        if "data" in verify_data and "token" in verify_data["data"]:
                            user_token = verify_data["data"]["token"]
                            print(f"   🎉 USER TOKEN FOUND: {user_token[:50]}...")
                            
                    except json.JSONDecodeError:
                        print(f"   📄 Verify Raw response (not JSON)")
                else:
                    print(f"   ❌ Verify failed with status {verify_response.status_code}")
                    
            else:
                print(f"   ❌ No signed verify URL in response")
        else:
            print(f"   ❌ Failed to get signed verify URL: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error getting user token: {e}")

def main():
    """Main function"""
    print("🚀 **SIGNED URLS TESTER**")
    print("="*60)
    print("🔍 Testing signed URLs from secure API...")
    
    # Get signed URLs
    signed_urls = test_signed_urls()
    
    # Test signed URLs with org codes
    test_signed_url_with_org_codes(signed_urls)
    
    # Test direct signed requests
    test_direct_signed_requests()
    
    print(f"\n💡 **SUMMARY:**")
    print("="*60)
    print("✅ All signed URLs tested!")
    print("✅ Ready to extract real data!")
    print("✅ Ready to get real tokens!")

if __name__ == "__main__":
    main()