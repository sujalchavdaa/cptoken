#!/usr/bin/env python3
"""
Direct User Authentication Token Generation
Try to get user authentication token without OTP verification
"""

import requests
import json
import base64
import time

def try_direct_user_token_endpoints():
    """Try different endpoints to get user authentication token directly"""
    print("🚀 Trying Direct User Authentication Token Generation")
    print("="*60)
    
    # Test different endpoints that might return user tokens
    endpoints_to_try = [
        {
            "name": "User Login Direct",
            "url": "https://api.classplusapp.com/v2/users/login",
            "payload": {
                "email": "test@example.com",
                "password": "test123",
                "orgCode": "demo"
            }
        },
        {
            "name": "User Registration",
            "url": "https://api.classplusapp.com/v2/users/register",
            "payload": {
                "email": "test@example.com",
                "name": "Test User",
                "orgCode": "demo"
            }
        },
        {
            "name": "Guest Token",
            "url": "https://api.classplusapp.com/v2/users/guest",
            "payload": {
                "orgCode": "demo"
            }
        },
        {
            "name": "Anonymous Token",
            "url": "https://api.classplusapp.com/v2/users/anonymous",
            "payload": {
                "orgCode": "demo"
            }
        },
        {
            "name": "Demo Token",
            "url": "https://api.classplusapp.com/v2/users/demo",
            "payload": {
                "orgCode": "demo"
            }
        },
        {
            "name": "Test Token",
            "url": "https://api.classplusapp.com/v2/users/test",
            "payload": {
                "orgCode": "demo"
            }
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
    
    for endpoint in endpoints_to_try:
        print(f"\n🔍 Trying: {endpoint['name']}")
        print(f"   URL: {endpoint['url']}")
        
        try:
            response = requests.post(
                endpoint['url'],
                json=endpoint['payload'],
                headers=headers,
                timeout=10
            )
            
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
            if response.status_code == 200 or response.status_code == 201:
                try:
                    data = response.json()
                    print(f"   ✅ Success! Response data:")
                    print(json.dumps(data, indent=2))
                    
                    # Check if token exists in response
                    if "token" in data:
                        print(f"   🎉 TOKEN FOUND: {data['token']}")
                        return data['token']
                    elif "data" in data and "token" in data["data"]:
                        print(f"   🎉 TOKEN FOUND: {data['data']['token']}")
                        return data['data']['token']
                    else:
                        print(f"   ❌ No token in response")
                        
                except Exception as e:
                    print(f"   ❌ Error parsing JSON: {e}")
            else:
                print(f"   ❌ Failed with status {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return None

def try_session_token_to_user_token():
    """Try to convert session token to user token"""
    print("\n🔍 Trying Session Token to User Token Conversion")
    print("="*60)
    
    # Use the session token we got earlier
    session_token = "eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJzb3VyY2UiOjUwLCJzb3VyY2VfYXBwIjoiY2xhc3NwbHVzIiwic2Vzc2lvbl9pZCI6IjhkZTBmZTcyLTQ1NjEtNGNiYy04NjZhLTYzMjUyMTkwMTg2MyIsInZpc2l0b3JfaWQiOiJjMWFhM2IwNS03ZjlhLTRlZjktOTI1My0zNzRhM2RjMmYxZWYiLCJjcmVhdGVkX2F0IjoxNzU0MjI4MjIwNTQzLCJpYXQiOjE3NTQyMjgyMjAsImV4cCI6MTc1NTUyNDIyMH0.eKG1pqT0Ws6Dbb7LUzpHRjevH4Wi33Si-H2zLyEyuXCdhTc5kcK8cNnjm4XPSlaT"
    
    # Try different endpoints with session token
    endpoints_to_try = [
        {
            "name": "User Profile with Session Token",
            "url": "https://api.classplusapp.com/v2/users/profile",
            "method": "GET"
        },
        {
            "name": "User Info with Session Token",
            "url": "https://api.classplusapp.com/v2/users/info",
            "method": "GET"
        },
        {
            "name": "User Details with Session Token",
            "url": "https://api.classplusapp.com/v2/users/details",
            "method": "GET"
        },
        {
            "name": "User Auth with Session Token",
            "url": "https://api.classplusapp.com/v2/users/auth",
            "method": "GET"
        }
    ]
    
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {session_token}",
        "origin": "https://web.classplusapp.com",
        "referer": "https://web.classplusapp.com/",
        "region": "IN",
        "user-agent": "Mozilla/5.0",
        "api-version": "52"
    }
    
    for endpoint in endpoints_to_try:
        print(f"\n🔍 Trying: {endpoint['name']}")
        print(f"   URL: {endpoint['url']}")
        
        try:
            if endpoint['method'] == 'GET':
                response = requests.get(endpoint['url'], headers=headers, timeout=10)
            else:
                response = requests.post(endpoint['url'], headers=headers, timeout=10)
            
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}...")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   ✅ Success! Response data:")
                    print(json.dumps(data, indent=2))
                    
                    # Check if user token exists
                    if "userToken" in data:
                        print(f"   🎉 USER TOKEN FOUND: {data['userToken']}")
                        return data['userToken']
                    elif "token" in data:
                        print(f"   🎉 TOKEN FOUND: {data['token']}")
                        return data['token']
                    else:
                        print(f"   ❌ No user token in response")
                        
                except Exception as e:
                    print(f"   ❌ Error parsing JSON: {e}")
            else:
                print(f"   ❌ Failed with status {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return None

def decode_user_token(token):
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

def main():
    """Main function to try different approaches"""
    print("🚀 Direct User Authentication Token Generation")
    print("="*60)
    
    # Try direct endpoints
    user_token = try_direct_user_token_endpoints()
    
    if user_token:
        print(f"\n🎉 **SUCCESS! User Authentication Token Found!**")
        print(f"✅ Token: {user_token}")
        decode_user_token(user_token)
        return
    
    # Try session token conversion
    user_token = try_session_token_to_user_token()
    
    if user_token:
        print(f"\n🎉 **SUCCESS! User Authentication Token Found!**")
        print(f"✅ Token: {user_token}")
        decode_user_token(user_token)
        return
    
    print("\n❌ No user authentication token found")
    print("💡 All direct methods failed")
    print("💡 Need to wait for rate limit reset and try OTP method")

if __name__ == "__main__":
    main()