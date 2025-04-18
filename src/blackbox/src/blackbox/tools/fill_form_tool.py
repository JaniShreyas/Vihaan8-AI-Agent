from typing import Type, List, Literal
from pydantic import BaseModel, Field
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from crewai.tools import BaseTool
from .driver import get_driver
import src.blackbox.config.config as config
import json


class FieldInput(BaseModel):
    """Represents a single input field to fill."""
    by: Literal[
        'id', 'xpath', 'css_selector', 'class_name', 
        'tag_name', 'link_text', 'partial_link_text'
    ] = Field('id', description="Locator strategy for this field.")
    name: str = Field(..., description="The locator value for the field.")
    value: str = Field(..., description="The text/value to enter into the field.")


class FillFormInput(BaseModel):
    """Input schema for FillFormTool."""
    fields: List[FieldInput] = Field(
        ..., description="List of fields to fill in the form."
    )
    submit: bool = Field(
        False, description="Whether to click the submit button after filling."
    )
    submit_by: Literal[
        'id', 'xpath', 'css_selector', 'class_name', 
        'tag_name', 'link_text', 'partial_link_text'
    ] = Field('xpath', description="Locator strategy for the submit button.")
    submit_locator: str = Field(
        '', description="The locator value for the submit button. Required if submit=True."
    )


class FillFormTool(BaseTool):
    name: str = "fill_form"
    description: str = (
        "Use single quotes wherever quotes are required"
        "Fills multiple input fields on the currently open page in a persistent Selenium session. "
        "Prioritize using by = id to identify fields"
        "Optionally clicks a submit button after populating all fields. "
        "Only give submit = True when you are certain you have filled all fields"
        "Start with trying to fill the Full Name field"
    )
    args_schema: Type[BaseModel] = FillFormInput

    def _run(self, fields: List[FieldInput], submit: bool, submit_by: str, submit_locator: str) -> str:
        driver = get_driver()

        # Mapping of locator strategies
        by_map = {
            'id': By.ID,
            'xpath': By.XPATH,
            'css_selector': By.CSS_SELECTOR,
            'class_name': By.CLASS_NAME,
            'tag_name': By.TAG_NAME,
            'link_text': By.LINK_TEXT,
            'partial_link_text': By.PARTIAL_LINK_TEXT,
        }

        try:
            # Fill each field
            for field in fields:
                locator_strategy = by_map.get(field.by)
                if not locator_strategy:
                    return f"Unsupported locator strategy for field: {field.by}"

                elem = driver.find_element(locator_strategy, field.name)
                elem.clear()
                elem.send_keys(field.value)

            # Optionally submit form
            if submit:
                submit_strategy = by_map.get(submit_by)
                if not submit_strategy:
                    return f"Unsupported locator strategy for submit button: {submit_by}"
                submit_elem = driver.find_element(submit_strategy, submit_locator)
                submit_elem.click()

            # Dump HAR data
            with open(config.HAR_DUMP_FILE_PATH, 'a') as f:
                json.dump(driver.har, f)
                f.write("\n")

            msg = f"Successfully filled {len(fields)} fields."
            if submit:
                msg += f" Submitted form via {submit_by}='{submit_locator}'."
            msg += f" Current URL: {driver.current_url}."
            return msg

        except Exception as e:
            return f"Error filling form: {str(e)}"

    async def _arun(self, *args, **kwargs) -> str:
        raise NotImplementedError("FillFormTool does not support async yet.")