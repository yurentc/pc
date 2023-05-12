# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
db = SQLAlchemy()

class URL(db.Model):
    __tablename__ = 'urls' # 定义表名为 link
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    click_count = db.Column(db.Integer, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('urls', lazy=True))


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    __table_args__ = {'extend_existing': True}

def create_app(qz=None):
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///link.db'
    app.secret_key = 'my_secret_key'  # 建议使用一个密钥来保护您的会话，这里用于演示使用，实际应用中可使用更安全的方式保护密钥。

    db.init_app(app)

    from py.main import main_bp
    app.register_blueprint(main_bp)

    from py.link import link_bp
    app.register_blueprint(link_bp, url_prefix='/link')

    @app.template_filter('compare_dates')
    def compare_dates_filter(date_string):
        today = datetime.datetime.today().date()
        review_date = datetime.datetime.strptime(date_string, '%Y-%m-%d').date()
        return review_date <= today

    return app
    # from app.study_plan.study_plan import study_plan_bp
    # app.register_blueprint(study_plan_bp, url_prefix='/study_plan')
    #
    # from app.study.programming.programming import programming_bp
    # app.register_blueprint(programming_bp, url_prefix='/code')
    #
    # from app.study.language.language import language_bp
    # app.register_blueprint(language_bp, url_prefix='/language')
    #
    # from app.study.math.math import math_bp
    # app.register_blueprint(math_bp, url_prefix='/math')
    #
    # from app.study.english.english import english_bp
    # app.register_blueprint(english_bp, url_prefix='/english')
    #
    # from app.study.exercise.exercise import exercise_bp
    # app.register_blueprint(exercise_bp, url_prefix='/exercise')
    #
    # from app.navigation.navigation import navigation_bp
    # app.register_blueprint(navigation_bp, url_prefix='/navigation')
    #
    # from app.message.message import message_bp
    # app.register_blueprint(message_bp, url_prefix='/message')

