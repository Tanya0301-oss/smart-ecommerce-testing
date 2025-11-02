import time

def wait_for_element(driver, by, value, timeout=10):
    """Wait for element to be present and visible"""
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, value))
    )

def highlight_element(driver, element):
    """Highlight a web element for debugging"""
    driver.execute_script(
        "arguments[0].style.border='3px solid red'", element
    )