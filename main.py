import csv
import time
from datetime import datetime
from threading import Thread

import telebot
import schedule
from telebot import types
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from settings import TG_TOKEN

bot = telebot.TeleBot(TG_TOKEN)
TIME_SENDING_MESSAGE = 25
TIME_CHECK_VENDOR_CODE = 20

def get_vendor_code():

    result = read_from_datebase()
    list_vc:list[int] =  [int(value[0]) for value in result if value is not None]
    list_vendor_code = []

    options_chrome = webdriver.ChromeOptions()
    options_chrome.add_argument('--headless')
    options_chrome.add_argument('--no-sandbox')
    s = Service('/home/ubuntu/dev/WBbot/chromedriver')
    #s = Service('/usr/local/bin/chromedriver')

    with webdriver.Chrome(
        options=options_chrome,
         service=s) as browser:
        for i, vc in enumerate(list_vc):
            line = []
            url = f'https://www.wildberries.ru/catalog/{vc}/detail.aspx?targetUrl=BP'
            line.append(vc)
            line.append(url)
            browser.get(url=url)
            time.sleep(3)
            try:
                lst_value = browser.find_element(
                    By.CLASS_NAME, 'delivery__store')
                line.append(lst_value.text)

                if lst_value.text.find('со склада продавца') != -1:
                    line.append(True)
                else:
                    line.append(False)

            except Exception as e:
                print(f'Not found class "delivery__store": {e}')
                try:
                    time.sleep(3)
                    lst_value = browser.find_element(
                        By.CLASS_NAME, 'product-line__price-now')

                    if lst_value.text.find('Нет в наличии') == -1:
                        line.append('Нет в наличии')
                        line.append(False)
                    else:
                        line.append('Неведомая ебанаая хуйня')

                except Exception as e:
                    print(f'Not found class "product-line__price-now": {e}')
                    line.append('Error')
                    line.append('Error')
            finally:
                date_now = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
                line.append(date_now)
                progress_bar = (i + 1) / len(list_vc) * 100
                print(f'Progress: {round(progress_bar, 1)} % {int(progress_bar) * "#"} {i}/{len(list_vc)}')

            list_vendor_code.append(line)
    
    print(f'Время последнией проверки: {date_now}')
    write_to_database(list_vendor_code)

        
def write_to_database(list_vc: list) -> None:
    with open('datebase.csv', 'w+') as csv_file:
        writer = csv.writer(csv_file)
        for line in list_vc:
            writer.writerow(line)


def read_from_datebase(): 
    result = []
    with open('datebase.csv', 'r') as csv_file:
        spamreader = csv.reader(csv_file, delimiter=',', quotechar='|')
        for row in spamreader:
            result.append(row)
    return result


def download_article_list(msg):
    if '\n' in msg or ' ' in msg:
        list_vendor_code = msg.split()
        if all(value.isdigit() for value in list_vendor_code):
            list_vendor_code = list(map(int, list_vendor_code))
            list_vendor_code = [[vc, None, True] for vc in list_vendor_code]
            write_to_database(list_vendor_code)
            print('Список загружен')
            return True
    return False


def send_message():
    '''Функция рассылки сообщений пользователям'''
    users_id = []
    with open('users_datebase.txt', 'r') as file:
        file_read = file.readlines()
        for line in file_read:
            try:
                id, name, flag = line.split()
                if flag != 'False':
                    users_id.append(id)
            except Exception as e:
                print(f'Error added userd in list - send_message: {e}')
                                
    bad_product_detected = False
    data = read_from_datebase()
    for user in users_id:
        for line_text in data:
            if line_text[3] == 'False' and line_text[2] != 'Нет в наличии':
                bot.send_message(user, line_text[1])
                bad_product_detected = True
    if bad_product_detected:
        bad_product = sum([1 for i in data if i[2] == 'Нет в наличии'])
        errors = sum([1 for i in data if i[3] == 'Error'])
        if bad_product:
            bot.send_message(user, f'Товар закончился: {bad_product}')
        if errors:
            bot.send_message(user, f'Ошибок: {errors}')
        bot.send_message(user, f'Время последней проверки: {line_text[-1]}')

def notification_on_off(chad_id, flag):
    with open('users_datebase.txt', 'r') as file:
        data = file.readlines()
        new_data = []
        try:
            for i, line in enumerate(data):
                id, name, _ = line.split()
                if chad_id == int(id):
                    new_data.append(f'{id} {name} {flag} \n')
                else:
                    new_data.append(line)
        except Exception as e:
         print(f'Error - notification_on_off : {e}')
    with open('users_datebase.txt', 'w') as file:
        file.writelines(new_data)

@bot.message_handler(commands=['start'])
def start(message):
    with open('users_datebase.txt', 'r+') as file:
        data = file.readlines()
        list_id = []
        try:
            for i in data:
                id, name, flag = i.split()
                list_id.append(int(id))
        except Exception as e:
            print(e)
            
        if message.chat.id not in list_id:
            file.write(f'{message.chat.id} {message.from_user.first_name} {True} \n')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Включить уведомления")
    btn2 = types.KeyboardButton("Выключить уведомления")
    btn3 = types.KeyboardButton("Просмотр не выкупленных товаров")
    btn4 = types.KeyboardButton("Просмотр товаров 'Нет в наличии'")
    btn5 = types.KeyboardButton("Полный просмотр")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(
        message.chat.id, text="Привет, {0.first_name}! Теперь ты подписан(а) на рассылку =)"
        .format(message.from_user), reply_markup=markup)
    bot.send_message(message.chat.id, f'Уведомления будут приходить каждые {TIME_SENDING_MESSAGE} мин')


@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "Включить уведомления"):
        notification_on_off(message.chat.id, True)
        bot.send_message(
            message.chat.id, 'Уведомления включены')

    elif (message.text == "Выключить уведомления"):
        notification_on_off(message.chat.id, False)
        bot.send_message(
            message.chat.id, 'Уведомления выключены')

    elif message.text == 'Просмотр не выкупленных товаров':
        answer = read_from_datebase()
        for line in answer:
            if line[3] == 'False' and line[2] != 'Нет в наличии':
                bot.send_message(message.chat.id, f'{line[1]}')

    elif message.text == "Просмотр товаров 'Нет в наличии'":
        answer = read_from_datebase()
        for line in answer:
            if line[2] == 'Нет в наличии':
                bot.send_message(message.chat.id, f'{line[1]}')
        bot.send_message(message.chat.id, f'Время последней проверки: {line[-1]}')

    elif message.text == 'Полный просмотр':
        answer = read_from_datebase()
        for line in answer:
            bot.send_message(message.chat.id, f'{line[0]} {line[1]} {line[4]}')
        bot.send_message(message.chat.id, f'Время последней проверки: {line[-1]}')

    else:
        if download_article_list(message.text):
            bot.send_message(message.chat.id, 'Cписок загружен')
        else:
            bot.send_message(
                message.chat.id, 'Разделитель должен быть пробел или ","')
            bot.send_message(message.chat.id, 'должы быть только цифры')


def sheduler():
    schedule.every(TIME_CHECK_VENDOR_CODE).minutes.do(get_vendor_code)
    schedule.every(TIME_SENDING_MESSAGE).minutes.do(send_message)
    while True:
        schedule.run_pending()
        time.sleep(1)


Thread(target=sheduler, args=()).start()
bot.polling(none_stop=True, timeout=5, interval=1)

while True:
    try:
        bot.polling(non_stop=True, interval=0)
    except Exception as e:
        print(e)
        time.sleep(5)
        continue
