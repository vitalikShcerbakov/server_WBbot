import requests
from settings import WB_API, TG_TOKEN
import telebot
from telebot import types  # для указание типов
from threading import Thread
import schedule
import time

TOKEN = TG_TOKEN
bot = telebot.TeleBot(TOKEN)

minutes = 10
list_vendor_code = []


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Просмотреть список артикулов")
    btn2 = types.KeyboardButton("Запустить проверку")
    btn3 = types.KeyboardButton("Задать интервал")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я bot версии 0.5 =))".format(message.from_user),
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    global list_vendor_code
    global minutes
    if (message.text == "Запустить проверку"):
        if len(list_vendor_code) == 0:
            bot.send_message(message.chat.id, 'Список пуст, загрузи его')
        else:
            answer = get_stock_info()
            bot.send_message(message.chat.id, str(answer))


    elif message.text == "Просмотреть список артикулов":
        bot.send_message(message.chat.id, str(list_vendor_code))

    elif message.text == 'Задать интервал':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("1 мин")
        item2 = types.KeyboardButton("5 мин")
        item3 = types.KeyboardButton("10 мин")
        item4 = types.KeyboardButton("15 мин")
        item5 = types.KeyboardButton("В главное меню")
        markup.add(item1, item2, item3, item4, item5)
        bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)
    elif message.text == '1 мин':
        minutes = 1
    elif message.text == '5 мин':
        minutes = 5
    elif message.text == '10 мин':
        minutes = 10
    elif message.text == '15 мин':
        minutes = 15
    elif message.text == 'В главное меню':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Просмотреть список артикулов")
        btn2 = types.KeyboardButton("Запустить проверку")
        btn3 = types.KeyboardButton("Задать интервал")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я bot версии 0.5 =))".format(message.from_user),
                         reply_markup=markup)
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

    key = WB_API
    # url = f'https://suppliers-stats.wildberries.ru/api/v1/supplier/stocks'
    url = f'https://suppliers-stats.wildberries.ru/api/v1/supplier/orders'

    response = requests.get(url, params={'key': key, 'dateFrom': '2022-09-05'}).json()

    for i in response:
        if i['nmId'] in list_vendor_code:
            answer[i['nmId']] = [i['warehouseName'],
                                 f'https://www.wildberries.ru/catalog/{i["nmId"]}/detail.aspx?targetUrl=MI']
    return answer


def my_func():
    answer = get_stock_info()
    bot.send_message(815599051, str(answer))   # ToDo получение id chat
    print('i am working')


def sheduler():
    global minutes
    schedule.every(minutes).minutes.do(my_func)
    while True:
        schedule.run_pending()
        time.sleep(1)


Thread(target=sheduler, args=()).start()

bot.polling(none_stop=True)

# 58989771
# 57824933
# warehouseName - скалд
# nmId - 58989771 артикул
