# importing the necessary libraries.
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

# the number of products you want to scrape.
desired_products = 50

# the main function that scrapes the data and puts it into a csv file.
def scrape_page():
    product = browser.find_elements(By.XPATH, "//span[@class='a-size-medium a-color-base a-text-normal']")
    price_elements = browser.find_elements(By.XPATH, "//div[@data-asin]//span[@class='a-price-whole']")

    for prod, cost in zip(product, price_elements):
        products.append(prod.text)
        prices.append(cost.text)

        # Print the data
        print(prod.text.strip() + " - " + cost.text)
        print("\n\n\n")

        # Write the data to CSV file
        csv_writer.writerow([prod.text.strip(), cost.text])

        
# Launch the browser and navigate to the webpage
browser = webdriver.Chrome()
browser.get('https://www.amazon.in')
browser.maximize_window()

# Get the input elements
input_search = browser.find_element(By.ID, 'twotabsearchtextbox')
search_button = browser.find_element(By.XPATH, "(//input[@type='submit'])[1]")

# Send the input to the webpage
input_search.send_keys("Smartphones under 10000")
search_button.click()

products = []
prices = []
scraped_products = 0

# Create a CSV file and write header
with open('amazon_smartphones_under_Rs_10000.csv', mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Product', 'Price'])

    while scraped_products < desired_products:
        print('Scraping page', scraped_products // 10 + 1)
        scrape_page()

        # Check if the desired number of products is reached
        if scraped_products >= desired_products:
            break

        try:
            next_button = browser.find_element(By.XPATH, "//a[text()='Next']")
            next_button.send_keys(Keys.RETURN)
        except:
            print('Could not find Next button. Exiting...')
            break

        # Add a delay between requests
        sleep(5)

        # Update the number of scraped products
        scraped_products = len(products)

browser.quit()
