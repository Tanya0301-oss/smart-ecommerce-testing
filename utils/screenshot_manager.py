import os
from datetime import datetime
from config.config import Config

class ScreenshotManager:
    def __init__(self, driver):
        self.driver = driver
    
    def capture_screenshot(self, test_name):
        """Capture screenshot and save with descriptive name"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{timestamp}.png"
        filepath = os.path.join(Config.SCREENSHOT_DIR, filename)
        
        self.driver.save_screenshot(filepath)
        return filepath