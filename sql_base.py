import sqlite3

db = sqlite3.connect('DATABASE1.db', check_same_thread=False)
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS RECORD (
    USER_ID          STRING  NOT NULL
                             PRIMARY KEY,
    ege_type         STRING  NOT NULL
                             DEFAULT math,
    ege_choose_state INTEGER NOT NULL
                             DEFAULT (10),
    ege_links        STRING
)""")


def usr_enlist(usr_id):
    sql.execute('SELECT USER_ID FROM RECORD WHERE USER_ID == (?)', (usr_id,))
    if sql.fetchone() is None:
        sql.execute("INSERT INTO RECORD(USER_ID) VALUES(?)", (usr_id,))
        db.commit()
    else:
        print('ошибк:', f'{usr_id} уже существуэ')

        for val in sql.execute("SELECT * FROM RECORD"):
            print(val)


def usr_data(usr_id):
    sql.execute('SELECT * FROM RECORD WHERE USER_ID == (?)', (usr_id,))
    return sql.fetchone()


def usr_update(usr_id, data: dict):
    for key in list(data.keys()):
        # "USER_ID" его нельзя вообще менять но мало ли мб захочу
        # "ege_type" предмет
        # "ege_choose_state" стадия выбора
        # "ege_links" ссылки, между ними □
        if key == "USER_ID":
            print('ошибк:', 'USER_ID НЕЛЬЗЯ МЕНЯТЬ' * 10)
        elif key == "ege_type":
            sql.execute('UPDATE RECORD SET ege_type = (?) WHERE USER_ID == (?)', (data[key], usr_id))
        elif key == "ege_choose_state":
            sql.execute('UPDATE RECORD SET ege_choose_state = (?) WHERE USER_ID == (?)', (data[key], usr_id))
        elif key == "ege_links":
            sql.execute('UPDATE RECORD SET ege_links = (?) WHERE USER_ID == (?)', (data[key], usr_id))
        db.commit()


def usr_delete(usr_id):
    sql.execute('DELETE FROM RECORD WHERE USER_ID == (?)', (usr_id,))
    db.commit()


def usr_get(usr_id, data: str):
    sql.execute('SELECT * FROM RECORD WHERE USER_ID == (?)', (usr_id,))
    usr_data_lst = sql.fetchone()
    num_dict = {
        'USER_ID': 0, 'ege_type': 1, 'ege_choose_state': 2, 'ege_links': 3
    }
    return usr_data_lst[num_dict[data]]
