import time
import telebot
from deeppavlov import build_model, configs
from deeppavlov.core.common.file import read_json

bot = telebot.TeleBot('5724405385:AAEiLzNDaJYzRkFC03Pszlfsv7gewWhYLh4')
f = open('context.txt', 'r', encoding="utf-8")
context = f.read()

model_config = read_json('../squad_ru_bert_infer.json')
# model = build_model(model_config, download=True)
model = build_model(model_config)

@bot.message_handler(content_types=['text'])
def get_text_message(message):
    bot.send_message(message.from_user.id, model([context], [message.text])[0][0])

print('bot listening')
while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(e)
        time.sleep(15)
