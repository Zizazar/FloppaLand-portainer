import os
import psycopg2
from flask import Flask, render_template, flash, url_for, redirect, request, flash, send_from_directory
from hashlib import md5
app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='db',
                            port=5432,
                            database='db',
                            user="postgres",
                            password="example")
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users;')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        conn = get_db_connection()
        cur = conn.cursor()

        username = request.form.get('username')
        password = md5(request.form.get('password').encode()).hexdigest()

        cur.execute('SELECT * FROM users WHERE username = %s', (username,))
        if cur.fetchall():
            return 'U are already registred'

        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()

        cur.close()
        conn.close()
        return 'User registered successfully'

    return render_template('register.html')
@app.route('/skin', methods=['GET','POST'])
def skin():
    if request.method == 'POST':
        conn = get_db_connection()
        cur = conn.cursor()

        username = request.form.get('username')
        password = md5(request.form.get('password').encode()).hexdigest()

        cur.execute(f"SELECT password FROM users WHERE username = '{username}'")
        db_pass = cur.fetchone()
        if db_pass != None:
            if db_pass[0] == password:
                if 'file' not in request.files:
                    return 'No files provided'+ str(request.files)
                file = request.files['file']
                
                if file.filename == '':
                    return 'No files'
                if file and file.filename.rsplit('.', 1)[1].lower() == 'png':
                    file.save(os.path.join("./data/skins", username + ".png"))
                    return 'Skin updated successfully'
            else:
                return 'Incorrect password'
        else:
            return 'User not found'

        cur.close()
        conn.close()

    return render_template('skin.html')

@app.route('/skins/<string:filename>')
def get_image(filename):
    return send_from_directory(os.getcwd() + "/data/skins", path=filename, as_attachment=False)

    
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)