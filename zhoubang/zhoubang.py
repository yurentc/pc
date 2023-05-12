from flask import Flask, render_template, request, g
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = 'messages3.db'

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
        return render_template('zhoubang.html', messages=messages)

if __name__ == '__main__':
    create_tables()
    app.run(port=5004)
