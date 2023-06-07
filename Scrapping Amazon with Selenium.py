#!/usr/bin/env python
# coding: utf-8

# ### Introduction
# This code extracts details from the Amazon web store using Selenium, a library for web scraping. Please note that if the website updates its system and changes the HTML elements, the code may no longer work. As of now, the code functions correctly.

# In[ ]:


# Installing webdriver manager
pip install webdriver-manager


# In[11]:


# Import webdriver
from selenium import webdriver

# Import time
import time

# import service
from selenium.webdriver.chrome.service import Service

# Import webdriver manager
from webdriver_manager.chrome import ChromeDriverManager 

#Importing web driver by function
from selenium.webdriver.common.by import By

# Import NoSuchElementException
from selenium.common.exceptions import NoSuchElementException


# In[ ]:


# Adding your Chrome driver path
CHROME_DRIVER_PATH = 'Users/user/Downloads/chromedriver_mac64/chromedriver'

# initialize the Selenium WebDriver
driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)

# create a driver object using driver_path as a parameter
driver = webdriver.Chrome(service = Service(executable_path=CHROME_DRIVER_PATH))


# In[ ]:


# Create object ChromeOptions()
chrome_options = webdriver.ChromeOptions()            
chrome_options.add_argument('--headless')           
chrome_options.add_argument('--no-sandbox')                             
chrome_options.add_argument('--disable-dev-shm-usage')

driver= webdriver.Chrome(options=chrome_options, service = Service(ChromeDriverManager().install()))


# In[12]:


# assign your website to scrape
URL = 'https://www.amazon.com'

# Opening the URL with driver.get()
driver.get(URL)


# In[1]:


# Writing a function that scrapes informations out of Amazon
def scrape_amazon(search_term, max_pages):
    '''
    This function scrapes the products title, price, and ratings. It takes two arguments;
    search_term: This is the item we want to scrape
    max_pages: This is the number of pages we want to loop through on the Amazon webpage.
    '''
    # Find the search box and input the search term
    search_field = driver.find_element(By.ID,'twotabsearchtextbox')
    search_field.send_keys(search_term)
    
    # Click the search button
    search_button = driver.find_element(By.ID,'nav-search-submit-button')
    search_button.click()
    
    # set a timer delay
    time.sleep(5)
    
    # Initialize an empty list to store the results
    results = []

    # Loop through the specified number of pages
    for i in range(max_pages):
        
        # Wait for the page to load
        time.sleep(5)
        
        # Find all of the search result elements on the page
        search_results = driver.find_elements(By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')
        
        # Loop through each search result and extract the product information
        for result in search_results:
            
            # Extracting the products title
            try:
                title = result.find_element(By.CSS_SELECTOR,"h2 a span").text
            except NoSuchElementException:
                title = "N/A"
            
            # Extracting the products price
            try:
                whole_price = result.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
                fraction_price = result.find_elements(By.XPATH, './/span[@class="a-price-fraction"]')
                price = '.'.join([whole_price[0].text, fraction_price[0].text])
            except NoSuchElementException:
                price = "N/A"
            
            # Extracting the products ratings
            try:
                ratings_box = result.find_elements(By.XPATH, './/div[@class="a-row a-size-small"]/span')
                ratings = ratings_box[0].get_attribute('aria-label')
            except NoSuchElementException:
                ratings = "N/A"

            # Add the product information to the list of results
            results.append({
                "title": title,
                "price": price,
                "rating": ratings
            })

        # Click the "Next" button
        try:
            next_button = driver.find_element(By.CSS_SELECTOR,"a.s-pagination-next")
            next_button.click()
        except NoSuchElementException:
            break

    # Close the browser window
    driver.quit()
    return results #Return the list


# In[13]:


search_term = 'Iphone'
max_pages = 2
scrape_amazon(search_term, max_pages)


# In[ ]:




