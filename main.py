# import undetected_chromedriver as webdriver
import csv
import sys
import time

from python_rucaptcha.re_captcha import ReCaptcha

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

url = 'https://www.ceneo.pl/;39543-0v.htm'

page = 1

with open('captcha_api_key.txt', 'r', encoding='utf-8') as f:
    captcha_token = f.read().replace('\n', '')

options=webdriver.ChromeOptions()
# options.add_argument("--start-maximized")
# options.add_argument("--headless")

def captcha_solve(browser):
    """
    Решение капчи
    """
    browser.find_element(By.CSS_SELECTOR, 'div.captcha-bot')
    response_area = browser.find_element(By.ID, 'g-recaptcha-response')
    browser.execute_script("arguments[0].style.display = 'block';",
                           response_area)
    captcha_key = browser.find_element(By.CSS_SELECTOR,
                                       'div.g-recaptcha').get_attribute(
        'data-sitekey')
    button = browser.find_element(By.CSS_SELECTOR, 'button.btn-info')
    recaptcha = ReCaptcha(
        rucaptcha_key=captcha_token,
        websiteURL=link,
        websiteKey=captcha_key,
        mathod='userrecaptcha'
    )
    print('Решаю капчу')
    result = recaptcha.captcha_handler()
    result = result['solution']['gRecaptchaResponse']
    print('Капча Решена!')
    response_area.send_keys(result)
    button.click()
    time.sleep(5)


with webdriver.Chrome(options=options) as browser:
    with open('result.csv', 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['ссылка', 'самая низкая цена 1', 'продавец 1', 'самая низкая цена 2', 'продавец 2', 'количество предложений'])
    while True:
        if page == 1:
            link = url
        else:
            link = f'https://www.ceneo.pl/;39543-0v;0020-30-0-0-{page}.htm'
        browser.get(link)
        try:
            captcha_solve(browser)
        except:
            print(' ')
        products_blocks = browser.find_elements(By.CSS_SELECTOR, 'div.cat-prod-row')
        current_window = browser.window_handles[0]
        iteration=0
        for block in products_blocks:
            # при вводе несуществующей страницы, сайт перекидывает на первую страницу. Чтобы понять что парсинг закончился, беру имя первого товара и буду каждый раз сравнивать текущее имя с ним
            if iteration==0:
                first_product_name = browser.find_element(By.CSS_SELECTOR, 'div.cat-prod-row').find_element(
                    By.CSS_SELECTOR, 'div.cat-prod-row__desc-col').text
            name = block.find_element(By.CSS_SELECTOR, 'div.cat-prod-row__desc-col').text
            if iteration>0:
                if name==first_product_name:
                    sys.exit()
            iteration+=1
            product_link = block.find_element(By.CSS_SELECTOR, 'span.prod-review__qo').find_element(By.TAG_NAME,
                                                                                                    'a').get_attribute(
                'href')
            browser.execute_script("window.open('');")
            new_window = browser.window_handles[1]
            browser.switch_to.window(new_window)
            browser.get(product_link)
            try:
                captcha_solve(browser)
            except:
                print(' ')
            print(f"беру ссылку {product_link}")
            try:
                erotic_button=browser.find_element(By.CSS_SELECTOR, 'button.btn-primary')
                erotic_button.click()
                time.sleep(2)
            except:
                print('')
            offers_button = browser.find_element(By.CSS_SELECTOR, 'li.page-tab').find_element(By.TAG_NAME, 'a')
            offers_count=int("".join([i for i in offers_button.text if i.isdigit()]))
            offers_button.click()
            try:
                show_offers = browser.find_element(By.CSS_SELECTOR, 'div.show-remaining-offers').find_element(
                    By.CSS_SELECTOR, 'span.link')
                browser.execute_script("arguments[0].scrollIntoView(true);", show_offers)
                time.sleep(0.5)
                show_offers.click()
            except:
                print(' ')
            while True:
                offers = browser.find_elements(By.CLASS_NAME, 'product-offers__list__item')
                if len(offers)!=offers_count:
                    time.sleep(0.5)
                    continue
                else:
                    break
            prices_dict = {}
            if len(offers) == 1:
                price = browser.find_element(By.CSS_SELECTOR, 'span.price').text.replace(',', '.')
                seller = offers[0].find_element(By.CSS_SELECTOR, 'li.offer-shop-opinions').find_element(By.TAG_NAME,
                                                                                                        'a').get_attribute(
                    'href').split('sklepy/')[1].split('.pl')[0] + '.pl'
                try:
                    price = float(price)
                except Exception:
                    print('Ошибка цены')
                    continue
                prices_dict[seller] = price
            else:
                for offer in offers:
                    price = offer.find_element(By.CSS_SELECTOR, 'span.price').text.replace(',','.')
                    seller = offer.find_element(By.CSS_SELECTOR, 'li.offer-shop-opinions').find_element(By.TAG_NAME,
                                                                                                        'a').get_attribute(
                        'href').split('sklepy/')[1].split('.pl')[0] + '.pl'
                    try:
                        price = float(price)
                        prices_dict[seller] = price
                    except Exception:
                        print(' ')
            min_values = []
            for item in sorted(prices_dict.items(), key=lambda pair: pair[1]):
                min_values.append(item)
                if len(min_values) == 2:
                    break
            if len(min_values) == 2:
                first_min_price_shop = min_values[0][0]
                first_min_price = str(min_values[0][1]).replace('.', ',')
                second_min_price_shop = min_values[1][0]
                second_min_price = str(min_values[1][1]).replace('.',',')
            else:
                first_min_price_shop = min_values[0][0]
                first_min_price = min_values[0][1]
                second_min_price_shop = '-'
                second_min_price = '-'
            print(product_link)
            with open('result.csv', 'a', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(
                    [product_link, first_min_price, first_min_price_shop, second_min_price, second_min_price_shop, len(offers)])
            browser.close()
            time.sleep(1)
            browser.switch_to.window(current_window)
            continue
        page += 1
