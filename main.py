import telebot
import os
from datetime import date
from ege_parser import *
from markups import *
from take_a_screenshot import *
from sql_base import *

print('салам алейкум')
# cd C:\Users\Администратор\Documents\tg_bot
# ege_choose_state   0 - не выбираем ниче  1 - выбор предмета  2 - выбор номера  3 - поиск
# переменная чисто для кнопки назад нужна если че 4 - теория выбор предмета 5 - выбор номера теория
# STARTTGBOT в cmd
# bot.edit_message_text(chat_id, message_id, inline_message_id, text, parse_mode, disable_web_page_preview, reply_markup)

BOT_TOKEN = "5095740599:AAEkSiFF83WwMCo4oWlU8_ejuPG7IusGmOs"
ege_type, ege_num, ege_choose_state, ege_links = 'math', 1, 0, []
lol = [f'кста седня {date.today()}', 'ыстык пишстер', 'бигаэ по полю весело кабанчик', 'капибары.....',
       'ватружка']
idk = ['я не понимаю', 'у меня ступор', 'ай донт адерстенд', 'че', 'ага да',
       'ниче не понял сори', 'слишком сложно, пиши яснее', 'ниче не понял', 'что?',
       'я непон', 'не знаю такую команду', 'неизвестная команда', 'еще раз', '🥺', '🤯']
ege_names = {
    'math': 'математике', 'rus': 'русскому', 'inf': 'инфе'
}
ege_types_len = {
    'math': 18, 'rus': 27, 'inf': 27
}
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['GET'])
def dev1(msg):
    bot.send_message(msg.chat.id, f'инфа\n{usr_data(str(msg.from_user.id))}\n{type(msg.from_user.id)}'
                                  f'{usr_get(str(msg.from_user.id), "ege_type")}')


@bot.message_handler(commands=['SET'])
def dev2(msg, change_me=None):
    if str(msg.from_user.id) == '569255452':
        if change_me is None:
            change_me = {
                "USER_ID": 'REDACTED', "ege_type": "REDACTED",
                "ege_choose_state": 0, "ege_links": "REDACTED"
            }
        usr_update(str(msg.from_user.id), change_me)
        bot.send_message(msg.chat.id, f'обновил\n{usr_data(str(msg.from_user.id))}')
    else:
        bot.send_message(msg.chat.id, 'доступ запрещен лол')


@bot.message_handler(commands=['DEL'])
def dev3(msg):
    if msg.from_user.id == 569255452:
        usr_delete(str(msg.from_user.id))
        bot.send_message(msg.chat.id, f'снизу должно быть пусто\n{usr_data(str(msg.from_user.id))}')
    else:
        bot.send_message(msg.chat.id, 'доступ запрещен лол')


@bot.message_handler(commands=['ege_theory'])
def send_theory(msg):
    global ege_choose_state
    bot.reply_to(msg, 'Какой предмет выбирешь?', reply_markup=gen_markup_ege_type())
    ege_choose_state = 4
    # bot.send_message(msg.chat.id, parsy_by_theory(ege_num, ege_type))


@bot.message_handler(commands=['cat'])
def send_cats(msg):
    CatPhoto = cat_get()
    # bot.send_photo(msg.chat.id, cat_get())
    bot.send_message(msg.chat.id, f"рандомный кот\n{CatPhoto}")


@bot.message_handler(commands=['dog'])
def send_dogs(msg):
    DogPhoto = dog_get()
    # bot.send_photo(msg.chat.id, dog_get())
    bot.send_message(msg.chat.id, f"рандомный собака\n{DogPhoto}")


@bot.message_handler(commands=['ege_task'])
def call_ege_task(msg):
    global ege_choose_state
    bot.reply_to(msg, 'Какой предмет выбирешь?', reply_markup=gen_markup_ege_type())
    ege_choose_state = 1


@bot.message_handler(commands=['start'])
def send_welcome(msg):
    bot.send_message(msg.chat.id, '🥳')
    bot.reply_to(msg, f'дарова карова\nID {msg.from_user.id}')
    usr_enlist(str(msg.from_user.id))


@bot.message_handler(commands=['info'])
def send_help(msg):
    bot.reply_to(msg, f"разраб - https://instagram.com/therock\n рандом задача по егэ - /ege_task\n"
                      f"ьжььжжььь - /random\nтестить приколы ржаки - тест\nкошка или собака - /cat /dog\n"
                      f"теория по задаче - /ege_theory (в разработке)")
    # bot.send_message(msg.chat.id, f"||spoiler||", parse_mode='MarkdownV2')


def rand_ege_question(msg, ege_link, curr_num, all_nums):
    global ege_choose_state
    # ege_num = random.choice([i + 1 for i in range(17)])
    bot.send_message(msg.chat.id, '🧐')
    search1 = bot.send_message(msg.chat.id,
                               f'ищем рандомную {ege_num}ую задачу по '
                               f'{ege_names[usr_get(str(msg.from_user.id), "ege_type")]} '
                               f'пджи\nэто {curr_num} задача из {all_nums}\n'
                               f'может какое-то время!')
    print('I\'m tryin to parse....')
    # ege_link = parse_by_num(ege_num, ege_type)
    ege_choose_state = 7  # хз просто блочить ввод, мб прокатит
    if ege_link == 'INDEX_ERR':
        print('ошибк:', 'PARSE FAILURE')
        bot.reply_to(msg, f'ошибка поиска, я сломался лол')
    else:
        photo_name = get_website_screenshot(ege_link)
        bot.edit_message_text(chat_id=search1.chat.id, message_id=search1.message_id, text='Готово!')
        bot.send_photo(msg.chat.id, photo=open(photo_name, 'rb'))
        bot.send_message(msg.chat.id, f'<a href="{ege_link}"><b>РЕШЕНИЕ ЗАДАЧИ №{ege_num}</b></a>',
                         parse_mode='HTML', disable_web_page_preview=True)
        time.sleep(1)
        print('DELETING IMAGE...')
        time.sleep(1)
        os.remove('task_ege_math.png')
    bot.send_sticker(msg.chat.id, "https://i.ibb.co/y5cY6L4/SHKA.webp")
    ege_choose_state = 0


@bot.message_handler(regexp="бб")
def echo_message2(msg):
    bot.send_message(msg.chat.id, 'бб')
    exit('EMERGENCY EXIT')


@bot.message_handler(commands=['random'])
def random_absolute(msg):
    bot.send_message(msg.chat.id, 'я не знаю че это')
    stks = ['https://i.ibb.co/ww4HmYK/shka-bored.webp', 'https://i.ibb.co/98gGPKB/tire1-Fe-ZUo-I.webp']
    bot.send_sticker(msg.chat.id, random.choice(stks))
    time.sleep(random.randint(1, 5))
    bot.send_message(msg.chat.id, random.choice(lol))


@bot.message_handler()
def check_commands(msg):
    global ege_num, ege_type, ege_choose_state, ege_links

    # назад перемотка
    if msg.text == "🔙 закрыть это меню" or msg.text == "🔙 назад" or msg.text == '!назад':
        markup_type = clear_markups()
        if ege_choose_state - 1 <= 0:
            ege_choose_state = 0
            markup_type = clear_markups()
        elif ege_choose_state - 1 == 1 or ege_choose_state - 1 == 4:
            ege_choose_state -= 1
            markup_type = gen_markup_ege_type()
        elif ege_choose_state == 3:
            ege_choose_state -= 1
            markup_type = gen_markup_ege_18() if \
                usr_get(str(msg.from_user.id), "ege_type") == 'math' else gen_markup_ege_27()
        bot.send_message(msg.chat.id, 'лады ✅', reply_markup=markup_type)

    # номер задачи егэ
    elif msg.text.isdigit():
        if int(msg.text) <= ege_types_len[usr_get(str(msg.from_user.id), "ege_type")]:
            ege_num = int(msg.text)
            if ege_choose_state == 2:
                bot.send_message(msg.chat.id, 'Подожди немног', reply_markup=clear_markups())
                ege_links = parse_by_num(ege_num, usr_get(str(msg.from_user.id), "ege_type"))
                bot.send_message(msg.chat.id, f'Сколько задач скинуть?\nОт 1 до {len(ege_links)}\n'
                                              f'количество пиши с \'!\'\nпример: !5 - я скину 5 задач, '
                                              f'!назад - перейти к выбору номера')
                ege_choose_state = 3
            elif ege_choose_state == 5:
                bot.send_message(msg.chat.id,
                                 f'пока только ссылку на всю теорию могу дать\n'
                                 f'{parsy_by_theory(ege_num, usr_get(str(msg.from_user.id), "ege_type"))}',
                                 reply_markup=clear_markups())
                ege_choose_state = 0
            else:
                bot.send_message(msg.chat.id, f'ошибка {ege_num}', reply_markup=clear_markups())
        elif ege_choose_state == 2:
            bot.send_message(msg.chat.id, 'такого номера в егэ нет🥺')

    # все что ниже это какой прдмет мы выбрали >>> ege_type
    elif msg.text == "📗Русский":
        usr_update(str(msg.from_user.id), {'ege_type': 'rus'})
        if ege_choose_state == 1:
            bot.send_message(msg.chat.id, 'Номер задачи какой?', reply_markup=gen_markup_ege_27())
            ege_choose_state = 2
        elif ege_choose_state == 4:
            bot.send_message(msg.chat.id, 'какое задание?\nв разработке', reply_markup=gen_markup_ege_27())
            ege_choose_state = 5

    elif msg.text == "📙Математика":
        usr_update(str(msg.from_user.id), {'ege_type': 'math'})
        if ege_choose_state == 1:
            bot.send_message(msg.chat.id, 'Номер задачи какой?', reply_markup=gen_markup_ege_18())
            ege_choose_state = 2
        elif ege_choose_state == 4:
            bot.send_message(msg.chat.id, 'какое задание?\nв разработке', reply_markup=gen_markup_ege_18())
            ege_choose_state = 5

    elif msg.text == "📘Информатика":
        usr_update(str(msg.from_user.id), {'ege_type': 'inf'})
        if ege_choose_state == 1:
            bot.send_message(msg.chat.id, 'Номер задачи какой?', reply_markup=gen_markup_ege_27())
            ege_choose_state = 2
        elif ege_choose_state == 4:
            bot.send_message(msg.chat.id, 'какое задание?\nв разработке', reply_markup=gen_markup_ege_27())
            ege_choose_state = 5
    elif msg.text[0] == '!' and msg.text[1:].isdigit() and ege_choose_state == 3:
        task_send_amount = int(msg.text[1:])
        if task_send_amount > len(ege_links):
            bot.send_message(msg.chat.id, 'Слишком большое число')
        else:
            for task_num in range(task_send_amount):
                rand_ege_question(msg, ege_links[task_num]['link'], task_num + 1, task_send_amount)
    else:
        bot.send_message(msg.chat.id, random.choice(idk))


bot.infinity_polling()
