from flask import Flask
from flask import app
import functions as fn


app = Flask(__name__)


@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/launches')
def launches():
    print('Getting SpaceX and NASA launches')
    return fn.format_launches()

@app.route('/sites')
def sites():
    print('Getting SpaceX pads')
    return fn.format_sites()

@app.route('/ajax.js')
#AJAX functions
def ajax():
    return app.send_static_file('ajax.js')

@app.route('/pinx.png')
#map marker SpaceX
def pinx():
    return app.send_static_file('pinx.png')

@app.route('/pinn.png')
#map marker NASA
def pinn():
    return app.send_static_file('pinn.png')

@app.route('/shadow.png')
#map marker shadow
def shadow():
    return app.send_static_file('shadow.png')

if __name__ == '__main__':
    app.run()