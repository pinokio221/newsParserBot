import telebot
import time
import json
import pymysql
import requests
from urllib.request import Request, urlopen
import urllib
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error

new_posts = []
bot = telebot.TeleBot('1078037079:AAHJJTMECkQU4WWfUr5oB6S3nZnorz06mio')
connection = pymysql.connect(host='localhost', database='cybernews', user='root', password='Ogurec_22')

@bot.message_handler(commands=['update'])
def botUpdate(message):
    def publish(new_posts):
        print(new_posts)
        try:
            if len(new_posts) >=1:
                for post in new_posts:
                    bot.send_message(-1001486779923, post)
                    print(post)
                    cursor = connection.cursor()
                    addQuery = "INSERT INTO news_info (link) VALUES(%s)"
                    varTuple = (post)
                    cursor.execute(addQuery, varTuple)
                    result = cursor.fetchall()
            new_posts.clear()
            connection.commit()
        except:
            print("Something wrong when you try publish posts")

        def checkUpdatesTimer():
            time.sleep(15)
            parseNews()
        checkUpdatesTimer()

    def databaseCheck(connection, parseNews):
        data = json.loads(parseNews)
        for item in data['news']:
            cursor = connection.cursor()
            checkLink = item['link']
            query = "SELECT link FROM news_info WHERE link LIKE %s"
            cursor.execute(query, checkLink)
            post = cursor.fetchall()
            if not post:
                new_posts.append(checkLink)
            else:
                print("Nothing new")
        publish(new_posts)

    def parseNews():
        req = Request("https://thehackernews.com/", headers={'User-Agent': 'Mozilla/5.0'})
        page = urlopen(req).read()
        soup = BeautifulSoup(page, "html.parser")
        news_block = soup.findAll('div', class_='body-post clear')
        dict = {}
        dict['news'] = []
        if len(news_block) > 0:
            for url in news_block:
                if url.img:
                    link = url.a['href']
                    object_ = {
                        "link": link
                    }
                    dict['news'].append(object_)
            json_convert = json.dumps(dict)
            databaseCheck(connection, json_convert)
    parseNews()
bot.polling()


