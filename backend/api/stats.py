from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, world!"  # or your homepage content

@app.route('/api/stats', methods=['GET'])
def get_stats():
    file_path = os.path.join(os.path.dirname(__file__), 'stats.json')
    with open(file_path, 'r') as f:
        stats = json.load(f)
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)
