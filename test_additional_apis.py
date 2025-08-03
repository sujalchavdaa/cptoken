#!/usr/bin/env python3
"""
Test Additional APIs for Real Data
"""

import requests
import json
import time

def test_additional_apis():
    """Test additional APIs provided by user"""
    print("🔍 Testing Additional APIs for Real Data")
    print("="*60)
    
    # Additional APIs to test (user can provide more)
    additional_apis = [
        {
            "name": "Alternative Classplus API",
            "url": "https://api.classplusapp.com/v2/orgs/getOrgId",
            "method": "POST",
            "payload": {"orgCode": "test"},
            "description": "Main Classplus API"
        },
        {
            "name": "Event API",
            "url": "https://event-api.classplusapp.com/analytics-api/v1/session/token",
            "method": "POST", 
            "payload": {"source": 50, "source_app": "classplus"},
            "description": "Event API for session tokens"
        },
        {
            "name": "Alternative User API",
            "url": "https://api.classplusapp.com/v2/users/verify",
            "method": "POST",
            "payload": {
                "otp": "123456",
                "countryExt": "91",
                "sessionId": "test",
                "orgId": 1,
                "fingerprintId": "dummy",
                "email": "test@example.com"
            },
            "description": "User verification API"
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
    
    results = []
    
    for api in additional_apis:
        print(f"\n🔍 Testing: {api['name']}")
        print(f"   URL: {api['url']}")
        print(f"   Description: {api['description']}")
        
        try:
            if api['method'] == 'GET':
                response = requests.get(api['url'], headers=headers, timeout=10)
            else:
                response = requests.post(api['url'], json=api['payload'], headers=headers, timeout=10)
            
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:300]}...")
            
            if response.status_code in [200, 201]:
                try:
                    data = response.json()
                    print(f"   ✅ Success! Response data:")
                    print(json.dumps(data, indent=2))
                    
                    # Check for useful data
                    if isinstance(data, dict):
                        if 'data' in data:
                            print(f"   🎯 Found data section")
                        if 'token' in data:
                            print(f"   🎯 Found token: {data['token'][:50]}...")
                        if 'orgId' in data:
                            print(f"   🎯 Found org ID: {data['orgId']}")
                    
                    results.append({
                        "api": api['name'],
                        "status": "success",
                        "data": data
                    })
                    
                except Exception as e:
                    print(f"   ❌ Error parsing JSON: {e}")
                    results.append({
                        "api": api['name'],
                        "status": "error",
                        "error": str(e)
                    })
            else:
                print(f"   ❌ Failed with status {response.status_code}")
                results.append({
                    "api": api['name'],
                    "status": "failed",
                    "status_code": response.status_code
                })
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({
                "api": api['name'],
                "status": "error",
                "error": str(e)
            })
    
    return results

def analyze_results(results):
    """Analyze API test results"""
    print("\n📊 **API TEST RESULTS ANALYSIS:**")
    print("="*60)
    
    successful_apis = [r for r in results if r['status'] == 'success']
    failed_apis = [r for r in results if r['status'] == 'failed']
    error_apis = [r for r in results if r['status'] == 'error']
    
    print(f"✅ Successful APIs: {len(successful_apis)}")
    print(f"❌ Failed APIs: {len(failed_apis)}")
    print(f"⚠️ Error APIs: {len(error_apis)}")
    
    if successful_apis:
        print(f"\n🎉 **SUCCESSFUL APIs:**")
        for api in successful_apis:
            print(f"   • {api['api']}")
            if 'data' in api:
                data = api['data']
                if 'token' in data:
                    print(f"     - Token found: {data['token'][:50]}...")
                if 'orgId' in data:
                    print(f"     - Org ID: {data['orgId']}")
    
    if failed_apis:
        print(f"\n❌ **FAILED APIs:**")
        for api in failed_apis:
            print(f"   • {api['api']} (Status: {api['status_code']})")
    
    if error_apis:
        print(f"\n⚠️ **ERROR APIs:**")
        for api in error_apis:
            print(f"   • {api['api']}: {api['error']}")

def main():
    """Main function"""
    print("🚀 **ADDITIONAL API TESTER**")
    print("="*60)
    print("🔍 Testing additional APIs for real data...")
    
    # Test additional APIs
    results = test_additional_apis()
    
    # Analyze results
    analyze_results(results)
    
    print(f"\n💡 **NEXT STEPS:**")
    print("="*60)
    print("✅ If you have more APIs, provide them!")
    print("✅ If any API works, we can extract real data!")
    print("✅ Ready to test with your provided APIs!")

if __name__ == "__main__":
    main()