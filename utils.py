from scipy.optimize import direct
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support.wait import WebDriverWait


def wait_for_page_elements_to_load_by(driver, elementIdentifier, elementValue, seconds):
    try:
        WebDriverWait(driver=driver, timeout=seconds).until(
            EC.presence_of_element_located((elementIdentifier, elementValue))
        )
        return driver.find_elements(elementIdentifier, elementValue)
    finally:
        pass