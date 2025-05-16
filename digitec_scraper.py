from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://www.digitec.ch/fr/s1/producttype/ordinateur-portable-6")

print("Web page opened successfully.")
sleep(3)

# Function to process laptop articles
def process_laptops():
    # Find all laptop articles within the grid
    laptop_articles = driver.find_elements(By.CSS_SELECTOR, "div.yj6YNQW2 article.yArygEf2")
    print(f"Found {len(laptop_articles)} laptop articles")

    # Iterate through each laptop article
    for index, article in enumerate(laptop_articles):
        try:
            # Find the laptop type link that contains "Ordinateur portable"
            laptop_type_links = article.find_elements(By.CSS_SELECTOR, "a.yArygEfA")
            is_portable = False
            for link in laptop_type_links:
                if "Ordinateur portable" in link.text:
                    is_portable = True
                    break

            if is_portable:
                # Extract the laptop name/model from the aria-label attribute
                try:
                    laptop_info_element = article.find_element(By.CSS_SELECTOR, "a[aria-label]")
                    laptop_name = laptop_info_element.get_attribute("aria-label")
                    print(f"Laptop #{index+1}: {laptop_name}")
                except NoSuchElementException:
                    print(f"Laptop #{index+1}: Could not find laptop name")
        except Exception as e:
            print(f"Error processing laptop #{index+1}: {str(e)}")

# Process initial laptops
process_laptops()

# Loop to click "Afficher plus" button
while True:
    try:
        # Wait for the "Afficher plus" button to be clickable
        show_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Afficher plus de produits']"))
        )

        # Scroll to the button
        driver.execute_script("arguments[0].scrollIntoView(true);", show_more_button)

        # Click the button using JavaScript
        driver.execute_script("arguments[0].click();", show_more_button)

        print("Clicked 'Afficher plus' button")

        # Wait for new laptops to load
        sleep(5)

        # Get the number of laptops before processing
        initial_laptop_count = len(driver.find_elements(By.CSS_SELECTOR, "div.yj6YNQW2 article.yArygEf2"))

        # Process the newly loaded laptops
        process_laptops()

        # Get the number of laptops after processing
        new_laptop_count = len(driver.find_elements(By.CSS_SELECTOR, "div.yj6YNQW2 article.yArygEf2"))

        # If no new laptops are loaded, break the loop
        if new_laptop_count == initial_laptop_count:
            print("No new laptops loaded")
            break

    except NoSuchElementException:
        print("No more 'Afficher plus' button found")
        break
    except ElementClickInterceptedException:
        print("Element click intercepted, trying JavaScript click")
        try:
            driver.execute_script("arguments[0].click();", show_more_button)
            sleep(5)
            process_laptops()
        except Exception as e:
            print(f"Error clicking 'Afficher plus' button with JavaScript: {str(e)}")
            break
    except Exception as e:
        print(f"Error clicking 'Afficher plus' button: {str(e)}")
        break

# Close the browser
sleep(2)
driver.quit()
