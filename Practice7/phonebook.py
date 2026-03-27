import csv
from connect import connect

def insert_contact(username,phone):#(добавление)
    conn = connect()#подключение к бд
    cur = conn.cursor()#объект для выполнения SQL
    
    cur.execute( # выполнить в бд
    "INSERT INTO phonebook (username, phone) VALUES (%s, %s) ON CONFLICT (username) DO NOTHING",
    (username, phone)
    )

    conn.commit() #сохр изменения 
    cur.close() 
    conn.close()

def insert_from_csv(filename): #берёт данные из CSV-файла и добавляет их в базу PostgreSQL
    conn = connect()
    cur = conn.cursor()

    with open(filename,encoding='utf-8') as file: # открываем файл (цшер автоматически закроет)
        reader = csv.reader(file) # читаем 
        for row in reader:# цыкл по сторкам
            cur.execute(
                "INSERT INTO phonebook (username, phone) VALUES (%s, %s) ON CONFLICT (username) DO NOTHING" ,
                (row[0],row[1])# имя _ телефон
            )
    conn.commit()
    cur.close()
    conn.close()

def query_contacts(filter_value): #поиск
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM phonebook WHERE username ILIKE %s OR phone LIKE %s",
        (f"%{filter_value}%", f"{filter_value}%")
    )
    #ILIKE поиск без учёта регистра


    rows = cur.fetchall()#все результаты
    for row in rows:
        print(row)

    cur.close()
    conn.close()

def update_contact(username, new_phone): # обновление
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE phonebook SET phone=%s WHERE username=%s",
        (new_phone, username)
    )#находим по имени, меняем телефон

    conn.commit()
    cur.close()
    conn.close()

def delete_contact(value):# удаление
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM phonebook WHERE username=%s OR phone=%s",
        (value, value) # удалить по имени или гомеру
    )

    conn.commit()
    cur.close()
    conn.close()

def menu():
    while True:  #бесконечный цикл
        print("\n1. Add contact")
        print("2. Import from CSV")
        print("3. Search")
        print("4. Update")
        print("5. Delete")
        print("6. Exit")

        choice = input("Choose: ")

        if choice == "1":
            name = input("Name: ")
            phone = input("Phone: ")
            insert_contact(name, phone)

        elif choice == "2":
            insert_from_csv("contacts.csv")

        elif choice == "3":
            value = input("Search: ")
            query_contacts(value)

        elif choice == "4":
            name = input("Name to update: ")
            phone = input("New phone: ")
            update_contact(name, phone)

        elif choice == "5":
            value = input("Delete by name or phone: ")
            delete_contact(value)

        elif choice == "6":
            break

#запустить код только при прямом запуске файла
if __name__ == "__main__":
    menu()




#Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
#venv\Scripts\Activate.ps1

# CREATE TABLE phonebook (
#     id SERIAL PRIMARY KEY,
#     username VARCHAR(100) UNIQUE NOT NULL,
#     phone VARCHAR(20) NOT NULL
# # );