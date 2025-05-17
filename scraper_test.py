from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time
import random
import re
import os
from datetime import datetime

# File paths
input_csv_path = "laptops_copy.csv"  # Your original CSV file
output_csv_path = f"laptops_to_clean.csv"

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
chrome_options.add_argument("--headless=new")  # Run in headless mode for speed
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)

# Set up the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Disable detection
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

def random_sleep(min_seconds=1, max_seconds=3):
    """Sleep for a random duration to appear more human-like"""
    sleep_time = random.uniform(min_seconds, max_seconds)
    time.sleep(sleep_time)

def extract_price_from_page(url):
    """Extract price from the product page"""
    try:
        driver.get(url)
        random_sleep(2, 4)  # Wait for page to load
        
        # Try multiple price selectors
        price_selectors = [
            ".yKEoTuX7",  # The class you provided
            ".yKEoTuX6 span", 
            "span.yXGq3V4",
            ".product-price",
            ".current-price",
            "[data-test='current-price']"
        ]
        
        for selector in price_selectors:
            try:
                # Wait for element to be present
                price_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                
                # Extract the price text
                price_text = price_element.text.strip()
                
                # If found, format and return
                if price_text:
                    # Clean up the price text
                    price_text = price_text.replace('\n', ' ')
                    
                    # If doesn't start with CHF, add it
                    if not price_text.upper().startswith('CHF'):
                        if re.search(r'[0-9]', price_text):  # Only format if there are digits
                            price_text = f"CHF {price_text}"
                    
                    print(f"Found price: {price_text}")
                    return price_text
            except (TimeoutException, NoSuchElementException):
                continue
        
        # If all selectors fail, try regex on page source
        page_source = driver.page_source
        price_patterns = [
            'class="yKEoTuX7">[^<]*?CHF[^<]*?</span>([^<]+)</strong>',
            'class="yKEoTuX6"><span[^>]*>CHF</span>([^<]+)</button>',
            'class="yXGq3V4">[^\d]*(\d+\.\d+)',
            'yXGq3V4">\s*CHF\s*(\d+\.\d+)',
            'data-price="([^"]+)"',
            'itemprop="price"[^>]*content="([^"]+)"'
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, page_source, re.DOTALL)
            if match:
                price_value = match.group(1).strip()
                formatted_price = f"CHF {price_value}"
                print(f"Found price with regex: {formatted_price}")
                return formatted_price
        
        # If still no price found, try one last direct approach with JavaScript
        try:
            # Try to extract price with JavaScript
            js_price = driver.execute_script("""
                // Try to find any element with price-related text
                const priceCandidates = Array.from(document.querySelectorAll('*')).filter(
                    el => el.textContent && 
                    (el.textContent.includes('CHF') || 
                     el.textContent.includes('Fr.') ||
                     /\\d+\\.\\d+/.test(el.textContent))
                );
                
                // Filter to likely price elements
                const priceElements = priceCandidates.filter(el => {
                    const text = el.textContent.trim();
                    // Look for price-like patterns
                    return (text.includes('CHF') || text.includes('Fr.')) && /\\d+\\.\\d+/.test(text);
                });
                
                return priceElements.length > 0 ? priceElements[0].textContent.trim() : null;
            """)
            
            if js_price:
                print(f"Found price with JavaScript: {js_price}")
                return js_price
        except:
            pass
        
        print(f"No price found for {url}")
        return ""
    except Exception as e:
        print(f"Error extracting price from {url}: {str(e)}")
        return ""

def update_csv_with_prices():
    """Read the input CSV, get prices for rows without them, and write to a new CSV"""
    # Read the input CSV
    all_rows = []
    rows_without_price = []
    
    try:
        with open(input_csv_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)  # Get the headers
            price_index = headers.index('Price') if 'Price' in headers else -1
            link_index = headers.index('Link') if 'Link' in headers else -1
            
            if price_index == -1 or link_index == -1:
                print("Error: CSV does not contain 'Price' or 'Link' columns")
                return
            
            # Read all rows and identify those without prices
            for i, row in enumerate(reader, 1):
                all_rows.append(row)
                if i == 1:  # Skip header row
                    continue
                
                if len(row) > price_index and (not row[price_index] or row[price_index].strip() == ''):
                    if len(row) > link_index and row[link_index]:
                        rows_without_price.append((i, row))
    except Exception as e:
        print(f"Error reading input CSV: {str(e)}")
        return
    
    print(f"Found {len(rows_without_price)} rows without prices out of {len(all_rows)} total rows")
    
    # Process rows without prices
    updated_count = 0
    for i, (row_index, row) in enumerate(rows_without_price):
        print(f"\nProcessing row {row_index} ({i+1}/{len(rows_without_price)})")
        
        try:
            url = row[link_index]
            price = extract_price_from_page(url)
            
            if price:
                # Update the price in the row
                row[price_index] = price
                all_rows[row_index - 1] = row  # -1 to account for 0-based indexing
                updated_count += 1
                print(f"Updated price for row {row_index}: {price}")
            
            # Random delay between requests to avoid being blocked
            if i < len(rows_without_price) - 1:  # Don't sleep after the last item
                random_sleep(2, 5)
        except Exception as e:
            print(f"Error processing row {row_index}: {str(e)}")
    
    # Write the updated data to the output CSV
    try:
        with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)  # Write headers
            for row in all_rows:
                writer.writerow(row)
        
        print(f"\nUpdated {updated_count} out of {len(rows_without_price)} missing prices")
        print(f"Updated data saved to {output_csv_path}")
    except Exception as e:
        print(f"Error writing output CSV: {str(e)}")

# Main execution
try:
    print(f"Starting price update process. Reading from {input_csv_path}")
    print(f"Results will be saved to {output_csv_path}")
    
    # Check if input file exists
    if not os.path.exists(input_csv_path):
        print(f"Error: Input file {input_csv_path} does not exist")
    else:
        update_csv_with_prices()
except Exception as e:
    print(f"Critical error in main execution: {str(e)}")
    import traceback
    traceback.print_exc()
finally:
    # Clean up WebDriver
    driver.quit()
    print("WebDriver closed")