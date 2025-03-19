from flask import Flask, render_template, request, redirect, url_for, session, flash
import pyodbc
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Замените на свой секретный ключ

# Настройки подключения к базе данных
server = 'localhost'  # Или '127.0.0.1'
database = 'Lev'  # Имя базы данных
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

@app.route('/')
def home():
    return render_template('index.html')

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
            return redirect(url_for('dashboard'))  # Перенаправляем на страницу после входа
        else:
            flash('Неверное имя пользователя или пароль.')
            return redirect(url_for('home'))
    except Exception as e:
        flash(f"Ошибка подключения к базе данных: {e}")
        return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    # Хешируем пароль
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Проверяем, существует ли пользователь
        cursor.execute("SELECT * FROM Users WHERE Username=?", (username,))
        if cursor.fetchone():
            flash('Пользователь с таким именем уже существует.')
            return redirect(url_for('home'))

        # Добавляем нового пользователя
        cursor.execute("INSERT INTO Users (Username, PasswordHash, Email) VALUES (?, ?, ?)", (username, password_hash, email))
        conn.commit()
        flash('Регистрация прошла успешно! Теперь вы можете войти.')
        return redirect(url_for('home'))
    except Exception as e:
        flash(f"Ошибка подключения к базе данных: {e}")
        return redirect(url_for('home'))
    
@app.route('/properties')
def properties():
    # Логика для отображения объектов недвижимости
    return render_template('properties.html')

@app.route('/edit_property')
def edit_property():
    # Логика для редактирования объектов недвижимости
    return render_template('edit_property.html')

if __name__ == '__main__':
    app.run(debug=True)
