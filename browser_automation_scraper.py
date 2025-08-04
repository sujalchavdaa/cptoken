#!/usr/bin/env python3
"""
Browser Automation & Web Scraping for Classplus PDF Downloads
"""

import time
import json
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import requests
from urllib.parse import urlparse, parse_qs

class ClassplusBrowserScraper:
    def __init__(self):
        self.download_folder = "browser_downloaded_pdfs"
        self.org_code = "Uievjh"
        self.course_url = f"https://{self.org_code}.courses.store"
        
        # Create download folder
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
            print(f"📁 Created download folder: {self.download_folder}")
        
        # Setup Chrome options
        self.chrome_options = Options()
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Download preferences
        prefs = {
            "download.default_directory": os.path.abspath(self.download_folder),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        self.chrome_options.add_experimental_option("prefs", prefs)
        
        self.driver = None

    def setup_driver(self):
        """Setup Chrome driver"""
        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("✅ Chrome driver setup successful")
            return True
        except Exception as e:
            print(f"❌ Failed to setup Chrome driver: {e}")
            return False

    def navigate_to_course(self):
        """Navigate to the course page"""
        try:
            print(f"🌐 Navigating to: {self.course_url}")
            self.driver.get(self.course_url)
            
            # Wait for page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            print("✅ Course page loaded successfully")
            
            # Get page title
            title = self.driver.title
            print(f"📄 Page title: {title}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to navigate to course: {e}")
            return False

    def find_course_links(self):
        """Find course links on the page"""
        try:
            print("🔍 Searching for course links...")
            
            # Look for course cards/links
            course_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                "a[href*='course'], .course-card, .course-item, [data-course-id]")
            
            courses = []
            for element in course_elements:
                try:
                    href = element.get_attribute('href')
                    text = element.text.strip()
                    if href and 'course' in href.lower():
                        courses.append({
                            'url': href,
                            'title': text,
                            'element': element
                        })
                        print(f"   📚 Found course: {text[:50]}...")
                except:
                    continue
            
            print(f"✅ Found {len(courses)} course links")
            return courses
            
        except Exception as e:
            print(f"❌ Error finding course links: {e}")
            return []

    def click_on_ras_course(self, courses):
        """Click on RAS PRE course if found"""
        try:
            print("🔍 Looking for RAS PRE course...")
            
            for course in courses:
                title = course['title'].lower()
                if 'ras' in title and ('pre' in title or 'prelims' in title):
                    print(f"🎯 Found RAS course: {course['title']}")
                    print(f"   Clicking on: {course['url']}")
                    
                    # Click on the course
                    course['element'].click()
                    
                    # Wait for page to load
                    time.sleep(3)
                    
                    print("✅ Clicked on RAS course")
                    return True
            
            print("❌ RAS PRE course not found")
            return False
            
        except Exception as e:
            print(f"❌ Error clicking on RAS course: {e}")
            return False

    def find_pdf_elements(self):
        """Find PDF elements on the course page"""
        try:
            print("🔍 Searching for PDF elements...")
            
            # Wait for content to load
            time.sleep(5)
            
            # Look for PDF elements
            pdf_selectors = [
                "a[href*='.pdf']",
                "a[href*='document']",
                "a[href*='download']",
                ".pdf-item",
                ".document-item",
                "[data-content-type='3']",
                ".content-item"
            ]
            
            pdf_elements = []
            for selector in pdf_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    pdf_elements.extend(elements)
                except:
                    continue
            
            # Remove duplicates
            unique_elements = []
            seen_urls = set()
            
            for element in pdf_elements:
                try:
                    href = element.get_attribute('href')
                    if href and href not in seen_urls:
                        seen_urls.add(href)
                        unique_elements.append(element)
                except:
                    continue
            
            print(f"✅ Found {len(unique_elements)} PDF elements")
            return unique_elements
            
        except Exception as e:
            print(f"❌ Error finding PDF elements: {e}")
            return []

    def extract_pdf_info(self, pdf_elements):
        """Extract PDF information from elements"""
        pdfs = []
        
        for i, element in enumerate(pdf_elements):
            try:
                href = element.get_attribute('href')
                text = element.text.strip()
                title = element.get_attribute('title') or text
                
                if href:
                    pdfs.append({
                        'index': i + 1,
                        'title': title,
                        'url': href,
                        'element': element
                    })
                    print(f"   📄 {i+1}. {title[:50]}...")
                    print(f"      URL: {href[:80]}...")
                
            except Exception as e:
                print(f"   ❌ Error extracting PDF {i+1}: {e}")
                continue
        
        return pdfs

    def download_pdfs_browser(self, pdfs):
        """Download PDFs using browser automation"""
        print(f"\n🚀 **BROWSER PDF DOWNLOAD**")
        print("=" * 50)
        print(f"📁 Download folder: {self.download_folder}")
        print(f"📄 Total PDFs to download: {len(pdfs)}")
        
        successful_downloads = 0
        failed_downloads = 0
        
        for i, pdf in enumerate(pdfs, 1):
            try:
                print(f"\n📄 [{i}/{len(pdfs)}] Downloading: {pdf['title']}")
                print(f"   URL: {pdf['url'][:80]}...")
                
                # Click on PDF element to trigger download
                pdf['element'].click()
                
                # Wait for download to start
                time.sleep(3)
                
                # Check if file was downloaded
                downloaded_files = os.listdir(self.download_folder)
                if downloaded_files:
                    print(f"✅ Download successful")
                    successful_downloads += 1
                else:
                    print(f"❌ Download failed")
                    failed_downloads += 1
                
                # Small delay between downloads
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Error downloading {pdf['title']}: {e}")
                failed_downloads += 1
        
        print(f"\n📊 **DOWNLOAD SUMMARY:**")
        print("=" * 40)
        print(f"✅ Successful downloads: {successful_downloads}")
        print(f"❌ Failed downloads: {failed_downloads}")
        print(f"📁 Files saved in: {self.download_folder}")
        
        return successful_downloads, failed_downloads

    def scrape_page_source(self):
        """Scrape page source for PDF URLs"""
        try:
            print("🔍 Scraping page source for PDF URLs...")
            
            page_source = self.driver.page_source
            
            # Look for PDF URLs in page source
            pdf_url_patterns = [
                r'https?://[^"\s]*\.pdf[^"\s]*',
                r'https?://[^"\s]*document[^"\s]*',
                r'https?://[^"\s]*download[^"\s]*',
                r'"url":"([^"]*\.pdf[^"]*)"',
                r'"downloadUrl":"([^"]*)"',
                r'"fileUrl":"([^"]*)"'
            ]
            
            found_urls = []
            for pattern in pdf_url_patterns:
                matches = re.findall(pattern, page_source, re.IGNORECASE)
                found_urls.extend(matches)
            
            # Remove duplicates
            unique_urls = list(set(found_urls))
            
            print(f"✅ Found {len(unique_urls)} PDF URLs in page source")
            for i, url in enumerate(unique_urls[:10], 1):  # Show first 10
                print(f"   {i}. {url[:80]}...")
            
            return unique_urls
            
        except Exception as e:
            print(f"❌ Error scraping page source: {e}")
            return []

    def download_pdfs_direct(self, pdf_urls):
        """Download PDFs directly using requests"""
        print(f"\n🚀 **DIRECT PDF DOWNLOAD**")
        print("=" * 50)
        
        successful_downloads = 0
        failed_downloads = 0
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        for i, url in enumerate(pdf_urls, 1):
            try:
                print(f"\n📄 [{i}/{len(pdf_urls)}] Downloading from: {url[:80]}...")
                
                # Get filename from URL
                filename = os.path.basename(urlparse(url).path)
                if not filename.endswith('.pdf'):
                    filename = f"pdf_{i}.pdf"
                
                filepath = os.path.join(self.download_folder, filename)
                
                # Download file
                response = requests.get(url, headers=headers, stream=True)
                
                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    print(f"✅ Downloaded: {filename}")
                    successful_downloads += 1
                else:
                    print(f"❌ Download failed: {response.status_code}")
                    failed_downloads += 1
                
                time.sleep(1)  # Small delay
                
            except Exception as e:
                print(f"❌ Error downloading {url}: {e}")
                failed_downloads += 1
        
        print(f"\n📊 **DIRECT DOWNLOAD SUMMARY:**")
        print("=" * 40)
        print(f"✅ Successful downloads: {successful_downloads}")
        print(f"❌ Failed downloads: {failed_downloads}")
        
        return successful_downloads, failed_downloads

    def run_scraping(self):
        """Main scraping function"""
        print("🚀 **BROWSER AUTOMATION & WEB SCRAPING**")
        print("=" * 60)
        
        # Setup driver
        if not self.setup_driver():
            return
        
        try:
            # Navigate to course
            if not self.navigate_to_course():
                return
            
            # Find course links
            courses = self.find_course_links()
            
            # Click on RAS course
            if courses:
                if not self.click_on_ras_course(courses):
                    print("⚠️  RAS course not found, continuing with current page...")
            
            # Find PDF elements
            pdf_elements = self.find_pdf_elements()
            
            if pdf_elements:
                # Extract PDF info
                pdfs = self.extract_pdf_info(pdf_elements)
                
                # Download PDFs using browser
                browser_success, browser_failed = self.download_pdfs_browser(pdfs)
                
                print(f"\n📊 Browser download results: {browser_success} success, {browser_failed} failed")
            
            # Scrape page source for direct URLs
            pdf_urls = self.scrape_page_source()
            
            if pdf_urls:
                # Download PDFs directly
                direct_success, direct_failed = self.download_pdfs_direct(pdf_urls)
                
                print(f"\n📊 Direct download results: {direct_success} success, {direct_failed} failed")
            
            print(f"\n🎉 **SCRAPING COMPLETE**")
            print("=" * 40)
            print(f"📁 Check folder: {self.download_folder}")
            
        except Exception as e:
            print(f"❌ Error during scraping: {e}")
        
        finally:
            # Close browser
            if self.driver:
                self.driver.quit()
                print("🔒 Browser closed")

def main():
    scraper = ClassplusBrowserScraper()
    scraper.run_scraping()

if __name__ == "__main__":
    main()