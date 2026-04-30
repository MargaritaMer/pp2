import json
import os

# Получаем путь к папке где находится скрипт
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_settings_path():
    """Возвращает полный путь к settings.json"""
    return os.path.join(BASE_DIR, "settings.json")

def get_leaderboard_path():
    """Возвращает полный путь к leaderboard.json"""
    return os.path.join(BASE_DIR, "leaderboard.json")

def load_settings():
    """Загрузка настроек из файла в папке с игрой"""
    settings_path = get_settings_path()
    
    default_settings = {
        "sound": True,
        "car_color": "red",
        "difficulty": "normal"
    }
    
    if os.path.exists(settings_path):
        try:
            with open(settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                # Обновляем default_settings с загруженными значениями
                default_settings.update(settings)
        except:
            pass
    
    return default_settings

def save_settings(settings):
    """Сохранение настроек в файл в папке с игрой"""
    settings_path = get_settings_path()
    
    try:
        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
        return True
    except:
        return False

def load_leaderboard():
    """Загрузка таблицы рекордов из файла в папке с игрой"""
    leaderboard_path = get_leaderboard_path()
    
    default_leaderboard = []
    
    if os.path.exists(leaderboard_path):
        try:
            with open(leaderboard_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except:
            pass
    
    return default_leaderboard

def save_leaderboard(leaderboard):
    """Сохранение таблицы рекордов в файл в папке с игрой"""
    leaderboard_path = get_leaderboard_path()
    
    try:
        with open(leaderboard_path, 'w', encoding='utf-8') as f:
            json.dump(leaderboard, f, indent=4, ensure_ascii=False)
        return True
    except:
        return False

def add_score(leaderboard, name, score, distance):
    """Добавление нового рекорда в таблицу"""
    # Создаем новую запись
    new_entry = {
        "name": name,
        "score": score,
        "distance": distance
    }
    
    # Добавляем в список
    leaderboard.append(new_entry)
    
    # Сортируем по убыванию очков
    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    
    # Оставляем только топ 10
    leaderboard = leaderboard[:10]
    
    return leaderboard