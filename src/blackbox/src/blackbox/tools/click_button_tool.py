from typing import Type, Literal
from pydantic import BaseModel, Field
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from crewai.tools import BaseTool
from .driver import get_driver
import src.blackbox.config.config as config
import json

class ClickButtonInput(BaseModel):
    """Input schema for ClickButtonTool (reuses existing driver)."""
    by: Literal['id', 'name', 'xpath', 'css_selector', 'class_name', 'tag_name', 'link_text', 'partial_link_text'] = \
        Field('id', description="Locator strategy to find the button.")
    value: str = Field(..., description="The locator value (e.g. the id or CSS selector).")

har_data_list = []

class ClickButtonTool(BaseTool):
    name: str = "click_button"
    description: str = (
        "Clicks a button on the currently open page in a persistent Selenium session. "
        "Initialize the session with init_driver() elsewhere in your agent startup."
        "Give priority to using XPATH, but if that doesn't work, try all other approaches until one works or you have used all"
        "Make sure your first action is to click the Signup button"
        "Example by = XPATH, //button[span[text()='Signup']] to go to the signup page"
    )
    args_schema: Type[BaseModel] = ClickButtonInput

    def _run(self, by: str, value: str) -> str:
        # Ensure driver is ready
        driver = get_driver()

        # Locator mapping
        by_map = {
            'id': By.ID,
            'name': By.NAME,
            'xpath': By.XPATH,
            'css_selector': By.CSS_SELECTOR,
            'class_name': By.CLASS_NAME,
            'tag_name': By.TAG_NAME,
            'link_text': By.LINK_TEXT,
            'partial_link_text': By.PARTIAL_LINK_TEXT,
        }
        locator = by_map.get(by)
        if locator is None:
            return f"Unsupported locator strategy: {by}"

        try:
            element = driver.find_element(locator, value)
            element.click()
            
            with open(config.HAR_DUMP_FILE_PATH, 'a') as f:
                json.dump(driver.har, f)
                f.write("\n")

            return f"Successfully clicked element by {by}='{value}' Current URL: {driver.current_url}."
        
        except Exception as e:
            return f"Error clicking element: {str(e)}"

    async def _arun(self, *args, **kwargs) -> str:
        raise NotImplementedError("ClickButtonTool does not support async yet.")
