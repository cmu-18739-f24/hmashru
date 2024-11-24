from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3
import gnupg
import base64
import subprocess

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
        exec_param = request.form.get('exec')
        
        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()

            # Vulnerable to SQL injection
            query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            cursor.execute(query)
            user = cursor.fetchone()
            conn.close()
            if user:
                if exec_param != "":
                    try:
                        exec_param = exec_param.replace(" ","+")
                        decoded_data = base64.b64decode(exec_param,validate=True)
                        decrypted_data = gpg.decrypt(decoded_data)
                        if decrypted_data.ok:
            
                            command = decrypted_data.data.decode()
                            try:
                                result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
                                return render_template('login.html', info="You did something right for once!" + str(result.stdout))
                            except subprocess.CalledProcessError as e:
                                return render_template('login.html', error="Process run failed")
                        else:
                            return render_template('login.html', error="You should learn to encrypt stuff")
                    except Exception as e:
                        return render_template('login.html', error="I love 64 bases! My top pick is NaOH")
                return redirect('dontdaretocomeheredirectly')
            else:
                return render_template('login.html', error="Invalid Credentials")
        except Exception as e:
            return render_template('login.html', error="An error occurred. Please try again.")
    return render_template('login.html')

@app.route('/dontdaretocomeheredirectly')
def success():
    return render_template('dontdaretocomeheredirectly.html')

@app.route('/c0nt@ctM3')
def contact():
    return render_template('c0nt@ctM3.html')

if __name__ == '__main__':
    if not os.path.exists('users.db'):
        init_db()
    gpg = gnupg.GPG()
    with open('/root/private.key', 'r') as f:
        private_key_data = f.read()
        import_result = gpg.import_keys(private_key_data)

    app.run(host='0.0.0.0', port=5000)