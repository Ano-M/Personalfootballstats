import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import json
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Hello, world!"  # or your homepage content

@app.route('/api/savedstats', methods=['GET', 'POST'])
def get_stats():
    return jsonify(load_stats())

@app.route('/api/submit', methods=['POST'])
@cross_origin()
def submit_stats():
    stats_data = request.get_json()
    stats = load_stats()

    match_id = str(uuid.uuid4())
    stats_data['match_id'] = match_id
    print(stats_data)
    print("---------------------")
    print("---------------------")
    print(stats)

    stats.append(stats_data)
    save_stats(stats)
    return jsonify(f"Form submitted successfully!")

def load_stats():
    try:
        if not os.path.exists("stats.json") or os.stat("stats.json").st_size == 0:
            return []  # empty file → return empty list
        with open("stats.json", "r") as f:
            loaded_stats = json.load(f)
            if isinstance(loaded_stats, dict):
                return [loaded_stats]
            elif isinstance(loaded_stats, list):
                return loaded_stats
            # Must return list so new data can be appended (subject to change with proper db)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_stats(all_stats):
    with open("stats.json", "w") as f:
        json.dump(all_stats, f, indent=4)

if __name__ == '__main__':
    app.run(debug=True)
