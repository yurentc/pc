from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random
from datetime import datetime

geyan = Flask(__name__)

# Configure the database URI
geyan.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages3.db'

# Create the SQLAlchemy object
db = SQLAlchemy(geyan)

# Define the Quote model
class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f"Quote('{self.quote}')"

def create_tables():
    # Create all the tables defined in the models
    db.create_all()

def get_geyan():
    # Get a random quote from the database
    quote = Quote.query.order_by(func.random()).first()
    if quote:
        return quote.quote
    else:
        return None

def geyan_add():
    quote = request.form['quote']
    # Create a new quote object and add it to the database
    new_quote = Quote(quote=quote)
    db.session.add(new_quote)
    db.session.commit()
    # Get all the quotes from the database and render the template
    quotes = Quote.query.all()
    return render_template('geyan.html', rows=quotes)

def geyan_delete():
    quote_id = request.form['quote_id']
    # Delete the quote with the given ID from the database
    quote = Quote.query.get(quote_id)
    db.session.delete(quote)
    db.session.commit()
    # Get all the quotes from the database and render the template
    quotes = Quote.query.all()
    return render_template('geyan.html', rows=quotes)

def messagess():
    # Get the last 30 messages from the database
    messages = Message.query.order_by(Message.id.desc()).limit(30).all()
    return messages

def send_messages(name, message):
    if name and message:
        # Create a new message object and add it to the database
        new_message = Message(name=name, message=message, timestamp=datetime.now())
        db.session.add(new_message)
        db.session.commit()

def delete_messages(message_id):
    # Delete the message with the given ID from the database
    message = Message.query.get(message_id)
    db.session.delete(message)
    db.session.commit()

if __name__ == '__main__':
    # Create the tables if they don't exist
    create_tables()
    geyan.run()