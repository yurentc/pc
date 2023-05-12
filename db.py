from flask import Flask, render_template, request
import sqlite3
import random
from datetime import datetime

geyan = Flask(__name__)
DATABASE = 'messages3.db'
def get_geyan():
    # 创建数据库连接
    conn = sqlite3.connect('励志名言.db')
    c = conn.cursor()

    # 创建名言表
    c.execute('''CREATE TABLE IF NOT EXISTS quotes (id INTEGER PRIMARY KEY, quote TEXT)''')
    # 插入一些数据
    quote = "在小小的题库里面刷啊刷啊刷，做小小的题目学小小的算法呀。在特别难的题库里面刷啊刷啊刷，做特别难的题目学特别深的算法呀！"

    # 检查数据库中是否已存在相同的引语记录
    c.execute("SELECT * FROM quotes WHERE quote = ?", (quote,))
    existing_row = c.fetchone()

    if not existing_row:
        # 在数据库中插入引语记录
        c.execute("INSERT INTO quotes (quote) VALUES (?)", (quote,))

    # 查询所有记录并随机输出一条
    c.execute("SELECT * FROM quotes")
    geyan = None
    rows = c.fetchall()
    if rows:
        random_index = random.choice(range(len(rows)-1))
        geyan = rows[random_index][1]
        # print(rows[random_index])
    else:
        print('没有记录可输出')

    # 关闭数据库连接
    conn.close()

    return geyan


def get_db_connection():
    # 创建数据库连接
    conn = sqlite3.connect('励志名言.db')
    return conn

def get_all_quotes():
    # 创建数据库连接
    conn = get_db_connection()
    c = conn.cursor()
    # 查询所有记录
    c.execute("SELECT * FROM quotes")
    rows = c.fetchall()
    # 关闭数据库连接
    conn.close()
    return rows

def geyan_delete():
    quote_id = request.form['quote_id']
    # 创建数据库连接
    conn = get_db_connection()
    c = conn.cursor()
    # 根据quote_id删除记录
    c.execute("DELETE FROM quotes WHERE id = ?", (quote_id,))
    # 提交事务
    conn.commit()
    conn.close()
    # 获取所有格言记录
    rows = get_all_quotes()
    # 关闭数据库连接
    return render_template('geyan.html', rows=rows)


def geyan_add():
    quote = request.form['quote']
    # 创建数据库连接
    conn = get_db_connection()
    c = conn.cursor()
    # 在数据库中插入引语记录
    c.execute("INSERT INTO quotes (quote) VALUES (?)", (quote,))
    # 提交事务
    conn.commit()
    conn.close()
    # 获取所有格言记录
    rows = get_all_quotes()
    return render_template('geyan.html', rows=rows)



def get_db():

    db = sqlite3.connect(DATABASE)
    return db

def create_tables():

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

def messagess():
    create_tables()
    db = get_db()
    c = db.cursor()
    c.execute("SELECT * FROM messages ORDER BY id DESC LIMIT 30")
    messages = c.fetchall()
    return messages

def send_messages(name,message):
    if name and message:
        db = get_db()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c = db.cursor()
        c.execute("INSERT INTO messages (name, message, timestamp) VALUES (?, ?, ?)", (name, message, timestamp))
        db.commit()

def delete_messages(message_id):
    db = get_db()
    c = db.cursor()
    c.execute('DELETE FROM messages WHERE id = ?', (message_id,))
    db.commit()


if __name__ == '__main__':
    geyan.run()