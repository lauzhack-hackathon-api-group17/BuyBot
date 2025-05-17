import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC, wait
import FinanceBot.utils as utils
import csv

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://www.digitec.ch/fr/s1/producttype/ordinateur-portable-6?filterGrid=expanded")


#get cpu:
utils.wait_for_page_elements_to_load_by(driver, By.XPATH, "//button[@aria-label='Type de processeur']", 10)
table = utils.wait_for_page_elements_to_load_by(driver, By.CLASS_NAME, "yd88NAO8", 10)[0]
rows = table.find_elements(By.TAG_NAME, "li")
with open("../scraped_lists/CPU.csv", "w") as file:
    writer = csv.writer(file)
    for row in rows:
        try:
            text = row.find_element(By.CLASS_NAME, "yx26KTL1").text
            print(text)
            writer.writerow([text])
        except:
            continue