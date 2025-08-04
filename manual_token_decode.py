#!/usr/bin/env python3
"""
Manual token decoding to show exact details
"""

import base64
import json

def decode_token_manual(token):
    """Manually decode token with proper padding"""
    # Add padding
    if len(token) % 4 == 1:
        token += "==="
    elif len(token) % 4 == 2:
        token += "=="
    elif len(token) % 4 == 3:
        token += "="
    
    try:
        decoded = base64.b64decode(token).decode('utf-8')
        return decoded
    except Exception as e:
        return f"Error: {e}"

# Tokens from our extraction
hash_token = "eyJ0dXRvcklkIjpudWxsLCJvcmdJZCI6NzYzMzIwLCJjYXRlZ2orySWQiOm51bGx9"
batch_token = "eyJjb3Vyc2VJZCI6IjY5NzE5NzIiLCJ0dXRvcklkIjpudWxsLCJvcmdJZCI6NzYzMzIwLCJjYXRlZ2orySWQiOm51bGx9"

print("🔍 **TOKEN DETAILS ANALYSIS**")
print("=" * 60)

print("\n📊 **HASH TOKEN:**")
print(f"Original: {hash_token}")
print(f"Length: {len(hash_token)} characters")
print(f"Padding needed: {4 - (len(hash_token) % 4)}")

# Try different padding approaches
print("\n🔧 **Decoding attempts:**")

# Method 1: Add 3 padding
token1 = hash_token + "==="
try:
    decoded1 = base64.b64decode(token1).decode('utf-8')
    print(f"Method 1 (add ===): {decoded1}")
    try:
        data1 = json.loads(decoded1)
        print("✅ Valid JSON:")
        for key, value in data1.items():
            print(f"   {key}: {value}")
    except:
        print("❌ Not valid JSON")
except Exception as e:
    print(f"❌ Method 1 failed: {e}")

# Method 2: Add 2 padding
token2 = hash_token + "=="
try:
    decoded2 = base64.b64decode(token2).decode('utf-8')
    print(f"Method 2 (add ==): {decoded2}")
    try:
        data2 = json.loads(decoded2)
        print("✅ Valid JSON:")
        for key, value in data2.items():
            print(f"   {key}: {value}")
    except:
        print("❌ Not valid JSON")
except Exception as e:
    print(f"❌ Method 2 failed: {e}")

# Method 3: Add 1 padding
token3 = hash_token + "="
try:
    decoded3 = base64.b64decode(token3).decode('utf-8')
    print(f"Method 3 (add =): {decoded3}")
    try:
        data3 = json.loads(decoded3)
        print("✅ Valid JSON:")
        for key, value in data3.items():
            print(f"   {key}: {value}")
    except:
        print("❌ Not valid JSON")
except Exception as e:
    print(f"❌ Method 3 failed: {e}")

print("\n📊 **BATCH TOKEN:**")
print(f"Original: {batch_token}")
print(f"Length: {len(batch_token)} characters")
print(f"Padding needed: {4 - (len(batch_token) % 4)}")

# Try different padding approaches for batch token
print("\n🔧 **Decoding attempts:**")

# Method 1: Add 3 padding
btoken1 = batch_token + "==="
try:
    bdecoded1 = base64.b64decode(btoken1).decode('utf-8')
    print(f"Method 1 (add ===): {bdecoded1}")
    try:
        bdata1 = json.loads(bdecoded1)
        print("✅ Valid JSON:")
        for key, value in bdata1.items():
            print(f"   {key}: {value}")
    except:
        print("❌ Not valid JSON")
except Exception as e:
    print(f"❌ Method 1 failed: {e}")

# Method 2: Add 2 padding
btoken2 = batch_token + "=="
try:
    bdecoded2 = base64.b64decode(btoken2).decode('utf-8')
    print(f"Method 2 (add ==): {bdecoded2}")
    try:
        bdata2 = json.loads(bdecoded2)
        print("✅ Valid JSON:")
        for key, value in bdata2.items():
            print(f"   {key}: {value}")
    except:
        print("❌ Not valid JSON")
except Exception as e:
    print(f"❌ Method 2 failed: {e}")

# Method 3: Add 1 padding
btoken3 = batch_token + "="
try:
    bdecoded3 = base64.b64decode(btoken3).decode('utf-8')
    print(f"Method 3 (add =): {bdecoded3}")
    try:
        bdata3 = json.loads(bdecoded3)
        print("✅ Valid JSON:")
        for key, value in bdata3.items():
            print(f"   {key}: {value}")
    except:
        print("❌ Not valid JSON")
except Exception as e:
    print(f"❌ Method 3 failed: {e}")

print("\n📊 **CONTENT IDS SUMMARY:**")
content_ids = [
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

print(f"Total Content IDs: {len(content_ids)}")
print(f"Range: {min(content_ids)} to {max(content_ids)}")
print(f"All IDs are 8 digits long")

# Group by first 2 digits
ranges = {}
for cid in content_ids:
    prefix = cid[:2]
    if prefix not in ranges:
        ranges[prefix] = []
    ranges[prefix].append(cid)

print("\n📊 **Content ID Ranges:**")
for prefix, ids in sorted(ranges.items()):
    print(f"   {prefix}xx: {len(ids)} IDs")