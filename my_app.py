from flask import Flask, render_template, request, redirect, url_for
import  sqlite3


app = Flask(__name__)

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
        db = sqlite3.connect('Database.db')
        cursor = db.cursor()
        cursor.execute(f'SELECT * FROM users WHERE email = {email} AND password_hash = {password}')
        if cursor.fetchone() != None:
            return "Вы успешно вошли!"
        else:
            return "Ошибка: Неверные данные"
        db.commit()
        db.close()
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
        db = sqlite3.connect('Database.db')
        cursor = db.cursor()
        cursor.execute(f'INSERT INTO users VALUES(NULL,{username},{email},{password},NULL,NULL)')
        db.commit()
        db.close()
        return redirect(url_for('login'))
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
