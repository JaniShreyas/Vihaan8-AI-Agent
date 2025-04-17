from seleniumwire import webdriver
from selenium.webdriver.firefox.options import Options
import time

# Module-level Selenium driver for reuse
_driver = None

def init_driver(headless: bool = True) -> webdriver.Firefox:
    """
    Initialize a Selenium Wire Firefox driver (singleton).
    Subsequent calls return the same driver instance.
    """
    global _driver
    if _driver is None:
        firefox_options = Options()
        if headless:
            firefox_options.add_argument('--headless')
        firefox_options.add_argument('--disable-gpu')
        firefox_options.add_argument('--no-sandbox')

        seleniumwire_options = {
            'enable_har': True,
            'enable_har_cookies': True
        }

        _driver = webdriver.Firefox(options=firefox_options, seleniumwire_options=seleniumwire_options)
        _driver.get("localhost:8888")
        time.sleep(3)
    return _driver

def get_driver() -> webdriver.Firefox:
    """
    Retrieve the initialized driver. Raises if not yet initialized.
    """
    if _driver is None:
        init_driver()
        
    return _driver