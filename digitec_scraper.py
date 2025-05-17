from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import random

# Only these specific parameters we want to extract
TARGET_PARAMETERS = {
    "Fabricant": "Manufacturer",
    "Mémoire vive": "RAM",
    "Capacité SSD": "Storage",
    "Version du système d'exploitation": "OS Version",
    "Définition de l'écran": "Display Resolution",
    "Type de processeur": "CPU Type",
    "RAM max.": "Max RAM",
    "Poids": "Weight",
    "Système d'exploitation": "Operating System",
    "Architecture": "Architecture",
    "Longueur": "Length",
    "Largeur": "Width"
}

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")

# Set up the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://www.digitec.ch/fr/s1/producttype/ordinateur-portable-6")
print("Web page opened successfully.")
sleep(random.uniform(2, 5))

def extract_specs_from_detail_page():
    FRENCH_PARAMETERS = [
        "Famille de processeur",
        "Type de processeur",
        "Mémoire vive",
        "Capacité SSD",
        "Capacité totale",
        "Définition de l'écran",
        "Résolution de l'image",
        "Taille de l'écran",
        "Modèle de carte graphique (intégrée)",
        "Modèle de carte graphique (dédiée)",
        "Version du système d'exploitation",
        "Poids"
    ]

    extracted_specs = {}

    try:
        # Wait for the rows with class 'yOkvvt63'
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "tr.yOkvvt63"))
        )

        rows = driver.find_elements(By.CSS_SELECTOR, "tr.yOkvvt63")

        for row in rows:
            tds = row.find_elements(By.TAG_NAME, "td")
            if len(tds) >= 2:
                key_divs = tds[0].find_elements(By.CLASS_NAME, "ywIf8Ay")
                if key_divs:
                    key = key_divs[0].text.strip()
                    if key in FRENCH_PARAMETERS:
                        value = tds[1].text.strip()
                        value = value.replace("\u00a0", " ")  # Replace non-breaking spaces
                        extracted_specs[key] = value

        if extracted_specs:
            print("\n=== Spécifications du portable ===")
            for spec_name, spec_value in extracted_specs.items():
                print(f"{spec_name}: {spec_value}")
            print("===============================")
        else:
            print("Aucune spécification correspondante trouvée dans les lignes du tableau")

    except TimeoutException:
        print("Temps dépassé en attendant les lignes de spécifications")
    except Exception as e:
        print(f"Erreur lors de l'extraction des spécifications: {str(e)}")

    return extracted_specs

def process_laptops(start_index):
    try:
        laptop_articles = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.yj6YNQW2 article.yArygEf2"))
        )
        print(f"Found {len(laptop_articles)} laptop articles")
        for index, article in enumerate(laptop_articles[start_index:], start=start_index + 1):
            try:
                laptop_type_links = article.find_elements(By.CSS_SELECTOR, "a.yArygEfA")
                is_portable = any("Ordinateur portable" in link.text for link in laptop_type_links)

                if is_portable:
                    try:
                        laptop_info_element = article.find_element(By.CSS_SELECTOR, "a[aria-label]")
                        laptop_name = laptop_info_element.get_attribute("aria-label")
                        product_link = laptop_info_element.get_attribute("href")

                        print(f"\n=== Processing Laptop #{index}: {laptop_name} ===")

                        # Open detail page in new tab
                        driver.execute_script("window.open(arguments[0]);", product_link)
                        driver.switch_to.window(driver.window_handles[1])

                        # Wait for page to load and extract specs
                        sleep(random.uniform(3, 5))
                        extract_specs_from_detail_page()

                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])

                    except NoSuchElementException:
                        print(f"Laptop #{index}: Could not find laptop name or link")
            except Exception as e:
                print(f"Error processing laptop #{index}: {str(e)}")

        return len(laptop_articles)
    except Exception as e:
        print(f"Error in process_laptops: {str(e)}")
        return start_index

# Main execution
start_index = 0
total_laptops = process_laptops(start_index)

# Try to click the "Afficher plus" button multiple times
max_clicks = 60
click_count = 0

while click_count < max_clicks:
    try:
        show_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Afficher plus de produits']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", show_more_button)
        driver.execute_script("arguments[0].click();", show_more_button)

        print(f"Clicked 'Afficher plus' button {click_count + 1} times")
        sleep(random.uniform(3, 7))

        new_total_laptops = process_laptops(total_laptops)
        if new_total_laptops > total_laptops:
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