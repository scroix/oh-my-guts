import os
from flask import Flask, render_template, request, json

class FlaskServer:
    app = Flask(__name__)

    @app.route('/')
    def load_index(self = None):
        print('Rendering main page.')
        return render_template('index.html')

    def __init__(self):
        self.app.run(host='0.0.0.0')

if __name__ == "__main__":
    main = FlaskServer()