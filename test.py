import os
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import model

app = Flask(__name__)
upload_folder = "uploads/"
detected_folder = "detected/"

if not os.path.exists(upload_folder):
    os.mkdir(upload_folder)
if not os.path.exists(detected_folder):
    os.mkdir(detected_folder)

app.config['UPLOAD_FOLDER'] = upload_folder
app.config['DETECTED_FOLDER'] = detected_folder

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('Database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Main page
@app.route('/')
def home():
    return render_template('main.html')

# Login page
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
            return "Error: Incorrect login details"

    return render_template('login.html')

# Registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = email.split('@', 1)[0] if '@' in email else email
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Error: Passwords do not match!"

        hashed_password = generate_password_hash(password)

        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        if cursor.fetchone():
            db.close()
            return "Error: This email is already registered!"

        cursor.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                       (username, email, hashed_password))
        db.commit()
        db.close()

        return redirect(url_for('login'))

    return render_template('register.html')

# Upload and process images
@app.route('/upload', methods=['GET', 'POST'])
def uploadfile():
    if request.method == 'POST':
        f = request.files['file']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
        f.save(file_path)
        processed_path = os.path.join(app.config['DETECTED_FOLDER'], secure_filename(f.filename))

        prediction = model.process_image(file_path)
        os.rename(file_path, processed_path)

        return render_template('result.html', processed_image=processed_path, prediction=prediction)
    return render_template('upload1.html')

# Result display page
@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
