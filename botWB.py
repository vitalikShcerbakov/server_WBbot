from selenium import webdriver
from selenium.webdriver.common.by import By
import time

import telebot

TOKEN = '1722383778:AAFr6EEVT9z16sIxOmRhvFDuHcX8mRXquSE'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Введите список артикулов")

@bot.message_handler(content_types='text')
def get_lst_vendor_code(message):
    bot.send_message(message.chat.id, 'Проверка началась, это может занять несколько минут')
    #bot.reply_to(message, message.text)    # Отправка сообщения
    for vc in message.text.split():
        msg = get_name_stock(vc)
        bot.send_message(message.chat.id, msg)  # Отправка сообщения

    bot.send_message(message.chat.id, 'Проверка завершена')


@bot.message_handler(commands=['time'])
def execution_interval(message):
    bot.send_message(message.chat.id, 'Введите время в минутах')



def get_name_stock(vc):
    try:
        time.sleep(5)
        url = f'https://www.wildberries.ru/catalog/{vc}/detail.aspx?targetUrl=BP'

        with webdriver.Chrome(executable_path='/usr/local/bin/chromedriver') as browser:
            browser.get(url=url)
            lst_value = browser.find_element(By.CLASS_NAME, 'delivery__store')

            if not lst_value.text == 'со склада продавца':
                return f'ВНИМАНИЕ!!! Артикул - {vc} {url} {lst_value.text} '

            return f'{url} OK'
    except Exception:
        return f'Произошла ошибка! Арктикул {vc}'

bot.infinity_polling()