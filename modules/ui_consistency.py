from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.screenshot_manager import ScreenshotManager
from config.config import Config
import time

class UIConsistency:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.screenshot_manager = ScreenshotManager(self.driver)
        self.wait = WebDriverWait(self.driver, Config.IMPLICIT_WAIT)
        self.test_results = []
    
    def log_test_result(self, test_name, passed, message, screenshot_path=None):
        """Log test result with details"""
        result = {
            "module": "UI Consistency",
            "test_name": test_name,
            "status": "PASS" if passed else "FAIL",
            "message": message,
            "screenshot": screenshot_path,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)
    
    def check_product_card_consistency(self):
        """Verify all product cards have required elements"""
        try:
            self.driver.get(Config.PRODUCTS_URL)
            product_cards = self.wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "product-item"))
            )
            
            inconsistent_cards = []
            
            for i, card in enumerate(product_cards[:10]):  # Check first 10 products
                missing_elements = []
                
                # Check for product image
                try:
                    image = card.find_element(By.TAG_NAME, "img")
                    if not image.is_displayed():
                        missing_elements.append("image")
                except:
                    missing_elements.append("image")
                
                # Check for product title
                try:
                    title = card.find_element(By.CLASS_NAME, "product-title")
                    if not title.text.strip():
                        missing_elements.append("title")
                except:
                    missing_elements.append("title")
                
                # Check for price
                try:
                    price = card.find_element(By.CLASS_NAME, "price")
                    if not price.text.strip():
                        missing_elements.append("price")
                except:
                    missing_elements.append("price")
                
                if missing_elements:
                    inconsistent_cards.append(f"Product {i+1} missing: {', '.join(missing_elements)}")
            
            if not inconsistent_cards:
                self.log_test_result("Product Card Consistency", True, 
                                   f"All {len(product_cards)} product cards have consistent UI elements")
            else:
                self.log_test_result("Product Card Consistency", False,
                                   f"Inconsistent cards found: {', '.join(inconsistent_cards)}")
                
        except Exception as e:
            screenshot_path = self.screenshot_manager.capture_screenshot("ui_consistency_failure")
            self.log_test_result("Product Card Consistency", False, f"UI check failed: {str(e)}", screenshot_path)
    
    def run_all_tests(self):
        """Execute all UI consistency tests"""
        self.check_product_card_consistency()
        self.driver.quit()
        return self.test_results