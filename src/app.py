from flask import Flask
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return f"Hello (Khe), this is a test build! - {datetime.datetime.now()}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

