from flask import Flask, render_template, request, g, session, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key'
DATABASE = 'messages3.db'
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def create_tables():
    with app.app_context():
        db = get_db()
        c = db.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')
        db.commit()

def is_admin():
    return 'username' in session and session['username'] == ADMIN_USERNAME

@app.route('/', methods=['GET', 'POST'])
def index():
    with app.app_context():
        db = get_db()
        if request.method == 'POST':
            name = request.form['name']
            message = request.form['message']
            if name and message:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                c = db.cursor()
                c.execute("INSERT INTO messages (name, message, timestamp) VALUES (?, ?, ?)", (name, message, timestamp))
                db.commit()
        c = db.cursor()
        c.execute("SELECT * FROM messages ORDER BY id DESC LIMIT 30")
        messages = c.fetchall()
        return render_template('a.html', messages=messages, is_admin=is_admin())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 执行身份验证逻辑

        # 如果身份验证成功，设置会话变量并重定向到管理页面
        session['username'] = username
        return redirect('/management')

    return render_template('login.html')


# 管理页面
@app.route('/management')
def management():
    if 'username' in session:
        username = session['username']
        return render_template('management.html', username=username)

    return redirect('/login')


# 注销
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/delete_message/<int:message_id>')
def delete_message(message_id):
    if is_admin():
        with app.app_context():
            db = get_db()
            c = db.cursor()
            c.execute("DELETE FROM messages WHERE id = ?", (message_id,))
            db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    create_tables()
    app.run(port=5005)
