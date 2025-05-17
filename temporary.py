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
    """
    Extract laptop specifications using a hybrid approach that prioritizes speed and reliability.
    """
    # Initialize dictionary with all desired specs set to None
    extracted_specs = {spec: None for spec in DESIRED_SPECS}
    
    try:
        # Use a shorter wait time but still sufficient for page loading
        wait = WebDriverWait(driver, 7)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ypBxcVsA")))
        
        # Try to expand specifications - this is important for reliability
        try:
            show_more_button = driver.find_element(By.CSS_SELECTOR, "button[aria-controls^='«r']")
            if "Afficher" in show_more_button.text:
                driver.execute_script("arguments[0].click();", show_more_button)
                # Short wait for expansion
                sleep(1)
        except:
            # Continue even if button not found
            pass
        
        # Efficient scroll - just enough to load content
        driver.execute_script("window.scrollTo(0, 600)")
        sleep(0.3)
        
        # Extract product name (fast)
        try:
            raw_model = driver.title.split('|')[0].strip() 
            model = clean_model_name(raw_model)
            print(f"Product: {model}")
        except:
            model = "Unknown Model"
        
        # Fast direct extraction of brand
        brand = None
        try:
            # Target specific XPath for brand
            brand_elements = driver.find_elements(By.XPATH, "//div[text()='Fabricant']/../../following-sibling::td//a")
            if brand_elements:
                brand = brand_elements[0].text.strip()
                print(f"Found Brand: {brand}")
        except:
            # Continue if brand not found this way
            pass
        
        # If brand still not found, extract from model name
        if not brand and model:
            common_brands = ["HP", "Dell", "Lenovo", "Asus", "Acer", "Apple", "MSI", 
                            "Samsung", "Huawei", "Microsoft", "LG"]
            for b in common_brands:
                if model.lower().startswith(b.lower()):
                    brand = b
                    print(f"Extracted Brand from model name: {brand}")
                    break
        
        # PRIMARY EXTRACTION METHOD: Direct element access - most reliable and reasonably fast
        # Get all specification tables - this is very reliable
        spec_tables = driver.find_elements(By.CLASS_NAME, "yxKaXMd")
        
        for table in spec_tables:
            rows = table.find_elements(By.TAG_NAME, "tr")
            
            for row in rows:
                try:
                    # Find cells
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) >= 2:
                        # Get spec name efficiently
                        spec_elem = cells[0].find_element(By.CLASS_NAME, "ywIf8Ay")
                        spec_name = spec_elem.text.strip()
                        
                        # Only process specs we care about - saves time
                        if spec_name in DESIRED_SPECS:
                            # Get value from second cell
                            value = cells[1].text.strip()
                            
                            # Clean value (remove info button indicator)
                            value = re.sub(r'\s*i\s*$', '', value)
                            
                            # Save spec
                            extracted_specs[spec_name] = value
                            print(f"Found {spec_name}: {value}")
                except:
                    # Skip problematic rows
                    continue
        
        # SECONDARY METHOD: For specs still missing, use optimized direct lookup
        missing_specs = [spec for spec in DESIRED_SPECS if extracted_specs[spec] is None]
        if missing_specs:
            print(f"Still missing: {missing_specs}")
            
            for spec in missing_specs:
                try:
                    # Efficient direct XPath for each missing spec
                    xpath = f"//div[contains(text(),'{spec}')]/../../following-sibling::td"
                    spec_value_cells = driver.find_elements(By.XPATH, xpath)
                    
                    if spec_value_cells:
                        value = spec_value_cells[0].text.strip()
                        value = re.sub(r'\s*i\s*$', '', value)
                        extracted_specs[spec] = value
                        print(f"Found {spec} (secondary): {value}")
                except:
                    # Continue if this spec can't be found
                    continue
        
        # Get price efficiently
        price = None
        try:
            # Try the most common price selectors
            selectors = [
                "button.yKEoTuX6", 
                "span.yXGq3V4", 
                "div.yXGq3V4",
                "div.yPLxjm2z"
            ]
            
            for selector in selectors:
                price_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if price_elements:
                    price_text = price_elements[0].text.strip()
                    if "CHF" in price_text or ".-" in price_text:
                        price = price_text
                        # Ensure price starts with CHF
                        if not price.startswith("CHF"):
                            price = f"CHF {price}"
                        print(f"Price: {price}")
                        break
        except:
            # Continue without price if not found
            pass
        
        # Map extracted specs to CSV format
        taille_ecran = extracted_specs.get("Taille de l'écran", "")
        definition_ecran = extracted_specs.get("Définition de l'écran", "")
        display = f"{taille_ecran} {definition_ecran}".strip()
        
        # Prepare CSV data
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
        
        # Save to CSV efficiently
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
        
        # Minimal logging
        total_found = sum(1 for value in extracted_specs.values() if value)
        print(f"Extracted {total_found} specs for {model}")
        
    except Exception as e:
        print(f"Error extracting specs: {str(e)}")
    
    return extracted_specs

def process_laptops(start_index, max_per_batch=10):
    try:
        # Find all laptop articles with reduced wait time
        laptop_articles = WebDriverWait(driver, 7).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.yj6YNQW2 article.yArygEf2"))
        )
        print(f"Found {len(laptop_articles)} laptop articles")
        
        # Process only a subset for efficiency
        end_index = min(start_index + max_per_batch, len(laptop_articles))
        to_process = laptop_articles[start_index:end_index]
        
        processed_count = 0
        
        for index, article in enumerate(to_process, start=start_index + 1):
            try:
                # Skip type checking - we know we're on laptop page
                try:
                    # Get link directly - faster
                    laptop_info_element = article.find_element(By.CSS_SELECTOR, "a[aria-label]")
                    laptop_name = laptop_info_element.get_attribute("aria-label")
                    product_link = laptop_info_element.get_attribute("href")
                    
                    print(f"Processing: {laptop_name}")
                    
                    # Open in new tab
                    driver.execute_script("window.open(arguments[0]);", product_link)
                    driver.switch_to.window(driver.window_handles[1])
                    
                    # Extract specs
                    extract_specs_from_detail_page(driver, product_link)
                    processed_count += 1
                    
                    # Close tab and return to main page
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    
                except NoSuchElementException:
                    print(f"Laptop #{index}: Missing link")
                    continue
                    
            except Exception as e:
                print(f"Error on laptop #{index}: {str(e)[:50]}...")
                continue
                
        print(f"Processed {processed_count} laptops")
        return len(laptop_articles)
        
    except Exception as e:
        print(f"Error in process_laptops: {str(e)}")
        return start_index

# Main execution with optimizations
print(f"Starting data collection. Results will be saved to {csv_filename}")

# Open page and wait for load
driver.get("https://www.digitec.ch/fr/s1/producttype/ordinateur-portable-6")
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.yj6YNQW2"))
)
print("Web page loaded")

# Process initial batch with smaller count for speed
start_index = 0
batch_size = 5  # Smaller initial batch for faster feedback
total_laptops = process_laptops(start_index, batch_size)

# Load more products - with optimized waits
max_clicks = 3  # Reduced for testing
click_count = 0

while click_count < max_clicks:
    try:
        # Find "Show more" button with reduced wait time
        show_more_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Afficher plus de produits']"))
        )
        
        # Scroll and click
        driver.execute_script("arguments[0].scrollIntoView(true);", show_more_button)
        driver.execute_script("arguments[0].click();", show_more_button)
        
        print(f"Clicked 'Show more' button ({click_count + 1})")
        
        # Shorter wait after click - just enough for content to load
        sleep(2)
        
        # Process next batch with increased size
        batch_size = 10  # Can increase for subsequent batches
        new_total_laptops = process_laptops(total_laptops, batch_size)
        
        if new_total_laptops > total_laptops:
            total_laptops = new_total_laptops
            click_count += 1
        else:
            print("No new laptops loaded")
            break
            
    except TimeoutException:
        print("'Show more' button not found")
        break
    except Exception as e:
        print(f"Error clicking 'Show more' button: {str(e)[:50]}...")
        break

print(f"\nData collection complete. Saved to {csv_filename}")
driver.quit()