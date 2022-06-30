# -*- coding: utf8 -*-

#______________________________________________________________________________________________

#   _____  ____  _            __   _____  ____  _      _____ _______ ______ ____             _____  _____  _      _____ _____       _______ _____ ____  _   _  _____ 
#  / ____|/ __ \| |          / /  / ____|/ __ \| |    |_   _|__   __|  ____|___ \      /\   |  __ \|  __ \| |    |_   _/ ____|   /\|__   __|_   _/ __ \| \ | |/ ____|
# | (___ | |  | | |         / /  | (___ | |  | | |      | |    | |  | |__    __) |    /  \  | |__) | |__) | |      | || |       /  \  | |    | || |  | |  \| | (___  
#  \___ \| |  | | |        / /    \___ \| |  | | |      | |    | |  |  __|  |__ <    / /\ \ |  ___/|  ___/| |      | || |      / /\ \ | |    | || |  | | . ` |\___ \ 
#  ____) | |__| | |____   / /     ____) | |__| | |____ _| |_   | |  | |____ ___) |  / ____ \| |    | |    | |____ _| || |____ / ____ \| |   _| || |__| | |\  |____) |
# |_____/ \___\_\______| /_/     |_____/ \___\_\______|_____|  |_|  |______|____/  /_/    \_\_|    |_|    |______|_____\_____/_/    \_\_|  |_____\____/|_| \_|_____/ 
                                                                                                                                                                    
                                                                                                                                                                    
#______________________________________________________________________________________________

import sqlite3
import pandas as pd
from aiogram import types
import pickle
import os

#______________________________________________________________________________________________

def sql_check_base(message_id):
    con = sqlite3.connect("telegram.db")
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS USERS (chat_id text,rating int,user_name text, chat_group text, vk_id text)''')
    
    df = pd.read_sql("SELECT * from USERS", con)
    con.close()
    ids = df['chat_id'].tolist()
    for i in ids:
        if int(message_id) == int(i):
            return True
    else:
        return False
#______________________________________________________________________________________________
def add_vk_id(vkid,message_id):
    con = sqlite3.connect("telegram.db")
    con.execute("""UPDATE USERS SET vk_id =? WHERE chat_id =?""", (vkid, message_id))
    con.commit()
    con.close()
    return True

def add_vk_id_vk(vkid):
    con = sqlite3.connect("telegram.db")
    con.execute("""UPDATE USERS SET vk_id =? WHERE vk_id =?""", (None, vkid))
    con.commit()
    con.close()
    return True

def add_vk_id_to_tg_id(vkid):
    con = sqlite3.connect("telegram.db")
    cur = con.cursor()
    df = "SELECT chat_id from USERS WHERE vk_id=?"
    cun = cur.execute(df, [(vkid)])
    name = list(cun.fetchone())[0]
    print(name)
    return name
#______________________________________________________________________________________________
def sql_check_base_name(user_name):
    con = sqlite3.connect("telegram.db")
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS USERS (chat_id text,rating int,user_name text, chat_group text, vk_id text)''')
    
    df = pd.read_sql("SELECT * from USERS", con)
    con.close()
    ids = df['user_name'].tolist()
    for i in ids:
        if user_name.lower() == i.lower():
            return True
    else:
        return False

def delete_all_users_works(user_id):
    con = sqlite3.connect("sub.db",check_same_thread = False)
    cur = con.cursor()

    warn_user = """SELECT img FROM IMAGES WHERE users_id =?"""
    unique_num = cur.execute(warn_user, [(user_id)])
    warn_user = list(unique_num.fetchall())
    for i in warn_user:
        im = pickle.loads(list(i)[0])
        os.remove(im[0]) 
    unique_num = 'DELETE FROM IMAGES WHERE users_id =?'
    unique_num = cur.execute(unique_num, [(user_id)])
    con.commit()
    con.close()

def get_info_user_id(id_user):
    if str(id_user) in get_users_ids():
        con = sqlite3.connect("telegram.db")
        cur = con.cursor()
        sql = "SELECT * from USERS WHERE chat_id=?"
        df = list(cur.execute(sql, [(id_user)]).fetchall()[::-1][0])
        con.close()
        con = sqlite3.connect("sub.db",check_same_thread = False)
        cur = con.cursor()
        cur.execute('SELECT Count(*) FROM IMAGES WHERE users_id={}'.format(df[0]))
        count_works = list(cur.fetchone())
        df.append(count_works[0])
        con.close()
        print(df)
        return df
    else:
        print('net')
        return False

def get_info_user_id_vk(id_user):
    if str(id_user) in get_users_ids_vk():
        con = sqlite3.connect("telegram.db")
        cur = con.cursor()
        sql = "SELECT * from USERS WHERE vk_id=?"
        df = list(cur.execute(sql, [(id_user)]).fetchall()[::-1][0])
        con.close()
        con = sqlite3.connect("sub.db",check_same_thread = False)
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS IMAGES (name text,img text, caption text, subject text, course integer, checked boolean, users_id text, rating integer, var_1 text, var_2 text, var_3 text, var_4 text, date_day text,date_month text,date_year text,unique_num int, mode text, warning int)''')
        cur.execute('SELECT Count(*) FROM IMAGES WHERE users_id={}'.format(df[0]))
        count_works = list(cur.fetchone())
        df.append(count_works[0])
        con.close()
        return df
    else:
        print('net')
        return False
#______________________________________________________________________________________________
def sql_check_base_vkid(vkids):
    con = sqlite3.connect("telegram.db")
    cur = con.cursor()
    df = pd.read_sql("SELECT * from USERS", con)
    con.close()
    ids = df['vk_id'].tolist()
    for i in ids:
        if i:
            if int(i) == vkids:
                return True
    else:
        return False
#______________________________________________________________________________________________

def all_names():
    con = sqlite3.connect("telegram.db")
    cur = con.cursor()
    df = pd.read_sql("SELECT * from USERS", con)
    con.close()
    names = df['user_name'].tolist()
    return names

def get_info_user_name(id_user):
    if id_user in all_names():
        con = sqlite3.connect("telegram.db")
        cur = con.cursor()
        sql = "SELECT * from USERS WHERE user_name=?"
        df = list(cur.execute(sql, [(id_user)]).fetchall()[::-1][0])
        con.close()

        con = sqlite3.connect("sub.db",check_same_thread = False)
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS IMAGES (name text,img text, caption text, subject text, course integer, checked boolean, users_id text, rating integer, var_1 text, var_2 text, var_3 text, var_4 text, date_day text,date_month text,date_year text,unique_num int, mode text, warning int)''')
        cur.execute('SELECT Count(*) FROM IMAGES WHERE users_id={}'.format(df[0]))
        count_works = list(cur.fetchone())
        df.append(count_works[0])
        con.close()
        return df
#______________________________________________________________________________________________
def all_users():
    con = sqlite3.connect("telegram.db")
    cur = con.cursor()
    df = pd.read_sql("SELECT * from USERS", con)
    con.close()
    names = df['user_name'].tolist()
    ids = df['chat_id'].tolist()
    status = df['rating'].tolist()
    return [names,ids,status]

def all_admins():
    con = sqlite3.connect("telegram.db")
    cur = con.cursor()
    df = pd.read_sql("SELECT * from USERS WHERE rating=3", con)
    con.close()
    names = df['user_name'].tolist()
    ids = df['chat_id'].tolist()
    return [names,ids]

def get_users_ids():
    con = sqlite3.connect("telegram.db")
    cur = con.cursor()
    df = pd.read_sql("SELECT * from USERS", con)
    con.close()
    ids = df['chat_id'].tolist()
    if ids:
        return ids
    else:
        pass

def get_users_ids_alert():
    con = sqlite3.connect("telegram.db")
    cur = con.cursor()
    df = pd.read_sql("SELECT * from USERS WHERE rating!=2", con)
    con.close()
    ids = df['chat_id'].tolist()
    if ids:
        return ids
    else:
        pass

def get_users_ids_vk():
    con = sqlite3.connect("telegram.db")
    cur = con.cursor()
    df = pd.read_sql("SELECT * from USERS", con)
    con.close()
    ids = df['vk_id'].tolist()
    if ids:
        return ids
    else:
        pass
#______________________________________________________________________________________________
def img_save(img,caption,subject,course,check,mode,varss,date_cortage,users_id, unique_num, name):
    con = sqlite3.connect("sub.db",check_same_thread = False)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS IMAGES (name text,img text, caption text, subject text, course integer, checked boolean, users_id text, rating integer, var_1 text, var_2 text, var_3 text, var_4 text, date_day text,date_month text,date_year text,unique_num int, mode text, warning int)''')
    #Загрузка файла в БД
    img= pickle.dumps(img)
    warning = 0
    if mode == 'p':
        con.execute("INSERT INTO IMAGES VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",(name,img,caption,subject,course,check,users_id,0,str(varss[0]),str(varss[1]),str(varss[2]),str(varss[3]),str(date_cortage[0]),str(date_cortage[1]),str(date_cortage[2]),int(unique_num),'p',warning,))
    elif mode == 'f':
        con.execute("INSERT INTO IMAGES VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",(name,img,caption,subject,course,check,users_id,0,str(varss[0]),str(varss[1]),str(varss[2]),str(varss[3]),str(date_cortage[0]),str(date_cortage[1]),str(date_cortage[2]),int(unique_num),'f',warning,))
    con.commit()
    con.close()
    return unique_num



def see_data():
    subjects = ['математика','физика','родной язык','астрономия','русский язык','иностранный язык','информатика','история','обж','технология','литература','география','химия']
    con = sqlite3.connect("sub.db",check_same_thread = False)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS IMAGES (name text,img text, caption text, subject text, course integer, checked boolean, users_id text, rating integer, var_1 text, var_2 text, var_3 text, var_4 text, date_day text,date_month text,date_year text,unique_num int, mode text, warning int)''')
    df = pd.read_sql_query("SELECT * from IMAGES WHERE mode ='p' AND warning != 2", con)
    con.close()

    keyboard = types.InlineKeyboardMarkup()

    if len(df["subject"].unique())  == 0:
        key_yes = types.InlineKeyboardButton(text='Загрузить работу', callback_data='upload_works');
        keyboard.add(key_yes)
        return 'К сожалению здесь ничего нет', keyboard

    else:

        for i in df["subject"].unique():
            index = subjects.index(i)
            subject_button = types.InlineKeyboardButton(text=str(i)+' ('+str(len(df[(df['subject'] ==i)]))+')', callback_data=i);
            keyboard.add(subject_button);

        return 'Выбери предмет', keyboard

def see_data_file():
    subjects = ['математика','физика','родной язык','астрономия','русский язык','иностранный язык','информатика','история','обж','технология','литература','география','химия']
    con = sqlite3.connect("sub.db",check_same_thread = False)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS IMAGES (name text,img text, caption text, subject text, course integer, checked boolean, users_id text, rating integer, var_1 text, var_2 text, var_3 text, var_4 text, date_day text,date_month text,date_year text,unique_num int, mode text, warning int)''')
    df = pd.read_sql_query("SELECT * from IMAGES WHERE mode ='f' AND warning !=2", con)
    keyboard = types.InlineKeyboardMarkup()
    con.close()
    if len(df["subject"].unique())  == 0:
        key_no= types.InlineKeyboardButton(text='Загрузить файл работы', callback_data='upload_files');
        keyboard.add(key_no)
        return 'К сожалению здесь ничего нет',keyboard
    else:
        for i in df["subject"].unique():
            index = subjects.index(i)
            subject_button = types.InlineKeyboardButton( text=str(i)+' ('+str(len(df[(df['subject'] ==i)]))+')', callback_data=i);
            keyboard.add(subject_button);
        return 'Выбери предмет',keyboard

#______________________________________________________________________________________________
def show_data(predmetos):
    con = sqlite3.connect("sub.db",check_same_thread = False)
    cur = con.cursor()

    sql_img = "SELECT img, caption, unique_num FROM IMAGES WHERE subject=? AND mode='p' AND warning !=2"
    cun_img = cur.execute(sql_img, [(predmetos)]).fetchall()[::-1]
    con.close()
    return cun_img

def give_file(num):
    con = sqlite3.connect("sub.db",check_same_thread = False)
    cur = con.cursor()

    sql_img = "SELECT img, name, caption FROM IMAGES WHERE unique_num=? AND mode='f'"
    cun_img = cur.execute(sql_img, [(num)]).fetchall()
    con.close()
    return cun_img

def show_data_file(predmetos):
    con = sqlite3.connect("sub.db",check_same_thread = False)
    cur = con.cursor()

    sql_img = "SELECT name, caption, img, unique_num FROM IMAGES WHERE subject=? AND mode='f'"
    cun_img = cur.execute(sql_img, [(predmetos)]).fetchall()[::-1]
    con.close()
    return cun_img

def show_work_delete(sub,id_user):
    con = sqlite3.connect("sub.db",check_same_thread = False)
    cur = con.cursor() 
    sql_img = "SELECT img, name, caption, unique_num FROM IMAGES WHERE subject='{}' AND users_id={} AND mode='p'".format(sub,id_user)
    cun_img = cur.execute(sql_img)
    cun_img=cun_img.fetchall()
    con.close()
    return cun_img

def last_works(n):
    con = sqlite3.connect("sub.db",check_same_thread = False)
    cur = con.cursor() 
    sql_img = "SELECT unique_num, caption FROM IMAGES"
    cun_img = cur.execute(sql_img)
    cun_img=cun_img.fetchall()
    cun_img = list(reversed(cun_img))
    if int(len(cun_img)/4)>= n:
            cun_img = cun_img[0+4*n:4+4*n]
            con.close()
            return cun_img
    else:
            return False

def show_file_delete(sub,id_user):
    con = sqlite3.connect("sub.db",check_same_thread = False)
    cur = con.cursor() 
    sql_img = "SELECT img, name, caption, unique_num FROM IMAGES WHERE subject='{}' AND users_id={} AND mode='f'".format(sub,id_user)
    cun_img = cur.execute(sql_img)
    cun_img=cun_img.fetchall()
    con.close()
    return cun_img


def show_delete_work(id_user):
    con = sqlite3.connect("sub.db",check_same_thread = False)
    ask ="SELECT * from IMAGES WHERE users_id={} AND mode='p'".format(str(id_user))
    df = pd.read_sql_query(ask, con)
    con.close()

    keyboard = types.InlineKeyboardMarkup()

    if len(df["subject"].unique())  == 0:
        key_yes = types.InlineKeyboardButton(text='Загрузить работу', callback_data='upload_works');
        keyboard.add(key_yes)
        key_cancel= types.InlineKeyboardButton(text='Отмена', callback_data='cancel');
        keyboard.add(key_cancel);
        return 'К сожалению здесь ничего нет', keyboard

    else:

        for i in df["subject"].unique():
            subject_button = types.InlineKeyboardButton(text=str(i)+' ('+str(len(df[(df['subject'] ==i)]))+')', callback_data=i+'_'+str(id_user));
            keyboard.add(subject_button);

        print(keyboard)
        return 'Выбери предмет', keyboard


def show_delete_file(id_user):
    con = sqlite3.connect("sub.db",check_same_thread = False)
    ask ="SELECT * from IMAGES WHERE users_id={} AND mode='f'".format(str(id_user))
    df = pd.read_sql_query(ask, con)
    con.close()

    keyboard = types.InlineKeyboardMarkup()

    if len(df["subject"].unique())  == 0:
        key_no= types.InlineKeyboardButton(text='Загрузить файл работы', callback_data='upload_files');
        keyboard.add(key_no)
        key_no= types.InlineKeyboardButton(text='Отмена', callback_data='cancel');
        keyboard.add(key_no)
        return 'К сожалению здесь ничего нет',keyboard
    else:

        for i in df["subject"].unique():
            subject_button = types.InlineKeyboardButton(text=str(i)+' ('+str(len(df[(df['subject'] ==i)]))+')', callback_data=i+'_'+str(id_user));
            keyboard.add(subject_button);

        return 'Выбери предмет', keyboard



def user_id_to_name(id_user):
        con = sqlite3.connect("telegram.db",check_same_thread = False)
        cur = con.cursor()
        df = "SELECT user_name, chat_group from USERS WHERE chat_id=?"
        cun = cur.execute(df, [(id_user)])
        name = cun.fetchone()
        con.close()
        return name

def user_id_to_vkid(id_user):
        con = sqlite3.connect("telegram.db",check_same_thread = False)
        cur = con.cursor()
        df = "SELECT user_name, chat_group, chat_id from USERS WHERE vk_id=?"
        cun = cur.execute(df, [(id_user)])
        name = cun.fetchone()
        con.close()
        return name

def show_work_unique(num):
    con = sqlite3.connect("sub.db",check_same_thread = False)
    sql_img = "SELECT img,caption,mode,name FROM IMAGES WHERE unique_num={}".format(num)
    df = con.execute(sql_img)
    print('_________________-')
    information = df.fetchall()
    print(information)
    print(type(information))
    df = list(information)[0]
    con.close()
    print(type(df))
    print(df)
    return df

def warn_work(num):
    con = sqlite3.connect("sub.db",check_same_thread = False)
    cur = con.cursor()
    con.execute("""UPDATE IMAGES SET warning =? WHERE unique_num =?""", (1, num))
    warn_user = con.execute("""SELECT users_id FROM IMAGES WHERE unique_num =?""", [((num))])
    warn_user = list(warn_user.fetchall())[0]
    con.commit()
    con.close()
    return warn_user
#______________________________________________________________________________________________
def ban_user(id_user,id_user_who_asked):
    con = sqlite3.connect("telegram.db",check_same_thread = False)
    cur = con.cursor()
    df = pd.read_sql("SELECT * from USERS", con)
    arr = df['chat_id'].tolist()
    if id_user in arr:
            id_user_who_asked_id = id_user_who_asked
            cun_img ="""SELECT rating FROM USERS WHERE chat_id =?"""
            cun_img = cur.execute(cun_img, [(id_user)])
            id_user_who_asked_rating = """SELECT rating FROM USERS WHERE chat_id =?"""
            id_user_who_asked_rating = con.execute(id_user_who_asked_rating,[(str(id_user_who_asked_id))])
            img_data = list(cun_img.fetchone())
            id_user_who_asked_rating = list(id_user_who_asked_rating.fetchone())

            if id_user_who_asked_rating[0] == 5 and img_data[0] == 5:
                return [False, 'Чел, не надо', None]

            elif img_data[0] == 5:
                return [False, 'У вас нет прав на эту комманду', id_user_who_asked_id]

            elif id_user_who_asked_rating[0] == 3 and img_data[0] == 3:
                return [False, 'Вы не можете банить администраторов', None]

            elif id_user_who_asked_rating[0] == 5 and img_data[0] == 3:
                sql = """UPDATE USERS SET rating =2 WHERE chat_id =?"""
                cur.execute(sql, [(id_user)])
                con.commit()
                return [True, 'Администратор '+id_user+' забанен', None]

            elif img_data[0] == 2:
                return [False, 'Данный человек уже забанен', None]

            elif id_user_who_asked_rating[0] == 5 or id_user_who_asked_rating[0] == 3 and img_data[0] !=2 and img_data[0] !=3 and img_data[0] !=5:
                sql = """UPDATE USERS SET rating =2 WHERE chat_id =?"""
                cur.execute(sql, [(id_user)])
                con.commit()
                return [True, 'Юзер '+id_user+' забанен', None]

            elif id_user_who_asked_rating[0] == 2:
                return [False, 'Вы забанены', None]
    else:
        return [False,'Нет такого id', None]
    con.close()

def ban_user_name(id_user,id_user_who_asked):
    con = sqlite3.connect("telegram.db",check_same_thread = False)
    cur = con.cursor()
    df = pd.read_sql("SELECT * from USERS", con)
    arr = df['user_name'].tolist()
    print(id_user_who_asked)
    if id_user in arr:
            id_user_who_asked_id = id_user_who_asked
            cun_img ="""SELECT rating FROM USERS WHERE user_name =?"""
            cun_img = cur.execute(cun_img, [(id_user)])
            id_user_who_asked_rating = """SELECT rating FROM USERS WHERE chat_id =?"""
            id_user_who_asked_rating = con.execute(id_user_who_asked_rating,[(id_user_who_asked_id)])

            img_data = list(cun_img.fetchone())

            id_user_who_asked_rating = list(id_user_who_asked_rating.fetchone())

            if id_user_who_asked_rating[0] == 5 and img_data[0] == 5:
                return [False, 'Чел, не надо', None]

            elif img_data[0] == 5:
                return [False, 'У вас нет прав на эту комманду', id_user_who_asked_id]

            elif id_user_who_asked_rating[0] == 3 and img_data[0] == 3:
                return [False, 'Вы не можете банить администраторов', None]

            elif id_user_who_asked_rating[0] == 5 and img_data[0] == 3:
                sql = """UPDATE USERS SET rating =2 WHERE user_name =?"""
                cur.execute(sql, [(id_user)])
                con.commit()
                return [True, 'Администратор '+id_user+' забанен', None]

            elif img_data[0] == 2:
                return [False, 'Данный человек уже забанен', None]

            elif id_user_who_asked_rating[0] == 5 or id_user_who_asked_rating[0] == 3 and img_data[0] !=2 and img_data[0] !=3 and img_data[0] !=5:
                sql = """UPDATE USERS SET rating =2 WHERE user_name =?"""
                cur.execute(sql, [(id_user)])
                con.commit()
                return [True, 'Юзер '+id_user+' забанен', None]

            elif id_user_who_asked_rating[0] == 2:
                return [False, 'Вы забанены', None]
    else:
        return [False,'Нет такого имени', None]
    con.close()

def unban_user_name(id_user,id_user_who_asked):
    con = sqlite3.connect("telegram.db",check_same_thread = False)
    cur = con.cursor()
    df = pd.read_sql("SELECT * from USERS", con)
    arr = df['user_name'].tolist()
    print(id_user_who_asked)
    if id_user in arr:
            id_user_who_asked_id = id_user_who_asked
            cun_img ="""SELECT rating FROM USERS WHERE user_name =?"""
            cun_img = cur.execute(cun_img, [(id_user)])
            id_user_who_asked_rating = """SELECT rating FROM USERS WHERE chat_id =?"""
            id_user_who_asked_rating = con.execute(id_user_who_asked_rating,[(id_user_who_asked_id)])

            img_data = list(cun_img.fetchone())

            id_user_who_asked_rating = list(id_user_who_asked_rating.fetchone())
            if id_user_who_asked_rating[0] == 5 and img_data[0] == 5:
                    return [False, 'Чел, не надо', None]

            elif img_data[0] == 5:
                return [False, 'У вас нет прав на эту комманду', id_user_who_asked_id]

            elif id_user_who_asked_rating[0] == 3 and img_data[0] == 3:
                return [False, 'Вы не можете разбанить администраторов', None]

            elif img_data[0] == 0:
                return [False, 'Данный человек еще не забанен', None]

            elif id_user_who_asked_rating[0] == 5 or id_user_who_asked_rating[0] == 3 and img_data[0] !=2 and img_data[0] !=3 and img_data[0] !=5:
                sql = """UPDATE USERS SET rating =0 WHERE user_name =?"""
                cur.execute(sql, [(id_user)])
                con.commit()
                return [True, 'Юзер '+id_user+' разбанен', None]
    else:
        return [False,'Нет такого никнейма', None]
    con.close()

def unban_user(id_user,id_user_who_asked):
    con = sqlite3.connect("telegram.db",check_same_thread = False)
    cur = con.cursor()
    df = pd.read_sql("SELECT * from USERS", con)
    arr = df['chat_id'].tolist()
    if id_user in arr:
            id_user_who_asked_id = id_user_who_asked
            cun_img ="""SELECT rating FROM USERS WHERE chat_id =?"""
            cun_img = cur.execute(cun_img, [(id_user)])
            id_user_who_asked_rating = """SELECT rating FROM USERS WHERE chat_id =?"""
            id_user_who_asked_rating = con.execute(id_user_who_asked_rating,[(str(id_user_who_asked_id))])
            img_data = list(cun_img.fetchone())
            id_user_who_asked_rating = list(id_user_who_asked_rating.fetchone())
            if id_user_who_asked_rating[0] == 5 and img_data[0] == 5:
                    return [False, 'Чел, не надо', None]

            elif img_data[0] == 5:
                return [False, 'У вас нет прав на эту комманду', id_user_who_asked_id]

            elif id_user_who_asked_rating[0] == 3 and img_data[0] == 3:
                return [False, 'Вы не можете разбанить администраторов', None]

            elif img_data[0] == 0:
                return [False, 'Данный человек еще не забанен', None]

            elif id_user_who_asked_rating[0] == 5 or id_user_who_asked_rating[0] == 3 and img_data[0] !=2 and img_data[0] !=3 and img_data[0] !=5:
                sql = """UPDATE USERS SET rating =0 WHERE chat_id =?"""
                cur.execute(sql, [(id_user)])
                con.commit()
                return [True, 'Юзер '+id_user+' разбанен', None]
    else:
        return [False,'Нет такого никнейма', None]
    con.close()
#______________________________________________________________________________________________
def check_user_rating(id_user):
    print(id_user)
    con = sqlite3.connect("telegram.db",check_same_thread = False)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS USERS (chat_id text,rating int,user_name text, chat_group text, vk_id text)''')
    cun_img = """SELECT rating FROM USERS WHERE chat_id =?"""
    cun_img = cur.execute(cun_img, [(id_user)])
    img_data = cun_img.fetchone()
    if img_data:
        img_data = list(img_data)[0]
        if img_data ==3 or img_data==5 or img_data==0:
            return True
        elif img_data==2:
            return 'ban'
    else:
        return None

def check_user_rating_vk(id_user):
    con = sqlite3.connect("telegram.db",check_same_thread = False)
    cur = con.cursor()
    cun_img = """SELECT rating FROM USERS WHERE vk_id =?"""
    cun_img = cur.execute(cun_img, [(id_user)])
    img_data = cun_img.fetchone()
    if img_data:
        img_data = list(img_data)[0]
        if img_data ==3 or img_data==5 or img_data==0:
            return True
        elif img_data==2:
            return 'ban'
    else:
        return None

def check_user_rating_admin(id_user):
    con = sqlite3.connect("telegram.db",check_same_thread = False)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS USERS (chat_id text,rating int,user_name text, chat_group text, vk_id text)''')
    cun_img = """SELECT rating FROM USERS WHERE chat_id =?"""
    cun_img = cur.execute(cun_img, [(id_user)])
    img_data = cun_img.fetchone()
    if img_data:
        img_data = list(img_data)[0]
        if img_data ==3 or img_data==5:
            return True
        else:
            return False
    else:
        return False

def check_user_rating_admin_vk(id_user):
    con = sqlite3.connect("telegram.db",check_same_thread = False)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS USERS (chat_id text,rating int,user_name text, chat_group text, vk_id text)''')
    cun_img = """SELECT rating FROM USERS WHERE vk_id =?"""
    cun_img = cur.execute(cun_img, [(id_user)])
    img_data = cun_img.fetchone()
    if img_data:
        img_data = list(img_data)[0]
        if img_data ==3 or img_data==5:
            return True
        else:
            return False
    else:
        return False
def show_work_warn():
    con = sqlite3.connect("sub.db",check_same_thread = False)
    cur = con.cursor()
    sql_img = "SELECT img,caption,unique_num,name, mode FROM IMAGES WHERE warning=?"
    cun_img = cur.execute(sql_img, [(1)])
    img_data = list(cun_img.fetchall())
    con.close()
    return img_data

def show_work_ban():
    con = sqlite3.connect("sub.db",check_same_thread = False)
    cur = con.cursor()
    sql_img = "SELECT img,caption,unique_num,name, mode FROM IMAGES WHERE warning=?"
    cun_img = cur.execute(sql_img, [(2)])
    img_data = list(cun_img.fetchall())
    con.close()
    return img_data

def delete_ban_work(num):
    con = sqlite3.connect("sub.db",check_same_thread = False)
    cur = con.cursor()
    way = 'SELECT img FROM IMAGES WHERE warning = 2 AND unique_num =?'
    unique_num = cur.execute(way, [(num)])
    img_data = list(unique_num.fetchone())
    images = pickle.loads(img_data[0])
    for i in images:
        os.remove(i) 
    #warning user about deleting
    warn_user = """SELECT users_id FROM IMAGES WHERE unique_num =?"""
    unique_num = cur.execute(warn_user, [(num)])
    warn_user = list(unique_num.fetchall())[0] 
    #Deleting from bd
    unique_num = 'DELETE FROM IMAGES WHERE unique_num =?'
    unique_num = cur.execute(unique_num, [(num)])
    con.commit()
    con.close()
    return warn_user

def delete_ban_file(num):
    con = sqlite3.connect("sub.db",check_same_thread = False)
    cur = con.cursor()
    way = 'SELECT img FROM IMAGES WHERE warning = 2 AND unique_num =?'
    unique_num = cur.execute(way, [(num)])
    img_data = list(unique_num.fetchone())
    images = pickle.loads(img_data[0])
    print(images)
    os.remove(images) 
    #warning user about deleting
    warn_user = """SELECT users_id FROM IMAGES WHERE unique_num =?"""
    unique_num = cur.execute(warn_user, [(num)])
    warn_user = list(unique_num.fetchall())[0] 
    #Deleting from bd
    unique_num = 'DELETE FROM IMAGES WHERE unique_num =?'
    unique_num = cur.execute(unique_num, [(num)])
    con.commit()
    con.close()
    return warn_user

def delete_user_work(num, id_user):
    con = sqlite3.connect("sub.db",check_same_thread = False)
    cur = con.cursor()
    cun_img = con.execute("""SELECT img FROM IMAGES WHERE users_id =? AND unique_num =?""", (id_user,num,))
    img_data = list(cun_img.fetchone())
    images = pickle.loads(img_data[0])
    print('IMAGES BLYA')
    print(images)
    for i in images:
        os.remove(i)
    sql_img = "DELETE FROM IMAGES WHERE users_id ={} AND unique_num ={}".format(id_user,num)
    print('____________________')
    print(sql_img)
    con.execute(sql_img)
    con.commit()
    con.close()

def delete_user_file(num, id_user):
    con = sqlite3.connect("sub.db",check_same_thread = False)
    cur = con.cursor()
    cun_img = con.execute("""SELECT img FROM IMAGES WHERE users_id =? AND unique_num =?""", (id_user,num))
    img_data = list(cun_img.fetchone())
    images = pickle.loads(img_data[0])
    print(images)
    os.remove(images)
    con.execute("""DELETE FROM IMAGES WHERE users_id =? AND unique_num =?""", (id_user,num))
    con.commit()
    con.close()

def delete_thms(num):
    con = sqlite3.connect("sub.db",check_same_thread = False)
    cur = con.cursor()
    
    sql_img = "SELECT img,mode FROM IMAGES WHERE unique_num=?"
    cun_img = cur.execute(sql_img, [(num)])
    img_data = list(cun_img.fetchone())
    
    print(img_data)
    images = pickle.loads(img_data[0])
    
    if img_data[1] == 'f':
         print(images)
         os.remove(images)
         ss = """DELETE FROM IMAGES WHERE unique_num =?"""
         cur.execute(ss, [(num)])
         con.commit()
    elif img_data[1] == 'p':
         for i in images:
            os.remove(i)
         ss = "DELETE FROM IMAGES WHERE unique_num =?"
         cur.execute(ss, [(num)])
         con.commit()
    con.close()

def unique_num():
        con = sqlite3.connect("sub.db",check_same_thread = False)
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS IMAGES (name text,img text, caption text, subject text, course integer, checked boolean, users_id text, rating integer, var_1 text, var_2 text, var_3 text, var_4 text, date_day text,date_month text,date_year text,unique_num int, mode text, warning int)''')
        
        df = pd.read_sql_query("SELECT * from IMAGES", con)
        aboba = df['unique_num'].tolist()
        aboba.sort()
        print(aboba)
        if aboba:
            bb = [x for x in range(min(aboba), max(aboba)+1)]
            if aboba == bb:
                return(max(aboba)+1)
            else:
                print((list(set(aboba) ^set(bb))))
                return(min(list(set(aboba) ^set(bb))))
        else:
            return(unique_num_max())
        con.close()

def unique_num_max():     
        con = sqlite3.connect("sub.db",check_same_thread = False)
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS IMAGES (name text,img text, caption text, subject text, course integer, checked boolean, users_id text, rating integer, var_1 text, var_2 text, var_3 text, var_4 text, date_day text,date_month text,date_year text,unique_num int, mode text, warning int)''')
        df = pd.read_sql("SELECT * from IMAGES", con)
        arr = max(df['unique_num'].tolist())
        con.close()
        return arr


def unique_num_ask_arr():     
        con = sqlite3.connect("sub.db",check_same_thread = False)
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS IMAGES (name text,img text, caption text, subject text, course integer, checked boolean, users_id text, rating integer, var_1 text, var_2 text, var_3 text, var_4 text, date_day text,date_month text,date_year text,unique_num int, mode text, warning int)''')
        df = pd.read_sql("SELECT * from IMAGES", con)
        arr = df['unique_num'].tolist()
        con.close()
        return arr



def unique_num_ask(num):
        con = sqlite3.connect("sub.db",check_same_thread = False)
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS IMAGES (name text,img text, caption text, subject text, course integer, checked boolean, users_id text, rating integer, var_1 text, var_2 text, var_3 text, var_4 text, date_day text,date_month text,date_year text,unique_num int, mode text, warning int)''')
        unique_num = 'SELECT img FROM IMAGES WHERE unique_num=?'
        unique_num = cur.execute(unique_num, [(num)])
        unique_num = list(unique_num.fetchall())
        con.close()
        return unique_num

def sql_write_base_user(chat_id,user_name, group):
    con = sqlite3.connect("telegram.db", check_same_thread = False)
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS USERS (chat_id text,user_name text, chat_group text, rating int)''')
    rating = int(0)
    if chat_id == 1066122447:
        rating = int(5)
    con.execute("INSERT INTO Users VALUES(?,?,?,?,?);",(chat_id, rating,user_name, group,None))
    con.commit()
    con.close()

def sql_delete_base_user(chat_id):
    con = sqlite3.connect("telegram.db", check_same_thread = False)
    cur = con.cursor()
    con.execute("""DELETE FROM Users WHERE chat_id = '{}' """.format(chat_id))
    con.commit()
    con.close()


def ban_work(num):
    num = str(num)
    con = sqlite3.connect("sub.db",check_same_thread = False)
    cur = con.cursor()
    con.execute("""UPDATE IMAGES SET warning =? WHERE unique_num =?""", (2, num))
    con.commit()
    warn_user = con.execute("""SELECT users_id FROM IMAGES WHERE unique_num =?""", [(num)])
    warn_user = list(warn_user.fetchone())[0]
    con.close()
    return warn_user

def praise_work(num):
    num = str(num)
    con = sqlite3.connect("sub.db",check_same_thread = False)
    cur = con.cursor()
    con.execute("""UPDATE IMAGES SET warning =? WHERE unique_num =?""", (0, num))
    con.commit()
    warn_user = con.execute("""SELECT users_id FROM IMAGES WHERE unique_num =?""", [(num)])
    warn_user = list(warn_user.fetchone())[0]
    con.close()
    return warn_user

def sql_info_base_user(chat_id):
        con = sqlite3.connect("telegram.db",check_same_thread = False)
        cursor = con.cursor()
        sql = "SELECT user_name, chat_group, rating  FROM Users WHERE chat_id=?"
        cun = cursor.execute(sql, [(chat_id)])
        cun = cursor.fetchall()
        return list(cun[0])

def sql_rename_base_user(name, chat_id):
        con = sqlite3.connect("telegram.db",check_same_thread = False)
        sql = "SELECT rating  FROM Users WHERE chat_id=?"
        cursor = con.cursor()
        cun = cursor.execute(sql, [(chat_id)])
        rating_new = list(cursor.fetchall())[0]
        rating_new  = rating_new[0]
        con.execute("""UPDATE Users SET user_name =?  WHERE chat_id =?""",(name, chat_id))
        con.execute("""UPDATE Users SET rating=? WHERE chat_id =?""",(rating_new, chat_id))
        con.commit()
        con.close()

def sql_rename_group_user(name, chat_id):
        con = sqlite3.connect("telegram.db",check_same_thread = False)
        sql = "SELECT rating  FROM Users WHERE chat_id=?"
        cursor = con.cursor()
        cun = cursor.execute(sql, [(chat_id)])
        rating_new = list(cursor.fetchall())[0]
        rating_new = rating_new[0]
        con.execute("""UPDATE Users SET chat_group =?  WHERE chat_id =?""",(name, chat_id))
        con.execute("""UPDATE Users SET rating=? WHERE chat_id =?""",(rating_new, chat_id))
        con.commit()
        con.close()

def add_admin(id_user,id_user_who_asked):
    con = sqlite3.connect("telegram.db",check_same_thread = False)
    cur = con.cursor()
    df = pd.read_sql("SELECT * from USERS", con)
    arr = df['chat_id'].tolist()
    if id_user in arr:
            id_user_who_asked_id = id_user_who_asked
            cun_img ="""SELECT rating FROM USERS WHERE chat_id =?"""
            cun_img = cur.execute(cun_img, [(id_user)])
            id_user_who_asked_rating = """SELECT rating FROM USERS WHERE chat_id =?"""
            id_user_who_asked_rating = con.execute(id_user_who_asked_rating,[(str(id_user_who_asked_id))])
            img_data = list(cun_img.fetchone())
            id_user_who_asked_rating = int(list(id_user_who_asked_rating.fetchone())[0])
            if id_user_who_asked_rating == 5 and img_data[0] == 5:
                    return [False, 'Чел, не надо', None]

            elif img_data[0] == 5:
                return [False, 'У вас нет прав на эту комманду', id_user_who_asked_id]

            elif id_user_who_asked_rating == 3:
                return [False, 'Вы не добавлять администраторов', None]

            elif id_user_who_asked_rating == 5 and img_data[0] == 0:
                sql = """UPDATE USERS SET rating =3 WHERE chat_id =?"""
                cur.execute(sql, [(id_user)])
                con.commit()
                return [True, 'Администратор '+id_user+' добавлен', None]

            elif id_user_who_asked_rating == 5 and img_data[0] == 3:
                return [True, id_user+' уже админ', None]
    else:
        return [False,'Нет такого id', None]
    con.close()

def add_admin_name(id_user,id_user_who_asked):
    con = sqlite3.connect("telegram.db",check_same_thread = False)
    cur = con.cursor()
    df = pd.read_sql("SELECT * from USERS", con)
    arr = df['user_name'].tolist()
    if id_user in arr:
            print('yes')
            id_user_who_asked_id = id_user_who_asked
            cun_img ="""SELECT rating FROM USERS WHERE user_name =?"""
            cun_img = cur.execute(cun_img, [(id_user)])

            id_user_who_asked_rating = """SELECT rating FROM USERS WHERE chat_id =?"""
            id_user_who_asked_rating = con.execute(id_user_who_asked_rating,[(str(id_user_who_asked_id))])
            img_data = list(cun_img.fetchone())
            print(img_data)
            id_user_who_asked_rating = int(list(id_user_who_asked_rating.fetchone())[0])
            if id_user_who_asked_rating == 5 and img_data[0] == 5:
                    return [False, 'Чел, не надо', None]

            elif img_data[0] == 5:
                return [False, 'У вас нет прав на эту комманду', id_user_who_asked_id]

            elif id_user_who_asked_rating == 3:
                return [False, 'Вы не можете добавлять администраторов', None]

            elif id_user_who_asked_rating == 5 and img_data[0] == 0:
                sql = """UPDATE USERS SET rating =3 WHERE user_name =?"""
                cur.execute(sql, [(id_user)])
                con.commit()
                return [True, 'Администратор '+id_user+' добавлен', None]

            elif id_user_who_asked_rating == 5 and img_data[0] == 3:
                return [True,'Пользователь - '+id_user+' уже админ', None]

    else:
        return [False,'Нет такого никнейма', None]
    con.close()

def remove_admin(id_user,id_user_who_asked):
    con = sqlite3.connect("telegram.db",check_same_thread = False)
    cur = con.cursor()
    df = pd.read_sql("SELECT * from USERS", con)
    arr = df['chat_id'].tolist()
    if id_user in arr:
            id_user_who_asked_id = id_user_who_asked
            cun_img ="""SELECT rating FROM USERS WHERE chat_id =?"""
            cun_img = cur.execute(cun_img, [(id_user)])
            id_user_who_asked_rating = """SELECT rating FROM USERS WHERE chat_id =?"""
            id_user_who_asked_rating = con.execute(id_user_who_asked_rating,[(str(id_user_who_asked_id))])
            img_data = list(cun_img.fetchone())
            id_user_who_asked_rating = int(list(id_user_who_asked_rating.fetchone())[0])
            if id_user_who_asked_rating == 5 and img_data[0] == 5:
                    return [False, 'Чел, не надо', None]

            elif img_data[0] == 5:
                return [False, 'У вас нет прав на эту комманду', id_user_who_asked_id]

            elif id_user_who_asked_rating == 3:
                return [False, 'Вы не можете удалять администраторов', None]

            elif id_user_who_asked_rating == 5 and img_data[0] == 3:
                sql = """UPDATE USERS SET rating =0 WHERE chat_id =?"""
                cur.execute(sql, [(id_user)])
                con.commit()
                return [True, 'Администратор '+id_user+' удален', None]
            elif id_user_who_asked_rating == 5 or 3 and img_data[0] == 0:
                return [False, 'Пользователь не админ', None]
    else:
        return [False,'Нет такого id', None]
    con.close()

def remove_admin_name(id_user,id_user_who_asked):
    con = sqlite3.connect("telegram.db",check_same_thread = False)
    cur = con.cursor()
    df = pd.read_sql("SELECT * from USERS", con)
    arr = df['user_name'].tolist()
    if id_user in arr:
            id_user_who_asked_id = id_user_who_asked
            cun_img ="""SELECT rating FROM USERS WHERE user_name =?"""
            cun_img = cur.execute(cun_img, [(id_user)])
            id_user_who_asked_rating = """SELECT rating FROM USERS WHERE chat_id =?"""
            id_user_who_asked_rating = con.execute(id_user_who_asked_rating,[(str(id_user_who_asked_id))])
            img_data = int(list(cun_img.fetchone())[0])
            id_user_who_asked_rating = int(list(id_user_who_asked_rating.fetchone())[0])

            if id_user_who_asked_rating == 5 and img_data == 5:
                    return [False, 'Чел, не надо', None]

            elif img_data == 5:
                return [False, 'У вас нет прав на эту комманду', id_user_who_asked_id]

            elif id_user_who_asked_rating == 3:
                return [False, 'Вы не удалять администраторов', None]

            elif id_user_who_asked_rating == 5 and img_data == 3:
                sql = """UPDATE USERS SET rating =0 WHERE user_name =?"""
                cur.execute(sql, [(id_user)])
                con.commit()
                return [True, 'Администратор '+id_user+' удален', None]

            elif id_user_who_asked_rating == 5 or 3 and img_data == 0:
                return [False, 'Пользователь не админ', None]
    else:
        return [False,'Нет такого id', None]
    con.close()

def admin_buttons():
        con = sqlite3.connect("sub.db",check_same_thread = False)
        cur = con.cursor()
        cur.execute('SELECT Count(*) FROM IMAGES WHERE warning={}'.format(1))
        count_ban = list(cur.fetchone())

        cur.execute('SELECT Count(*) FROM IMAGES WHERE warning={}'.format(2))
        count_unban = list(cur.fetchone())

        con.close()
    


        keyboard = types.InlineKeyboardMarkup()
        row  = []
        row.append(types.InlineKeyboardButton(text='ban ('+str(count_ban[0])+')', callback_data='ban'))
        row.append(types.InlineKeyboardButton(text='unban ('+str(count_unban[0])+')', callback_data='unban'))
        keyboard.row(*row)
        return keyboard
        
def timetable(day_of_week):
	    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
	    print(days[day_of_week])
	    pass
#______________________________________________________________________________________________