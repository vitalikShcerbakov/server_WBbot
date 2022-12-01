
import csv
import time
from datetime import datetime
from threading import Thread

import schedule
import telebot
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from telebot import types




def get_data_from_website(vc_list):
    
    list_vc: list[int] = [int(val[0]) for val in vc_list if val is not None]
    list_vendor_code = []

    options_chrome = webdriver.ChromeOptions()
    options_chrome.add_argument('--headless')
    options_chrome.add_argument('--no-sandbox')
    s = Service('/usr/local/bin/chromedriver')

    with webdriver.Chrome(
        options=options_chrome,
         service=s) as browser:
        for i, vc in enumerate(list_vc):
            line = []
            url = f'https://www.wildberries.ru/catalog/{vc}/detail.aspx?targetUrl=BP'
            browser.get(url=url)
            time.sleep(3)
            try:
                lst_value = browser.find_element(
                    By.CLASS_NAME, 'delivery__store')
                description = lst_value.text

                if lst_value.text.find('со склада продавца') != -1:
                    status = True 
                else:
                    status = False

            except Exception as e:
                print(f'Not found class "delivery__store": {e}')
                try:
                    time.sleep(3)
                    lst_value = browser.find_element(
                        By.CLASS_NAME, 'product-line__price-now')

                    if lst_value.text.find('Нет в наличии') == -1:
                        description = 'Нет в наличии'
                        status = True
                    else:
                        description = 'Неведомая ебанаая хуйня'
                        status = None
                        
                except Exception as e:
                    print(f'Not found class "product-line__price-now": {e}')
                    description = None
                    status = None
            finally:
                date_now = datetime.now().replace(microsecond=0, second=0)
                list_value = (vc, url, description, status, date_now)
                
                progress_bar = (i + 1) / len(list_vc) * 100
                print(f'Progress: {round(progress_bar, 1)} % {i}/{len(list_vc)}')

            list_vendor_code.append(list_value)

    print(f'Время последнией проверки: {date_now:%Y-%m-%d %H:%M:%S}')
    return list_vendor_code