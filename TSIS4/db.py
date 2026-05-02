import psycopg2
from psycopg2 import sql
from datetime import datetime

class Database:
    def __init__(self):
        try:
            
            self.conn_params = {
                'host': 'localhost',
                'database': 'snake_game',
                'user': 'postgres',
                'password': '1234',  
                'port': '5432',
                'client_encoding': 'UTF8'  
            }
            
            print("Подключение к PostgreSQL...")
            self.conn = psycopg2.connect(**self.conn_params)
            self.conn.autocommit = False
            print("Подключение успешно!")
            self.create_tables()
            
        except psycopg2.OperationalError as e:
            print(f"Ошибка подключения: {e}")
            print("\nПроверьте:")
            print("1. Запущен ли PostgreSQL сервер")
            print("2. Пароль правильный (временно используйте 'postgres')")
            print("3. База данных 'snake_game' существует")
            print("4. В pgAdmin проверьте подключение")
            raise
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            raise
    
    def create_tables(self):
        try:
            cursor = self.conn.cursor()
            
           
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL
                )
            """)
            
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS game_sessions (
                    id SERIAL PRIMARY KEY,
                    player_id INTEGER REFERENCES players(id),
                    score INTEGER NOT NULL,
                    level_reached INTEGER NOT NULL,
                    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            self.conn.commit()
            print("Таблицы созданы/проверены")
            cursor.close()
            
        except Exception as e:
            print(f"Ошибка при создании таблиц: {e}")
            self.conn.rollback()
            raise
    
    def get_or_create_player(self, username):
        cursor = self.conn.cursor()
        
        try:
            
            cursor.execute("SELECT id FROM players WHERE username = %s", (username,))
            result = cursor.fetchone()
            
            if result:
                player_id = result[0]
            else:
               
                cursor.execute("INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
                player_id = cursor.fetchone()[0]
                self.conn.commit()
            
            cursor.close()
            return player_id
            
        except Exception as e:
            self.conn.rollback()
            cursor.close()
            raise e
    
    def save_game_result(self, username, score, level_reached):
        try:
            player_id = self.get_or_create_player(username)
            cursor = self.conn.cursor()
            
            cursor.execute("""
                INSERT INTO game_sessions (player_id, score, level_reached)
                VALUES (%s, %s, %s)
            """, (player_id, score, level_reached))
            
            self.conn.commit()
            print(f"Результат сохранен: {username} - {score} очков")
            cursor.close()
            
        except Exception as e:
            print(f"Ошибка сохранения результата: {e}")
            self.conn.rollback()
    
    def get_top_scores(self, limit=10):
        try:
            cursor = self.conn.cursor()
            
            cursor.execute("""
                SELECT p.username, gs.score, gs.level_reached, gs.played_at
                FROM game_sessions gs
                JOIN players p ON gs.player_id = p.id
                ORDER BY gs.score DESC
                LIMIT %s
            """, (limit,))
            
            results = cursor.fetchall()
            cursor.close()
            return results
            
        except Exception as e:
            print(f"Ошибка получения топ-списка: {e}")
            return []
    
    def get_personal_best(self, username):
        try:
            player_id = self.get_or_create_player(username)
            cursor = self.conn.cursor()
            
            cursor.execute("""
                SELECT MAX(score)
                FROM game_sessions
                WHERE player_id = %s
            """, (player_id,))
            
            result = cursor.fetchone()[0]
            cursor.close()
            return result if result else 0
            
        except Exception as e:
            print(f"Ошибка получения персонального рекорда: {e}")
            return 0
    
    def close(self):
        try:
            if self.conn:
                self.conn.close()
                print("Соединение с БД закрыто")
        except:
            pass