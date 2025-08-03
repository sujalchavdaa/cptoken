import json
import base64
import time

def decode_session_token():
    """Decode the direct session token"""
    print("🔍 Decoding Direct Session Token...")
    print("="*60)
    
    # The direct session token we got
    token = "eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJzb3VyY2UiOjUwLCJzb3VyY2VfYXBwIjoiY2xhc3NwbHVzIiwic2Vzc2lvbl9pZCI6IjhkZTBmZTcyLTQ1NjEtNGNiYy04NjZhLTYzMjUyMTkwMTg2MyIsInZpc2l0b3JfaWQiOiJjMWFhM2IwNS03ZjlhLTRlZjktOTI1My0zNzRhM2RjMmYxZWYiLCJjcmVhdGVkX2F0IjoxNzU0MjI4MjIwNTQzLCJpYXQiOjE3NTQyMjgyMjAsImV4cCI6MTc1NTUyNDIyMH0.eKG1pqT0Ws6Dbb7LUzpHRjevH4Wi33Si-H2zLyEyuXCdhTc5kcK8cNnjm4XPSlaT"
    
    try:
        # Split the token into parts
        parts = token.split('.')
        
        if len(parts) != 3:
            print("❌ Invalid JWT token format")
            return
        
        # Decode header
        print("📋 HEADER:")
        print("-" * 30)
        header = parts[0]
        # Add padding if needed
        header += '=' * (4 - len(header) % 4)
        header_decoded = base64.b64decode(header).decode('utf-8')
        header_json = json.loads(header_decoded)
        print(json.dumps(header_json, indent=2))
        
        print("\n📋 PAYLOAD:")
        print("-" * 30)
        payload = parts[1]
        # Add padding if needed
        payload += '=' * (4 - len(payload) % 4)
        payload_decoded = base64.b64decode(payload).decode('utf-8')
        payload_json = json.loads(payload_decoded)
        
        # Pretty print with explanations
        print("🔑 Session Token Information:")
        print(f"   • Source: {payload_json.get('source', 'N/A')}")
        print(f"   • Source App: {payload_json.get('source_app', 'N/A')}")
        print(f"   • Session ID: {payload_json.get('session_id', 'N/A')}")
        print(f"   • Visitor ID: {payload_json.get('visitor_id', 'N/A')}")
        print(f"   • Created At: {payload_json.get('created_at', 'N/A')}")
        print(f"   • Issued At (iat): {payload_json.get('iat', 'N/A')}")
        print(f"   • Expires At (exp): {payload_json.get('exp', 'N/A')}")
        
        print("\n📊 Full Payload JSON:")
        print(json.dumps(payload_json, indent=2))
        
        # Calculate token validity
        if 'iat' in payload_json and 'exp' in payload_json:
            current_time = int(time.time())
            issued_at = payload_json['iat']
            expires_at = payload_json['exp']
            
            print(f"\n⏰ Token Timing:")
            print(f"   • Issued: {issued_at} (Unix timestamp)")
            print(f"   • Expires: {expires_at} (Unix timestamp)")
            print(f"   • Current: {current_time} (Unix timestamp)")
            
            if current_time < expires_at:
                remaining = expires_at - current_time
                days = remaining // 86400
                hours = (remaining % 86400) // 3600
                minutes = (remaining % 3600) // 60
                print(f"   • Status: ✅ VALID")
                print(f"   • Remaining: {days} days, {hours} hours, {minutes} minutes")
            else:
                print(f"   • Status: ❌ EXPIRED")
        
        print("\n🔐 SIGNATURE:")
        print("-" * 30)
        signature = parts[2]
        print(f"Signature: {signature[:50]}...")
        print("(Signature is used for token verification)")
        
        print("\n" + "="*60)
        print("📋 SUMMARY:")
        print("="*60)
        print(f"✅ Token Type: JWT (JSON Web Token)")
        print(f"✅ Algorithm: {header_json.get('alg', 'N/A')}")
        print(f"✅ Token Type: {header_json.get('typ', 'N/A')}")
        print(f"✅ Source: {payload_json.get('source', 'N/A')}")
        print(f"✅ App: {payload_json.get('source_app', 'N/A')}")
        print(f"✅ Session: {payload_json.get('session_id', 'N/A')[:20]}...")
        print(f"✅ Visitor: {payload_json.get('visitor_id', 'N/A')[:20]}...")
        
        # Additional analysis
        print(f"\n🔍 ANALYSIS:")
        print(f"   • This is a Classplus session token")
        print(f"   • Source 50 = Classplus official")
        print(f"   • Valid for API access")
        print(f"   • Can be used for Classplus APIs")
        print(f"   • 15 days validity period")
        
    except Exception as e:
        print(f"❌ Error decoding token: {e}")

if __name__ == "__main__":
    decode_session_token()