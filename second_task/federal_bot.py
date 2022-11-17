import telebot
import time
import requests
from bs4 import BeautifulSoup
from deeppavlov import build_model, train_model
from deeppavlov.core.common.file import read_json

cqa_model_config = read_json('../squad_ru_bert_infer.json')
cqa_model = build_model(cqa_model_config, download=True)

intent_catcher_model_config = read_json('../intent_catcher.json')
# intent_catcher_model = build_model(intent_catcher_model_config)
# intent_catcher_model = train_model(intent_catcher_model_config, download=True)

bot = telebot.TeleBot('5724405385:AAEiLzNDaJYzRkFC03Pszlfsv7gewWhYLh4')
min_limit = 500
context = ''


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


def get_first_message(message):
    bot.reply_to(message, "Введите ссылку")
    bot.register_next_step_handler(message, get_url_message)


def get_url_message(message):
    global context
    print("Ссылка:", message.text)
    context = html_to_text(message.text)
    bot.reply_to(message, 'Задавайте вопросы')


def get_answer_message(message):
    answer = cqa_model([context], [message.text])
    print("Метрики модели cqa:", answer)
    if answer[2][0] < min_limit:
        bot.reply_to(message, "Я не могу дать достоверный ответ! Задайте вопрос по-другому!")
    else:
        bot.reply_to(message, answer)


@bot.message_handler(content_types=['text'])
def get_text_message(message):
    intent_catcher_model = build_model(intent_catcher_model_config)
    # intent_catcher_model = train_model(intent_catcher_model_config)
    intent_result = intent_catcher_model([message.text])
    print("Сообщение:", message.text)
    print("Интент:", intent_result[0])
    if intent_result[0] == 'start':
        get_first_message(message)
    elif intent_result[0] == 'cqa':
        get_answer_message(message)
    elif intent_result[0] == 'search':
        bot.reply_to(message, "Выполнен поиск статей о написании ботов")
    else:
        bot.reply_to(message, "Я не понимаю, что Вы от меня хотите:(")


print('bot listening')
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)
