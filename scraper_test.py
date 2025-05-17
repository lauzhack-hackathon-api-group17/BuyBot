from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from time import sleep
import random

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

# Set up the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://www.digitec.ch/fr/s1/producttype/ordinateur-portable-6")

print("Web page opened successfully.")

# Wait for the initial content to load
sleep(random.uniform(2, 5))

# Try to click the "Afficher plus" button once
try:
    # Wait for the "Afficher plus" button to be clickable
    show_more_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Afficher plus de produits']")

    # Scroll to the button
    driver.execute_script("arguments[0].scrollIntoView(true);", show_more_button)

    # Click the button using JavaScript
    driver.execute_script("arguments[0].click();", show_more_button)

    print("Clicked 'Afficher plus' button")

except Exception as e:
    print(f"Error clicking 'Afficher plus' button: {str(e)}")

# Wait for 30 seconds to allow new content to load
sleep(30)

# Close the browser
driver.quit()
