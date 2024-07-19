# Basic Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from typing import List, Set, Counter
import csv
from datetime import datetime
import time
from collections import Counter

class WoltPharmacyExtractor:

    def __init__(self) -> None:
        """
        Initializes the extractor and creates an instance of the driver
        as well as an items dictionary.
        """
        self.start()
        self.items = []
        self.categories: Counter[str] = Counter()

    def start(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def quit(self):
        self.driver.quit()

    def _open_wolt_page(self) -> None:
        """
        Opens up the Athens Greece Wolt page and accepts cookies. 
        """
        self.driver.get("https://wolt.com/el/grc/athens")
        # Find and click accept cookies
        wait = WebDriverWait(self.driver, 10)
        button = button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@data-localization-key='gdpr-consents.banner.accept-button']")))
        button.click()

    def _search_for_pharmacies(self) -> None:
        """
        Assumes that the Wolt Homepage is open and performs a search for all the available pharmacies
        If everything runs smoothly a page with all the pharmacies should be present
        """
        try:
            search_box = self.driver.find_element(By.TAG_NAME, 'input')
            search_box.send_keys('pharmacy')
            search_box.send_keys(Keys.RETURN)
        except Exception as e:
            print(f"Error interacting with the search box: {e}")

    def _open_pharmacy_tabs_and_perform_function(self, max_links=None) -> None:
        wait = WebDriverWait(self.driver, 10)
        pharmacy_links = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@data-test-id, 'venueCard')]")))

            # Ensure we have at least 5 links, or take only the available ones if fewer
        if max_links is not None:
            num_links = min(len(pharmacy_links), max_links)
        else:
            num_links = len(pharmacy_links)
        index = 0 # Pharmacy index
        for i in range(num_links):
            # Open each link in a new tab
            link = pharmacy_links[i].get_attribute('href')
            self.driver.execute_script("window.open(arguments[0], '_blank');", link)
            index += 1
            print(f"processing pharmacy {index}/{num_links}")
            self.driver.switch_to.window(self.driver.window_handles[-1])
            self._open_categories_in_tabs()
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

    def _open_categories_in_tabs(self, text_to_match=None) -> None:
        # List of texts to match
        if text_to_match is None:
            text_to_match = ["ΑΝΤΗΛΙΑΚΑ", "ΣΥΜΠΛ", "ΒΙΤΑΜΙΝΕΣ", "ΦΑΡΜΑΚ"]  # Populate this list with the desired texts
            # text_to_match = ["Frezyderm"]  # Populate this list with the desired texts

        # Find all <a> elements with the data-test-id 'navigation-bar-link'
        links = self.driver.find_elements(By.CSS_SELECTOR, '[data-test-id="navigation-bar-link"]')
        # Open each href in a new tab if any text snippet is contained in the link's text
        index = 0 # category index
        category = str()
        for link in links:
            self.categories.update([link.text.strip()])
            if True:  # if any(text in link.text for text in text_to_match):
                category = link.text.strip()
                href = link.get_attribute('href')
                if href:
                    self.driver.execute_script("window.open(arguments[0], '_blank');", href)
                    index += 1
                    print(f"\tprocessing category {index}/{len(links)}")
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    self._extract_items_from_current_category(category)
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[-1])

    def _extract_items_from_current_category(self, category: str) -> None:
        """
        Extracts item prices and names into a new dicitonary and updates 
        the items dictionary with it's pairs
        """

        # Find all <div> elements with class 'sc-4bc6cfeb-3' and 'khFUE'
        div_elements = self.driver.find_elements(By.CLASS_NAME, 'sc-4bc6cfeb-3.khFUE')
        # Process each <div> element
        for index, div in enumerate(div_elements, start=1):
            try:
                # Extract the text from the <h3> element located at div2/div2
                h3_text = div.find_element(By.XPATH, './div[2]/div[2]/h3').text.strip()
                
                # Extract the text from the <span> element located at div2/div1
                span_text = div.find_element(By.XPATH, './div[2]/div[1]/span').text.strip()
                
                # append the tuple to the list of items
                self.items.append((h3_text, span_text, category))
                # self.item_id += 1
                
            except Exception as e:
                print(f"Error processing div {index}: {e}")

    def __str__(self) -> None:
        return str(self.items)

    def _save_items_to_csv(self):
        # Generate a timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"date/items_{timestamp}.csv"
        
        # Open a new CSV file and write the items with UTF-8 encoding
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write the header
            writer.writerow(['Description', 'Price String', 'Category'])
            # Write the data from the list of tuples
            for item in self.items:
                writer.writerow(item)
            
            print(f"Items saved to {filename}")
    
    def _print_categories(self) -> None:
        print('Distinct Categories, Occurences')
        for category, occurences in self.categories.items():
            print(f'{category}, {occurences}')

    def _categories_to_file(self) -> None:
        # Generate a timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"categories_{timestamp}.csv"
        
        # Write elements to the file
        with open(filename, 'w', encoding='utf-8') as file:
            for category, occurences in self.categories.items():
                file.write(f"{category}, {occurences}\n")
        
        print(f"Elements written to {filename}")

    def extract_items(self, num_pharmacies: int=None, categories: List[str]=None, save_to_file=True, max_links=None) -> None:
        """
        This is the public method that does it all, by using all the private methods defined earlier.
        The private methods are not meant to be used on their own because they assume a particular web page
        state. This function ensures correct states and proceeds with the necessary steps
        """
        self._open_wolt_page()
        self._search_for_pharmacies()
        self._open_pharmacy_tabs_and_perform_function(max_links)
        
        if save_to_file:
            self._save_items_to_csv()
            self._categories_to_file()
        else:
            self._print_categories()
            print(self)
        self.driver.close()
    
if __name__ == "__main__":
    wpe = WoltPharmacyExtractor()
    wpe.extract_items(max_links=None, save_to_file=True)
