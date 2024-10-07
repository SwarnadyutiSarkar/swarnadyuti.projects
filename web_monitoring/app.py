# app.py

from flask import Flask, render_template, request, jsonify
import requests
import sqlite3
import time
import threading

app = Flask(__name__)

# Database setup
def init_db():
    with sqlite3.connect('monitoring.db') as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS monitoring (id INTEGER PRIMARY KEY, url TEXT, status TEXT, response_time REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')
    print("Database initialized.")

init_db()

def monitor_url(url):
    while True:
        try:
            start_time = time.time()
            response = requests.get(url)
            response_time = time.time() - start_time
            status = 'up' if response.status_code == 200 else 'down'
        except Exception as e:
            status = 'down'
            response_time = None

        log_result(url, status, response_time)
        time.sleep(60)  # Check every minute

def log_result(url, status, response_time):
    with sqlite3.connect('monitoring.db') as conn:
        conn.execute('INSERT INTO monitoring (url, status, response_time) VALUES (?, ?, ?)', (url, status, response_time))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_monitoring', methods=['POST'])
def start_monitoring():
    data = request.json
    url = data['url']
    threading.Thread(target=monitor_url, args=(url,), daemon=True).start()
    return jsonify({"status": "Monitoring started", "url": url})

@app.route('/results', methods=['GET'])
def results():
    with sqlite3.connect('monitoring.db') as conn:
        cursor = conn.execute('SELECT * FROM monitoring ORDER BY timestamp DESC LIMIT 10')
        rows = cursor.fetchall()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
