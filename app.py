from flask import Flask, render_template, request, redirect, url_for, session, flash
import pyodbc
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Заменить на свой секретный ключ (не трогать)

# Настройки подключения к базе данных
server = 'localhost'  # Или '127.0.0.1'
database = 'Lev'  # Имя базы данных
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

@app.route('/')                                        # Главная страница
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])                 # Авторизация
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Хешируем пароль
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Подключаемся к базе данных
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Проверяем пользователя
        cursor.execute("SELECT * FROM users WHERE Username=? AND hashed_password=?", (username, hashed_password))
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

@app.route('/register', methods=['POST']) # 
def register():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']

    # Хешируем пароль
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Проверяем, существует ли пользователь
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        if cursor.fetchone():
            flash('Пользователь с таким именем уже существует.')
            return redirect(url_for('home'))

        # Добавляем нового пользователя
        cursor.execute("INSERT INTO users (username, hashed_password, email) VALUES (?, ?, ?)", (username, hashed_password, email))
        conn.commit()
        flash('Регистрация прошла успешно! Теперь вы можете войти.')
        return redirect(url_for('home'))
    except Exception as e:
        flash(f"Ошибка подключения к базе данных: {e}")
        return redirect(url_for('home'))

@app.route('/dashboard') #                                            Личный кабинет
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('home'))

@app.route('/logout') #                                               Выход
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/properties') #                                           Объекты
def properties():
    # Логика для отображения объектов недвижимости
    return render_template('properties.html')

@app.route('/edit_property') #                                        Создание объектов
def edit_property():
    # Логика для редактирования объектов недвижимости
    return render_template('edit_property.html')

if __name__ == '__main__':
    app.run(debug=True)