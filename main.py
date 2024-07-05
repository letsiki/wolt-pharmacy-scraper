# Basic Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# wd manager deals with finding the correct driver so that we don't have to install it
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())

# otherwise if we had the correct version in our folder we would do the following
# driver = webdriver.Chrome()


driver.get("https://wolt.com/el/grc/athens")

 # Find the button by the text it contains
# Wait for the button to be present (optional)
wait = WebDriverWait(driver, 10)
button = button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@data-localization-key='gdpr-consents.banner.accept-button']")))


# Click the button
button.click()

# Interact with the page to search for pharmacies in Athens
try:
    search_box = driver.find_element(By.TAG_NAME, 'input')
    search_box.send_keys('pharmacy')
    search_box.send_keys(Keys.RETURN)
except Exception as e:
    print(f"Error interacting with the search box: {e}")

pharmacy_links = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@data-test-id, 'venueCard')]")))

    # Ensure we have at least 5 links, or take only the available ones if fewer
num_links = min(len(pharmacy_links), 5)

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
for i in range(num_links):
    driver.switch_to.window(driver.window_handles[1])  # Switch to the tab to be closed
    driver.close()





# Keep the browser open
input("Press Enter to close the browser...")

# Close the browser
driver.quit()



# driver.get("http://www.python.org")
# assert "Python" in driver.title
# elem = driver.find_element(By.NAME, "q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()