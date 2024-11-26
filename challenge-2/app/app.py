from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import re

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('admin', 'p@@5w0rd!'))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()

            query = "SELECT * FROM users WHERE username = ? AND password = ?"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            conn.close()
            if user:
                render_template('admin-thermostat-dashboard')
            else:
                return render_template('login.html', error="Did you think it was this easy??")
        except Exception as e:
            return render_template('login.html', error="An error occurred. Please try again.")
    return render_template('login.html')

@app.route('/robots.txt')
def robots_txt():
    return render_template('robots.txt')

@app.route('/admin-thermostat-dashboard', methods=['GET', 'POST'])
def admin_thermostat_dashboard():
    if request.method == 'POST':
        target_temp = request.form.get('target_temp')

        numbers = numbers = list(map(int, re.split(r'[+\-*/]', target_temp)))
        
        has_greater_than_five = any(num > 5 for num in numbers)
        if has_greater_than_five:
            flash("Max allowed is 5")
            return render_template('admin-thermostat-dashboard.html', temp=1)
        
        if re.fullmatch(r'[0-9+\-*/]+', target_temp):
            try:
                result = eval(target_temp, {"__builtins__": None}, {})
                if not isinstance(result, (int, float)):
                    flash("What are you trying to do?")
                    return render_template('admin-thermostat-dashboard.html')
                with open('/root/flag.txt', 'r') as f:
                    a = f.readline()
                if int(result) == 69:
                    flash("Fine you win :( " + str(a))
                    return render_template('admin-thermostat-dashboard.html', temp=result)
                else:
                    flash("What now??")
                    return render_template('admin-thermostat-dashboard.html', temp=result)
            except Exception as e:
                flash("Exception occured.")
                return render_template('admin-thermostat-dashboard.html', temp=1)
        else:
            flash("Alphabets & weird characters not allowed; I am flexible but restrictive :)")
            return render_template('admin-thermostat-dashboard.html', temp=1)
    return render_template('admin-thermostat-dashboard.html', temp=1)

app.secret_key = b'm\xd8S\xc0\xa5/8s\xe6s6\x9dsN?\x135c%.|\xcd\xcd\x00'

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=4000)