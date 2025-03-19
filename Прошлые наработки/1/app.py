from flask import Flask, render_template, request, redirect, url_for, session
import pyodbc
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Заменить на свой секретный ключ (не нужно менять)

# Настройки подключения к базе данных с использованием Windows Authentication
server = 'localhost'  # Или '127.0.0.1'
database = 'Lev'  # Укажите имя вашей базы данных
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Хешируем пароль
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # Подключаемся к базе данных
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Проверяем пользователя
        cursor.execute("SELECT * FROM Users WHERE Username=? AND PasswordHash=?", (username, password_hash))
        user = cursor.fetchone()
        
        if user:
            session['username'] = username
            return f"Добро пожаловать, {username}!"
        else:
            return "Неверное имя пользователя или пароль."
    except Exception as e:
        return f"Ошибка подключения к базе данных: {e}"

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)