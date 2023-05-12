# run.py
from flask import Flask
from py import create_app

app = Flask(__name__, static_folder='static')
# <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
# <img src="{{ url_for('static', filename='images/image.jpg') }}" alt="Image">
# <script src="{{ url_for('static', filename='js/script.js') }}"></script>
app = create_app()

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8000)

