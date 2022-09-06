from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import schedule
import telebot
from telebot import types


TOKEN = '1722383778:AAFr6EEVT9z16sIxOmRhvFDuHcX8mRXquSE'
bot = telebot.TeleBot(TOKEN)

lst_vendor_code = []
vendor_code_error = []

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, '''Привет) Это версия 000000.2 =))
                            Для загрузки списка артикулов набери - "list"
                            Для старта набери -  "run"
                            Для просмотра списка артикулов набери - "show"
                            ''')


@bot.message_handler(content_types='text')
def message_reply(message):
    global lst_vendor_code

    if message.text == "list":
        bot.send_message(message.chat.id, "Загрузи сюда чтонибудь")

    elif message.text == 'run':
        if len(lst_vendor_code) == 0:
            bot.send_message(message.chat.id, 'Список пуст, загрузите список атрибутов')  # Отправка сообщения
        for vc in lst_vendor_code:
            msg = get_name_stock(vc)
            bot.send_message(message.chat.id, msg)  # Отправка сообщения

        bot.send_message(message.chat.id, f'Проверка завершена, Ошибок - {len(vendor_code_error)}')
        #bot.send_message(message.chat.id, 'Проверка завершена')

    elif message.text == 'show':
        if len(lst_vendor_code) == 0:
            bot.send_message(message.chat.id, 'Список пуст, загрузите список атрибутов')  # Отправка сообщения
        else:
            bot.send_message(message.chat.id, str(lst_vendor_code))

    elif message.text == 'time':
        pass


    else:
        if '\n' in message.text:
            lst_vendor_code = message.text.split()
            if all(value.isdigit() for value in lst_vendor_code):  # checking for a number
                lst_vendor_code = list(map(int, lst_vendor_code))
                bot.send_message(message.chat.id, 'Список загружен, для просмотра введи - "show"')
        else:
            bot.send_message(message.chat.id, '''Я тебя не пойму....(((
                            Для загрузки списка артикулов набери - "list"
                            Для старта набери -  "run"
                            Для просмотра списка - "show"
                            ''')


def get_name_stock(vc):
    global vendor_code_error
    try:
        time.sleep(5)
        url = f'https://www.wildberries.ru/catalog/{vc}/detail.aspx?targetUrl=BP'

        with webdriver.Chrome(executable_path='/usr/local/bin/chromedriver') as browser:
            browser.get(url=url)
            lst_value = browser.find_element(By.CLASS_NAME, 'delivery__store')

            if not lst_value.text == 'со склада продавца':
                return f'ВНИМАНИЕ!!! Артикул - {vc} {url} {lst_value.text} '

            return f'{vc}{url} OK'
    except Exception:
        vendor_code_error.append(vc)
        return f'Произошла ошибка! Арктикул {vc}'


bot.infinity_polling()
