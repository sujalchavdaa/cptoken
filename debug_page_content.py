#!/usr/bin/env python3
"""
Debug script to analyze Classplus page content
"""

import requests
import re
import json

class PageDebugger:
    def __init__(self):
        self.org_code = "Uievjh"
        self.base_url = f"https://{self.org_code}.courses.store"
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

    def get_page_content(self, url):
        """Get page content"""
        try:
            print(f"🌐 Fetching: {url}")
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Successfully fetched page")
                return response.text
            else:
                print(f"❌ Failed to fetch page: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error fetching page: {e}")
            return None

    def analyze_page_structure(self, html_content):
        """Analyze page structure"""
        print("\n🔍 **PAGE STRUCTURE ANALYSIS**")
        print("=" * 50)
        
        # Check page title
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
        if title_match:
            print(f"📄 Page Title: {title_match.group(1)}")
        
        # Check for meta tags
        meta_tags = re.findall(r'<meta[^>]+>', html_content)
        print(f"📊 Meta tags found: {len(meta_tags)}")
        
        # Check for script tags
        script_tags = re.findall(r'<script[^>]*>', html_content)
        print(f"📊 Script tags found: {len(script_tags)}")
        
        # Check for links
        link_tags = re.findall(r'<a[^>]+>', html_content)
        print(f"📊 Link tags found: {len(link_tags)}")
        
        # Check for divs with specific classes
        div_classes = re.findall(r'class=["\']([^"\']+)["\']', html_content)
        unique_classes = list(set(div_classes))
        print(f"📊 Unique CSS classes found: {len(unique_classes)}")
        
        # Show some interesting classes
        interesting_classes = [cls for cls in unique_classes if any(keyword in cls.lower() for keyword in ['course', 'pdf', 'document', 'content', 'download'])]
        print(f"📊 Interesting classes: {interesting_classes[:10]}")

    def extract_all_urls(self, html_content):
        """Extract all URLs from page"""
        print("\n🔍 **URL EXTRACTION**")
        print("=" * 50)
        
        # Find all URLs
        url_patterns = [
            r'href=["\']([^"\']+)["\']',
            r'src=["\']([^"\']+)["\']',
            r'url\(["\']?([^"\')\s]+)["\']?\)',
            r'https?://[^\s"\'<>]+'
        ]
        
        all_urls = []
        for pattern in url_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            all_urls.extend(matches)
        
        # Remove duplicates
        unique_urls = list(set(all_urls))
        print(f"📊 Total unique URLs found: {len(unique_urls)}")
        
        # Categorize URLs
        course_urls = [url for url in unique_urls if 'course' in url.lower()]
        pdf_urls = [url for url in unique_urls if 'pdf' in url.lower()]
        document_urls = [url for url in unique_urls if 'document' in url.lower()]
        download_urls = [url for url in unique_urls if 'download' in url.lower()]
        
        print(f"📊 Course URLs: {len(course_urls)}")
        print(f"📊 PDF URLs: {len(pdf_urls)}")
        print(f"📊 Document URLs: {len(document_urls)}")
        print(f"📊 Download URLs: {len(download_urls)}")
        
        # Show some examples
        if course_urls:
            print(f"\n📚 Course URL examples:")
            for i, url in enumerate(course_urls[:5], 1):
                print(f"   {i}. {url}")
        
        if pdf_urls:
            print(f"\n📄 PDF URL examples:")
            for i, url in enumerate(pdf_urls[:5], 1):
                print(f"   {i}. {url}")
        
        return unique_urls

    def extract_json_data(self, html_content):
        """Extract and analyze JSON data"""
        print("\n🔍 **JSON DATA EXTRACTION**")
        print("=" * 50)
        
        # Look for JSON data
        json_patterns = [
            r'window\.__INITIAL_STATE__\s*=\s*({[^;]+});',
            r'window\.data\s*=\s*({[^;]+});',
            r'window\.courses\s*=\s*({[^;]+});',
            r'window\.content\s*=\s*({[^;]+});',
            r'<script[^>]*>([^<]*window[^<]*)</script>',
            r'<script[^>]*>([^<]*courses[^<]*)</script>',
            r'<script[^>]*>([^<]*content[^<]*)</script>',
            r'<script[^>]*>([^<]*data[^<]*)</script>'
        ]
        
        json_data_found = []
        for pattern in json_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            for match in matches:
                try:
                    # Try to find JSON objects in the match
                    json_objects = re.findall(r'\{[^{}]*\}', match)
                    for obj in json_objects:
                        try:
                            data = json.loads(obj)
                            json_data_found.append(data)
                            print(f"✅ Found JSON data with {len(data)} keys")
                        except:
                            continue
                except:
                    continue
        
        print(f"📊 Total JSON objects found: {len(json_data_found)}")
        
        # Analyze JSON data
        for i, data in enumerate(json_data_found):
            print(f"\n📊 JSON Object {i+1}:")
            print(f"   Keys: {list(data.keys())}")
            if 'courses' in data:
                print(f"   Courses: {len(data['courses'])}")
            if 'content' in data:
                print(f"   Content: {len(data['content'])}")

    def extract_script_content(self, html_content):
        """Extract and analyze script content"""
        print("\n🔍 **SCRIPT CONTENT ANALYSIS**")
        print("=" * 50)
        
        # Find all script tags
        script_pattern = r'<script[^>]*>([^<]*)</script>'
        scripts = re.findall(script_pattern, html_content, re.IGNORECASE)
        
        print(f"📊 Script tags found: {len(scripts)}")
        
        # Look for interesting content in scripts
        interesting_keywords = ['course', 'pdf', 'document', 'download', 'content', 'url', 'hash']
        
        for i, script in enumerate(scripts):
            if any(keyword in script.lower() for keyword in interesting_keywords):
                print(f"\n📊 Interesting Script {i+1}:")
                print(f"   Length: {len(script)} characters")
                print(f"   Keywords found: {[kw for kw in interesting_keywords if kw in script.lower()]}")
                print(f"   Preview: {script[:200]}...")

    def run_debug(self):
        """Main debug function"""
        print("🚀 **PAGE CONTENT DEBUGGER**")
        print("=" * 60)
        
        # Get page content
        html_content = self.get_page_content(self.base_url)
        if not html_content:
            print("❌ Failed to get page content")
            return
        
        # Save page content for analysis
        with open("debug_page_content.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("💾 Saved page content to: debug_page_content.html")
        
        # Analyze page structure
        self.analyze_page_structure(html_content)
        
        # Extract URLs
        urls = self.extract_all_urls(html_content)
        
        # Extract JSON data
        self.extract_json_data(html_content)
        
        # Extract script content
        self.extract_script_content(html_content)
        
        print(f"\n🎉 **DEBUG COMPLETE**")
        print("=" * 40)
        print("📁 Check debug_page_content.html for full page content")

def main():
    debugger = PageDebugger()
    debugger.run_debug()

if __name__ == "__main__":
    main()