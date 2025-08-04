#!/usr/bin/env python3
"""
Decode and analyze the main session token from the Extractor code
"""

import base64
import json
import jwt
from datetime import datetime

def decode_jwt_token(token):
    """Decode JWT token without verification"""
    try:
        # Split the token
        parts = token.split('.')
        if len(parts) != 3:
            print("❌ Invalid JWT token format")
            return None
        
        # Decode header
        header = parts[0]
        header += '=' * (4 - len(header) % 4)
        header_decoded = base64.b64decode(header).decode('utf-8')
        header_json = json.loads(header_decoded)
        
        # Decode payload
        payload = parts[1]
        payload += '=' * (4 - len(payload) % 4)
        payload_decoded = base64.b64decode(payload).decode('utf-8')
        payload_json = json.loads(payload_decoded)
        
        return {
            'header': header_json,
            'payload': payload_json,
            'signature': parts[2]
        }
    except Exception as e:
        print(f"❌ Error decoding token: {e}")
        return None

def analyze_extractor_token():
    """Analyze the main session token from Extractor"""
    
    # Main session token from direct_user_token.py
    session_token = "eyJhbGciOiJIUzM4NCIsInR5cCI6IkpXVCJ9.eyJzb3VyY2UiOjUwLCJzb3VyY2VfYXBwIjoiY2xhc3NwbHVzIiwic2Vzc2lvbl9pZCI6IjhkZTBmZTcyLTQ1NjEtNGNiYy04NjZhLTYzMjUyMTkwMTg2MyIsInZpc2l0b3JfaWQiOiJjMWFhM2IwNS03ZjlhLTRlZjktOTI1My0zNzRhM2RjMmYxZWYiLCJjcmVhdGVkX2F0IjoxNzU0MjI4MjIwNTQzLCJpYXQiOjE3NTQyMjgyMjAsImV4cCI6MTc1NTUyNDIyMH0.eKG1pqT0Ws6Dbb7LUzpHRjevH4Wi33Si-H2zLyEyuXCdhTc5kcK8cNnjm4XPSlaT"
    
    print("🔍 **EXTRACTOR SESSION TOKEN ANALYSIS**")
    print("=" * 60)
    
    print(f"📊 **Token Details:**")
    print(f"   Length: {len(session_token)} characters")
    print(f"   Format: JWT (JSON Web Token)")
    
    # Decode the token
    decoded = decode_jwt_token(session_token)
    
    if decoded:
        print(f"\n📊 **JWT Header:**")
        for key, value in decoded['header'].items():
            print(f"   {key}: {value}")
        
        print(f"\n📊 **JWT Payload:**")
        for key, value in decoded['payload'].items():
            if key in ['iat', 'exp', 'created_at']:
                # Convert timestamp to readable date
                try:
                    timestamp = int(value)
                    date = datetime.fromtimestamp(timestamp)
                    print(f"   {key}: {value} ({date.strftime('%Y-%m-%d %H:%M:%S')})")
                except:
                    print(f"   {key}: {value}")
            else:
                print(f"   {key}: {value}")
        
        print(f"\n📊 **Token Analysis:**")
        
        # Analyze source
        source = decoded['payload'].get('source', 'N/A')
        source_app = decoded['payload'].get('source_app', 'N/A')
        print(f"   Source: {source}")
        print(f"   Source App: {source_app}")
        
        # Analyze session info
        session_id = decoded['payload'].get('session_id', 'N/A')
        visitor_id = decoded['payload'].get('visitor_id', 'N/A')
        print(f"   Session ID: {session_id}")
        print(f"   Visitor ID: {visitor_id}")
        
        # Analyze timestamps
        iat = decoded['payload'].get('iat', 0)
        exp = decoded['payload'].get('exp', 0)
        created_at = decoded['payload'].get('created_at', 0)
        
        if iat:
            iat_date = datetime.fromtimestamp(iat)
            print(f"   Issued At: {iat_date.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if exp:
            exp_date = datetime.fromtimestamp(exp)
            print(f"   Expires At: {exp_date.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Check if expired
            now = datetime.now()
            if exp_date < now:
                print(f"   ⚠️  TOKEN IS EXPIRED!")
            else:
                days_left = (exp_date - now).days
                print(f"   ✅ Token valid for {days_left} more days")
        
        if created_at:
            created_date = datetime.fromtimestamp(created_at)
            print(f"   Created At: {created_date.strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"\n📊 **Security Analysis:**")
        print(f"   Algorithm: {decoded['header'].get('alg', 'N/A')}")
        print(f"   Token Type: {decoded['header'].get('typ', 'N/A')}")
        print(f"   Signature Length: {len(decoded['signature'])} characters")
        
        # Check if it's a Classplus token
        if source_app == 'classplus':
            print(f"   ✅ This is a Classplus session token")
        
        print(f"\n📊 **Usage Context:**")
        print(f"   This token is used for:")
        print(f"   - Authenticating API requests to Classplus")
        print(f"   - Accessing course content")
        print(f"   - User session management")
        print(f"   - API version: 52 (as seen in headers)")
        
    else:
        print("❌ Failed to decode token")

def main():
    analyze_extractor_token()

if __name__ == "__main__":
    main()