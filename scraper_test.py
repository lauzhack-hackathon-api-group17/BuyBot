from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

try:
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # Set up the WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Disable detection
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    # Open the webpage
    print("Opening web page...")
    driver.get("https://www.digitec.ch/fr/s1/product/hp-probook-460-g11-16-intel-core-ultra-7-155u-32-go-1000-go-ch-ordinateur-portable-46443765")
    print("Web page opened, waiting for load...")
    
    # Wait for content to load with explicit wait
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ypBxcVsA")))
    
    # Specifications to extract
    desired_specs = {
        "Type de processeur": None,
        "Définition de l'écran": None,
        "Taille de l'écran": None,
        "Nombre de threads": None,
        "Mémoire vive": None,
        "Système d'exploitation": None,
        "Puce graphique (GPU)": None,
        "Poids": None,
        "Longueur": None,
        "Largeur": None,
        "RAM max.": None
    }
    
    # Get the page source
    page_source = driver.page_source
    
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
    for spec in desired_specs.keys():
        # Try each pattern until we find a match
        for pattern_key, pattern_template in patterns.items():
            pattern = pattern_template.format(spec=re.escape(spec))
            match = re.search(pattern, page_source, re.DOTALL)
            
            if match:
                value = match.group(1).strip()
                # Clean up non-breaking spaces and other special characters
                value = value.replace('&nbsp;', ' ')
                desired_specs[spec] = value
                print(f"Found {spec}: {value} (Pattern {pattern_key})")
                break
    
    # Try direct element extraction for missing specs
    if not any(desired_specs.values()):
        print("No specs found with regex, trying direct element approach...")
        
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
                        if spec_name in desired_specs:
                            desired_specs[spec_name] = value
                            print(f"Found {spec_name}: {value} (Direct element)")
                    except:
                        continue
    
    # Extract product name and brand
    try:
        product_title = driver.find_element(By.CSS_SELECTOR, "h1.yKx7OX2").text
        print(f"Product: {product_title}")
        
        # Try to extract brand from product name
        brand_match = re.search(r'^([A-Za-z]+)\s', product_title)
        if brand_match:
            brand = brand_match.group(1)
            print(f"Extracted Brand from model name: {brand}")
            desired_specs["Marque"] = brand
    except:
        print("Could not extract product name")
    
    # Get the price
    try:
        price_elem = driver.find_element(By.CSS_SELECTOR, "div.yPLxjm2z")
        price = price_elem.text.strip()
        desired_specs["Prix"] = price
        print(f"Prix: {price}")
    except:
        # Try alternative approach with regex
        price_pattern = r'class="yKEoTuX6"><span.*?>.*?</span>(.*?)</button>'
        price_match = re.search(price_pattern, page_source)
        if price_match:
            price = price_match.group(1).strip()
            desired_specs["Prix"] = f"CHF {price}"
            print(f"Prix: CHF {price}")
    
    # Print summary
    print("\n=== Spécifications du portable ===")
    for spec, value in desired_specs.items():
        if value:
            print(f"{spec}: {value}")
    
    total_found = sum(1 for value in desired_specs.values() if value)
    print(f"Total specifications found: {total_found}")
    print("===============================")

except Exception as e:
    print(f"An error occurred: {e}")
    import traceback
    traceback.print_exc()

finally:
    # Close the browser
    if 'driver' in locals():
        driver.quit()
    print("Browser closed.")