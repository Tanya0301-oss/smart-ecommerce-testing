from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os

def quick_test_fixed():
    try:
        print("🚀 Running fixed quick test...")
        
        # Chrome options
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        
        # FORCE using manual chromedriver - skip webdriver-manager completely
        if os.path.exists("chromedriver.exe"):
            service = Service("chromedriver.exe")
            print("✅ Using manual chromedriver.exe from project folder")
        else:
            print("❌ chromedriver.exe not found in project folder")
            print("💡 Please make sure chromedriver.exe is in the same folder as this script")
            return False
        
        # Create driver
        driver = webdriver.Chrome(service=service, options=options)
        
        # Test basic navigation
        test_url = "https://demo.nopcommerce.com"
        print(f"🌐 Opening: {test_url}")
        driver.get(test_url)
        
        # Check title
        print(f"📄 Page title: {driver.title}")
        
        # Take screenshot
        driver.save_screenshot("quick_test_success.png")
        print("✅ Screenshot saved as 'quick_test_success.png'")
        
        # Wait a bit to see the page
        time.sleep(3)
        
        driver.quit()
        print("🎉 Quick test passed! You're ready to run the full suite.")
        return True
        
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        return False

if __name__ == "__main__":
    quick_test_fixed()