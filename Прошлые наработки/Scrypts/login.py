import pyodbc
from flask import Flask, request
import html

app = Flask(__name__)

# Конфигурация подключения к базе данных
server = 'localhost'
database = 'Lev'

# Устанавливаем соединение с использованием Windows Authentication
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
conn = pyodbc.connect(conn_str)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Запрос для проверки пользователя
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()

    if row:
        # Проверка пароля
        if check_password(password, row.password):
            return f"Добро пожаловать, {html.escape(username)}!"
        else:
            return "Неверный пароль."
    else:
        return "Пользователь не найден."

def check_password(input_password, stored_password):
    return input_password == stored_password  # Замените на вашу логику проверки

if __name__ == '__main__':
    app.run(debug=True)

import atexit
atexit.register(lambda: conn.close())