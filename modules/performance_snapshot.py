from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config.config import Config
import time

class PerformanceSnapshot:
    def __init__(self):
        chrome_options = Options()
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        self.driver = webdriver.Chrome(options=chrome_options)
        self.test_results = []
    
    def log_test_result(self, test_name, passed, message):
        """Log test result with details"""
        result = {
            "module": "Performance",
            "test_name": test_name,
            "status": "PASS" if passed else "FAIL",
            "message": message,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)
    
    def measure_page_load_time(self, url, page_name):
        """Measure page load time for a specific URL"""
        try:
            start_time = time.time()
            self.driver.get(url)
            load_time = time.time() - start_time
            
            if load_time <= Config.ACCEPTABLE_LOAD_TIME:
                self.log_test_result(f"{page_name} Load Time", True, 
                                   f"Page loaded in {load_time:.2f}s (within acceptable limit)")
            elif load_time <= Config.MAX_PAGE_LOAD_TIME:
                self.log_test_result(f"{page_name} Load Time", True, 
                                   f"Page loaded in {load_time:.2f}s (slightly slow but acceptable)")
            else:
                self.log_test_result(f"{page_name} Load Time", False, 
                                   f"Page loaded in {load_time:.2f}s (exceeds maximum limit)")
            
            return load_time
            
        except Exception as e:
            self.log_test_result(f"{page_name} Load Time", False, f"Failed to measure load time: {str(e)}")
            return None
    
    def measure_performance(self):
        """Measure performance for critical pages"""
        pages_to_test = [
            (Config.BASE_URL, "Homepage"),
            (Config.PRODUCTS_URL, "Products Page"),
            (Config.LOGIN_URL, "Login Page")
        ]
        
        for url, page_name in pages_to_test:
            self.measure_page_load_time(url, page_name)
            time.sleep(2)  # Wait between requests
        
        self.driver.quit()
        return self.test_results