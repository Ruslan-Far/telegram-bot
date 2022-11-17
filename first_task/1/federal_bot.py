import time
import telebot
from deeppavlov import build_model, configs
from deeppavlov.core.common.file import read_json

bot = telebot.TeleBot('5724405385:AAEiLzNDaJYzRkFC03Pszlfsv7gewWhYLh4')
min_limit = 500
f = open('context.txt', 'r', encoding="utf-8")
context = f.read()
arrayContext = context.split('\n\n')

model_config = read_json('../../squad_ru_bert_infer.json')
model = build_model(model_config, download=True)
# model = build_model(model_config)


# @bot.message_handler(content_types=['text'])
# def get_text_message(message):
#     details = model([context], [message.text])
#     print(details)
#     if details[2][0] > min_limit:
#         if details[0][0] != '':
#             bot.send_message(message.from_user.id, details[0][0])
#         else:
#             bot.send_message(message.from_user.id, '[пусто]')
#     else:
#         bot.send_message(message.from_user.id, 'Я не могу дать достоверный ответ! Задайте вопрос по-другому!')


def search_max(details):
    max_num = -1
    i = 0
    index = 0
    while i < len(details[2]):
        if details[2][i] > max_num:
            max_num = details[2][i]
            index = i
        i += 1
    return index


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    arrayMessage = []
    i = 0
    while i < len(arrayContext):
        arrayMessage.append(message.text)
        i += 1
    details = model(arrayContext, arrayMessage)
    i = search_max(details)
    print(details[0][i])
    print(details[2][i])
    if details[2][i] > min_limit:
        if details[0][i] != '':
            bot.send_message(message.from_user.id, details[0][i])
        else:
            bot.send_message(message.from_user.id, '[пусто]')
    else:
        bot.send_message(message.from_user.id, 'Я не могу дать достоверный ответ! Задайте вопрос по-другому!')


print('bot listening')
while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(e)
        time.sleep(15)


# @bot.message_handler(content_types=['text'])
# def get_text_message(message):
#     details = model(arrayContext, [message.text])
#     print(details)
#     if details[1][0] > min_limit:
#         bot.send_message(message.from_user.id, details[0][0])
#     else:
#         bot.send_message(message.from_user.id, 'Я не могу дать достоверный ответ! Задайте вопрос по-другому!')
