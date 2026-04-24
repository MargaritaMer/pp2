from connect import get_connection
import json


def add_contact():
    conn = get_connection()
    cur = conn.cursor()

    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")

    cur.execute("""
        INSERT INTO contacts(name, email, birthday)
        VALUES (%s, %s, %s)
    """, (name, email, birthday))

    conn.commit()

    print("Contact added!")

    cur.close()
    conn.close() 


def add_phone():
    conn = get_connection()
    cur = conn.cursor()

    name = input("Contact name: ")
    phone = input("Phone: ")
    ptype = input("Type (home/work/mobile): ")

    try:
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
        conn.commit()
        print("Phone added!")
    except Exception as e:
        print("Error:", e)

    cur.close()
    conn.close()



def move_group():
    conn = get_connection()
    cur = conn.cursor()

    name = input("Contact name: ")
    group = input("Group: ")

    try:
        cur.execute("CALL move_to_group(%s, %s)", (name, group))
        conn.commit()
        print("Moved!")
    except Exception as e:
        print("Error:", e)

    cur.close()
    conn.close()



def search():
    conn = get_connection()
    cur = conn.cursor()

    q = input("Search: ")
    cur.execute("SELECT * FROM search_contacts(%s)", (q,))

    rows = cur.fetchall()

    for r in rows:
        print(f"Name: {r[0]}, Email: {r[1]}, Phone: {r[2]}")

    cur.close()
    conn.close()



def sort_contacts():
    conn = get_connection()
    cur = conn.cursor()

    print("Sort by: name / email / birthday")
    order = input("Choose: ")

    if order not in ["name", "email", "birthday"]:
        order = "name"

    cur.execute(f"""
        SELECT name, email, birthday
        FROM contacts
        ORDER BY {order} NULLS LAST
    """)

    for r in cur.fetchall():
        print(r)

    cur.close()
    conn.close()



def pagination():
    conn = get_connection()
    cur = conn.cursor()

    limit = 3
    offset = 0

    while True:
        cur.execute("""
            SELECT name, email, birthday
            FROM contacts
            ORDER BY name
            LIMIT %s OFFSET %s
        """, (limit, offset))

        rows = cur.fetchall()

        if not rows:
            print("No more data")
            break

        print("\n--- PAGE ---")
        for r in rows:
            print(r)

        cmd = input("(next / prev / quit): ")

        if cmd == "next":
            offset += limit
        elif cmd == "prev":
            offset = max(0, offset - limit)
        elif cmd == "quit":
            break

    cur.close()
    conn.close()



def export_json():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
    """)

    data = []

    for r in cur.fetchall():
        data.append({
            "name": r[0],
            "email": r[1],
            "birthday": str(r[2]) if r[2] else None,
            "group": r[3]
        })

    with open("contacts.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("Exported to contacts.json")

    cur.close()
    conn.close()



def import_json():
    conn = get_connection()
    cur = conn.cursor()

    with open("contacts.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for c in data:
        cur.execute("SELECT id FROM contacts WHERE name=%s", (c["name"],))
        exists = cur.fetchone()

        if exists:
            choice = input(f"{c['name']} exists (skip/overwrite): ")

            if choice == "skip":
                continue

            cur.execute("""
                UPDATE contacts
                SET email=%s, birthday=%s
                WHERE name=%s
            """, (c["email"], c["birthday"], c["name"]))

        else:
            cur.execute("""
                INSERT INTO contacts(name, email, birthday)
                VALUES (%s, %s, %s)
            """, (c["name"], c["email"], c["birthday"]))

    conn.commit()
    print("Import done!")

    cur.close()
    conn.close()



def menu():
    while True:
        print("""
1. Add contact
2. Add phone
3. Move to group
4. Search
5. Sort
6. Pagination
7. Export JSON
8. Import JSON
0. Exit
""")

        c = input("Choose: ")

        if c == "1":
            add_contact()
        elif c == "2":
            add_phone()

        elif c == "3":
            move_group()
        elif c == "4":
            search()
        elif c == "5":
            sort_contacts()
        elif c == "6":
            pagination()
        elif c == "7":
            export_json()
        elif c == "8":
            import_json()
        elif c == "0":
            break


if __name__ == "__main__":
    menu()