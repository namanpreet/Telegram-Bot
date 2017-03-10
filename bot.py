import telepot
import time
import bms
from urllib2 import *
import requests
from bs4 import BeautifulSoup

details_url = "https://in.bookmyshow.com/national-capital-region-ncr/movies/%s/%s"
zomato_api = "ff1c6ad67bb2a85b7c8fe210eeadae51"

latitude=0.0
longitude=0.0

def sendMenu(msg):
    print 'Message of menu wanted ',msg
    username=msg['from']['first_name']
    chat_id=msg['from']['id']
    command=msg['text']

    command=command.split(' ',1)[1]
    print command
    command=command.title()
    baseurl1='https://developers.zomato.com/api/v2.1/geocode?lat=%f&lon=%f' %(latitude,longitude)
    header= {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": zomato_api}
    response= requests.get(baseurl1,headers=header)
    p=response.json()
    bot.sendMessage(chat_id,"This is the link of the menu: ")
    for x in range(len(p['nearby_restaurants'])):
        print p['nearby_restaurants'][x]['restaurant']['menu_url']
        if p['nearby_restaurants'][x]['restaurant']['name'] == command:
            print p['nearby_restaurants'][x]['restaurant']['menu_url']
            bot.sendMessage(chat_id, p['nearby_restaurants'][x]['restaurant']['menu_url'])
    print baseurl1
    return

def sendnear(msg):
    print 'MESSAGE OF LOCATION ',msg
    username=msg['from']['first_name']
    chat_id=msg['from']['id']
    lat=msg['location']['latitude']
    lon=msg['location']['longitude']
    global latitude
    latitude=lat
    global longitude
    longitude=lon
    baseurl='https://developers.zomato.com/api/v2.1/geocode?lat=%f&lon=%f' %(lat,lon)
    header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": zomato_api}
    response = requests.get(baseurl, headers=header)
    print baseurl
    print str(lat)
    g = response.json()
    bot.sendMessage(chat_id,'These are the list of restaurants and cafes near your :\n')
    for x in range(len(g['nearby_restaurants'])):
        print g['nearby_restaurants'][x]['restaurant']['name']
        bot.sendMessage(chat_id,g['nearby_restaurants'][x]['restaurant']['name'])
    print g['nearby_restaurants'][0]['restaurant']['name']
    return

def scrape_movie(msg, name, code):
    content_type, chat_type, chat_id = telepot.glance(msg)

    final_url = details_url % (name, code)
    html = urlopen(final_url)
    bsObj = BeautifulSoup(html.read(), 'html.parser')

    duration = bsObj.find("span", {"itemprop" : "duration"}).get_text()
    image_url = bsObj.find("img", {"id" : "poster"})['data-src']
    image_url = "https:" + image_url

    rating = bsObj.find("ul", {"class" : "rating-stars"})['data-value']
    names = bsObj.find_all("div", {"class" : "__cast-member"})
    name_list = ""

    for name in names:
        name_list += name['content'] + "\n"

    final_msg = "Details\n\n" + "Duration : " + duration + "\n\nRating : " + rating + "\n\n" + name_list
    # print(duration + "\n" + image_url + "\n" + rating + "\n" + name_list)
    bot.sendMessage(chat_id, final_msg)

def convert_name(name):
    name = name.lower()
    new_name = ''
    for s in name:
        if s == ' ':
            new_name += '-'
        elif not s.isalpha():
            new_name += ''
        else:
            new_name += s
    return new_name

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    user_name = msg['from']['first_name']
    print(msg)

    if content_type == 'text':
        message = msg['text']

        if message == '/movie':
            bms_client = bms.BookMyShowClient('national-capital-region-ncr')
            movie_list = bms_client.get_now_showing()
            index = 1
            movie_msg = ''
            print movie_list
            for movie in movie_list:
                if movie[5] == 'Hindi' or movie[5] == 'Punjabi' or movie[5] == 'English':
                    movie_msg += str(index) + '. ' +  str(movie[0]) + ' '+ str(movie[3]) + ' ' + str(movie[5]) + '\n'
                    index = index + 1

            bot.sendMessage(chat_id, movie_msg)

        elif message.split(' ')[0] == 'movie' :
            bms_client = bms.BookMyShowClient('national-capital-region-ncr')
            movie_list = bms_client.get_now_showing()

            new_list = []
            for movie in movie_list:
                if movie[5] == 'Hindi' or movie[5] == 'Punjabi' or movie[5] == 'English':
                    new_list.append(movie)

            current_movie = new_list[int(message.split(' ')[1]) - 1]
            print(current_movie)

            url_name = convert_name(current_movie[0])
            scrape_movie(msg, url_name, current_movie[1])

        elif message.split(' ',1)[0]=='menu':
            sendMenu(msg)

        else:
            bot.sendMessage(chat_id, "invalid input")

    elif content_type == 'location':
        sendnear(msg)
    else:
        bot.sendMessage(chat_id, 'Send text only')

TOKEN = '274701019:AAGuSc0hJ6lUqhZFMW7I__bkYBSOhTK-Nus'

bot = telepot.Bot(TOKEN)
bot.setWebhook()
bot.message_loop(handle)
print('Listening....')

while 1:
    time.sleep(5)
# Telegram-Bot
# Telegram-Bot
