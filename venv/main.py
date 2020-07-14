import telebot
import config
import json
import requests
import random
import re

bot = telebot.TeleBot(config.TOKEN)
@bot.message_handler(commands=['start'])
def start_message(message):
    pic = 'https://memepedia.ru/wp-content/uploads/2018/01/%D0%B2%D1%8B-%D0%BA%D1%82%D0%BE-%D1%82%D0%B0%D0%BA%D0%B8%D0%B5-%D1%8F-%D0%B2%D0%B0%D1%81-%D0%BD%D0%B5-%D0%B7%D0%B2%D0%B0%D0%BB-5.jpg'
    bot.send_photo(message.chat.id , pic)

@bot.message_handler(commands=['help'])
def help_message(ms):
    string = 'Все команды бота: \n' + \
        '/start - выводит приветствие \n'+ \
        '/help - помощь \n' + \
        '/randomCat - случайная фотография с котом \n'+ \
        '/randomDog - случайный контент с собаками \n' + \
        '/randomFox - случайная лиса \n' + \
        'Боту можно задать любой вопрос и он ответит да или нет \n' + \
        ''.__str__()
    bot.send_message(ms.chat.id, string)

@bot.message_handler(commands=['randomCat'])
def random_cat_message(ms):
    request = requests.get(config.RANDOMCAT)
    pic = request.json()['file']
    bot.send_photo(ms.chat.id, pic)

@bot.message_handler(commands=['randomDog'])
def random_dog_message(ms):
        while True:
            request = requests.get(config.RANDOMDOG)
            #print(request.json())
            data = request.json()['url'].__str__()
            if (not(data.endswith('webm')) and request.json()['fileSizeBytes'] < 5000000):
                break
        if (data.endswith('mp4') or data.endswith('gif')):

            bot.send_document(ms.chat.id, data)
        else :
            bot.send_photo(ms.chat.id, data)

@bot.message_handler(commands=['randomFox'])
def random_fox_message(ms):
    request = requests.get(config.RANDOMFOX)
    data = request.json()['image']
    bot.send_photo(ms.chat.id, data)

@bot.message_handler(regexp=r'[А-яёA-z][А-яёA-z, ]*\?')
def yes_no_message(ms):
    request = requests.get(config.YESNO)
    data = request.json()['image']
    bot.send_document(ms.chat.id, data)
    if (request.json()['answer'] == "no"):
        bot.send_message(ms.chat.id, "Нет")
    else:
        bot.send_message(ms.chat.id, "Да")

@bot.message_handler(content_types=['text'])
def conversation(message):
    bot.send_message(message.chat.id, 'Такой команды нет')

# RUN
bot.polling(none_stop=True)