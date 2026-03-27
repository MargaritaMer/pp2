import psycopg2 
from config import load_config

def connect(): #функ для подключения к бд
    config = load_config() # вызываем фунr, получаем словарь с настройками
    conn=psycopg2.connect(**config) # соединение с БД =  распаковка словаря
    return conn 
