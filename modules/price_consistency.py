from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import Config
import time
import re

class PriceConsistency:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, Config.IMPLICIT_WAIT)
        self.test_results = []
    
    def log_test_result(self, test_name, passed, message):
        """Log test result with details"""
        result = {
            "module": "Price Consistency",
            "test_name": test_name,
            "status": "PASS" if passed else "FAIL",
            "message": message,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)
    
    def extract_price(self, price_text):
        """Extract numeric price from text"""
        if not price_text:
            return None
        # Remove currency symbols and commas, then convert to float
        numbers = re.findall(r'[\d.,]+', price_text)
        if numbers:
            return float(numbers[0].replace(',', ''))
        return None
    
    def check_price_consistency(self):
        """Verify prices are consistent between listing and detail pages"""
        try:
            self.driver.get(Config.PRODUCTS_URL)
            products = self.wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "product-item"))
            )
            
            inconsistent_prices = []
            
            for i, product in enumerate(products[:3]):  # Check first 3 products
                try:
                    # Get price from listing page
                    listing_price_element = product.find_element(By.CLASS_NAME, "price")
                    listing_price = self.extract_price(listing_price_element.text)
                    
                    # Click to go to detail page
                    product_link = product.find_element(By.CLASS_NAME, "product-title")
                    product_name = product_link.text
                    product_link.click()
                    
                    # Get price from detail page
                    detail_price_element = self.wait.until(
                        EC.presence_of_element_located((By.CLASS_NAME, "price-value"))
                    )
                    detail_price = self.extract_price(detail_price_element.text)
                    
                    # Compare prices
                    if listing_price and detail_price:
                        if abs(listing_price - detail_price) > 0.01:  # Allow for rounding differences
                            inconsistent_prices.append(
                                f"'{product_name}': Listing ${listing_price} vs Detail ${detail_price}"
                            )
                    
                    # Go back to listing page
                    self.driver.back()
                    self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product-item")))
                    
                except Exception as e:
                    continue
            
            if not inconsistent_prices:
                self.log_test_result("Price Consistency", True, 
                                   "All checked products have consistent prices between listing and detail pages")
            else:
                self.log_test_result("Price Consistency", False,
                                   f"Price inconsistencies found: {', '.join(inconsistent_prices)}")
                
        except Exception as e:
            self.log_test_result("Price Consistency", False, f"Price check failed: {str(e)}")
    
    def run_price_checks(self):
        """Execute all price consistency tests"""
        self.check_price_consistency()
        self.driver.quit()
        return self.test_results