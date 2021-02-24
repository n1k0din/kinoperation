import requests
import json
from time import sleep

import config
import telebot
from telebot import types
from random import choice, shuffle
import io


HEADERS = {
        'X-API-KEY': config.api_key
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
    url, film_id = get_random_img()
    d = FILMS[film_id]
    country = d['countries'][0]['country']
    year = int(d['year'])
    genre = d['genres'][0]['genre']

    f = lambda x: year - 5 <= int(x['year']) <= year + 5 and \
                        x['genres'][0]['genre'] != 'мультфильм'
    if genre == 'мультфильм':
        f = lambda x: x['genres'][0]['genre'] == genre


    filtered = filter(f, FILMS.values())
    lst = list(filtered)
    options = []
    options.append(FILMS[film_id]['nameRu'])

    added_count = 0
    while added_count < 3:
        choiced = choice(lst)['nameRu']
        if choiced not in options:       
            options.append(choiced)
            added_count += 1

    response = requests.get(url)
    photo = io.BytesIO(response.content)    
    photo.name = 'img.jpg'
    
    shuffle(options)
    msg = " или ".join(options)

    if message.chat.type == 'private':
        if message.text == 'Случайный кадр':
            bot.send_photo(message.chat.id, photo)
            bot.send_message(message.chat.id, msg)


def get_random_img():
    
    film_id = choice(list(FILMS.keys()))
    image_url = frames_by_id(film_id)
    return choice(image_url['frames'])['image'], film_id


def list_of_dicts_to_dict(lst):   
    
    return {d['filmId']: d for d in lst}   


def main():
    data = data_from_file()
    global FILMS
    films_list = data['films']
    FILMS = list_of_dicts_to_dict(films_list)
    
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
