#!/usr/bin/env python3
"""
Get PDF URLs using content IDs from RAS PRELIMS COURSE
"""

import requests
import json
import re
import asyncio
import aiohttp
import base64
import time

class PDFURLByIDExtractor:
    def __init__(self):
        self.classplus_apis = {
            "course_preview": "https://api.classplusapp.com/v2/course/preview/similar/{token}",
            "course_content": "https://api.classplusapp.com/v2/course/preview/content/list/{Batch_Token}",
            "org_info": "https://api.classplusapp.com/v2/course/preview/org/info",
            "content_details": "https://api.classplusapp.com/v2/course/preview/content/details/{content_id}",
            "document_download": "https://api.classplusapp.com/v2/course/preview/document/download/{content_id}"
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

    async def get_content_details(self, content_id):
        """Get detailed content information including URL"""
        url = f"https://api.classplusapp.com/v2/course/preview/content/details/{content_id}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.classplus_headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('data', {})
                    else:
                        print(f"❌ Failed to get content details: {response.status}")
                        return {}
                        
        except Exception as e:
            print(f"❌ Error getting content details: {e}")
            return {}

    async def get_document_download_url(self, content_id):
        """Get document download URL"""
        url = f"https://api.classplusapp.com/v2/course/preview/document/download/{content_id}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.classplus_headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('data', {}).get('url')
                    else:
                        print(f"❌ Failed to get download URL: {response.status}")
                        return None
                        
        except Exception as e:
            print(f"❌ Error getting download URL: {e}")
            return None

    async def extract_pdfs_with_ids_recursively(self, batch_token, folder_id=0, depth=0):
        """Recursively extract PDFs with their IDs"""
        pdfs = []
        indent = "  " * depth
        
        try:
            contents = await self.get_course_content(batch_token, folder_id)
            
            for content in contents:
                content_type = content.get('contentType')
                name = content.get('name', '')
                content_id = content.get('id')
                
                # Type 3 = PDF/Document
                if content_type == 3:
                    pdfs.append({
                        'name': name,
                        'id': content_id,
                        'folder_depth': depth,
                        'content_type': content_type,
                        'format': content.get('format', ''),
                        'documentDownloadFlag': content.get('documentDownloadFlag', 0),
                        'documentSecurityFlag': content.get('documentSecurityFlag', 0),
                        'pdfDownloadOnWeb': content.get('pdfDownloadOnWeb', 0),
                        'pdfSecuirityOnWeb': content.get('pdfSecuirityOnWeb', 0)
                    })
                    print(f"{indent}📄 PDF Found: {name} (ID: {content_id})")
                
                # Check if it's a folder (contentType == 1)
                elif content_type == 1:
                    folder_id = content.get('id')
                    if folder_id:
                        print(f"{indent}📁 Entering folder: {name} (ID: {folder_id})")
                        # Recursively get folder contents
                        folder_pdfs = await self.extract_pdfs_with_ids_recursively(batch_token, folder_id, depth + 1)
                        pdfs.extend(folder_pdfs)
                        print(f"{indent}📁 Exiting folder: {name}")
            
        except Exception as e:
            print(f"{indent}❌ Error in folder {folder_id}: {e}")
        
        return pdfs

    async def get_pdf_urls_by_ids(self, pdfs):
        """Get PDF URLs using content IDs"""
        pdfs_with_urls = []
        
        for pdf in pdfs:
            content_id = pdf['id']
            name = pdf['name']
            
            print(f"🔍 Getting URL for: {name} (ID: {content_id})")
            
            # Try content details API
            details = await self.get_content_details(content_id)
            if details:
                url = details.get('url') or details.get('downloadUrl') or details.get('fileUrl')
                if url:
                    pdf['url'] = url
                    pdf['url_source'] = 'content_details'
                    pdfs_with_urls.append(pdf)
                    print(f"   ✅ URL found via content details: {url[:50]}...")
                    continue
            
            # Try document download API
            download_url = await self.get_document_download_url(content_id)
            if download_url:
                pdf['url'] = download_url
                pdf['url_source'] = 'document_download'
                pdfs_with_urls.append(pdf)
                print(f"   ✅ URL found via document download: {download_url[:50]}...")
                continue
            
            # If no URL found, still add to list for reference
            pdf['url'] = None
            pdf['url_source'] = 'not_found'
            pdfs_with_urls.append(pdf)
            print(f"   ❌ No URL found for: {name}")
        
        return pdfs_with_urls

    async def extract_ras_pre_pdfs_with_urls(self, org_code="Uievjh"):
        """Main function to extract RAS PRE PDFs with URLs using IDs"""
        print("🚀 **RAS PRE PDF URL EXTRACTOR (BY ID)**")
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
                            
                            # Extract PDFs with IDs recursively
                            print(f"📝 Step 5: Extracting PDFs with IDs...")
                            pdfs = await self.extract_pdfs_with_ids_recursively(batch_token)
                            
                            if pdfs:
                                print(f"\n🎉 **FOUND {len(pdfs)} PDFs WITH IDs:**")
                                print("=" * 60)
                                
                                # Get URLs using IDs
                                print(f"📝 Step 6: Getting URLs using content IDs...")
                                pdfs_with_urls = await self.get_pdf_urls_by_ids(pdfs)
                                
                                # Save to file
                                filename = f"ras_pre_pdfs_with_urls_by_id_{int(time.time())}.txt"
                                with open(filename, 'w', encoding='utf-8') as f:
                                    f.write(f"RAS PRELIMS COURSE - PDFs with URLs (by ID)\n")
                                    f.write(f"Extracted on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                                    f.write(f"Total PDFs: {len(pdfs_with_urls)}\n")
                                    f.write(f"=" * 60 + "\n\n")
                                    
                                    for i, pdf in enumerate(pdfs_with_urls, 1):
                                        f.write(f"{i}. {pdf['name']}\n")
                                        f.write(f"   Content ID: {pdf['id']}\n")
                                        f.write(f"   Format: {pdf['format']}\n")
                                        f.write(f"   Download Flag: {pdf['documentDownloadFlag']}\n")
                                        f.write(f"   Security Flag: {pdf['documentSecurityFlag']}\n")
                                        f.write(f"   PDF Download on Web: {pdf['pdfDownloadOnWeb']}\n")
                                        f.write(f"   PDF Security on Web: {pdf['pdfSecuirityOnWeb']}\n")
                                        if pdf['url']:
                                            f.write(f"   URL: {pdf['url']}\n")
                                            f.write(f"   URL Source: {pdf['url_source']}\n")
                                        else:
                                            f.write(f"   URL: Not found\n")
                                        f.write(f"\n")
                                
                                print(f"\n💾 Saved to: {filename}")
                                
                                # Show summary
                                urls_found = sum(1 for pdf in pdfs_with_urls if pdf['url'])
                                print(f"\n📊 **SUMMARY:**")
                                print(f"   Total PDFs found: {len(pdfs_with_urls)}")
                                print(f"   PDFs with URLs: {urls_found}")
                                print(f"   PDFs without URLs: {len(pdfs_with_urls) - urls_found}")
                                
                            else:
                                print("❌ No PDFs found in content")
                        else:
                            print(f"❌ Failed to get batch token: {response.status}")
                            
            except Exception as e:
                print(f"❌ Error getting course content: {e}")

async def main():
    extractor = PDFURLByIDExtractor()
    await extractor.extract_ras_pre_pdfs_with_urls()

if __name__ == "__main__":
    asyncio.run(main())