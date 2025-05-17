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
import re
import csv
from datetime import datetime

# Only these specific parameters we want to extract
DESIRED_SPECS = [
    "Type de processeur",
    "Définition de l'écran",
    "Taille de l'écran",
    "Nombre de threads",
    "Mémoire vive", 
    "Système d'exploitation",
    "Puce graphique (GPU)",
    "Poids",
    "Longueur",
    "Largeur",
    "RAM max.",
    "Capacité SSD"
]

# CSV column headers
CSV_HEADERS = ["Brand", "Model", "Category", "Display", "CPU", "RAM", "Storage", "GPU", "OS", "Weight", "Price", "Link"]

# Create or open the CSV file
csv_filename = f"laptops_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

# Set up the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Disable detection
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# Initialize CSV file with headers
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(CSV_HEADERS)

def clean_model_name(model_name):
    """Clean the model name to remove unwanted text."""
    # Remove "- acheter sur Digitec" and similar suffixes
    suffixes = [
        " - acheter sur Digitec", 
        " - Digitec", 
        " - acheter"
    ]
    for suffix in suffixes:
        if suffix in model_name:
            model_name = model_name.replace(suffix, "")
    
    # Remove specs in parentheses - matches any text in parentheses
    model_name = re.sub(r'\([^)]*\)', '', model_name)
    
    # Clean up extra spaces and trim
    model_name = re.sub(r'\s+', ' ', model_name).strip()
    
    return model_name

def extract_specs_from_detail_page(driver, product_url):
    # Initialize dictionary with all desired specs set to None
    extracted_specs = {spec: None for spec in DESIRED_SPECS}
    
    try:
        # Wait for the page to load properly with explicit wait
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ypBxcVsA")))
        
        # Try to find and click any "Show more specs" button
        try:
            show_more_buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'yqCAcxE')]")
            for button in show_more_buttons:
                if "Afficher plus" in button.text or "Afficher" in button.text:
                    driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    driver.execute_script("arguments[0].click();", button)
                    print("Clicked 'Show more specifications' button")
                    sleep(2)  # Wait for expanded content to load
        except Exception as e:
            print(f"Note: Could not find or click show more button: {e}")
        
        # Scroll through page to ensure all content is loaded
        for scroll_position in [300, 600, 900, 1200, 1500]:
            driver.execute_script(f"window.scrollTo(0, {scroll_position})")
            sleep(0.5)
        
        # Scroll back to top
        driver.execute_script("window.scrollTo(0, 0)")
        sleep(1)
        
        # Get the page source after all interactions
        page_source = driver.page_source
        
        # Extract product name
        raw_model = driver.title.split('|')[0].strip() if '|' in driver.title else driver.title.strip()
        # Clean the model name to remove unwanted text
        model = clean_model_name(raw_model)
        print(f"Product: {model}")
        
        # Extract brand
        brand = None
        # Try multiple patterns for brand extraction
        brand_patterns = [
            '<div class="ywIf8Ay">Fabricant</div></td><td.*?><a.*?>(.*?)</a>',
            '<a class="yRfMIL6 yRfMIL66" href="/fr/brand/.*?">(.*?)</a>'
        ]
        
        for pattern in brand_patterns:
            brand_match = re.search(pattern, page_source, re.DOTALL)
            if brand_match:
                brand = brand_match.group(1).strip()
                print(f"Found Brand: {brand}")
                break
        
        # If brand still not found, try to extract from model name
        if not brand and model:
            common_brands = ["HP", "Dell", "Lenovo", "Asus", "Acer", "Apple", "MSI", "Samsung", "Huawei", "Microsoft"]
            for b in common_brands:
                if model.lower().startswith(b.lower()):
                    brand = b
                    print(f"Extracted Brand from model name: {brand}")
                    break
        
        # More flexible patterns for different HTML structures
        patterns = {
            # Pattern 1: Standard text in span
            1: r'<div class="ywIf8Ay">{spec}.*?</div></td><td.*?><span>([^<]+)',
            # Pattern 2: Text in double nested spans
            2: r'<div class="ywIf8Ay">{spec}.*?</div></td><td.*?><div class="yQqusFs1"><span class="yQqusFs"><span>([^<]+)',
            # Pattern 3: Text without any span (directly in td)
            3: r'<div class="ywIf8Ay">{spec}.*?</div></td><td[^>]*>([^<\s][^<]*)',
            # Pattern 4: Text in link
            4: r'<div class="ywIf8Ay">{spec}.*?</div></td><td.*?><a[^>]*>([^<]+)',
        }
        
        # Manual extraction from the page source
        for spec in DESIRED_SPECS:
            # Try each pattern until we find a match
            for pattern_key, pattern_template in patterns.items():
                pattern = pattern_template.format(spec=re.escape(spec))
                match = re.search(pattern, page_source, re.DOTALL)
                
                if match:
                    value = match.group(1).strip()
                    # Clean up non-breaking spaces and other special characters
                    value = value.replace('&nbsp;', ' ')
                    extracted_specs[spec] = value
                    print(f"Found {spec}: {value} (Pattern {pattern_key})")
                    break
        
        # If regex approach didn't find enough specs, try direct element extraction
        if sum(1 for value in extracted_specs.values() if value) <= 3:
            print("Few specs found with regex, trying direct element approach...")
            
            # Get all specification tables
            spec_tables = driver.find_elements(By.CLASS_NAME, "yxKaXMd")
            
            for table in spec_tables:
                rows = table.find_elements(By.TAG_NAME, "tr")
                
                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) >= 2:
                        try:
                            # Get spec name from first cell
                            spec_elem = cells[0].find_element(By.CLASS_NAME, "ywIf8Ay")
                            spec_name = spec_elem.text.strip()
                            
                            # Get spec value from second cell
                            value = cells[1].text.strip()
                            
                            # Check if it's one of our desired specs
                            if spec_name in DESIRED_SPECS and not extracted_specs[spec_name]:
                                extracted_specs[spec_name] = value
                                print(f"Found {spec_name}: {value} (Direct element)")
                        except:
                            continue
        
        # Get the price using multiple methods
        price = None
        # Method 1: Regex pattern
        price_patterns = [
            'class="yKEoTuX6"><span.*?>.*?</span>(.*?)</button>',
            'class="yXGq3V4">[^\d]*(\d+\.–)',
            'yXGq3V4">\s*CHF\s*(\d+\.–)'
        ]
        
        for pattern in price_patterns:
            price_match = re.search(pattern, page_source, re.DOTALL)
            if price_match:
                price = f"CHF {price_match.group(1).strip()}"
                print(f"Prix: {price}")
                break
        
        # Method 2: Direct element approach if regex failed
        if not price:
            try:
                price_element = driver.find_element(By.CSS_SELECTOR, "button.yKEoTuX6, span.yXGq3V4")
                price = price_element.text.strip()
                print(f"Prix (direct element): {price}")
            except:
                print("Could not find price element")
        
        # Print the summary for this laptop
        print("\n=== Spécifications du portable ===")
        for spec_name, spec_value in extracted_specs.items():
            if spec_value:
                print(f"{spec_name}: {spec_value}")
        if price:
            print(f"Prix: {price}")
        
        total_found = sum(1 for value in extracted_specs.values() if value) + (1 if price else 0)
        print(f"Total specifications found: {total_found}")
        print("===============================")
        
        # Map the extracted specs to the CSV format
        taille_ecran = extracted_specs.get("Taille de l'écran", "")
        definition_ecran = extracted_specs.get("Définition de l'écran", "")
        display = f"{taille_ecran} {definition_ecran}".strip()
        
        csv_data = {
            "Brand": brand if brand else "",
            "Model": model if model else "",
            "Category": "Ordinateur portable",
            "Display": display,
            "CPU": extracted_specs.get("Type de processeur", ""),
            "RAM": extracted_specs.get("Mémoire vive", ""),
            "Storage": extracted_specs.get("Capacité SSD", ""),
            "GPU": extracted_specs.get("Puce graphique (GPU)", ""),
            "OS": extracted_specs.get("Système d'exploitation", ""),
            "Weight": extracted_specs.get("Poids", ""),
            "Price": price if price else "",
            "Link": product_url
        }
        
        # Save to CSV
        with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([
                csv_data["Brand"],
                csv_data["Model"],
                csv_data["Category"],
                csv_data["Display"],
                csv_data["CPU"],
                csv_data["RAM"],
                csv_data["Storage"],
                csv_data["GPU"],
                csv_data["OS"],
                csv_data["Weight"],
                csv_data["Price"],
                csv_data["Link"]
            ])
        
        print(f"Data saved to {csv_filename}")
        
    except Exception as e:
        print(f"Erreur lors de l'extraction des spécifications: {str(e)}")
        import traceback
        traceback.print_exc()
    
    return extracted_specs

def process_laptops(start_index):
    try:
        laptop_articles = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.yj6YNQW2 article.yArygEf2"))
        )
        print(f"Found {len(laptop_articles)} laptop articles")
        processed_count = 0
        
        for index, article in enumerate(laptop_articles[start_index:], start=start_index + 1):
            try:
                laptop_type_links = article.find_elements(By.CSS_SELECTOR, "a.yArygEfA")
                is_portable = True  # Assume all are laptops since we're on the laptop category page
                if laptop_type_links:
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

                        # Wait for page to load and extract specs using the new method
                        specs = extract_specs_from_detail_page(driver, product_link)
                        processed_count += 1
                        
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])

                    except NoSuchElementException:
                        print(f"Laptop #{index}: Could not find laptop name or link")
            except Exception as e:
                print(f"Error processing laptop #{index}: {str(e)}")

        print(f"Processed {processed_count} laptops in this batch")
        return len(laptop_articles)
    except Exception as e:
        print(f"Error in process_laptops: {str(e)}")
        return start_index

# Main execution
print(f"Starting data collection. Results will be saved to {csv_filename}")
driver.get("https://www.digitec.ch/fr/s1/producttype/ordinateur-portable-6")
print("Web page opened successfully.")
sleep(random.uniform(2, 5))

start_index = 0
total_laptops = process_laptops(start_index)

# Try to click the "Afficher plus" button multiple times
max_clicks = 3  # Reduced for testing
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

print(f"\nData collection complete. Data saved to {csv_filename}")
sleep(2)
driver.quit()