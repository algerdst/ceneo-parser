# import undetected_chromedriver as webdriver
import csv
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver


with webdriver.Chrome() as browser:
    browser.get('https://www.ceneo.pl/125540202#tab=click')
    try:
        show_offers = browser.find_element(By.CSS_SELECTOR, 'div.show-remaining-offers').find_element(
            By.CSS_SELECTOR, 'span.link')
        browser.execute_script("arguments[0].scrollIntoView(true);", show_offers)
        show_offers.click()
        time.sleep(2)
    except:
        print(' ')
    offers = browser.find_elements(By.CLASS_NAME, 'product-offers__list__item')
    prices_dict = {}
    if len(offers)==1:
        price=browser.find_element(By.CSS_SELECTOR, 'span.price').text
        seller = offers[0].find_element(By.CSS_SELECTOR, 'li.offer-shop-opinions').find_element(By.TAG_NAME,
                                                                                            'a').get_attribute(
            'href').split('sklepy/')[1].split('.pl')[0] + '.pl'
        price = float(price)
        prices_dict[seller] = price
    else:
        for offer in offers:
            price = offer.find_element(By.CSS_SELECTOR, 'span.price').text.replace(',', '.')
            seller = offer.find_element(By.CSS_SELECTOR, 'li.offer-shop-opinions').find_element(By.TAG_NAME,
                                                                                                'a').get_attribute(
                'href').split('sklepy/')[1].split('.pl')[0] + '.pl'
            try:
                price = float(price)
                prices_dict[seller] = price
            except Exception:
                print(' ')