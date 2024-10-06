from flask import Flask, render_template
import psutil
import time

app = Flask(__name__)

@app.route('/')
def index():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent

    return render_template('index.html', cpu_usage=cpu_usage, memory_usage=memory_usage)

if __name__ == '__main__':
    app.run(debug=True)
