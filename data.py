#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import requests
import json
from bs4 import BeautifulSoup

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

date_today = datetime.datetime.now().strftime('%Y-%m-%d')
time_today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')


def bit_course():
    cryptos = ['BTC', 'LTC', 'ETH']
    prices = []

    for crypto in cryptos:
        url = f"https://api.bittrex.com/api/v1.1/public/getticker?market=USD-{crypto}"
        j = requests.get(url)
        data = json.loads(j.text)
        price = data['result']['Ask']
        prices.append(price)

    btc_price = prices[0]
    ltc_price = prices[1]
    eth_price = prices[2]

    with open(f'data/course/_{date_today}_bit_course.json', 'w+') as file:
        data = {
            'btc': btc_price,
            'ltc': ltc_price,
            'eth': eth_price
        }
        json.dump(data, file)

def weather(city, ow_token):

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={ow_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in emoji:
            wd = emoji[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]

        with open(f'data/weather/{city}_{date_today}.json', 'w+') as file:
            d = {
                'date': date_today,
                'city': city,
                'temp': cur_weather,
                'humidity': humidity,
                'pressure': pressure,
                'wind': wind,
                'wd': wd,
            }
            json.dump(d, file)

    except Exception as ex:
        print(ex)
        print("Проверьте название города")

def course_money():
    link = 'https://www.banki.ru/products/currency/cash/moskva/'
    src = requests.get(link).text
    soup = BeautifulSoup(src, "lxml")
    table = soup.find('div', class_='currency-table').find('div',class_='table-flex table-flex--no-borders rates-summary rates-summary--renessans')
    course_by = 'ЦБ РФ'
    course_dollar = table.find_all('div', class_='table-flex__cell table-flex__cell--without-padding padding-left-default')[1].text
    course_euro = table.find_all('div', class_='table-flex__cell table-flex__cell--without-padding padding-left-default')[2].text

    with open(f'data/course/_{date_today}_course_of_Money.json', 'w+') as file:
        d = {
            'time': date_today,
            'usd': course_dollar,
            'eur': course_euro,
            'c_b': course_by
        }
        json.dump(d, file)

def news():
    link ='https://yandex.ru/'
    src = requests.get(link).text
    soup = BeautifulSoup(src, 'lxml')
    table = soup.find('div', id='news_panel_news', class_='news__panel mix-tabber-slide2__panel').find('ol')
    items = table.find_all('span', class_='news__item-content')
    notes = []
    for item in items:
        notes.append(item.text)

    with open(f'data/news/_{date_today}_News_.json', 'w+') as file:
        note1 = notes[0]
        note2 = notes[1]
        note3 = notes[2]
        note4 = notes[3]
        d = {
            'time': time_today,
            'note1': note1,
            'note2': note2,
            'note3': note3,
            'note4': note4,
        }
        json.dump(d, file)

def vogue():
    link ='https://www.vogue.ru/fashion/news'
    src = requests.get(link).text
    soup = BeautifulSoup(src, 'lxml')
    notes = soup.find('div', class_='SummaryCollectionGridItems-dxucGh jVrJeN '
                                    'hide-read-more-ad').find_all('div', class_='summary-item summary-item--has-mobi'
                                                                                'le-border summary-item--has-rule su'
                                                                                'mmary-item--gallery summary-item--n'
                                                                                'o-icon summary-item--text-align-le'
                                                                                'ft summary-item--layout-placement-t'
                                                                                'ext-below-desktop-only summary-item-'
                                                                                '-layout-position-image-left summary-'
                                                                                'item--layout-proportions-33-66 summar'
                                                                                'y-item--side-by-side-align-top summar'
                                                                                'y-item--standard SummaryCollectionGri'
                                                                                'dSummaryItem-immaEG hXYvtS')

    headers = []
    hrefs = []
    for note in notes:
        header = note.find('a', class_='summary-item-tracking__hed-link summary-item__hed-link').find('h2').text
        href = note.find('a', class_='summary-item-tracking__hed-link summary-item__hed-link').get('href')
        formatted_href = 'https://www.vogue.ru/' + href
        headers.append(header)
        hrefs.append(formatted_href)


    with open(f'data/news/_{date_today}_Vogue_.json', 'w+') as file:
        header1 = headers[0]
        href1 = hrefs[0]
        header2 = headers[1]
        href2 = hrefs[1]
        header3 = headers[2]
        href3 = hrefs[2]

        d = {
            'time': date_today,
            'header1': header1,
            'href1': href1,
            'header2': header2,
            'href2': href2,
            'header3': header3,
            'href3': href3,
        }
        json.dump(d, file)


vogue()