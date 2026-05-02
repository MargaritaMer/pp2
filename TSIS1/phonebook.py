from connect import get_connection
import json
import csv
from datetime import datetime
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def add_contact():
    """Добавление нового контакта"""
    conn = get_connection()
    cur = conn.cursor()
    
    print("\n--- Добавление контакта ---")
    name = input("Имя: ")
    email = input("Email: ")
    birthday = input("Дата рождения (YYYY-MM-DD): ")
    
    
    print("\nДоступные группы:")
    cur.execute("SELECT id, name FROM groups ORDER BY name")
    groups = cur.fetchall()
    for i, g in enumerate(groups, 1):
        print(f"{i}. {g[1]}")
    print("0. Новая группа")
    
    group_choice = input("Выберите номер группы или 0 для новой: ")
    group_id = None
    
    if group_choice == "0":
        new_group = input("Название новой группы: ")
        cur.execute("INSERT INTO groups(name) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING id", (new_group,))
        result = cur.fetchone()
        if result:
            group_id = result[0]
        else:
            cur.execute("SELECT id FROM groups WHERE name = %s", (new_group,))
            result = cur.fetchone()
            if result:
                group_id = result[0]
    elif group_choice.isdigit():
        idx = int(group_choice) - 1
        if 0 <= idx < len(groups):
            group_id = groups[idx][0]
        else:
            print("Неверный номер группы")
    else:
        print("Неверный ввод, группа не выбрана")
    
    try:
        cur.execute("""
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
        """, (name, email if email else None, birthday if birthday else None, group_id))
        
      
        while True:
            phone = input("Телефон (или Enter для пропуска): ")
            if not phone:
                break
            phone_type = input("Тип (home/work/mobile): ").lower()
            if phone_type not in ['home', 'work', 'mobile']:
                phone_type = 'mobile'
            
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES ((SELECT id FROM contacts WHERE name=%s), %s, %s)
            """, (name, phone, phone_type))
        
        conn.commit()
        print(f"Контакт '{name}' добавлен!")
    except Exception as e:
        print(f"Ошибка: {e}")
        conn.rollback()
    
    cur.close()
    conn.close()


def add_phone():
    """Добавление телефона к существующему контакту"""
    conn = get_connection()
    cur = conn.cursor()
    
    print("\n--- Добавление телефона ---")
    name = input("Имя контакта: ")
    
    
    cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
    if not cur.fetchone():
        print("Контакт не найден!")
        cur.close()
        conn.close()
        return
    
    phone = input("Телефон: ")
    ptype = input("Тип (home/work/mobile): ").lower()
    
    try:
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
        conn.commit()
        print("Телефон добавлен!")
    except Exception as e:
        print("Ошибка:", e)
    
    cur.close()
    conn.close()


def move_to_group():
    
    conn = get_connection()
    cur = conn.cursor()
    
    print("\n--- Перемещение в группу ---")
    name = input("Имя контакта: ")
    
    
    cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
    if not cur.fetchone():
        print("Контакт не найден!")
        cur.close()
        conn.close()
        return
    
    group = input("Группа: ")
    
    try:
        cur.execute("CALL move_to_group(%s, %s)", (name, group))
        conn.commit()
        print("Перемещено!")
    except Exception as e:
        print("Ошибка:", e)
    
    cur.close()
    conn.close()


def search_contacts():
    """Поиск контактов"""
    conn = get_connection()
    cur = conn.cursor()
    
    print("\n--- Поиск контактов ---")
    q = input("Поиск (имя/email/телефон): ")
    
    cur.execute("SELECT * FROM search_contacts(%s)", (q,))
    rows = cur.fetchall()
    
    if not rows:
        print("Ничего не найдено")
    else:
        print(f"\nНайдено {len(rows)} контактов:")
        for r in rows:
      
            if len(r) == 3:
                name, email, phone = r
                group = ""
            elif len(r) == 4:
                name, email, phone, group = r
                group = f" (группа: {group})" if group else ""
            else:
                name = r[0]
                email = r[1] if len(r) > 1 else "нет email"
                phone = r[2] if len(r) > 2 else "нет телефона"
                group = f" (группа: {r[3]})" if len(r) > 3 and r[3] else ""
            
            email_str = email if email else "нет email"
            phone_str = phone if phone else "нет телефона"
            print(f"  • {name} — {email_str}, тел: {phone_str}{group}")
    
    cur.close()
    conn.close()

def filter_by_group():
    """Фильтр по группе"""
    conn = get_connection()
    cur = conn.cursor()
    
    print("\n--- Фильтр по группе ---")
    
    # Список групп
    cur.execute("SELECT name FROM groups ORDER BY name")
    groups = cur.fetchall()
    
    if not groups:
        print("Нет созданных групп")
        cur.close()
        conn.close()
        return
    
    print("Доступные группы:")
    for i, g in enumerate(groups, 1):
        print(f"{i}. {g[0]}")
    
    choice = input("Выберите номер группы: ")
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(groups):
            group_name = groups[idx][0]
            
            # Используем существующую функцию из БД
            cur.execute("SELECT * FROM get_contacts_by_group(%s)", (group_name,))
            rows = cur.fetchall()
            
            if not rows:
                print(f"Нет контактов в группе '{group_name}'")
            else:
                print(f"\nКонтакты в группе '{group_name}':")
                for r in rows:
                    birthday = f" (ДР: {r[2]})" if r[2] else ""
                    email = r[1] if r[1] else "нет email"
                    print(f"  • {r[0]} — {email}{birthday}")
        else:
            print("Неверный номер группы")
    except ValueError:
        print("Пожалуйста, введите номер группы (цифру)")
    
    cur.close()
    conn.close()

def sort_contacts():
    """Сортировка контактов"""
    conn = get_connection()
    cur = conn.cursor()
    
    print("\n--- Сортировка контактов ---")
    print("Сортировать по:")
    print("1. Имени")
    print("2. Email")
    print("3. Дате рождения")
    
    choice = input("Выберите (1-3): ")
    
    order_map = {
        "1": "name",
        "2": "email", 
        "3": "birthday"
    }
    
    order = order_map.get(choice, "name")
    
  
    if order not in ["name", "email", "birthday"]:
        order = "name"
    
    cur.execute(f"""
        SELECT name, email, birthday
        FROM contacts
        ORDER BY {order} NULLS LAST
    """)
    
    print("\nРезультаты сортировки:")
    for r in cur.fetchall():
        birthday = f", ДР: {r[2]}" if r[2] else ""
        email = r[1] if r[1] else "нет email"
        print(f"  • {r[0]} — {email}{birthday}")
    
    cur.close()
    conn.close()


def pagination():
    """Пагинация с навигацией"""
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
            print("\n--- Больше нет данных ---")
            break
        
        print(f"\n--- Страница {offset//limit + 1} ---")
        for r in rows:
            birthday = f" (ДР: {r[2]})" if r[2] else ""
            print(f"  {r[0]} — {r[1]}{birthday}")
        
        cmd = input("\n(next / prev / quit): ").lower()
        
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
        SELECT 
            c.name, 
            c.email, 
            c.birthday,
            g.name as group_name,
            c.created_at
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.name
    """)
    
    data = []
    
    for r in cur.fetchall():
        cur.execute("""
            SELECT phone, type FROM phones 
            WHERE contact_id = (SELECT id FROM contacts WHERE name=%s)
        """, (r[0],))
        phones = [{"number": p[0], "type": p[1]} for p in cur.fetchall()]
        
        data.append({
            "name": r[0],
            "email": r[1],
            "birthday": str(r[2]) if r[2] else None,
            "group": r[3],
            "phones": phones,
            "created_at": str(r[4]) if r[4] else None
        })
    
    import os
    
    if not os.path.exists("TSIS1_export"):
        os.makedirs("TSIS1_export")
    
    filename = f"TSIS1_export/contacts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"Экспортировано в {filename} ({len(data)} контактов)")
    
    cur.close()
    conn.close()


def import_json():
    """Импорт контактов из JSON"""
    conn = get_connection()
    cur = conn.cursor()
    
    print("\n--- Импорт из JSON ---")
    
    
    import os
    json_files = [f for f in os.listdir('.') if f.endswith('.json') and f != 'contacts.json']
    
    if json_files:
        print("\nДоступные JSON файлы:")
        for i, f in enumerate(json_files, 1):
            print(f"{i}. {f}")
        print("0. Ввести имя файла вручную")
        choice = input("\nВыберите вариант: ")
        
        if choice == "0":
            filename = input("Имя JSON файла: ")
            if not filename.endswith('.json'):
                filename += '.json'
        elif choice.isdigit() and 1 <= int(choice) <= len(json_files):
            filename = json_files[int(choice)-1]
        else:
            print("Неверный выбор")
            cur.close()
            conn.close()
            return
    else:
        filename = input("Имя JSON файла (например: contacts.json): ")
        if not filename.endswith('.json'):
            filename += '.json'
    
   
    if not os.path.exists(filename):
        print(f"Файл '{filename}' не найден в текущей директории")
        print(f"Текущая директория: {os.getcwd()}")
        cur.close()
        conn.close()
        return
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print("Ошибка формата JSON")
        cur.close()
        conn.close()
        return
    
    imported = 0
    skipped = 0
    
    for c in data:
        
        cur.execute("SELECT id, name FROM contacts WHERE name=%s", (c["name"],))
        exists = cur.fetchone()
        
        if exists:
            choice = input(f"Контакт '{c['name']}' уже существует (skip/overwrite): ").lower()
            if choice == "skip":
                skipped += 1
                continue
            elif choice == "overwrite":
          
                cur.execute("""
                    UPDATE contacts
                    SET email=%s, birthday=%s
                    WHERE name=%s
                """, (c.get("email"), c.get("birthday"), c["name"]))
                
                
                if c.get("group"):
                    cur.execute("SELECT id FROM groups WHERE name=%s", (c["group"],))
                    group = cur.fetchone()
                    if group:
                        cur.execute("UPDATE contacts SET group_id=%s WHERE name=%s", (group[0], c["name"]))
                    else:
                        cur.execute("INSERT INTO groups(name) VALUES (%s) RETURNING id", (c["group"],))
                        cur.execute("UPDATE contacts SET group_id=%s WHERE name=%s", (cur.fetchone()[0], c["name"]))
                
                
                cur.execute("DELETE FROM phones WHERE contact_id=(SELECT id FROM contacts WHERE name=%s)", (c["name"],))
        else:
            
            group_id = None
            if c.get("group"):
                cur.execute("SELECT id FROM groups WHERE name=%s", (c["group"],))
                group = cur.fetchone()
                if group:
                    group_id = group[0]
                else:
                    cur.execute("INSERT INTO groups(name) VALUES (%s) RETURNING id", (c["group"],))
                    group_id = cur.fetchone()[0]
            
            cur.execute("""
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (c["name"], c.get("email"), c.get("birthday"), group_id))
            contact_id = cur.fetchone()[0]
            
            
            for phone in c.get("phones", []):
                cur.execute("""
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s)
                """, (contact_id, phone["number"], phone.get("type", "mobile")))
        
        imported += 1
    
    conn.commit()
    print(f"Импорт завершён: {imported} обработано (пропущено: {skipped})")
    
    cur.close()
    conn.close()

def import_csv():
    """Импорт из CSV с новыми полями"""
    conn = get_connection()
    cur = conn.cursor()
    
    print("\n--- Импорт из CSV ---")
    
   
    import os
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    
    if csv_files:
        print("\nДоступные CSV файлы:")
        for i, f in enumerate(csv_files, 1):
            print(f"{i}. {f}")
        print("0. Ввести имя файла вручную")
        choice = input("\nВыберите вариант: ")
        
        if choice == "0":
            filename = input("Имя CSV файла: ")
            if not filename.endswith('.csv'):
                filename += '.csv'
        elif choice.isdigit() and 1 <= int(choice) <= len(csv_files):
            filename = csv_files[int(choice)-1]
        else:
            print("Неверный выбор")
            cur.close()
            conn.close()
            return
    else:
        filename = input("Имя CSV файла (например: contacts.csv): ")
        if not filename.endswith('.csv'):
            filename += '.csv'
    
    
    if not os.path.exists(filename):
        print(f"Файл '{filename}' не найден в текущей директории")
        print(f"Текущая директория: {os.getcwd()}")
        cur.close()
        conn.close()
        return
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
           
            first_row = next(reader)
         
            if first_row[0].lower() == 'name':
                data = list(reader)
            else:
                data = [first_row] + list(reader)
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return
    
    imported = 0
    
    for row in data:
   
        if len(row) < 6:
            print(f"Пропущена строка (недостаточно полей): {row}")
            continue
        
        name, phone, phone_type, email, birthday, group = row[:6]
        
       
        if not name or name.strip() == "":
            continue
        
      
        cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
        exists = cur.fetchone()
        
        if exists:
            choice = input(f"Контакт '{name}' существует (skip/overwrite): ").lower()
            if choice == "skip":
                continue
            elif choice != "overwrite":
                continue
        
      
        group_id = None
        if group and group.strip():
            cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
            g = cur.fetchone()
            if g:
                group_id = g[0]
            else:
                cur.execute("INSERT INTO groups(name) VALUES (%s) RETURNING id", (group,))
                group_id = cur.fetchone()[0]
        
        if exists and choice == "overwrite":
            cur.execute("""
                UPDATE contacts
                SET email=%s, birthday=%s, group_id=%s
                WHERE name=%s
            """, (email if email else None, birthday if birthday else None, group_id, name))
            cur.execute("DELETE FROM phones WHERE contact_id=(SELECT id FROM contacts WHERE name=%s)", (name,))
        else:
            cur.execute("""
                INSERT INTO contacts(name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id
            """, (name, email if email else None, birthday if birthday else None, group_id))
            contact_id = cur.fetchone()[0]
        
      
        if phone and phone.strip():
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES ((SELECT id FROM contacts WHERE name=%s), %s, %s)
            """, (name, phone, phone_type if phone_type in ['home','work','mobile'] else 'mobile'))
        
        imported += 1
    
    conn.commit()
    print(f"Импортировано {imported} контактов из CSV")
    
    cur.close()
    conn.close()


def menu():
    """Главное меню"""
    while True:
        print("\n" + "="*50)
        print("PHONEBOOK — Расширенное управление контактами")
        print("="*50)
        print("1. Добавить контакт")
        print("2. Добавить телефон")
        print("3. Переместить в группу")
        print("4. Поиск контактов")
        print("5. Фильтр по группе")
        print("6. Сортировка")
        print("7. Пагинация (страницы)")
        print("8. Экспорт в JSON")
        print("9. Импорт из JSON")
        print("10. Импорт из CSV")
        print("0. Выход")
        
        c = input("\nВыберите действие: ")
        
        actions = {
            "1": add_contact,
            "2": add_phone,
            "3": move_to_group,
            "4": search_contacts,
            "5": filter_by_group,
            "6": sort_contacts,
            "7": pagination,
            "8": export_json,
            "9": import_json,
            "10": import_csv,
            "0": lambda: None
        }
        
        if c in actions:
            if c == "0":
                print("До свидания!")
                break
            actions[c]()
        else:
            print("Неверный выбор!")


if __name__ == "__main__":
    menu()