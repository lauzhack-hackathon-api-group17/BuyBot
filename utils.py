import os
import csv
from scipy.optimize import direct
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import unidecode as ud
from selenium.webdriver.support.wait import WebDriverWait
from difflib import SequenceMatcher
import unicodedata
import re


def wait_for_page_elements_to_load_by(driver, elementIdentifier, elementValue, seconds):
    try:
        WebDriverWait(driver=driver, timeout=seconds).until(
            EC.presence_of_element_located((elementIdentifier, elementValue))
        )
        return driver.find_elements(elementIdentifier, elementValue)
    finally:
        pass

unwanted_chars_set = {
    '\u0000', '\u0001', '\u0002', '\u0003', '\u0004', '\u0005', '\u0006', '\u0007',
    '\u0008', '\u0009', '\u000a', '\u000b', '\u000c', '\u000d', '\u0010', '\u0011',
    '\u0012', '\u0013', '\u0014', '\u0015', '\u0016', '\u0017', '\u0018', '\u0019',
    '\u001a', '\u001b', '\u001c', '\u001d', '\u001e', '\u001f', '\u007f',
    '\u00a0',  # Non-breaking space
    '\u1680',  # Ogham space mark
    '\u180e',  # Mongolian vowel separator
    '\u2000', '\u2001', '\u2002', '\u2003', '\u2004', '\u2005',
    '\u2006', '\u2007', '\u2008', '\u2009', '\u200a',
    '\u200b', '\u200c', '\u200d',
    '\u2028', '\u2029', '\u202f',
    '\u205f', '\u2060',
    '\ufeff',
    '\ufff9', '\ufffa', '\ufffb',
}

PROBABILITY_THRESHOLD = 0.9
FILTER_THRESHOLD = 0.65


def clean_str(string: str):
    return ''.join(c for c in string if unicodedata.category(c)[0] not in ['C'] and c not in unwanted_chars_set)

def compare_strings(string1: str, string2: str) -> bool:
    """
        This method's role is to compare two strings and see if they have a high probability of matching
        :param string1: the string1
        :param string2: the string2
        :return: if the two strings have a high probability of matching
        """
    #First of all separate the strings in a list
    simplified1 = ud.unidecode(string1).lower().replace("-", " ")
    simplified2 = ud.unidecode(string2).lower().replace("-", " ")
    simplified1 = re.sub(r'[^a-zA-Z ]', '', simplified1)
    simplified2 = re.sub(r'[^a-zA-Z ]', '', simplified2)

    simplified1_list = simplified1.split()
    simplified1_list.sort()
    simplified2_list = simplified2.split()
    simplified2_list.sort()

    length1 = len(simplified1_list)
    length2 = len(simplified2_list)

    #detect names where there are multiple names
    if (length1 > 2 or length2 > 2) and length1 != length2 and one_sublist_of_another(simplified1_list, simplified2_list):
        return 1

    simplified1 = "".join(simplified1_list)
    simplified2 = "".join(simplified2_list)

    simplified1 = re.sub(r'[^a-zA-Z]', '', simplified1)
    simplified2 = re.sub(r'[^a-zA-Z]', '', simplified2)

    ratio = SequenceMatcher(None, simplified1, simplified2).ratio()

    return ratio


def probability_strings(string1: str, string2: str):
    simplified1 = re.sub(r'[^a-zA-Z]', '', string1)
    simplified2 = re.sub(r'[^a-zA-Z]', '', string2)

    ratio = SequenceMatcher(None, simplified1, simplified2).ratio()
    return ratio


def one_sublist_of_another(list1: list, list2: list) -> float:
    length1 = len(list1)
    length2 = len(list2)

    if length1 > length2:
        for word in list2:
            found = False
            for word1 in list1:
                if probability_strings(word, word1) >= PROBABILITY_THRESHOLD:
                    found = True
                    break
            if found is False:
                return False
            else:
                continue
    else:
        for word in list1:
            found = False
            for word1 in list2:
                if probability_strings(word, word1) >= PROBABILITY_THRESHOLD:
                    found = True
                    break
            if found is False:
                return False
            else:
                continue

    return True

def parse_number_from_string(string_to_parse: str) -> float:
    match = re.search(r"[-+]?\d*\.\d+|\d+", string_to_parse)
    if match:
        return float(match.group())
    else:
        raise ValueError(f"No number found in string: '{string_to_parse}'")


# Load the components possibilities from CSV files
def get_possibilities():
    """Load the possible values for each component from CSV files in the specified directory."""
    possibilities = {}
    directory = 'scraped_lists/LAPTOPS'
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            key = filename[:-4]  # remove .csv
            with open(os.path.join(directory, filename), newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                # flatten all rows into a single list
                values = [item for row in reader for item in row if item]
                possibilities[key] = values