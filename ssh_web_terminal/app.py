# app.py

from flask import Flask, render_template, request, jsonify
import paramiko
import threading
import os
import json

app = Flask(__name__)

class SSHClientThread(threading.Thread):
    def __init__(self, ip, username, password, callback):
        threading.Thread.__init__(self)
        self.ip = ip
        self.username = username
        self.password = password
        self.callback = callback
        self.client = None
        self.chan = None

    def run(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self.client.connect(self.ip, username=self.username, password=self.password)
            self.chan = self.client.invoke_shell()
            self.callback(self.chan)
        except Exception as e:
            print(f"Connection failed: {e}")
        finally:
            if self.client:
                self.client.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/connect', methods=['POST'])
def connect():
    data = request.json
    ip = data['ip']
    username = data['username']
    password = data['password']
    
    def callback(chan):
        while True:
            # Continuously read from the channel and send to the client
            output = chan.recv(1024).decode('utf-8')
            if output:
                os.write(1, output.encode('utf-8'))

    thread = SSHClientThread(ip, username, password, callback)
    thread.start()
    
    return jsonify({"status": "connected"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
