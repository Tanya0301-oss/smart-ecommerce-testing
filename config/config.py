import os
from datetime import datetime

class Config:
    # Browser Configuration
    BROWSER = "chrome"
    HEADLESS = False
    IMPLICIT_WAIT = 10
    PAGE_LOAD_TIMEOUT = 30
    
    # Test URLs - Using demo e-commerce site
    BASE_URL = "https://demo.nopcommerce.com"
    LOGIN_URL = f"{BASE_URL}/login"
    PRODUCTS_URL = f"{BASE_URL}/electronics"
    SEARCH_URL = f"{BASE_URL}/search"
    
    # Test Credentials - You'll need to register these first or use guest checkout
    TEST_EMAIL = "test@example.com"  # Update with actual registered email
    TEST_PASSWORD = "test123"        # Update with actual password
    
    # Performance Thresholds
    MAX_PAGE_LOAD_TIME = 5
    ACCEPTABLE_LOAD_TIME = 3
    
    # Paths
    SCREENSHOT_DIR = "screenshots"
    REPORT_DIR = "reports"
    
    # Test Data
    SEARCH_QUERY = "laptop"
    PRODUCT_CATEGORY = "electronics"
    
    # ChromeDriver path
    CHROME_DRIVER_PATH = "chromedriver.exe" if os.path.exists("chromedriver.exe") else None
    
    # Updated Element Selectors for demo.nopcommerce.com
    # Login Page Selectors
    LOGIN_EMAIL_SELECTOR = ( "id", "Email" )
    LOGIN_PASSWORD_SELECTOR = ( "id", "Password" )
    LOGIN_BUTTON_SELECTOR = ( "xpath", "//button[contains(@class, 'login-button')]" )
    LOGIN_SUCCESS_SELECTOR = ( "class name", "ico-account" )
    
    # Search Selectors
    SEARCH_BOX_SELECTOR = ( "id", "small-searchterms" )
    SEARCH_BUTTON_SELECTOR = ( "xpath", "//button[contains(text(), 'Search')]" )
    SEARCH_RESULTS_SELECTOR = ( "class name", "product-item" )
    
    # Product Selectors
    PRODUCT_TITLE_SELECTOR = ( "class name", "product-title" )
    PRODUCT_PRICE_SELECTOR = ( "class name", "price" )
    PRODUCT_IMAGE_SELECTOR = ( "xpath", ".//img" )
    
    # Cart Selectors
    ADD_TO_CART_BUTTON_SELECTOR = ( "xpath", "//input[@value='Add to cart']" )
    CART_SUCCESS_SELECTOR = ( "xpath", "//p[contains(text(), 'The product has been added to your')]" )
    
    # Navigation Selectors
    ACCOUNT_LINK_SELECTOR = ( "class name", "ico-account" )
    LOGOUT_LINK_SELECTOR = ( "class name", "ico-logout" )

    @classmethod
    def setup_directories(cls):
        os.makedirs(cls.SCREENSHOT_DIR, exist_ok=True)
        os.makedirs(cls.REPORT_DIR, exist_ok=True)