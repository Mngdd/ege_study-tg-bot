import requests
from bs4 import BeautifulSoup
import random

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 '
                  'Safari/537.36 Edge/12.246'
}  # имитация пользователя чтоб не кикнули


def parse_by_theory(num, object_type):  # измененная ф-ция parse_by_num()
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


def parse_by_task(URL, object_type, name=None):  # name для дебага
    # print(f'URL --> {URL}\n{name}\n')
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find_all('div', class_='prob_maindiv')
    comps = [{
        'link': f'https://{object_type}-ege.sdamgia.ru' + item.find('a').get('href')
    }
        for item in items]
    # for comp in range(len(comps)):
    #     print(comps[comp]['link'])
    print('PARSE BY SUBTASK SUCCESS!\n')
    return comps


def parse_by_num(num, object_type):
    URL = f"https://{object_type}-ege.sdamgia.ru/prob_catalog"
    response, ege_task_list = requests.get(URL, headers=HEADERS), []
    soup = BeautifulSoup(response.content, 'html.parser')

    # старое

    # items = soup.find_all('div', class_='cat_children')
    # items_nums = soup.find_all('b', class_='cat_name')  # крч можно было бы и проще типа запихачить cat name в
    # # айтем и там искать номер и ссылку + текст задачи но зачем лол
    #
    # for item in items:
    #     tmp = {
    #         'link': [x.get('href') for x in item.find_all('a')],
    #         'txt': [x.text for x in item.find_all('a')],
    #         'num': item
    #     }
    #     ege_task_list.append(tmp)
    #     print(item, '\n\n')
    #
    # for i in range(len(ege_task_list)):  # так то цикл особо смысла не несет, кроме того что все доп задачи помечает как None
    #     tmp = items_nums[i].find('span', class_="pcat_num")
    #     if tmp is not None:
    #         ege_task_list[int(tmp.text) - 1]['task_num'] = tmp.text
    #     else:
    #         ege_task_list[i]['task_num'] = tmp
    # print('\n' * 10)
    # for i in soup.find_all('a', class_='cat_name'):
    #     if i.find('span') and int(i.find('span').text) - 1 not in ege_task_list:
    #         ege_task_list[int(i.find('span').text) - 1]['task_num'] = i.find('span').text
    #         ege_task_list[int(i.find('span').text) - 1]['txt'] = [i.find('span').next_sibling[2:]]
    #         ege_task_list[int(i.find('span').text) - 1]['link'] = [i.get('href')]

    for task in soup.find_all('div', class_="cat_category"):  # проходимса по всем задачм
        real_task = task.find('span', class_='pcat_num')  # проверка что задача имеет номер т.е из егэ
        if real_task:
            subtasks = {
                'link': [x.get('href') for x in task.find_all('a')],
                'txt': [x.text if not x.text[0].isdigit() else x.text[x.text.index(' ') + 1:]
                        for x in task.find_all('a')],
                'num': real_task.text,
                'task_type': real_task.next_sibling[2:]
            }
            # чистка мусора \/
            subtasks['txt'], tmp = [el for el in subtasks['txt'] if el != 'Перейти'], []
            for el in subtasks['link']:
                if el not in tmp:
                    tmp.append(el)
            subtasks['link'] = tmp
            ege_task_list.append(subtasks)

    # for comp in ege_task_list:  # дебаг таблица
    #     print(f"{comp['num']}) {comp['task_type']}")
    #     for i in range(len(comp['link'])):
    #         print(f"https://{object_type}-ege.sdamgia.ru{comp['link'][i]}  {comp['txt'][i]}")
    #     print()
    # print()

    try:  # на всякий случай
        ans = []
        for n in range(len(ege_task_list[num - 1]['link'])):
            ans.extend(parse_by_task(f"https://{object_type}-ege.sdamgia.ru"
                                     f"{ege_task_list[num - 1]['link'][n]}&print=true",
                                     object_type, ege_task_list[num - 1]['txt'][n]))
        print('PARSE BY SUBTASKS SUCCESS!')
        return ans
    except IndexError:
        return 'INDEX_ERROR'


def cat_get():
    response = requests.get('https://api.thecatapi.com/v1/images/search', headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    return str(soup).split(',')[2][7:-1]


def dog_get():
    response = requests.get('https://dog.ceo/api/breeds/image/random', headers=HEADERS)
    soup = str(BeautifulSoup(response.content, 'html.parser'))[12:]
    return ''.join(['/' if i == '\\' else i for i in soup[:-21]])


if __name__ == '__main__':
    parse_by_num(12, 'inf')
