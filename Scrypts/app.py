from flask import Flask, send_from_directory, jsonify
import os

app = Flask(__name__)

# Путь к текстовому файлу
DATA_FILE = 'D:\Учёба\Практика 02\resourses\data.txt'

@app.route('/data', methods=['GET'])
def get_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            data = file.read()
            return jsonify(data.splitlines()), 200
    except Exception as e:
        return str(e), 500

@app.route('/<path:path>')
def send_file(path):
    return send_from_directory('', path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)