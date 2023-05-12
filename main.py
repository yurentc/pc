# 导入Flask类

from flask import Flask, render_template, request, jsonify, redirect, url_for
from vikas import VikaTable
import datetime
from pa import get_title_by_id
from 爬取数据.qz.py.htmlj import generate_table,generate_lstable,top
from db import geyan_delete, geyan_add, get_all_quotes, messagess,send_messages,delete_messages
from 爬取数据.qz.py.link import link_bp
from 爬取数据.qz.py.database import db

app = Flask(__name__, static_folder='static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(link_bp, url_prefix='/link')

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    click_count = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('urls', lazy=True))


@app.template_filter('compare_dates')
def compare_dates_filter(date_string):
    today = datetime.datetime.today().date()
    review_date = datetime.datetime.strptime(date_string, '%Y-%m-%d').date()
    return review_date <= today

@app.route('/')
def index():
    datass = []
    table = VikaTable()
    data = VikaTable.get_all(table)
    for datas in data:
        review_time = datetime.datetime.fromtimestamp(int(datas.json()["复习时间"]) / 1000)
        start_time = datetime.datetime.fromtimestamp(int(datas.json()["开始时间"]) / 1000)
        da = datas.json()
        da["复习时间"] = review_time.strftime("%Y-%m-%d")
        da["开始时间"] = start_time.strftime("%Y-%m-%d")
        if datas.json()['网址']['title'] != "":
            da['网址'] = datas.json()['网址']['title']
        datass.append(da)
    table = generate_table(acwing=10, learn=5, words=100, math=3, english=2, chinese=4)
    table2 = generate_lstable(acwing=10, learn=5, words=100, math=3, english=2, chinese=4)

    messages = messagess()
    tops=top()
    return render_template('index.html', table=table,table2=table2, data=datass, messages=messages,top=tops)


@app.route('/get_problem')  # 设置提交方法为post
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


@app.route('/update_table', methods=['POST'])
def update_table():
    try:
        # 读取表单数据
        data = request.json
        table = VikaTable()
        if data['复习时间'] == "完成了":
            data['复习时间'] = '2030-01-01'
        print(data)
        if int(data['次']) <= 8:
            table.upsert_record(data)
        return jsonify({'message': data})
    except Exception as e:
        print('Error:', e)
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/geyan/', methods=['GET', 'POST'])
def geyan_index():
    if request.method == 'POST':
        if request.form['action'] == 'delete':
            return geyan_delete()
        elif request.form['action'] == '添加':
            return geyan_add()
        else:
            rows = get_all_quotes()
            return render_template('geyan.html', rows=rows)
    else:
        rows = get_all_quotes()
        return render_template('geyan.html', rows=rows)

@app.route('/liuyan/', methods=['GET', 'POST'])
def liuyan():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        send_messages(name,message)
    messages = messagess()
    table = generate_table(acwing=10, learn=5, words=100, math=3, english=2, chinese=4)
    table2 = generate_lstable(acwing=10, learn=5, words=100, math=3, english=2, chinese=4)
    tops = top()
    return render_template('liuyan.html', messages=messages,table = table, table2 = table2,top =tops)

# 定义删除留言的路由和处理函数
@app.route('/liuyan/delete/<message_id>')
def delete_message(message_id):
    # 在这里处理删除留言的逻辑
    delete_messages(message_id)
    return redirect(url_for('liuyan'))

@app.route('/liuyan/modify/<message_id>', methods=['GET', 'POST'])
def modify_message(message_id):
    if request.method == 'POST':
        updated_message = request.form['message']

        for message in messages:
            if message[0] == message_id:
                message.editing = False
                break

        return redirect(url_for('liuyan'))

    for message in messages:
        if message[0] == message_id:
            message.editing = True
            break

    return render_template('modify.html', message_id=message_id)

def shijiancuo_to_time(ts):
    return str(datetime.datetime.fromtimestamp(int(ts) / 1000).strftime('%Y-%m-%d'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8000)
