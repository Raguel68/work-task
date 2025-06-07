import psycopg2
from fastapi import FastAPI
from typing import Optional
from psycopg2 import Error


#Функции для работы с БД
def request(id_us):
    try:
        # Подключение к существующей базе данных PostgreSQL
        connection = psycopg2.connect(user='postgres', password='postgres', host="postgres", port="5432", database="postgres_db")
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # Выполнение SQL-запроса
        cursor.execute("SELECT id, subscribe FROM users WHERE id = " + id_us)
        # Получить результат
        record = cursor.fetchone()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            return record[1]
            
def adding(id_us):
    try:
        # Подключение к существующей базе данных PostgreSQL
        connection = psycopg2.connect(user='postgres', password='postgres', host="postgres", port="5432", database="postgres_db")
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # Выполнение SQL-запроса
        cursor.execute("INSERT INTO users (id, subscribe) VALUES (" + id_us + ", True)")
        connection.commit()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            
def update(id_us, flag):
    try:
        # Подключение к существующей базе данных PostgreSQL
        connection = psycopg2.connect(user='postgres', password='postgres', host="postgres", port="5432", database="postgres_db")
        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # Выполнение SQL-запроса
        cursor.execute("UPDATE users SET subscribe = " + str(flag) + " WHERE id = " + id_us)
        connection.commit()
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            
#Словарь со всеми символами чисел
cifr = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

#Функции для работы с запросами от клиентов
app = FastAPI()
@app.get("/")
#обрабатываем get запросы
def get_all(id_us: Optional[int] = None):
    #обрабатываем пустой запрос
    if (id_us == None):
        print('Уточните свой запрос')
    #обрабатываем запрос с одним id
    elif (not(',' in id_us)):
        idd = ''
        for i in range(len(id_us)):
            if (id_us[i] in cifr):
                idd += id_us[i]
        return request(idd)
    #обрабатываем запрос с множеством id
    else:
        dictt = dict()
        i = 0
        store_id = '' + id_us
        while(store_id != ''):
            idd = ''
            while((store_id[i] != ',') and (i < len(store_id))):
                if (store_id[i] in cifr):
                    idd += store_id[i]
                i += 1
            if (store_id[i] == ','):
                store_id = store_id[(i+1):]
            else:
                store_id = ''
            i = 0
            dictt[idd] = request(idd)
        return dictt

@app.post("/")
def post_all(id_us: Optional[int] = None):
    #обрабатываем пустой запрос
    if (id_us == None):
        print('Уточните свой запрос')
    #обрабатываем запрос с одним id
    elif (not(',' in id_us)):
        idd = ''
        for i in range(len(id_us)):
            if (id_us[i] in cifr):
                idd += id_us[i]
        adding(idd)
    #обрабатываем запрос с множеством id
    else:
        listt = []
        i = 0
        store_id = '' + id_us
        while(store_id != ''):
            idd = ''
            while((store_id[i] != ',') and (i < len(store_id))):
                if (store_id[i] in cifr):
                    idd += store_id[i]
                i += 1
            if (store_id[i] == ','):
                store_id = store_id[(i+1):]
            else:
                store_id = ''
            i = 0
            listt.append(idd)
        for i in listt:
            adding(i)
@app.patch("/")
def patch_id(flag: str, id_us: Optional[int] = None):
     #обрабатываем пустой запрос
    if (id_us == None):
        print('Уточните свой запрос')
    #обрабатываем запрос с одним id
    elif (not(',' in id_us)):
        idd = ''
        for i in range(len(id_us)):
            if (id_us[i] in cifr):
                idd += id_us[i]
        if ("True" in flag):
            update(idd, "True")
        else:
            update(idd, "False")
    #обрабатываем запрос с множеством id
    else:
        dictt = dict()
        i = 0
        store_id = '' + id_us
        list_flag = flag.split(',')
        ii = 0
        while(store_id != ''):
            idd = ''
            while((store_id[i] != ',') and (i < len(store_id))):
                if (store_id[i] in cifr):
                    idd += store_id[i]
                i += 1
            if (store_id[i] == ','):
                store_id