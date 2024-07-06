# Basic Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def search_for_pharmacies(driver: webdriver.chrome.webdriver.WebDriver) -> None:
    """
    Use on the wolt homepage after having set the location.
    This will open up a page with all the pharmacies in the area
    """
    try:
        search_box = driver.find_element(By.TAG_NAME, 'input')
        search_box.send_keys('pharmacy')
        search_box.send_keys(Keys.RETURN)
    except Exception as e:
        print(f"Error interacting with the search box: {e}")

def open_tabs_and_perform_function(driver: webdriver.chrome.webdriver.WebDriver, max_links=5, function=None) -> None:
    wait = WebDriverWait(driver, 10)
    pharmacy_links = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@data-test-id, 'venueCard')]")))

        # Ensure we have at least 5 links, or take only the available ones if fewer
    num_links = min(len(pharmacy_links), max_links)

    for i in range(num_links):
        # Open each link in a new tab
        link = pharmacy_links[i].get_attribute('href')
        driver.execute_script("window.open(arguments[0], '_blank');", link)

    # Switch to each tab and perform actions if needed
    for i in range(num_links):
        driver.switch_to.window(driver.window_handles[i + 1])  # Switch to the newly opened tab
        # Add any actions you want to perform on the new page here
        print(f"Opened tab {i+1}: {driver.current_url}")

    # Optionally, close all tabs except the first one
    # for i in range(num_links):
    #     driver.switch_to.window(driver.window_handles[1])  # Switch to the tab to be closed
    #     driver.close()

def open_categories_in_tabs(driver: webdriver.chrome.webdriver.WebDriver, text_to_match=None) -> None:
    # List of texts to match
    if text_to_match is None:
        text_to_match = ["ΑΝΤΗΛΙΑΚΑ", "ΣΥΜΠΛ", "ΒΙΤΑΜΙΝΕΣ", "ΦΑΡΜΑΚ"]  # Populate this list with the desired texts

    # Find all <a> elements with the data-test-id 'navigation-bar-active-link'
    links = driver.find_elements(By.CSS_SELECTOR, '[data-test-id="navigation-bar-link"]')
    # Open each href in a new tab if any text snippet is contained in the link's text
    for link in links:
        if any(text in link.text for text in text_to_match):
            href = link.get_attribute('href')
            if href:
                driver.execute_script("window.open(arguments[0], '_blank');", href)



def extract_items_from_current_category(driver: webdriver.chrome.webdriver.WebDriver) -> dict:
    """
    Extracts item prices and names into a new dicitonary and return it
    """
    # Dictionary to store pairs of values
    data_dict = {}

    # Find all <div> elements with class 'sc-4bc6cfeb-3' and 'khFUE'
    div_elements = driver.find_elements(By.CLASS_NAME, 'sc-4bc6cfeb-3.khFUE')
    # Process each <div> element
    for index, div in enumerate(div_elements, start=1):
        try:
            # Extract the text from the <h3> element located at div2/div2
            h3_text = div.find_element(By.XPATH, './div[2]/div[2]/h3').text.strip()
            
            # Extract the text from the <span> element located at div2/div1
            span_text = div.find_element(By.XPATH, './div[2]/div[1]/span').text.strip()
            
            # Store the pair in the dictionary
            data_dict[f'Pair {index}'] = {'h3_text': h3_text, 'span_text': span_text}
            
        except Exception as e:
            print(f"Error processing div {index}: {e}")
    return data_dict


def print_item_dict(data_dict: dict) -> None:
    # Print the item dictionary in a nicely formatted way
    for key, value in data_dict.items():
        print(f"{key}:")
        print(f"  - h3_text: {value['h3_text']}")
        print(f"  - span_text: {value['span_text']}")
        print()