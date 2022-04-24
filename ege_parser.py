import requests
from bs4 import BeautifulSoup
import random

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 '
                  'Safari/537.36 Edge/12.246'
}  # имитация пользователя чтоб не кикнули


def parse_by_theory(num, object_type):  # измененная ф-ция parse_by_num()
    # return 'https://ege-study.ru/ru/ege/materialy/matematika/' if object_type == 'math' else \
    #     ''.join(['https://ege-study.ru/ru/ege/materialy/russkij-yazyk/' if object_type == 'rus' else
    #              'https://ege-study.ru/ru/ege/materialy/informatika/'])

    typo = {
        'inf': 'informatika', 'rus': 'russkij-yazyk', 'math': 'matematika'
    }
    response = requests.get(f"https://ege-study.ru/ru/ege/materialy/{typo[object_type]}/", headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    if object_type == 'inf':
        all_blocks = soup.find_all('div', class_='span4')
        titles = [str(el[7:]) for lst in [[task.get('title') for task in el.find_all('a') if task.get('title')]
                                          for el in all_blocks] for el in lst]
        titles = [int(el.strip()[1:][:el[1:].index('.')]) if el != '10' else 10 for el in titles]
        links = [el for lst in [[task.get('href') for task in el.find_all('a')] for el in all_blocks] for el in lst]
        return f"https://ege-study.ru/{sorted(zip(titles, links), key=lambda x: x[0])[num - 1][1]}"
    elif object_type == 'math':
        all_blocks = soup.find_all("a", target="_blank", rel="external nofollow noopener")
        all_tasks = [(int(el.text.split()[1][:-1]), el.get('href')) for el in all_blocks if 'Задание' in el.text]
        all_tasks.append((10, "/zadanie-10-ege-po-matematike-teoriya-veroyatnostej-povyshennyj-uroven-slozhnosti"))
        all_tasks.append((9, "/ru/ege/podgotovka/matematika/zadanie-9-ege-po-matematike-grafiki-funkcij/"))
        all_tasks.sort(key=lambda x: x[0])
        return f"https://ege-study.ru/" \
               f"{all_tasks[num - 1][1]}"
    else:  # русич
        tasks = soup.find('ul', class_='tab')
        return f"https://ege-study.ru/{[el.get('href') for el in tasks.find_all('a')][num - 1]}"


def parse_by_task(URL, object_type, name=None):  # name для дебага
    # print(f'URL --> {URL}\n{name}\n')  # дебаг
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find_all('div', class_='prob_maindiv')
    link = [{
        'link': f'https://{object_type}-ege.sdamgia.ru' + item.find('a').get('href')
    }
        for item in items]
    # for comp in range(len(comps)):  # дебаг
    #     print(comps[comp]['link'])
    print('PARSE BY SUBTASK SUCCESS!\n')
    return link


def parse_by_num(num, object_type):
    URL = f"https://{object_type}-ege.sdamgia.ru/prob_catalog"
    response, ege_task_list = requests.get(URL, headers=HEADERS), []
    soup = BeautifulSoup(response.content, 'html.parser')

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
