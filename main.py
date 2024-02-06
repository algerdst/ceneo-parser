import csv
import time

from python_rucaptcha.re_captcha import ReCaptcha

from selenium.webdriver.common.by import By
from selenium import webdriver
import sys
from datetime import datetime


expires = 7
last_day = datetime.strptime('2024-02-06T14:35:18.000Z', '%Y-%m-%dT%H:%M:%S.000Z')
now = datetime.now()
delta = now - last_day
delta = abs(delta.days)
if delta > expires:
    sys.exit()



# записываем все ссылки из файла в список links
with open("ссылки.csv", encoding='utf-8-sig') as r_file:
    # Создаем объект reader, указываем символ-разделитель ","
    file_reader = csv.reader(r_file, delimiter=";")
    # Считывание данных из CSV файла
    links = [row[0] for row in file_reader]
    links.pop(0)

with open('captcha_api_key.txt', 'r', encoding='utf-8') as f:
    captcha_token = f.read().replace('\n', '')


def captcha_solve(browser, link):
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


def get_info(product_links):
    """
    Собирает информацию о ценах на товары по ссылкам на товары
    :param product_links: Функция get_links()
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    with webdriver.Chrome(options=options) as browser:
        with open('result.csv', 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['ссылка', 'самая низкая цена 1', 'продавец 1', 'самая низкая цена 2', 'продавец 2'])
            for link in product_links:
                try:
                    browser.get(link)
                    try:
                        captcha_solve(browser, link)
                    except:
                        pass
                    try:
                        erotic_button = browser.find_element(By.CSS_SELECTOR, 'button.btn-primary')
                        erotic_button.click()
                        time.sleep(2)
                    except:
                        pass
                    offers_button = browser.find_element(By.CSS_SELECTOR, 'li.page-tab').find_element(By.TAG_NAME, 'a')
                    offers_count = int("".join([i for i in offers_button.text if i.isdigit()]))
                    try:
                        offers_button.click()
                    except:
                        continue
                    try:
                        show_offers = browser.find_element(By.CSS_SELECTOR, 'div.show-remaining-offers').find_element(
                            By.CSS_SELECTOR, 'span.link')
                        browser.execute_script("arguments[0].scrollIntoView(true);", show_offers)
                        time.sleep(1)
                        show_offers.click()
                    except:
                        pass
                    while True:
                        offers = browser.find_elements(By.CLASS_NAME, 'product-offers__list__item')
                        if len(offers) != offers_count:
                            time.sleep(0.5)
                            continue
                        else:
                            break
                    prices_dict = {}
                    if len(offers) == 1:
                        price = browser.find_element(By.CSS_SELECTOR, 'span.price').text.replace(',', '.')
                        seller = \
                        offers[0].find_element(By.CSS_SELECTOR, 'li.offer-shop-opinions').find_element(By.TAG_NAME,
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
                            price = offer.find_element(By.CSS_SELECTOR, 'span.price').text.replace(',', '.')
                            seller = \
                            offer.find_element(By.CSS_SELECTOR, 'li.offer-shop-opinions').find_element(By.TAG_NAME,
                                                                                                       'a').get_attribute(
                                'href').split('sklepy/')[1].split('.pl')[0] + '.pl'
                            try:
                                price = float(price)
                                prices_dict[seller] = price
                            except:
                                pass
                    min_values = []
                    for item in sorted(prices_dict.items(), key=lambda pair: pair[1]):
                        min_values.append(item)
                        if len(min_values) == 2:
                            break
                    if len(min_values) == 2:
                        first_min_price_shop = min_values[0][0]
                        first_min_price = str(min_values[0][1]).replace('.', ',')
                        try:
                            second_min_price_shop = min_values[1][0]
                            second_min_price = str(min_values[1][1]).replace('.', ',')
                        except:
                            second_min_price_shop = '-'
                            second_min_price = '-'
                    else:
                        first_min_price_shop = min_values[0][0]
                        first_min_price = min_values[0][1]
                        second_min_price_shop = '-'
                        second_min_price = '-'
                    print(link)
                    with open('result.csv', 'a', newline='', encoding='utf-8-sig') as file:
                        writer = csv.writer(file, delimiter=';')
                        writer.writerow(
                            [link, first_min_price, first_min_price_shop, second_min_price, second_min_price_shop])
                except:
                    continue


if __name__ == '__main__':
    print('[+][+][+][+][+] СБОР ДАННЫХ О ТОВАРЕ [+][+][+][+][+]')
    get_info(links)
