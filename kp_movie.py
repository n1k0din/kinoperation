class KP_Person():
    def init(self, name:str, career:list):
        self.name = name
        self.career = career


class KP_Movie():
    def __init__(self, name_ru, name_en, year, country, genre, director, id=0):
        self.id = id
        self.name_ru = name_ru
        self.name_en = name_en
        self.year = year
        self.country = country
        self.genre = genre
        self.director = director

    def __str__(self):
        return f'{self.name_ru} ({self.name_en}), {self.country}, {self.year}'
