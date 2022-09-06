import requests
import json
import telebot
from telebot import types # для указание типов

from threading import Thread
import schedule
import time

TOKEN = '1722383778:AAFr6EEVT9z16sIxOmRhvFDuHcX8mRXquSE'
bot = telebot.TeleBot(TOKEN)

list_vendor_code = []
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Просмотреть список артикулов")
    btn2 = types.KeyboardButton("Запустить проверку")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я bot версии 0.5 =))".format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    global list_vendor_code
    if(message.text == "Запустить проверку"):
        if len(list_vendor_code) == 0:
            bot.send_message(message.chat.id, 'Список пуст, загрузи его')
        else:
            answer = get_stock_info()
            bot.send_message(message.chat.id, str(answer))


    elif message.text == "Просмотреть список артикулов":
        bot.send_message(message.chat.id, str(list_vendor_code))

    else:
        if '\n' in message.text:
            list_vendor_code = message.text.split()
            if all(value.isdigit() for value in list_vendor_code):  # checking for a number
                list_vendor_code = list(map(int, list_vendor_code))
                bot.send_message(message.chat.id, 'Список загружен')
            else:
                bot.send_message(message.chat.id, 'Некорректный ввод, ')
        else:
            bot.send_message(message.chat.id, 'Я тебя не пойму....(((')


def get_stock_info():
    global list_vendor_code
    answer = dict()
    key = 'ZTFhNmVlMWEtYThlYi00ZmM4LTk3MjYtMWU5NTk0YWE4OTlk'
    url = f'https://suppliers-stats.wildberries.ru/api/v1/supplier/stocks'
    response = requests.get(url, params={'key': key, 'dateFrom': '2022-09-05'}).json()
    #list_vendor_code = [58989771, ] #57824933

    for i in response:
        if i['nmId'] in list_vendor_code:
            answer[i['nmId']] = [i['warehouseName'], f'https://www.wildberries.ru/catalog/{i["nmId"]}/detail.aspx?targetUrl=MI']
    return answer

@bot.message_handler(content_types=['text'])
def my_func(message='qw'):
    answer = get_stock_info()
    bot.send_message(message.chat.id, str(answer))

def sheduler():
    schedule.every(10).seconds.do(my_func)
    while True:
        schedule.run_pending()
        time.sleep(1)





Thread(target=sheduler, args=()).start()

bot.polling(none_stop=True)


# 58989771
# 57824933
# warehouseName - скалд
#nmId - 58989771 артикул