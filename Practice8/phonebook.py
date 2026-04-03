import csv
from connect import connect


def insert_contact(name, phone):
    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s, %s)", (name, phone))

    conn.commit()
    cur.close()
    conn.close()


def insert_from_csv(filename):
    names = []
    phones = []

    with open(filename, encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            names.append(row[0])
            phones.append(row[1])

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL insert_many_users(%s, %s)", (names, phones))

    conn.commit()
    cur.close()
    conn.close()


def query_contacts(value):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_contacts(%s)", (value,))

    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()


def get_paginated():
    conn = connect()
    cur = conn.cursor()

    limit = int(input("Limit: "))
    offset = int(input("Offset: "))

    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))

    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()


def delete_contact(value):
    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL delete_contact_proc(%s)", (value,))

    conn.commit()
    cur.close()
    conn.close()


def menu():
    while True:
        print("\n1. Add contact")
        print("2. Import from CSV")
        print("3. Search")
        print("4. Pagination")
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
            get_paginated()

        elif choice == "5":
            value = input("Delete: ")
            delete_contact(value)

        elif choice == "6":
            break


if __name__ == "__main__":
    menu()