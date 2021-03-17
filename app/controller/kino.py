import json
import requests
import io
from random import choice, shuffle

class Kino:
    def __init__(self):
        self.headers = {'X-API-KEY': ''}
        self.data = {}

    def set_api_token(self, token):
        self.headers['X-API-KEY'] = token


    @staticmethod
    def read_data_from_file(filename='res.json'):
        with open(filename, encoding='utf-8') as f:
            data = json.load(f)
        return data

    @staticmethod
    def get_photo_by_url(url):
        response = requests.get(url)
        photo = io.BytesIO(response.content)
        photo.name = 'img.jpg'

        return photo

    def filter_data(self, film_id, year_delta=5):
        """
        Возращает отфильтрованные данные по фильмам
        с годом выпуска +- year_delta от фильма filmd_id
        """
        film = self.data[film_id]
        year = int(film['year'])
        genre = film['genres'][0]['genre']

        special_genre = ('мультфильм', 'аниме')

        if genre in special_genre:
            f = lambda x: x[1]['genres'][0]['genre'] == genre
        else:
            f = lambda x: \
                year - year_delta <= int(x[1]['year']) <= year + year_delta and \
                x[1]['genres'][0]['genre'] not in special_genre

        lst = list(filter(f, self.data.items()))

        return {k: v for k, v in lst}


    def get_options_list(self, correct_id, data, n=3):
        """
        correct_id: id правильного ответа
        Возвращает n + 1 случайных названия фильма, включая правильный ответ
        """

        options = [self.data[correct_id]['filmId']]

        lst = list(data.keys())

        # собираем список n уникальных рандомных айдишников
        added_count = 0
        while added_count < n:
            random_id = choice(lst)
            if random_id not in options:
                options.append(random_id)
                added_count += 1

        # теперь получим имена фильмов
        res = [ self.data[id]['nameRu'] for id in options ]
        # и помешаем
        shuffle(res)

        return res


    def set_data(self):
        # данные приходят в виде 'films': 'куча_данных'
        # отбросим этот ключ films
        data = Kino.read_data_from_file()['films']

        # сделаем словарь {ид_фильма : вся_инфа_о_фильме}
        self.data = { d['filmId']: d for d in data }


    def frames_by_id(self, film_id):
        """
        Получает json с кадрами из фильма
        """
        url = f'https://kinopoiskapiunofficial.tech/api/v2.1/films/{film_id}/frames'
        r = requests.get(url, headers=self.headers)
        return r.json()


    def get_random_img(self, film_id):
        """
        Возвращает ссылку на рандомный кадр по id фильма
        """

        # film_id = choice(list(self.data.keys()))
        #
        image_urls = self.frames_by_id(film_id)

        return choice(image_urls['frames'])['image']

    @property
    def random_id(self):
        return choice(list(self.data.keys()))





def main():
    kino = Kino()
    kino.set_data()
    # print(kino.get_options_list(474))
    d = kino.data_filtered_by_year(474)
    print(kino.get_options_list(474, d))







if __name__ == '__main__':
    main()
