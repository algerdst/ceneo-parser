from bs4 import BeautifulSoup
import cloudscraper

import csv
import time

from python_rucaptcha.re_captcha import ReCaptcha

from selenium.webdriver.common.by import By
from selenium import webdriver


def get_links():
    """
    Собирает ссылки на товары
    :return:
    """
    headers = {
        'authority': 'www.ceneo.pl',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ru,en;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': '__utmf=911e946285f38d6c35d59ce603c665b2_IVYn7PurqlDb0ZCK8zu6ug%3D%3D; tc=testName=SearchRerankABTest&testVariant=3&testType=75&activeTest=SearchRerankABTest; sv2=1dda5c43-c29d-11ee-b37c-123c675a94ab; sv3=1.0_1dda5c43-c29d-11ee-b37c-123c675a94ab; userCeneo=ID=01397253-29dd-47b4-83ba-a21996902fa0&sc=1&mvv=0&nv=0; ai_user=95w6U|2024-02-03T14:04:16.410Z; _ga=GA1.2.2092835599.1706969057; browserBlStatus=0; ga4_ga=GA1.2.1dda5c43-c29d-11ee-b37c-123c675a94ab; consentcookie=eyJDb25zZW50cyI6WzQsMywyLDFdLCJWZXJzaW9uIjoidjEifQ==; FPID=FPID2.2.rIXbF53MytSWbx7HmocoACs8vkkJWInBHEorOzrqkYY%3D; _gcl_au=1.1.404764246.1706969138; _fbp=fb.1.1706969137803.712612052; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22unknown%22%7D; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22tdii9sfDXBykBK9jX6S5%22%7D; nps3=SessionStartTime=1706969897,SurveyId=59,ClosedOrCompleted=True; __RequestVerificationToken=ggP-DXfZLGU46NVF3_Nbi6NI1vqLKx1vsHnJpTL8KqGvD36V21vqXie1HXOk2Aa5q4gYvpzimx89Thg4rQs2fz6U1x6WLVts_K9IMiT5VbA1; st2=sref%3dhttps%3a%2f%2fkwork.ru%2f%2c_t%3d63842716313%2cencode%3dtrue; _gid=GA1.2.1066160768.1707115914; cProdCompare_v2=; FPLC=Oai7cfTSr0NZPatf8avG4dYU0RnnCCDjrWb9RmmcmYP8FSywex9JxkmbPm6vuh2EtvvJoU3I3PbUtYTQ%2BIjGibAEZWh%2BTHCO%2FdaGM9X0qLgo2FM%3D; cnaca=True; ai_sessionclicks=CIPAN0xuKaUuPv4qbSJ00v|1707130552823|1707130906177; rc=Mh4ufYzEpbU51+jlO9Tn617qesRi2JGZeCioCURo0uzM7zMsrLdVNAyIDTLo4hs2XKb9By6+MTOrbyphkd+jYLybIgldeygTiHvPBhn8KseANWlxi/RQ8oJXGWGI0jdSZidSOMmGsWR+cpwzPRL+TQaSFAqfTf2uq28qYZHfo2C3u4UYIGW0V843rTbH13iWx3rSPaPSiXAV0OiG+bv4KatvKmGR36NgeWOshvYPqIkrmv/V0Pe5fQQpH4Yy+kDHqbqhbAKKF1laNy9SMh+S0QUWOcDUwZynTo1/RemlQw8YV+Q9JQSx9LNppc79WCU6mS3Dd94MyyRew5fC76uU0txLFObUisUkeCioCURo0uw1Im/7V/L9MNsWGx+idwQ+; mbc=; __gads=ID=44e54af0a162b308:T=1706969057:RT=1707132440:S=ALNI_MbXiu9taZ42sYeV7I2AVkXFPmRXEQ; __gpi=UID=00000d4f96def4a1:T=1706969057:RT=1707132440:S=ALNI_MZz3Y20STslzcsUIzAFiSYwLoqPyQ; __eoi=ID=ad67e091be9d8265:T=1706969057:RT=1707132440:S=AA-AfjanVx5Ye0qGVOwBMY0JnxCT; ai_session=1u+fz|1707124877861|1707132584645.8; ga4_ga_K2N2M0CBQ6=GS1.2.1707124878.5.1.1707132585.0.0.0; mbc=',
        'referer': 'https://www.ceneo.pl/;39543-0v;0020-30-0-0-5.htm',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "YaBrowser";v="24.1", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36'
    }

    url = 'https://www.ceneo.pl/;39543-0v.htm'
    scraper = cloudscraper.create_scraper()
    pages = 18
    links = []
    print('[+][+][+][+][+] СБОР ССЫЛОК [+][+][+][+][+]')
    for page in range(pages):
        if page == 1:
            link = url
        else:
            link = f'https://www.ceneo.pl/;39543-0v;0020-30-0-0-{page}.htm'
        response = scraper.get(link, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        blocks = soup.findAll('div', class_='cat-prod-row')

        for block in blocks:
            item_link = 'https://www.ceneo.pl' + block.find('span', class_='prod-review__qo').find('a')['href']
            links.append(item_link)
            print(item_link)
        page += 1
    print(len(links))
    print('[+][+][+][+][+] ССЫЛКИ СОБРАНЫ [+][+][+][+][+]')
    print()
    print('[+][+][+][+][+] СБОР ДАННЫХ О ТОВАРЕ [+][+][+][+][+]')
    return links

with open('captcha_api_key.txt', 'r', encoding='utf-8') as f:
    captcha_token = f.read().replace('\n', '')

def captcha_solve(browser,link):
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
    options=webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    with webdriver.Chrome(options=options) as browser:
        with open('result.csv', 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['ссылка', 'самая низкая цена 1', 'продавец 1', 'самая низкая цена 2', 'продавец 2'])
            for link in product_links:
                browser.get(link)
                try:
                    captcha_solve(browser, link)
                except:
                    print(' ')
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
                    try:
                        second_min_price_shop = min_values[1][0]
                        second_min_price = str(min_values[1][1]).replace('.',',')
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


if __name__=='__main__':
    product_links=get_links()
    get_info(product_links)
