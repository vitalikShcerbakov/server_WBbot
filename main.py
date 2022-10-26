import re
from threading import Thread
import schedule
import time
from seleniumGet_vendor_code import get_vendor_code
import telebot
from telebot import types

from settings import TG_TOKEN
from datebase import read_from_datebase, write_to_database


bot = telebot.TeleBot(TG_TOKEN)

result = read_from_datebase()
list_vendor_code = [value[0] for value in result]

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Просмотреть список артикулов")
    btn2 = types.KeyboardButton("Запустить проверку")
    btn3 = types.KeyboardButton("Загрузить список артикулов")
    btn4 = types.KeyboardButton("Отооновить проверку")
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я bot версии 0.6 =))".format(message.from_user),
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    global list_vendor_code
    global chat_id
    chat_id = message.chat.id
    if (message.text == "Запустить проверку"):
        start_check_vc()

    elif message.text == "Просмотреть список артикулов":
        result = read_from_datebase()
        result = [value[0] for value in result]
        bot.send_message(message.chat.id, str(result))

    elif message.text == 'Загрузить список артикулов':
        bot.send_message(message.chat.id, 'Заргузи сюда список с артикулами')
        pass
    else:
        if '\n' in message.text or ' ' in message.text:
            list_vendor_code = message.text.split()
            if all(value.isdigit() for value in list_vendor_code):  # checking for a number
                list_vendor_code = list(map(int, list_vendor_code))
                bot.send_message(message.chat.id, 'Список загружен')
            else:
                bot.send_message(message.chat.id, 'Некорректный ввод, ')
        else:
            bot.send_message(message.chat.id, 'Я тебя не пойму....(((')


def start_check_vc():
    global list_vendor_code
    global chat_id

    bot.send_message(
            chat_id, 'Проверка займет некоторое время, подожди....')
    answer = get_vendor_code(list_vendor_code)
    for line in answer:
        write_to_database(line)
        if not line[2]:
            bot.send_message(chat_id, str(line))


# def sheduler():
#     schedule.every(10).minutes.do(start_check_vc)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)


# Thread(target=sheduler, args=()).start()
# bot.polling(none_stop=True)


bot.infinity_polling()
