from threading import Thread
import schedule
from datetime import datetime
import time
import csv
from seleniumGet_vendor_code import get_vendor_code
import telebot
from telebot import types
from settings import TG_TOKEN

bot = telebot.TeleBot(TG_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Просмотреть список артикулов")
    btn2 = types.KeyboardButton("Запустить проверку")
    btn3 = types.KeyboardButton("Просмотр последней проверки")
    #btn4 = types.KeyboardButton("Отооновить проверку")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я bot версии 0.9 =))".format(message.from_user),
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    global chat_id
    chat_id = message.chat.id
    if (message.text == "Запустить проверку"):
        bot.send_message(
            message.chat.id, 'Проверка займет некоторое время, подожди....')
        start_check_vc()

    elif message.text == "Просмотреть список артикулов":
        answer = show_result_check()
        for line in answer:       
            bot.send_message(message.chat.id, str(line))

    elif message.text == 'Просмотр последней проверки':
        answer = read_from_datebase()
        for line in answer:
            bot.send_message(message.chat.id, str(line))
        
    else:
        if download_article_list(message.text):
            bot.send_message(message.chat.id, 'Cписок загружен')
        else:
            bot.send_message(message.chat.id, 'Разделитель должен быть пробел или ","')
            bot.send_message(message.chat.id, 'должы быть только цифры')


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

def show_result_check():
    result = read_from_datebase()
    list_vendor_code = [int(value[0]) for value in result if value != None]
    return list_vendor_code

def download_article_list(msg):
    if '\n' in msg or ' ' in msg:
            list_vendor_code = msg.split()
            if all(value.isdigit() for value in list_vendor_code):  # checking for a number
                list_vendor_code = list(map(int, list_vendor_code))
                list_vendor_code = [[vc, None, True]for vc in list_vendor_code]
                write_to_database(list_vendor_code)
                print('Список загружен')
                return True
    return False


def start_check_vc():
    global chat_id

    list_vendor_code = show_result_check()
    answer = get_vendor_code(list_vendor_code)
    write_to_database(answer)
    for line in answer:
        print(line[2])
        if not line[2] or line[2] == 'Error':
            bot.send_message(chat_id, str(line))
            
    bot.send_message(chat_id, 'Провека окончена, для просмотра результата ')



def sheduler():
    schedule.every(10).seconds.do(start_check_vc)
    while True:
        schedule.run_pending()
        time.sleep(1)


Thread(target=sheduler, args=()).start()
bot.polling(none_stop=True)


#bot.infinity_polling()
