import requests
from bs4 import BeautifulSoup
import random

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
}


def parsy_by_theory(num, object_type):  # измененная ф-ция parse_by_num()
    return 'https://ege-study.ru/ru/ege/materialy/matematika/' if object_type == 'math' else \
        ''.join(['https://ege-study.ru/ru/ege/materialy/russkij-yazyk/' if object_type == 'rus' else
                 'https://ege-study.ru/ru/ege/materialy/informatika/'])

    #                  \/ \/ ДОДЕЛАТЬ (я забыл че это лол) \/ \/

    # URL = f"https://ege-study.ru/ru/ege/materialy/matematika/"
    # response = requests.get(URL, headers=HEADERS)
    # soup = BeautifulSoup(response.content, 'html.parser')
    # items = soup.find_all('ul', class_='tab')
    # links = [[i.get('href') for i in item.find_all('a')] for item in items]
    # print('======================', *items[1], '======================', sep='\n')
    # return links


def parse_by_task(URL, object_type):
    print(f'URL --> {URL}')
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find_all('div', class_='prob_maindiv')
    comps = [{
        'link': f'https://{object_type}-ege.sdamgia.ru' + item.find('a').get('href')
    }
        for item in items]
    for comp in range(len(comps)):
        print(comps[comp]['link'], comp + 1)
    print('PARSE BY TASK SUCCESS!')
    return comps


def parse_by_num(num, object_type):
    URL = f"https://{object_type}-ege.sdamgia.ru/prob_catalog"
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find_all('div', class_='cat_children')
    items_nums = soup.find_all('b', class_='cat_name')  # крч можно было бы и проще типа запихачить cat name в
    # айтем и там искать номер и ссылку + текст задачи но зачем лол
    comps = []
    for item in items:
        tmp = {
            'link': item.find_all('a'),
            'txt': item.find_all('a'),
        }
        tmp['link'] = [x.get('href') for x in tmp['link']]
        tmp['txt'] = [x.text for x in tmp['txt']]
        comps.append(tmp)

    for i in range(len(comps)):  # так то цикл особо смысла не несет, кроме того что все
        tmp = items_nums[i].find('span', class_="pcat_num")  # доп задачи отмечает как None
        if tmp is not None:
            comps[i]['task_num'] = tmp.text
        else:
            comps[i]['task_num'] = tmp

    for comp in comps:  # табличку делоет
        print(comp['task_num'])
        for i in range(len(comp['link'])):
            if i % 2 == 0:
                print(f"https://{object_type}-ege.sdamgia.ru{comp['link'][i]}  {comp['txt'][i]}")
    try:
        print('PARSE BY NUM SUCCESS!')
        return parse_by_task(f"https://{object_type}-ege.sdamgia.ru"
                             f"{random.choice(comps[num - 1]['link'])}&print=true", object_type)
    except IndexError:
        return 'INDEX_ERR'


def cat_get():
    response = requests.get('https://api.thecatapi.com/v1/images/search', headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    return str(soup).split(',')[2][7:-1]


def dog_get():
    response = requests.get('https://dog.ceo/api/breeds/image/random', headers=HEADERS)
    soup = str(BeautifulSoup(response.content, 'html.parser'))[12:]
    return ''.join(['/' if i == '\\' else i for i in soup[:-21]])


parse_by_num(12, 'inf')
