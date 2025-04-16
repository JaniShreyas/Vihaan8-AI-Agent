from seleniumwire import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import time

def count_buttons(url, headless=True):
    """
    Visit a webpage and count the number of buttons present.
    
    Args:
        url (str): The URL of the webpage to analyze
        headless (bool): Whether to run Firefox in headless mode
        
    Returns:
        int: The number of button elements found on the page
    """
    # Set up Firefox options
    firefox_options = Options()
    if headless:
        firefox_options.add_argument("--headless")
    
    # Initialize the WebDriver
    driver = webdriver.Firefox(options=firefox_options)
    
    try:
        print(f"Navigating to {url}...")
        driver.get(url)
        
        # Give the page time to fully load
        time.sleep(3)
        
        # Find all button elements (both <button> tags and input buttons)
        button_elements = driver.find_elements(By.TAG_NAME, "button")
        input_buttons = driver.find_elements(By.XPATH, "//input[@type='button' or @type='submit' or @type='reset']")
        
        total_buttons = len(button_elements) + len(input_buttons)
        
        print(f"Found {total_buttons} button elements on {url}")
        print(f"- {len(button_elements)} <button> elements")
        print(f"- {len(input_buttons)} <input> button elements")
        
        return total_buttons
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return -1
    
    finally:
        driver.quit()

if __name__ == "__main__":
    # Example usage
    target_url = "localhost:8888"
    count_buttons(target_url)