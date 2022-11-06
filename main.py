import csv
import time
from datetime import datetime
from threading import Thread

import telebot
import schedule
from telebot import types
from selenium import webdriver
from selenium.webdriver.common.by import By

from settings import TG_TOKEN

bot = telebot.TeleBot(TG_TOKEN)


def get_vendor_code():

    result = read_from_datebase()
    list_vc:list[int] =  [int(value[0]) for value in result if value is not None]
    list_vendor_code = []

    options_chrome = webdriver.ChromeOptions()
    options_chrome.add_argument('--headless')

    with webdriver.Chrome(
        options=options_chrome,
         #executable_path='/home/ubuntu/dev/chromedriver') as browser:
         executable_path='/usr/local/bin/chromedriver') as browser:
        for i, vc in enumerate(list_vc):
            line = []
            url = f'https://www.wildberries.ru/catalog/{vc}/detail.aspx?targetUrl=BP'
            try:
                browser.get(url=url)
                time.sleep(3)
                lst_value = browser.find_element(
                    By.CLASS_NAME, 'delivery__store')
                line.append(vc)
                line.append(url)
                line.append(lst_value.text)
                if lst_value.text.find('со склада продавца') != -1:
                    line.append(True)
                else:
                    line.append(False)
            except Exception:
                line.append(vc)
                line.append(url)
                line.append('Error')
                line.append('Error')
            finally:
                progress_bar = i / len(list_vc) * 100
                print(f'Progress: {round(progress_bar, 1)} % {int(progress_bar) * "#"} {i}/{len(list_vc)}')

            list_vendor_code.append(line)
    date_now = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    print(f'Время последнией проверки: {date_now}')
    write_to_database(list_vendor_code)


def notification_on_off(chad_id, flag):
    with open('users_datebase.txt', 'r+') as file:
        data = file.readlines()
        for i, line in enumerate(data):
            id, name, _ = line.split()
            if chad_id == int(id):
                data[i] = f'{id} {name} {flag} \n'
    with open('users_datebase.txt', 'r+') as file:
        print(data)
        file.writelines(data)

        
def write_to_database(list_vc: list) -> None:
    with open('datebase.csv', 'w+') as csv_file:
        writer = csv.writer(csv_file)
        for line in list_vc:
            date_write = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
            line.append(date_write)
            writer.writerow(line)


def read_from_datebase():  # ToDo annotation
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
                break                

    data = read_from_datebase()
    for user in users_id:
        for line_text in data:
            if line_text[3] == 'False':
                bot.send_message(user, line_text[1])

        errors = sum([1 for i in data if i[2] == 'Error'])
        bot.send_message(user, f'Время последней проверки: {line_text[-1]}')
        bot.send_message(user, f'Ошибок {errors}')


@bot.message_handler(commands=['start'])
def start(message):
    with open('users_datebase.txt', 'r+') as file:
        data = file.readlines()
        list_id = []
        try:
            for i in data:
                id, name, flag = i.split()
                list_id.append(int(id))
            print(list_id, message.from_user.first_name)
        except Exception as e:
            print(e)
            
        if message.chat.id not in list_id:
            file.write(f'{message.chat.id} {message.from_user.first_name} {True} \n')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Включить уведомления")
    btn2 = types.KeyboardButton("Выключить уведомления")
    btn3 = types.KeyboardButton("Просмотр последней проверки")
    markup.add(btn1, btn2, btn3)
    bot.send_message(
        message.chat.id, text="Привет, {0.first_name}! Введите /start"
        .format(message.from_user), reply_markup=markup)


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

    elif message.text == 'Просмотр последней проверки':
        answer = read_from_datebase()
        for line in answer:
            bot.send_message(message.chat.id, f'{line[0]} {line[1]} {line[2]}')
        bot.send_message(message.chat.id, f'Время последней проверки: {line[-1]}')

    else:
        if download_article_list(message.text):
            bot.send_message(message.chat.id, 'Cписок загружен')
        else:
            bot.send_message(
                message.chat.id, 'Разделитель должен быть пробел или ","')
            bot.send_message(message.chat.id, 'должы быть только цифры')


def sheduler():
    schedule.every(5).minutes.do(get_vendor_code)
    schedule.every(10).minutes.do(send_message)
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