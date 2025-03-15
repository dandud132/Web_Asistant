import os
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

import model

app = Flask(__name__)
upload_folder = "uploads/"
if not os.path.exists(upload_folder):
    os.mkdir(upload_folder)
# Creating the detected folder
detected_folder = "detected/"
if not os.path.exists(detected_folder):
    os.mkdir(detected_folder)

app.config['UPLOAD_FOLDER'] = upload_folder
app.config['DETECTED_FOLDER'] = detected_folder

# Функция для подключения к базе данных
def get_db_connection():
    conn = sqlite3.connect('Database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Главная страница
@app.route('/')
def home():
    return render_template('main.html')

# Страница авторизации
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        db.close()

        if user and check_password_hash(user['password_hash'], password):
            return render_template('main.html')
        else:
            return "Ошибка: Неверные данные"

    return render_template('login.html')

# Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = email.split('@', 1)[0] if '@' in email else email
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Ошибка: Пароли не совпадают!"

        hashed_password = generate_password_hash(password)

        db = get_db_connection()
        cursor = db.cursor()

        # Проверяем, есть ли уже такой пользователь
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            db.close()
            return "Ошибка: Этот email уже зарегистрирован!"

        cursor.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                       (username, email, hashed_password))
        db.commit()
        db.close()

        return redirect(url_for('login'))

    return render_template('register.html')
@app.route('/upload', methods=['GET', 'POST'])
def uploadfile():
    if request.method == 'POST':  # check if the method is post
        f = request.files['file']  # get the file from the files object
        # Saving the file in the required destination
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))  # this will secure the file
        model.process_image(f'uploads/{secure_filename(f.filename)}')
        return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)
