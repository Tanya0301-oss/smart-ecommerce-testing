import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urljoin, urlparse
from config.config import Config
import time

class BrokenLinksDetector:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.test_results = []
        self.checked_links = set()
    
    def log_test_result(self, test_name, passed, message):
        """Log test result with details"""
        result = {
            "module": "Broken Links",
            "test_name": test_name,
            "status": "PASS" if passed else "FAIL",
            "message": message,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)
    
    def is_valid_url(self, url):
        """Check if URL is valid and should be tested"""
        parsed = urlparse(url)
        if not parsed.netloc:
            return False
        if parsed.scheme not in ['http', 'https']:
            return False
        return True
    
    def check_link_status(self, url):
        """Check HTTP status of a link"""
        try:
            response = requests.head(url, timeout=10, allow_redirects=True)
            return response.status_code
        except requests.RequestException:
            return None
    
    def scan_website(self):
        """Scan website for broken links"""
        try:
            self.driver.get(Config.BASE_URL)
            all_links = self.driver.find_elements(By.TAG_NAME, "a")
            
            broken_links = []
            checked_count = 0
            
            for link in all_links[:50]:  # Limit to 50 links for demo
                try:
                    href = link.get_attribute('href')
                    if href and href not in self.checked_links and self.is_valid_url(href):
                        self.checked_links.add(href)
                        status_code = self.check_link_status(href)
                        
                        if status_code and status_code >= 400:
                            broken_links.append(f"{href} (Status: {status_code})")
                        
                        checked_count += 1
                        time.sleep(0.5)  # Be polite to the server
                        
                except Exception as e:
                    continue
            
            if not broken_links:
                self.log_test_result("Broken Links Scan", True, 
                                   f"Scanned {checked_count} links, no broken links found")
            else:
                self.log_test_result("Broken Links Scan", False,
                                   f"Found {len(broken_links)} broken links: {', '.join(broken_links[:5])}")
                
        except Exception as e:
            self.log_test_result("Broken Links Scan", False, f"Link scanning failed: {str(e)}")
        
        finally:
            self.driver.quit()
        
        return self.test_results