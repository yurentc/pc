#py/link.py
from flask import Flask, render_template, request, redirect, session, Blueprint, url_for,current_app
from flask_sqlalchemy import SQLAlchemy
from . import db,Category, URL

link_bp = Blueprint('link', __name__, url_prefix='/link')

@link_bp.route('/admin', methods=['GET'])
def admin():
    categories = Category.query.all()
    return render_template('/html/link/index.html', categories=categories)

@link_bp.route('/')
def link():

    categories = Category.query.all()
    return render_template('/html/link/link.html', categories=categories)


@link_bp.route('/add_category', methods=['POST'])
def add_category():
    name = request.form['name']
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return redirect(url_for('link.admin'))


@link_bp.route('/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    category = Category.query.get(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('link.admin'))


@link_bp.route('/edit_category/<int:category_id>', methods=['POST'])
def edit_category(category_id):
    category = db.session.query(Category).get(category_id)
    new_name = request.get_json(force=True, silent=True)['name']
    category.name = new_name
    db.session.commit()
    return {'name': category.name}


@link_bp.route('/add_url', methods=['POST'])
def add_url():
    category_id = int(request.form['category_id'])
    title = request.form['title']
    url = request.form['url']
    existing_url = db.session.query(URL).filter_by(category_id=category_id).filter((URL.title == title) | (URL.url == url)).first()
    if existing_url:
        if existing_url.title != title:
            existing_url.title = title
        if existing_url.url != url:
            existing_url.url = url
        db.session.commit()
    else:
        category = db.session.query(Category).get(category_id)
        new_url = URL(title=title, url=url, category=category)
        db.session.add(new_url)
        db.session.commit()
    return redirect(url_for('link.admin'))


@link_bp.route('/delete_url/<int:url_id>', methods=['POST'])
def delete_url(url_id):
    url = db.session.query(URL).get(url_id)
    db.session.delete(url)
    db.session.commit()
    return redirect(url_for('link.admin'))


@link_bp.route('/edit_url', methods=['POST'])
def edit_url():
    url_id = request.json.get('url_id')
    title = request.json.get('title')
    url = request.json.get('url')

    url_obj = db.session.query(URL).get(url_id)
    url_obj.title = title
    url_obj.url = url
    db.session.commit()

    return {'title': url_obj.title, 'url': url_obj.url}


@link_bp.route('/increase_click_count/<int:url_id>', methods=['POST'])
def increase_click_count(url_id):
    url = db.session.query(URL).get(url_id)
    url.click_count += 1
    db.session.commit()
    return '', 200


# 上下文处理器，用于获取urls_by_category
@link_bp.context_processor
def urls_by_category_processor():
    def get_urls_by_category(category_id):
        return db.session.query(URL).filter_by(category_id=category_id).order_by(URL.click_count.desc()).all()

    return dict(get_urls_by_category=get_urls_by_category)


if __name__ == '__main__':
    with link_bp.app_context():
        db.create_all()
    link_bp.run(port=5012)
