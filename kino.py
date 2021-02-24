import requests
import json
from time import sleep

import config
import telebot
from telebot import types
from random import choice
import io


HEADERS = {
        'X-API-KEY': 'a9b9e3ca-1e32-4070-8e4f-868b5d292b86'
    }

FILMS = {}

bot = telebot.TeleBot(config.token, parse_mode=None)


def get_data_from_api():    

    params = {
        'page': 1
    }

    url = 'https://kinopoiskapiunofficial.tech/api/v2.2/films/top'


    r = requests.get(url, headers=HEADERS, params=params)
    json_data = r.json()

    res_json_data = {
        'films': []
        }


    for page in range(13):
        params['page'] = page + 1
        print(f'Получаем страницу: {page}')
        r = requests.get(url, headers=HEADERS, params=params)
        json_data = r.json()
        res_json_data['films'].extend(json_data['films'])
        sleep(1)

    with open('res.json', 'w', encoding='utf-8') as f:
        json.dump(res_json_data, f, indent=4, ensure_ascii=False)


def data_from_file(filename='res.json'):
    with open(filename, encoding='utf-8') as f:
        data = json.load(f)
    return data


def frames_by_id(film_id):
    url = f'https://kinopoiskapiunofficial.tech/api/v2.1/films/{film_id}/frames'
    r = requests.get(url, headers=HEADERS)
    return r.json()

@bot.message_handler(commands=['go', 'start'])
def welcome_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton('Случайный кадр')
    markup.add(item)        
    msg = f"дарова отец"    

    bot.send_message(message.chat.id, msg, reply_markup=markup)

@bot.message_handler(content_types=["text"])
def send_message(message):
    url = get_random_img()    
    response = requests.get(url)
    photo = io.BytesIO(response.content)    
    photo.name = 'img.jpg'

    if message.chat.type == 'private':
        if message.text == 'Случайный кадр':
            bot.send_photo(message.chat.id, photo)


def get_random_img():
    film_id = int(choice(FILMS)['filmId'])
    image_url = frames_by_id(film_id)
    return choice(image_url['frames'])['image']

def main():
    data = data_from_file()
    global FILMS
    FILMS = data['films']
    print(len(FILMS))
    for film in sorted(FILMS, key=lambda x: x['ratingVoteCount'], reverse=True):
        print(film['nameRu'])
  
    
    
    try:
        bot.polling(none_stop=True)
    except ConnectionError as e:
        print('Ошибка соединения: ', e)
    except Exception as r:
        print("Непридвиденная ошибка: ", r)
    finally:
        print("Здесь всё закончилось")


if __name__ == '__main__':
    main()
