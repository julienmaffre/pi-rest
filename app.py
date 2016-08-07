#!/usr/bin/python
from flask import Flask, jsonify

app = Flask(__name__)

pins = [
    {
        'id': 1,
        'title': 'Orange LED',
        'status': 0,
    },
    {
        'id': 2,
        'title': 'Blue LED',
        'status': 1,
    }
]

@app.route('/pins', methods=['GET'])
def get_tasks():
    return jsonify({'pins': pins})

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0')
