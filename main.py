from functions import *
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
# wd manager deals with finding the correct driver so that we don't have to install it
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())

# otherwise if we had the correct version in our folder we would do the following
# driver = webdriver.Chrome()


driver.get("https://wolt.com/el/grc/athens")

# Find and click accept cookies
wait = WebDriverWait(driver, 10)
button = button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@data-localization-key='gdpr-consents.banner.accept-button']")))
button.click()


search_for_pharmacies(driver)

open_tabs_and_perform_function(driver)

open_categories_in_tabs(driver)

print_item_dict(extract_items_from_current_category(driver))



# # Keep the browser open
# input("Press Enter to close the browser...")

# # Close the browser
# driver.quit()



# driver.get("http://www.python.org")
# assert "Python" in driver.title
# elem = driver.find_element(By.NAME, "q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()