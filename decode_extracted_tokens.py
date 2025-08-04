#!/usr/bin/env python3
"""
Decode and analyze the tokens extracted from Classplus system
"""

import json
import base64
import time
from datetime import datetime

class TokenAnalyzer:
    def __init__(self):
        # Tokens we extracted from our analysis
        self.tokens = {
            "hash_token": "eyJ0dXRvcklkIjpudWxsLCJvcmdJZCI6NzYzMzIwLCJjYXRlZ2orySWQiOm51bGx9",
            "batch_token": "eyJjb3Vyc2VJZCI6IjY5NzE5NzIiLCJ0dXRvcklkIjpudWxsLCJvcmdJZCI6NzYzMzIwLCJjYXRlZ2orySWQiOm51bGx9",
            "content_ids": [
                "64802601", "64802602", "65257383", "65257384",  # Rajasthan History
                "65284784", "65284785", "65284786", "65284787",  # Polity Hindi
                "65284789", "65284788", "65284790", "65284791",  # Polity English
                "64832254", "64832253", "64832251", "65567922", "64832252",  # Polity Notes
                "64497224", "64916220", "64938807",  # Art & Culture
                "64213446", "64213447", "64595465", "64595466",  # Economy
                "65611991",  # Maths
                "65572498", "65572497", "65572499", "65572500", "65572501",  # Eco Survey Hindi
                "65572502", "65572503", "65572504", "65572505", "65572506",
                "65572507", "65572509", "65572508", "65572510", "65572511",  # Eco Survey English
                "65572512", "65572513", "65572514", "65572515", "65572516",
                "65660314", "65660315",  # Current Affairs April
                "65660316", "65660317",  # Current Affairs May
                "65660318", "65660319",  # Current Affairs June
                "65660329", "65660328", "65660330", "65660331", "65660332"  # Practice Questions
            ]
        }

    def decode_base64(self, token):
        """Decode base64 token"""
        try:
            # Add padding if needed
            padding = 4 - (len(token) % 4)
            if padding != 4:
                token += "=" * padding
            
            decoded = base64.b64decode(token).decode('utf-8')
            return decoded
        except Exception as e:
            return f"Error decoding: {e}"

    def analyze_hash_token(self):
        """Analyze the hash token"""
        print("🔍 **HASH TOKEN ANALYSIS**")
        print("=" * 50)
        
        hash_token = self.tokens["hash_token"]
        print(f"Hash Token: {hash_token}")
        
        # Try to decode
        decoded = self.decode_base64(hash_token)
        print(f"Decoded: {decoded}")
        
        # Try to parse as JSON
        try:
            data = json.loads(decoded)
            print("\n📊 **Token Structure:**")
            for key, value in data.items():
                print(f"   {key}: {value}")
        except:
            print("Not valid JSON format")

    def analyze_batch_token(self):
        """Analyze the batch token"""
        print("\n🔍 **BATCH TOKEN ANALYSIS**")
        print("=" * 50)
        
        batch_token = self.tokens["batch_token"]
        print(f"Batch Token: {batch_token}")
        
        # Try to decode
        decoded = self.decode_base64(batch_token)
        print(f"Decoded: {decoded}")
        
        # Try to parse as JSON
        try:
            data = json.loads(decoded)
            print("\n📊 **Token Structure:**")
            for key, value in data.items():
                print(f"   {key}: {value}")
        except:
            print("Not valid JSON format")

    def analyze_content_ids(self):
        """Analyze content IDs"""
        print("\n🔍 **CONTENT IDS ANALYSIS**")
        print("=" * 50)
        
        content_ids = self.tokens["content_ids"]
        print(f"Total Content IDs: {len(content_ids)}")
        
        # Group by ranges
        ranges = {}
        for cid in content_ids:
            prefix = cid[:2]  # First 2 digits
            if prefix not in ranges:
                ranges[prefix] = []
            ranges[prefix].append(cid)
        
        print("\n📊 **Content ID Ranges:**")
        for prefix, ids in sorted(ranges.items()):
            print(f"   Range {prefix}xx: {len(ids)} IDs")
            print(f"      Examples: {ids[:3]}")
        
        # Analyze patterns
        print("\n📊 **Pattern Analysis:**")
        print(f"   Smallest ID: {min(content_ids)}")
        print(f"   Largest ID: {max(content_ids)}")
        print(f"   ID Length: {len(content_ids[0])} digits")

    def analyze_token_patterns(self):
        """Analyze token patterns"""
        print("\n🔍 **TOKEN PATTERN ANALYSIS**")
        print("=" * 50)
        
        hash_token = self.tokens["hash_token"]
        batch_token = self.tokens["batch_token"]
        
        print("📊 **Token Characteristics:**")
        print(f"   Hash Token Length: {len(hash_token)} characters")
        print(f"   Batch Token Length: {len(batch_token)} characters")
        print(f"   Hash Token starts with: {hash_token[:20]}...")
        print(f"   Batch Token starts with: {batch_token[:20]}...")
        
        # Check if they're JWT tokens
        if hash_token.count('.') == 2:
            print("   Hash Token: Appears to be JWT format")
        if batch_token.count('.') == 2:
            print("   Batch Token: Appears to be JWT format")

    def generate_token_info(self):
        """Generate comprehensive token information"""
        print("🚀 **COMPLETE TOKEN ANALYSIS**")
        print("=" * 60)
        
        self.analyze_hash_token()
        self.analyze_batch_token()
        self.analyze_content_ids()
        self.analyze_token_patterns()
        
        # Save detailed analysis
        filename = f"token_analysis_{int(time.time())}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("CLASSPLUS TOKEN ANALYSIS\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            f.write("HASH TOKEN:\n")
            f.write(f"Token: {self.tokens['hash_token']}\n")
            f.write(f"Decoded: {self.decode_base64(self.tokens['hash_token'])}\n\n")
            
            f.write("BATCH TOKEN:\n")
            f.write(f"Token: {self.tokens['batch_token']}\n")
            f.write(f"Decoded: {self.decode_base64(self.tokens['batch_token'])}\n\n")
            
            f.write("CONTENT IDS:\n")
            for i, cid in enumerate(self.tokens['content_ids'], 1):
                f.write(f"{i:2d}. {cid}\n")
            
            f.write(f"\nTotal Content IDs: {len(self.tokens['content_ids'])}\n")
        
        print(f"\n💾 Detailed analysis saved to: {filename}")

def main():
    analyzer = TokenAnalyzer()
    analyzer.generate_token_info()

if __name__ == "__main__":
    main()