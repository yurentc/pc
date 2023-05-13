from flask import Flask, render_template, request, redirect, session, Blueprint, url_for,current_app
from flask_sqlalchemy import SQLAlchemy
from . import db,Category, URL

liuyan_bp = Blueprint('liuyan', __name__, url_prefix='/liuyan')



# def get_geyan():
#     # Get a random quote from the database
#     quote = Quote.query.order_by(func.random()).first()
#     if quote:
#         return quote.quote
#     else:
#         return None
#
# def messagess():
#     messages = Message.query.order_by(Message.id.desc()).limit(30).all()
#     return messages
#
# def send_messages(name, message):
#     if name and message:
#         new_message = Message(name=name, message=message, timestamp=datetime.now())
#         db.session.add(new_message)
#         db.session.commit()
#
# def delete_messages(message_id):
#     message = Message.query.get(message_id)
#     db.session.delete(message)
#     db.session.commit()
#
# @liuyan_bp.route('/')
# def index():
#     return render_template('index.html')
#
# @liuyan_bp.route('/liuyan', methods=['GET', 'POST'])
# def liuyan():
#     if request.method == 'POST':
#         name = request.form['name']
#         message = request.form['message']
#         send_messages(name, message)
#     messages = messagess()
#     return render_template('liuyan.html', messages=messages)
#
# @liuyan_bp.route('/management')
# def management():
#     messages = messagess()
#     return render_template('management.html', messages=messages)
#
# @liuyan_bp.route('/delete_message', methods=['POST'])
# def delete_message():
#     message_id = request.form['message_id']
#     delete_messages(message_id)
#     return 'Success'


def generate_table(acwing, learn, words, math, english, chinese):
    # 构建表格内容
    table_content = f"""
        <tr>
            <td>AcWing复习</td>
            <td>{acwing}</td>
        </tr>
        <tr>
            <td>AcWing学习</td>
            <td>{learn}</td>
        </tr>
        <tr>
            <td>单词背诵</td>
            <td>{words}</td>
        </tr>
        <tr>
            <td>数学课</td>
            <td>{math}</td>
        </tr>
        <tr>
            <td>英语课</td>
            <td>{english}</td>
        </tr>
        <tr>
            <td>语文课</td>
            <td>{chinese}</td>
        </tr>
                <tr>
            <td colspan="2"><input type="button" value="更新" onclick=""></td>
        </tr>

    """

    # 构建完整表格
    table = f"""
    <table>
        <tr>
            <th>本周学习总结</th>
            <th>数量</th>
        </tr>
        {table_content}

    </table>
    """

    return table


def generate_lstable(acwing, learn, words, math, english, chinese):
    # 构建表格内容
    table_content = f"""
        <tr>
            <td>AcWing复习</td>
            <td>{acwing}</td>
        </tr>
        <tr>
            <td>AcWing学习</td>
            <td>{learn}</td>
        </tr>
        <tr>
            <td>单词背诵</td>
            <td>{words}</td>
        </tr>
        <tr>
            <td>数学课</td>
            <td>{math}</td>
        </tr>
        <tr>
            <td>英语课</td>
            <td>{english}</td>
        </tr>
        <tr>
            <td>语文课</td>
            <td>{chinese}</td>
        </tr>
    """

    # 构建完整表格
    table = f"""
    <table>
        <tr>
            <th>历史之最</th>
            <th>数量</th>
        </tr>
        {table_content}

    </table>
    """

    return table


def top():
    # 构建表格内容
    # geyan = get_geyan(){geyan}
    tops = f"""

        <p style="text-align: right;font-size: x-small;"></p>
        <table style="width: 100%; background-color: #00B0FF; height: 15px;">
            <tr>
                <td style="width: 10%; text-align: center; color: #fff;"></td>
                <td style="width: 10%; text-align: center;"><a href="#"
                        style="color: #fff; font-weight: bold; text-decoration: none;">总计划</a></td>
                <td style="width: 10%; text-align: center;"><a href="/"
                        style="color: #fff; font-weight: bold; text-decoration: none;">编程</a></td>
                <td style="width: 10%; text-align: center;"><a href="#"
                        style="color: #fff; font-weight: bold; text-decoration: none;">语文</a></td>
                <td style="width: 10%; text-align: center;"><a href="#"
                        style="color: #fff; font-weight: bold; text-decoration: none;">数学</a></td>
                <td style="width: 10%; text-align: center;"><a href="#"
                        style="color: #fff; font-weight: bold; text-decoration: none;">英语</a></td>
                <td style="width: 10%; text-align: center;"><a href="#"
                        style="color: #fff; font-weight: bold; text-decoration: none;">锻炼</a></td>
                <td style="width: 10%; text-align: center;"><a href="/link/"
                        style="color: #fff; font-weight: bold; text-decoration: none;">网址</a></td>
                <td style="width: 10%; text-align: center;"><a href="/liuyan/"
                        style="color: #fff; font-weight: bold; text-decoration: none;">留言</a></td>
                <td style="width: 10%; text-align: center; color: #fff;"></td>
            </tr>
        </table>
    """
    return tops