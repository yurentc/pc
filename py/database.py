from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Link(db.Model):
    __tablename__ = 'link' # 定义表名为 link
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





