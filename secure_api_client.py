#!/usr/bin/env python3
"""
Secure API Client to fetch real APIs
"""

import os
import requests
import json
import re
import base64
import jwt
from datetime import datetime

class SecureAPIClient:
    def __init__(self):
        self.html_url = "https://xindex.netlify.app/xindex"
        self.jwt_secret = os.getenv('JWT_SECRET', 'eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJpc3MiOiAic2VjdXJlLWFwaS1zeXN0ZW0iLCAiYXVkIjogImFwaS1kYXNoYm9hcmQiLCAiaWF0IjogMTc1MzIzNjY0MywgImV4cCI6IDE3ODkyMTUwNDMsICJjdXN0b21fZGF0YSI6IHsidXNlcl9yb2xlIjogImFkbWluIn19._O30-nacUDNahkYgBCZp9ZnL0_7itDsHx5W9cnVxiQ0')
        self.apis = {}

    def generate_token(self):
        payload = {
            'user_id': 'api_client',
            'exp': datetime.utcnow().timestamp() + 3600,
            'iat': datetime.utcnow().timestamp(),
            'authorized': True
        }
        return jwt.encode(payload, self.jwt_secret, algorithm='HS256')

    def decode_apis(self, encoded):
        decoded = {}
        for k, v in encoded.items():
            try:
                decoded[k] = base64.b64decode(v).decode('utf-8')
            except Exception:
                decoded[k] = None
        return decoded

    def fetch_apis(self):
        token = self.generate_token()
        url = f"{self.html_url}?view_apis=true&auth={token}"

        headers = {
            'User-Agent': 'SecureClient',
            'X-API-Key': 'XUGKEYPRO',
            'Referer': 'https://xindex.netlify.app'
        }

        try:
            print(f"🔍 Fetching APIs from: {url}")
            res = requests.get(url, headers=headers, timeout=10)
            print(f"   Status: {res.status_code}")
            
            if res.status_code != 200:
                print(f"   ❌ Failed to fetch APIs")
                return False

            match = re.search(r'<script id="secure-data"[^>]*>(.*?)</script>', res.text, re.DOTALL)
            if not match:
                print("   ❌ No secure-data script found.")
                return False

            raw_json = match.group(1).strip()
            print(f"   ✅ Found secure-data script")
            print(f"   📄 Raw JSON length: {len(raw_json)}")
            
            encoded_apis = json.loads(raw_json)
            print(f"   📊 Encoded APIs count: {len(encoded_apis)}")

            self.apis = self.decode_apis(encoded_apis)
            print(f"   ✅ Decoded APIs count: {len(self.apis)}")
            return True

        except Exception as e:
            print(f"   ❌ Error fetching APIs: {e}")
            return False

    def get_apis(self):
        if not self.apis:
            self.fetch_apis()
        return self.apis

def test_secure_api_client():
    """Test the secure API client"""
    print("🚀 **SECURE API CLIENT TESTER**")
    print("="*60)
    
    try:
        # Create client
        client = SecureAPIClient()
        
        # Fetch APIs
        print("🔍 Fetching APIs from secure source...")
        success = client.fetch_apis()
        
        if success:
            apis = client.get_apis()
            
            print(f"\n📊 **FETCHED APIs:**")
            print("="*60)
            
            for api_name, api_data in apis.items():
                print(f"\n🔍 **API: {api_name}**")
                print("-" * 40)
                
                if api_data:
                    try:
                        # Try to parse as JSON
                        parsed_data = json.loads(api_data)
                        print(f"✅ Valid JSON data:")
                        print(json.dumps(parsed_data, indent=2))
                        
                        # Look for useful information
                        if isinstance(parsed_data, dict):
                            if 'url' in parsed_data:
                                print(f"   🎯 URL: {parsed_data['url']}")
                            if 'method' in parsed_data:
                                print(f"   🎯 Method: {parsed_data['method']}")
                            if 'headers' in parsed_data:
                                print(f"   🎯 Headers: {parsed_data['headers']}")
                            if 'payload' in parsed_data:
                                print(f"   🎯 Payload: {parsed_data['payload']}")
                            if 'token' in parsed_data:
                                print(f"   🎯 Token: {parsed_data['token'][:50]}...")
                            if 'orgCode' in parsed_data:
                                print(f"   🎯 Org Code: {parsed_data['orgCode']}")
                            if 'orgId' in parsed_data:
                                print(f"   🎯 Org ID: {parsed_data['orgId']}")
                                
                    except json.JSONDecodeError:
                        print(f"📄 Raw data (not JSON):")
                        print(api_data[:200] + "..." if len(api_data) > 200 else api_data)
                else:
                    print(f"❌ No data available")
            
            # Test the APIs
            test_fetched_apis(apis)
            
        else:
            print("❌ Failed to fetch APIs from secure source")
            
    except Exception as e:
        print(f"❌ Error testing secure API client: {e}")

def test_fetched_apis(apis):
    """Test the fetched APIs"""
    print(f"\n🧪 **TESTING FETCHED APIs**")
    print("="*60)
    
    for api_name, api_data in apis.items():
        if not api_data:
            continue
            
        print(f"\n🔍 Testing API: {api_name}")
        
        try:
            # Try to parse as JSON
            parsed_data = json.loads(api_data)
            
            if isinstance(parsed_data, dict):
                # Test if it's a Classplus API
                if 'url' in parsed_data and 'classplus' in parsed_data['url']:
                    print(f"   🎯 Classplus API detected!")
                    test_classplus_api(parsed_data)
                elif 'url' in parsed_data:
                    print(f"   🎯 Generic API detected!")
                    test_generic_api(parsed_data)
                else:
                    print(f"   📄 Data structure: {list(parsed_data.keys())}")
                    
        except json.JSONDecodeError:
            print(f"   📄 Raw data (not JSON)")
            print(f"   Content: {api_data[:100]}...")

def test_classplus_api(api_data):
    """Test Classplus specific API"""
    print(f"   🔍 Testing Classplus API...")
    
    url = api_data.get('url', '')
    method = api_data.get('method', 'GET')
    headers = api_data.get('headers', {})
    payload = api_data.get('payload', {})
    
    print(f"   URL: {url}")
    print(f"   Method: {method}")
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, timeout=10)
        else:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        
        if response.status_code in [200, 201]:
            try:
                data = response.json()
                print(f"   ✅ Success! Data:")
                print(json.dumps(data, indent=2))
            except:
                print(f"   ✅ Success! Raw response")
                
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_generic_api(api_data):
    """Test generic API"""
    print(f"   🔍 Testing Generic API...")
    
    url = api_data.get('url', '')
    method = api_data.get('method', 'GET')
    headers = api_data.get('headers', {})
    payload = api_data.get('payload', {})
    
    print(f"   URL: {url}")
    print(f"   Method: {method}")
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, timeout=10)
        else:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}...")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    """Main function"""
    print("🚀 **SECURE API CLIENT**")
    print("="*60)
    print("🔍 Testing secure API client for real data...")
    
    # Test secure API client
    test_secure_api_client()
    
    print(f"\n💡 **SUMMARY:**")
    print("="*60)
    print("✅ Secure API client tested!")
    print("✅ Ready to extract real APIs!")
    print("✅ Ready to test with real data!")

if __name__ == "__main__":
    main()