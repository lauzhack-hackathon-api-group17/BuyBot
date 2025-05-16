from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep
import random
from selenium.common.exceptions import NoSuchElementException, TimeoutException

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

def process_laptops(start_index):
    try:
        laptop_articles = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.yj6YNQW2 article.yArygEf2"))
        )
        print(f"Found {len(laptop_articles)} laptop articles")

        for index, article in enumerate(laptop_articles[start_index:], start=start_index + 1):
            try:
                laptop_type_links = article.find_elements(By.CSS_SELECTOR, "a.yArygEfA")
                is_portable = False
                for link in laptop_type_links:
                    if "Ordinateur portable" in link.text:
                        is_portable = True
                        break

                if is_portable:
                    try:
                        laptop_info_element = article.find_element(By.CSS_SELECTOR, "a[aria-label]")
                        laptop_name = laptop_info_element.get_attribute("aria-label")
                        print(f"Laptop #{index}: {laptop_name}")
                    except NoSuchElementException:
                        print(f"Laptop #{index}: Could not find laptop name")
            except Exception as e:
                print(f"Error processing laptop #{index}: {str(e)}")

        return len(laptop_articles)
    except Exception as e:
        print(f"Error in process_laptops: {str(e)}")
        return start_index

start_index = 0
total_laptops = process_laptops(start_index)

max_clicks = 5  # Set the maximum number of times to click the button
click_count = 0

while click_count < max_clicks:
    try:
        # Wait for the "Afficher plus" button to be clickable
        show_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Afficher plus de produits']"))
        )

        driver.execute_script("arguments[0].scrollIntoView(true);", show_more_button)

        driver.execute_script("arguments[0].click();", show_more_button)

        print(f"Clicked 'Afficher plus' button {click_count + 1} times")
        sleep(random.uniform(3, 7))
        new_total_laptops = process_laptops(start_index)
        if new_total_laptops > total_laptops:
            start_index = total_laptops
            total_laptops = new_total_laptops
        else:
            print("No new laptops loaded")
            break

        click_count += 1

    except TimeoutException:
        print("'Afficher plus' button not found or not clickable")
        break
    except Exception as e:
        print(f"Error clicking 'Afficher plus' button: {str(e)}")
        break

sleep(2)
driver.quit()
