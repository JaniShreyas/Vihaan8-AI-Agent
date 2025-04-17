from typing import Type, Literal
from pydantic import BaseModel, Field, HttpUrl
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from crewai.tools import BaseTool
from .driver import get_driver

class GetPageInput(BaseModel):
    """Input schema for GetPageTool."""
    url: HttpUrl = Field(..., description="The URL of the page to retrieve.")

class GetPageTool(BaseTool):
    name: str = "get_page"
    description: str = (
        "Goes to the given url and returns the page "
    )
    args_schema: Type[BaseModel] = GetPageInput

    def _run(self, url: str) -> str:
        url_str = str(url)
        driver = get_driver()
        try:
            driver.get(url_str)
            page_source = driver.page_source
            return page_source
        except Exception as e:
            return f"Error retrieving {url_str}: {str(e)}"