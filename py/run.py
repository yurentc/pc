from flask import Flask
from link import link_bp  # assuming you have defined a Blueprint named 'link_bp'

app = Flask(__name__)
app.register_blueprint(link_bp)

if __name__ == '__main__':
    app.run(debug=True,port=5010)