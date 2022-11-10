from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import urlretrieve

DRIVER_PATH = 'chromedriver'
URL = 'https://www.footlocker.com/category/shoes.html'
IMAGE_SAVE_PATH = 'images'


def get_images(driver, product_name):
    gallery = driver.find_element_by_class_name("ProductGallery--thumbRow")
    images = gallery.find_elements(By.TAG_NAME, "img")
    for index, image in enumerate(images):
        src = image.get_attribute('src')
        urlretrieve(src, IMAGE_SAVE_PATH + '/' + product_name + str(index) + '.jpg')


def visit_page(driver: webdriver.Chrome(), link: str):
    try:
        driver.get(link)
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ProductDetails-header"))
        )
        details = driver.find_element_by_class_name("ProductDetails-header")
        product_name = details.find_element_by_class_name("ProductName-primary").text
        description = driver.find_element_by_class_name("ProductDetails-description").text
        reviews_tab = driver.find_element_by_id("ProductDetails-tabs-reviews-tab")
        rating = reviews_tab.find_element(By.XPATH,
                                          '//*[@id="BVRRSummaryContainer"]/div/div/div/div/div/div/dl/dd[1]/div/a/span').text
        price = driver.find_element_by_class_name("ProductPrice").text
        print(product_name, description, rating, price)
        get_images(driver, product_name)

    finally:
        pass


def main():
    # Load the driver and the url to crawl
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    driver.get(URL)

    # Try waiting for the page to load so that all the elements in the page have loaded
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ProductCard-link"))
        )
        cards = driver.find_elements_by_class_name("ProductCard-link")
        for index, card in enumerate(cards):
            product_link = card.get_attribute('href')
            visit_page(driver, product_link)
            if index == 5:
                break

    finally:
        driver.quit()


if __name__ == '__main__':
    main()
