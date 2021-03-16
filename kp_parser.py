import kp_movie
import requests
from bs4 import BeautifulSoup
import re
from random import choice

def get_proxy():
    html = requests.get('https://free-proxy-list.net/').text
    soup = BeautifulSoup(html, 'lxml')

    trs = soup.find('table', id='proxylisttable').find_all('tr')[1:15]

    proxies = []

    for tr in trs:
        tds = tr.find_all('td')
        ip = tds[0].text.strip()
        port = tds[1].text.strip()
        schema = 'https' if 'yes' in tds[6].text.strip() else 'http'
        proxy = {'schema': schema, 'address': ip + ':' + port}
        proxies.append(proxy)

    print("Вот такие прокси нашлись:\n", proxies)

    return choice(proxies)

def read_file(filename='kp_example.html'):
    '''
    Читает тестовый файл в строку
    '''
    with open(filename, encoding='utf-8') as f:
        content = f.read()
        return content



def get_html(url):
    '''
    Получаем текст страницы по url
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.186 Safari/537.36'
      }
    p = get_proxy()
    address = f"{p['schema']}://{p['address']}"
    proxy = { p['schema']: address }
    print(proxy)

    r = requests.get(url, headers=headers, proxies=proxy, timeout=5)
    return r.text


def write_csv(data, filename='output.csv'):
    '''
    Дописываем в csv-файл filename словарь data
    '''
    with open(filename, 'a') as f:
        order = []
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)



def main():


    url = 'https://www.kinopoisk.ru/film/1101569/'
    html = get_html(url)
    print(html)
    #html = read_file()
    soup = BeautifulSoup(html, 'lxml')
    try:
        name = soup.find('h1', class_=re.compile('styles_title')).text
        name_en = soup.find('span', class_=re.compile('styles_originalTitle')).text
        table = soup.find('div', attrs={"data-test-id": "encyclopedic-table"})
        year = table.contents[0].contents[1].text
        country = table.contents[1].contents[1].text
        country = country.split(',')[0]
        genre = table.contents[2].contents[1].text
        genre = country.split(',')[0]
        director = table.contents[4].contents[1].text

        movie = kp_movie.KP_Movie(name_ru=name, name_en=name_en, year=year,
                            country=country, genre=genre, director=director)
    except:
        print('Ошибочка')

    with open('res.html', 'w', encoding='utf-8') as f:
        f.write(html)





if __name__ == '__main__':
    main()
