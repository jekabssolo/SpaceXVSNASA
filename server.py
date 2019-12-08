from flask import Flask
from flask import request
from flask import app
import functions as fn

app = Flask(__name__)


@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/launches')
def launches():
    return fn.format_launches()

@app.route('/sites')
def sites():
    return fn.format_sites()

@app.route('/ajax.js')
def ajax():
    return app.send_static_file('ajax.js')

@app.route('/pinx.png')
def pinx():
    return app.send_static_file('pinx.png')

@app.route('/pinn.png')
def pinn():
    return app.send_static_file('pinn.png')

@app.route('/shadow.png')
def shadow():
    return app.send_static_file('shadow.png')

if __name__ == '__main__':
    app.run()