#!/usr/bin/env python3
"""
Debug PDF structure to understand how Classplus stores PDF URLs
"""

import requests
import json
import re
import asyncio
import aiohttp
import base64
import time

class PDFStructureDebugger:
    def __init__(self):
        self.classplus_apis = {
            "course_preview": "https://api.classplusapp.com/v2/course/preview/similar/{token}",
            "course_content": "https://api.classplusapp.com/v2/course/preview/content/list/{Batch_Token}",
            "org_info": "https://api.classplusapp.com/v2/course/preview/org/info"
        }
        
        self.classplus_headers = {
            'accept-encoding': 'gzip',
            'accept-language': 'EN',
            'api-version': '35',
            'app-version': '1.4.73.2',
            'build-number': '35',
            'connection': 'Keep-Alive',
            'content-type': 'application/json',
            'device-details': 'Xiaomi_Redmi 7_SDK-32',
            'device-id': 'c28d3cb16bbdac01',
            'host': 'api.classplusapp.com',
            'region': 'IN',
            'user-agent': 'Mobile-Android',
            'webengage-luid': '00000187-6fe4-5d41-a530-26186858be4c'
        }
        
        self.hash_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://qsvfn.courses.store/?mainCategory=0&subCatList=[130504,62442]',
            'Sec-CH-UA': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
            'Sec-CH-UA-Mobile': '?0',
            'Sec-CH-UA-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        }

    async def get_hash_from_org_code(self, org_code):
        """Get hash from org code"""
        url = f"https://{org_code}.courses.store"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.hash_headers) as response:
                    if response.status == 200:
                        html_text = await response.text()
                        hash_match = re.search(r'"hash":"(.*?)"', html_text)
                        
                        if hash_match:
                            token = hash_match.group(1)
                            print(f"✅ Hash extracted: {token[:20]}...")
                            return token
                        else:
                            print(f"❌ Hash not found in HTML")
                            return None
                    else:
                        print(f"❌ Failed to get HTML: {response.status}")
                        return None
                        
        except Exception as e:
            print(f"❌ Error extracting hash: {e}")
            return None

    async def get_courses_from_hash(self, token, org_code):
        """Get courses from hash"""
        url = f"https://api.classplusapp.com/v2/course/preview/similar/{token}?limit=50"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.classplus_headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        courses = data.get('data', {}).get('coursesData', [])
                        return courses
                    else:
                        print(f"❌ Failed to get courses: {response.status}")
                        return []
                        
        except Exception as e:
            print(f"❌ Error getting courses: {e}")
            return []

    async def find_ras_pre_course(self, courses):
        """Find RAS PRE course from the list"""
        ras_courses = []
        
        for course in courses:
            name = course.get('name', '').lower()
            if 'ras' in name and ('pre' in name or 'prelims' in name):
                ras_courses.append(course)
        
        return ras_courses

    async def get_course_content(self, batch_token, folder_id=0):
        """Get course content including PDFs"""
        url = f"https://api.classplusapp.com/v2/course/preview/content/list/{batch_token}"
        params = {'folderId': folder_id, 'limit': 9999999999}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.classplus_headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        contents = data.get('data', [])
                        return contents
                    else:
                        print(f"❌ Failed to get content: {response.status}")
                        return []
                        
        except Exception as e:
            print(f"❌ Error getting content: {e}")
            return []

    async def debug_pdf_structure(self, batch_token, folder_id=0, depth=0):
        """Debug PDF structure to understand how URLs are stored"""
        indent = "  " * depth
        
        try:
            contents = await self.get_course_content(batch_token, folder_id)
            
            for content in contents:
                content_type = content.get('contentType')
                name = content.get('name', '')
                
                # Focus on PDFs (Type 3)
                if content_type == 3:
                    print(f"{indent}📄 PDF: {name}")
                    print(f"{indent}   Content Type: {content_type}")
                    print(f"{indent}   ID: {content.get('id')}")
                    print(f"{indent}   URL: {content.get('url')}")
                    print(f"{indent}   Thumbnail URL: {content.get('thumbnailUrl')}")
                    print(f"{indent}   All fields: {list(content.keys())}")
                    
                    # Show all non-None values
                    for key, value in content.items():
                        if value is not None and value != "":
                            print(f"{indent}   {key}: {value}")
                    
                    print(f"{indent}   " + "="*50)
                
                # Check if it's a folder (contentType == 1)
                elif content_type == 1:
                    folder_id = content.get('id')
                    if folder_id:
                        print(f"{indent}📁 Entering folder: {name} (ID: {folder_id})")
                        # Recursively debug folder contents
                        await self.debug_pdf_structure(batch_token, folder_id, depth + 1)
                        print(f"{indent}📁 Exiting folder: {name}")
            
        except Exception as e:
            print(f"{indent}❌ Error in folder {folder_id}: {e}")

    async def debug_ras_pre_pdf_structure(self, org_code="Uievjh"):
        """Main function to debug PDF structure"""
        print("🚀 **RAS PRE PDF STRUCTURE DEBUGGER**")
        print("=" * 60)
        
        # Step 1: Get hash
        print(f"📝 Step 1: Getting hash from {org_code}")
        token = await self.get_hash_from_org_code(org_code)
        if not token:
            print("❌ Failed to get hash")
            return
        
        # Step 2: Get courses
        print(f"📝 Step 2: Getting courses from hash")
        courses = await self.get_courses_from_hash(token, org_code)
        if not courses:
            print("❌ No courses found")
            return
        
        print(f"✅ Found {len(courses)} courses")
        
        # Step 3: Find RAS PRE courses
        print(f"📝 Step 3: Finding RAS PRE courses")
        ras_courses = await self.find_ras_pre_course(courses)
        
        if not ras_courses:
            print("❌ No RAS PRE courses found")
            return
        
        print(f"✅ Found {len(ras_courses)} RAS PRE courses:")
        for i, course in enumerate(ras_courses):
            print(f"   {i+1}. {course.get('name', 'Unknown')} - ₹{course.get('finalPrice', 0)}")
        
        # Step 4: Get content for first RAS course
        if ras_courses:
            selected_course = ras_courses[0]
            course_id = selected_course.get('id')
            course_name = selected_course.get('name', 'Unknown')
            
            print(f"📝 Step 4: Getting content for '{course_name}'")
            
            # Get batch token
            batch_headers = {
                'Accept': 'application/json, text/plain, */*',
                'region': 'IN',
                'accept-language': 'EN',
                'Api-Version': '22',
                'tutorWebsiteDomain': f'https://{org_code}.courses.store'
            }
            
            params = {'courseId': f'{course_id}'}
            
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://api.classplusapp.com/v2/course/preview/org/info", 
                                        params=params, headers=batch_headers) as response:
                        if response.status == 200:
                            data = await response.json()
                            batch_token = data['data']['hash']
                            app_name = data['data']['name']
                            
                            print(f"✅ Got batch token: {batch_token[:20]}...")
                            
                            # Debug PDF structure
                            print(f"📝 Step 5: Debugging PDF structure...")
                            await self.debug_pdf_structure(batch_token)
                            
                        else:
                            print(f"❌ Failed to get batch token: {response.status}")
                            
            except Exception as e:
                print(f"❌ Error getting course content: {e}")

async def main():
    debugger = PDFStructureDebugger()
    await debugger.debug_ras_pre_pdf_structure()

if __name__ == "__main__":
    asyncio.run(main())