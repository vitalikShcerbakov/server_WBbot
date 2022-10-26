from selenium import webdriver
from selenium.webdriver.common.by import By
import time
#
# lst = [52232480, 52233119, 52233721,
#        52234352, 67578772, 67586679, 67591155, 82455840, 67588134, 38272884, 38272572, 38272793, 38272922, 34964682,
#        31066345, 33147977, 33144939, 88107650, 88108097, 88108208, 113068831, 113068944]


def get_vendor_code(list_vc):
    list_vendor_code = []

    options_chrome = webdriver.ChromeOptions()
    options_chrome.add_argument('--headless')

    with webdriver.Chrome(options=options_chrome, executable_path='/usr/local/bin/chromedriver') as browser:
        for vc in list_vc:
            try:

                url = f'https://www.wildberries.ru/catalog/{vc}/detail.aspx?targetUrl=BP'
                browser.get(url=url)
                time.sleep(3)
                lst_value = browser.find_element(By.CLASS_NAME, 'delivery__store')

                if not lst_value.text == 'со склада продавца':
                    list_vendor_code.append(f'ВНИМАНИЕ!!! Артикул - {vc} {url} {lst_value.text}')

                #list_vendor_code.append(f'{url} OK')  # Закоментировать строку при работе с ботом

            except Exception:
                list_vendor_code.append(f'Произошла ошибка! Артикул {vc} ---- {url}')

    return list_vendor_code
