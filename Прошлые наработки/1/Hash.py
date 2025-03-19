
#                           Данный файл нужен для ввода хэша пароля в бд   (создание пользователя вручную)

import hashlib
import pyodbc

# Хешируем пароль
password = "1010"
password_hash = hashlib.sha256(password.encode()).hexdigest()

# Подключаемся к базе данных
server = 'localhost'  # Или '127.0.0.1'
database = 'Lev'  # Укажите имя вашей базы данных
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

# Запись пользователя в базу данных
username = "Lev"
try:
    cursor.execute("INSERT INTO Users (Username, PasswordHash) VALUES (?, ?)", (username, password_hash))
    conn.commit()
    print("Пользователь успешно добавлен!")
except Exception as e:
    print(f"Ошибка при добавлении пользователя: {e}")
finally:
    cursor.close()
    conn.close()