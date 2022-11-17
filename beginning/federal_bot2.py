import time
import telebot
from deeppavlov import build_model, configs
from deeppavlov.core.common.file import read_json

bot = telebot.TeleBot('5724405385:AAEiLzNDaJYzRkFC03Pszlfsv7gewWhYLh4')
context = ''
otherAnswer = 'Не знаю ответ'

model_config = read_json('../squad_ru_bert_infer.json')
# model = build_model(model_config, download=True)
model = build_model(model_config)

@bot.message_handler(content_types=['text'])
def get_text_message(message):
    global context
    if message.text[:3] == '/c ':
        context = message.text[3:]
    elif message.text[:3] == '/q ':
        answer = model([context], [message.text[3:]])[0][0]
        if answer != '':
            bot.send_message(message.from_user.id, answer)
        else:
            bot.send_message(message.from_user.id, otherAnswer)
    else:
        bot.send_message(message.from_user.id, otherAnswer)

print('bot listening')
while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(e)
        time.sleep(15)
