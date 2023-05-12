from flask import Flask, render_template,g, request, jsonify
import sqlite3,os
import datetime
from pa import get_title_by_id

app = Flask(__name__, static_folder='static')

basedir = os.path.abspath(os.path.dirname(__file__))

# 数据库文件的路径
DATABASE = os.path.join(basedir, 'data.db')
# 创建 SQLite 数据库连接和游标
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# 创建数据表（如果不存在）
cursor.execute('''
    CREATE TABLE IF NOT EXISTS problems (
        id INTEGER PRIMARY KEY,
        题号 TEXT,
        题目名称 TEXT,
        题目链接 TEXT,
        复习时间 TEXT,
        次 INTEGER,
        开始时间 TEXT,
        网址 TEXT
    )
''')
conn.commit()
app.config['DATABASE'] = os.path.join(basedir, 'data.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

@app.teardown_appcontext
def close_db(error):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    datass = []
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM problems')
    data = cursor.fetchall()
    for row in data:
        review_time = datetime.datetime.fromtimestamp(int(row[4]) / 1000)
        start_time = datetime.datetime.fromtimestamp(int(row[6]) / 1000)
        da = {
            '题号': row[1],
            '题目名称': row[2],
            '题目链接': row[3],
            '复习时间': review_time.strftime('%Y-%m-%d'),
            '次': row[5],
            '开始时间': start_time.strftime('%Y-%m-%d'),
            '网址': row[7]
        }
        if da['网址'] != "":
            da['网址'] = get_title_by_id(da['网址'])
        # table = generate_table(acwing=10, learn=5, words=100, math=3, english=2, chinese=4)
        datass.append(da)
    return render_template('index1.html', data=datass)
        # return render_template('index.html', table=table, data=da)


@app.route('/get_problem') # 设置提交方法为post
def get_problem():
    problem_id = request.args.get('id')
    problem_info = get_title_by_id(problem_id)
    if problem_info:
        return jsonify({
            "id": problem_id,
            "title": problem_info["title"],
            "link": problem_info["link"],
            "count": 0
        })
    else:
        return jsonify({"error": "获取题目信息失败"})

# @app.route('/update_table', methods=['POST'])
# def update_table():
#     try:
#         # 读取表单数据
#         data = request.json
#         table = VikaTable()
#         if data['复习时间'] == "完成了":
#             data['复习时间'] = '2030-01-01'
#         print(data)
#         if int(data['次'])<=8:
#             table.upsert_record(data)
#         return jsonify({'message': data})
#     except Exception as e:
#         print('Error:', e)
#         return jsonify({'status': 'error', 'message': str(e)})

def shijiancuo_to_time(ts):
        return str(datetime.datetime.fromtimestamp(int(ts)/ 1000).strftime('%Y-%m-%d'))

if __name__ == '__main__':
    app.run(host='192.168.31.226',port=8002)
