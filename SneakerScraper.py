# Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import urlretrieve
import os
import csv

# Global variables
DRIVER_PATH = 'chromedriver'
URL = 'https://www.footlocker.com/category/shoes.html'
IMAGE_SAVE_PATH = 'images'
CSV_FILENAME = 'Products.csv'


def get_images(driver, product_name):
    """
    Function to retrieve product images
    :param driver: the webdriver for simulating crawling
    :param product_name: the name of the product being crawled
    :return: None, stores the images, by creating a directory of the product name in the IMAGE_SAVE_PATH
    """
    gallery = driver.find_element_by_class_name("ProductGallery--thumbRow")
    images = gallery.find_elements(By.TAG_NAME, "img")
    for index, image in enumerate(images):
        src = image.get_attribute('src')
        directory = IMAGE_SAVE_PATH + '/' + product_name
        if not os.path.exists(directory):
            os.mkdir(directory)
        urlretrieve(src, directory + '/' + str(index) + '.jpg')


def visit_page(driver: webdriver.Chrome(), link: str):
    """
    Functionality to visit each page of the product
    :param driver: the webdriver for simulating the crawling
    :param link: the link for the product page
    :return: None, saves the product information in a csv file.
    """
    try:
        # Get the product page
        driver.get(link)
        # Wait for the page to load
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ProductDetails-header"))
        )

        # Fetch the product details from the page
        details = driver.find_element_by_class_name("ProductDetails-header")
        product_name = details.find_element_by_class_name("ProductName-primary").text
        description = driver.find_element_by_class_name("ProductDetails-description").text
        price = driver.find_element_by_class_name("ProductPrice").text

        # get images for the product
        get_images(driver, product_name)

    finally:
        pass

    return {'ProductName': product_name, 'Description': description, 'Price': price}


def sneaker_scraper():
    # Load the driver and the url to crawl
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    header = ['ProductName', 'Description', 'Price']

    # Try waiting for the page to load so that all the elements in the page have loaded
    try:
        driver.get(URL)
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ProductCard-link"))
        )

        # Fetch all the products on current page
        cards = driver.find_elements_by_class_name("ProductCard-link")

        # Store the links for the products on the current page in a list
        product_links = []
        for product in cards:
            product_links.append(product.get_attribute('href'))

        # Iterate over the links
        with open(CSV_FILENAME, 'w+') as csv_file:

            writer = csv.DictWriter(csv_file, fieldnames=header)
            writer.writeheader()

            for index, product_link in enumerate(product_links):

                #  Visit each product page individually
                product_data = visit_page(driver, product_link)
                writer.writerow(product_data)

                # Sampling for 5 products
                if index == 5:
                    break

    finally:
        driver.quit()
