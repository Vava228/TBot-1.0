#!/usr/bin/python
# -*- coding: utf-8 -*-

import telebot
from telebot import types
import data
from config import TOKEN, ow_token
import datetime
import requests
import json
from bs4 import BeautifulSoup
import csv


date_today = datetime.datetime.now().strftime('%Y-%m-%d')
time_today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

emoji = {
    "News": "📰",
    "Joke": "😆",
    "Vogue": "👗",
    "Support": "⁉",
    "Bitcoin": "₿",
    "Money": "💰",
    "Umbrella": "☂",
    "Clear": "Ясно \U00002600",
    "Clouds": "Облачно \U00002601",
    "Rain": "Дождь \U00002614",
    "Drizzle": "Дождь \U00002614",
    "Thunderstorm": "Гроза \U000026A1",
    "Snow": "Снег \U0001F328",
    "Mist": "Туман \U0001F32B"
}

bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f"Привет! Я - дружелюбный бот Вава - помощник, способный:\n"
                                    f"- посмотреть на погоду и сказать её вам;\n"
                                    f"- дать вам свежайшие курсы валют и криптобиржи;\n"
                                    f"- дать вам действительно смешной анекдот(раз в день!);\n"
                                    f"- или просто почитать новости мира или моды!\n"
                                    f"А если вас всё бесит, не с кем побеседовать или просто хочется помочь этому проекту - пиши мне: @VavaRus\n"
                                    f"И кстати, чтобы включить кнопки, набери\n ***( /button )***")

@bot.message_handler(commands=['button', 'start'])
def lalala(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(f"Дай погоду! {emoji['Umbrella']}")
    item2 = types.KeyboardButton(f"Дай курс валют {emoji['Money']}")
    item3 = types.KeyboardButton(f"--- ---? {emoji['Joke']}")
    item4 = types.KeyboardButton(f"Чего нового? {emoji['News']}, {emoji['Vogue']}")
    item5 = types.KeyboardButton(f"Дайте поддержку! {emoji['Support']}")
    markup.add(item1, item2, item3, item4, item5)

    bot.send_message(message.chat.id, 'Чего почитаем?', reply_markup=markup)

@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == f"Дай погоду! {emoji['Umbrella']}":
        markup = types.InlineKeyboardMarkup(row_width=3)
        item1 = types.InlineKeyboardButton("Москва", callback_data='moscow')
        item2 = types.InlineKeyboardButton("Подольск", callback_data='podolsk')
        item3 = types.InlineKeyboardButton("Курск", callback_data='kursk')

        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, "Выбери город:", reply_markup=markup)
    elif message.text == f"Дай курс валют {emoji['Money']}":
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton(f"Базов. валюта {emoji['Money']}", callback_data='money')
        item2 = types.InlineKeyboardButton(f"Биток {emoji['Bitcoin']}", callback_data='bitcoin')

        markup.add(item1, item2,)
        bot.send_message(message.chat.id, "Выбери курс валюты, которой тебе нужно узнать:", reply_markup=markup)
    elif message.text == f"--- ---? {emoji['Joke']}":
        pass
    elif message.text == f"Чего нового? {emoji['News']}, {emoji['Vogue']}":
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton(f"Новости {emoji['News']}", callback_data='news')
        item2 = types.InlineKeyboardButton(f"Мода {emoji['Vogue']}", callback_data='vogue')

        markup.add(item1, item2, )
        bot.send_message(message.chat.id, "Выбирай, что будем читать:", reply_markup=markup)
    elif message.text == f"Дайте поддержку! {emoji['Support']}":
        bot.send_message(message.chat.id, '💕💕💕\n'
                                          'Добрый день, {0.first_name}!\n'
                                          'Я хочу, чтобы ты рассказал обо всём моему хозяину:\n'
                                          '***\n'
                                          '@VavaRus\n'
                                          '***\n'
                                          'Он всё поймёт, ответит и поможет тебе!\n'
                                          '💕💕💕'.format(message.from_user, bot.get_me()))
    else:
        bot.send_message(message.chat.id, "Я не понимаю... 😢")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    #обработка def weather():
    if call.message:
        if call.data == 'moscow':
            city_name = 'Moscow'
            data.weather(city_name, ow_token)
            with open(f'data/weather/{city_name}_{date_today}.json', 'r') as file:
                d = json.load(file)
                humidity = d["humidity"]
                pressure = d["pressure"]
                wind = d["wind"]
                city = d["city"]
                cur_weather = d["temp"]
                wd = d['wd']
            bot.send_message(call.message.chat.id, f"***\n"
                                                   f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
               f"Погода в городе: {city}\nТемпература: {cur_weather}C°, {wd}\n"
               f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                                                   f"***\n"
               f"Хорошего дня!\n"
                                                   f"***\n")
        elif call.data == 'podolsk':
            city_name = 'Podolsk'
            data.weather(city_name, ow_token)
            with open(f'data/weather/{city_name}_{date_today}.json', 'r') as file:
                d = json.load(file)
                humidity = d["humidity"]
                pressure = d["pressure"]
                wind = d["wind"]
                city = d["city"]
                cur_weather = d["temp"]
                wd = d['wd']
            bot.send_message(call.message.chat.id, f"***\n"
                                                   f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
               f"Погода в городе: {city}\nТемпература: {cur_weather}C°, {wd}\n"
               f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                                                   f"***\n"
               f"Хорошего дня!\n"
                                                   f"***\n")
        elif call.data == 'kursk':
            city_name = 'Kursk'
            data.weather(city_name, ow_token)
            with open(f'data/weather/{city_name}_{date_today}.json', 'r') as file:
                d = json.load(file)
                humidity = d["humidity"]
                pressure = d["pressure"]
                wind = d["wind"]
                city = d["city"]
                cur_weather = d["temp"]
                wd = d['wd']
            bot.send_message(call.message.chat.id, f"***\n"
                                                   f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
               f"Погода в городе: {city}\nТемпература: {cur_weather}C°, {wd}\n"
               f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                                                   f"***\n"
               f"Хорошего дня!\n"
                                                   f"***\n")
        # обработка def course():
        elif call.data == 'money':
            data.course_money()
            with open(f'data/course/_{date_today}_course_of_Money.json', 'r') as file:
                d = json.load(file)
                time = d['time']
                eur = d['eur']
                usd = d['usd']
                c_b = d['c_b']
            bot.send_message(call.message.chat.id, f"***\n"
                                                   f"Курс доллара и евро:\n"
                                                   f"***{time}***\n"
                                                   f"(ПРЕДОСТАВЛЕНО {c_b})\n"
                                                   f"1 USD : {usd} рублей\n"
                                                   f"1 EUR : {eur} рублей\n"
                                                   f"***")
        # обработка def bit_course():
        elif call.data == 'bitcoin':
            data.bit_course()
            with open(f'data/course/_{date_today}_bit_course.json', 'r') as file:
                d = json.load(file)
                btc = d['btc']
                ltc = d['ltc']
                eth = d['eth']
            bot.send_message(call.message.chat.id, f'***\n'
                                                   f'***{date_today}***\n'
                                                   f'Курс основных криптовалют:\n'
                                                   f'BTC : {btc} USD,\n'
                                                   f'LTC : {ltc} USD,\n'
                                                   f'ETH : {eth} USD,\n'
                                                   f'***')
        # обработка def fashion_news():
        elif call.data == 'vogue':
            data.vogue()
            with open(f'data/news/_{date_today}_Vogue_.json', 'r') as file:
                d = json.load(file)
                header1 = d['header1']
                href1 = d['href1']
                header2 = d['header2']
                href2 = d['href2']
                header3 = d['header3']
                href3 = d['href3']

            bot.send_message(call.message.chat.id, f'***\n'
                                                   f'Новости моды:\n'
                                                   f'- {header1};\n'
                                                   f'Читать подробнее на:\n'
                                                   f'{href1};\n'
                                                   f'- {header2};\n'
                                                   f'Читать подробнее на:\n'
                                                   f'{href2};\n'
                                                   f'- {header3};\n'
                                                   f'Читать подробнее на:\n'
                                                   f'{href3}\n'
                                                   f'***')

        # обработка def news():
        elif call.data == 'news':
            data.news()
            with open(f'data/news/_{date_today}_News_.json', 'r') as file:
                d = json.load(file)
                note1 = d['note1']
                note2 = d['note2']
                note3 = d['note3']
                note4 = d['note4']
            bot.send_message(call.message.chat.id, f'***\n'
                                                   f'Новости на сегодня: \n'
                                                   f'- {note1};\n'
                                                   f'- {note2};\n'
                                                   f'- {note3};\n'
                                                   f'- {note4};\n'
                                                   f'***')



bot.polling(none_stop=True)






