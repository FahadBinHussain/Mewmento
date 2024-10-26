from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import base64

# Set up Browser options
chrome_options = Options()
chrome_options.add_extension('bypass-paywalls-chrome-clean-3.4.9.0.crx')
chrome_options.add_extension('uBlock-Origin.crx')

# Path to the BrowserDriver executable
service = Service('chromedriver.exe')

# Launch a browser
driver = webdriver.Chrome(service=service, options=chrome_options)

# Wait for the extensions to load properly
time.sleep(4000000)

try:
    # Navigate to the webpage
    driver.get("https://www.wsj.com/tech/personal-tech/things-to-do-our-12-top-tech-tips-of-2023-ab4e9899")

    # Calculate the total height of the page
    total_height = driver.execute_script("return document.body.scrollHeight")

    # Scroll through the page in 10% increments
    for i in range(1, 11):  # From 10% to 100% (in 10% steps)
        # Scroll to the desired percentage
        driver.execute_script(f"window.scrollTo(0, {total_height * i / 10});")
        # Wait for a moment to allow images to load
        time.sleep(1)

    print_options = {
    'landscape': False,
    'displayHeaderFooter': False,
    'printBackground': True,
    'preferCSSPageSize': True,
}

    # Execute the print command
    result = driver.execute_cdp_cmd('Page.printToPDF', print_options)

    # Get the PDF data, which should be base64 encoded
    pdf_base64 = result['data']

    # Decode the base64 data into bytes
    pdf_content = base64.b64decode(pdf_base64)

    # Write the PDF data to a file
    with open('page.pdf', 'wb') as file:
        file.write(pdf_content)

except Exception as e:
  print("An error occurred:", str(e))

finally:
  # Close the browser window
  driver.quit()
