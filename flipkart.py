import sys
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Check if the argument is provided
if len(sys.argv) < 2:
    print("Error: Please provide a search query as an argument.")
    sys.exit(1)

# Get the search query from the command-line argument
search_query = sys.argv[1]

# Set different options for the browser
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Remove SSL errors
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")

# Maximize the browser
chrome_options.add_argument("start-maximized")

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Open the Flipkart search page with the provided query
driver.get(f"https://www.flipkart.com/search?q={search_query}&page=1")
time.sleep(2)
print("Page - 1")
# Navigate to the next page
next_page_xpath = "//*[@id='container']/div/div[3]/div/div[2]/div[26]/div/div/nav/a[11]/span"
driver.find_element(by=By.XPATH, value=next_page_xpath).click()
time.sleep(2)
print("Successfully navigated to the next page.")

while True:
    # Store the current URL
    current_url = driver.current_url
    page_number_match = re.search(r'page=(\d+)', current_url)
    page_number = page_number_match.group(1) if page_number_match else "unknown"
    print("On Page :", page_number)
    # Click on the "Next" button
    next_button_xpath = "//*[@id='container']/div/div[3]/div/div[2]/div[26]/div/div/nav/a[12]/span"
    alternate_next_button_xpath = "//*[@id='container']/div/div[3]/div/div[2]/div[2]/div/div/nav/a[12]/span"
    
    try:
        # Use WebDriverWait to wait for the "Next" button to be clickable
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, next_button_xpath))
        )
        next_button.click()
        print("Successfully navigated to the next page.")
        time.sleep(2)  # Wait for the page to load
    except Exception as e:
        print("Trying alternate XPath due to exception or last page reached.")
        try:
            # Attempt using the alternate XPath
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, alternate_next_button_xpath))
            )
            next_button.click()
            print("Successfully navigated to the next page using alternate XPath.")
            time.sleep(2)
        except Exception as e:
            print(f"Error or last page reached: {e}")
            break

    # Get the new URL
    new_url = driver.current_url
    
    # If the URL hasn't changed, break the loop as it indicates the last page
    if new_url == current_url:
        print("Detected the last page; URL did not change.")
        break

# Save the HTML file
html = driver.page_source
output_filename = f"flipkart_{search_query}.html"
with open(output_filename, "w", encoding="utf-8") as f:
    f.write(html)

print(f"HTML content saved to {output_filename}")

# Browser will not be closed automatically after task completion
# If you want to close the browser after inspection, use:
# driver.quit()