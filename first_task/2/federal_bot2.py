import telebot
import time
import requests
from bs4 import BeautifulSoup
from deeppavlov import build_model, train_model
from deeppavlov.core.common.file import read_json

bot = telebot.TeleBot('5724405385:AAEiLzNDaJYzRkFC03Pszlfsv7gewWhYLh4')
min_limit = 500
model_config = read_json('../../squad_ru_bert_infer.json')
model = build_model(model_config, download=True)
# model = train_model(model_config, download=True)


def html_to_text(url):
    html = requests.get(url=url).text
    soup = BeautifulSoup(html, features="html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ''.join(chunk for chunk in chunks if chunk)
    return text


@bot.message_handler(commands=['start'])
def get_first_message(message):
    bot.reply_to(message, "Введите ссылку")
    bot.register_next_step_handler(message, get_url_message)


def get_url_message(message):
    print(message.text)
    text = html_to_text(message.text)
    bot.reply_to(message, 'Задавайте вопросы')
    bot.register_next_step_handler(message, get_answer_message, text)


def get_answer_message(message, context):
    answer = model([context], [message.text])
    print(answer)
    if answer[2][0] < min_limit:
        bot.reply_to(message, "Я не могу дать достоверный ответ! Задайте вопрос по-другому!")
    else:
        bot.reply_to(message, answer)
    bot.register_next_step_handler(message, get_answer_message, context)


print('bot listening')
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)
