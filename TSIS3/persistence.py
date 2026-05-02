import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_settings_path():
    return os.path.join(BASE_DIR, "settings.json")

def get_leaderboard_path():
    return os.path.join(BASE_DIR, "leaderboard.json")

def load_settings():
    """Загрузка настроек из файла"""
    settings_path = get_settings_path()
    
    default_settings = {
        "sound_enabled": True,  
        "music_volume": 0.5,    
        "sfx_volume": 0.7,      
        "car_color": "red",
        "difficulty": "normal"
    }
    
    if os.path.exists(settings_path):
        try:
            with open(settings_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                default_settings.update(settings)
        except:
            pass
    
    return default_settings

def save_settings(settings):
    """Сохранение настроек в файл"""
    settings_path = get_settings_path()
    
    try:
        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
        return True
    except:
        return False

def load_leaderboard():
    """Загрузка таблицы рекордов"""
    leaderboard_path = get_leaderboard_path()
    
    if os.path.exists(leaderboard_path):
        try:
            with open(leaderboard_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except:
            pass
    
    return []

def save_leaderboard(leaderboard):
    """Сохранение таблицы рекордов"""
    leaderboard_path = get_leaderboard_path()
    
    try:
        with open(leaderboard_path, 'w', encoding='utf-8') as f:
            json.dump(leaderboard, f, indent=4, ensure_ascii=False)
        return True
    except:
        return False

def add_score(leaderboard, name, score, distance):
    """Добавление нового рекорда"""
    new_entry = {
        "name": name,
        "score": score,
        "distance": distance
    }
    
    leaderboard.append(new_entry)
    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    leaderboard = leaderboard[:10]
    
    return leaderboard