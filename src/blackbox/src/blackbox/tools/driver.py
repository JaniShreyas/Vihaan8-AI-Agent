from seleniumwire import webdriver
from selenium.webdriver.firefox.options import Options

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
        _driver = webdriver.Firefox(options=firefox_options)
        _driver.get("localhost:8888")
    return _driver

def get_driver() -> webdriver.Firefox:
    """
    Retrieve the initialized driver. Raises if not yet initialized.
    """
    if _driver is None:
        raise RuntimeError("Selenium driver not initialized. Call init_driver() first.")
    return _driver