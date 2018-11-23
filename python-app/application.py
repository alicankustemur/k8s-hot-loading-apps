from flask import Flask
import sys
import optparse
import time

app = Flask(__name__)

start = int(round(time.time()))

@app.route("/")
def hello_world():
    return "hello world!"

app.run(host='0.0.0.0', port=5000, debug=False)