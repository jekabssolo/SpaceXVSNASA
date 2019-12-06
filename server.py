from flask import Flask
from flask import request
from flask import app
import requests
import json

def format_all_launches(year):
    all_launches = "https://launchlibrary.net/1.4/launch/" + str(year) + "-01-01/" + str(year) + "-07-01"
    r = requests.get(all_launches)

    if r.status_code == 200:
        dataset = r.json()
    else:
        print(r.status_code)
        return "Problem obtaining data"
    yeardata = []
    for i in dataset['launches']:
        if len(i['missions']) > 0:
            for j in i['missions']:
                if 'agencies' in j:
                    if j['agencies'] != None:
                        for l in j['agencies']:
                            if l['abbrev'] == 'NASA':
                                each_launch = {}
                                each_launch['name'] = i['rocket']['name']
                                each_launch['lat'] = i['location']['pads'][0]['latitude']
                                each_launch['lon'] = i['location']['pads'][0]['longitude']
                                each_launch['site'] = i['location']['pads'][0]['name']
                                yeardata.append(each_launch)

    all_launches = "https://launchlibrary.net/1.4/launch/" + str(year) + "-07-01/" + str(year + 1) + "-01-01"
    r = requests.get(all_launches)

    if r.status_code == 200:
        dataset = r.json()
    else:
        print(r.status_code)
        return "Problem obtaining data"
    for i in dataset['launches']:
        if len(i['missions']) > 0:
            for j in i['missions']:
                if 'agencies' in j:
                    if j['agencies'] != None:
                        for l in j['agencies']:
                            if l['abbrev'] == 'NASA':
                                each_launch = {}
                                each_launch['name'] = i['rocket']['name']
                                each_launch['lat'] = i['location']['pads'][0]['latitude']
                                each_launch['lon'] = i['location']['pads'][0]['longitude']
                                each_launch['site'] = i['location']['pads'][0]['name']
                                yeardata.append(each_launch)

    return yeardata

def format_launches():
    spacex_launches = "https://api.spacexdata.com/v3/launches"
    r = requests.get(spacex_launches)

    if r.status_code == 200:
        dataset = r.json()
    else:
        print(r.status_code)
        return "Problem obtaining data"
    newdata = []
    for i in dataset:
        each_launch = {}
        each_launch['number'] = i['flight_number']
        each_launch['year'] = i['launch_year']
        each_launch['date'] = i['launch_date_local']
        each_launch['rocket'] = i['rocket']['rocket_name']
        each_launch['upcoming'] = i['upcoming']
        each_launch['site'] = i['launch_site']['site_id']
        newdata.append(each_launch)

    first = int(newdata[0]['year'])
    last = int(newdata[-1]['year'])
    nasadata = {}
    for i in range(first, last + 1):
        nasadata[str(i)] = format_all_launches(i)
    send_back = {'spacex':newdata, 'nasa':nasadata}    
    return json.dumps(send_back)

def format_sites():
    spacex_sites = "https://api.spacexdata.com/v3/launchpads"
    r = requests.get(spacex_sites)

    if r.status_code == 200:
        dataset = r.json()
    else:
        print(r.status_code)
        return "Problem obtaining data"
    newdata = []
    for i in dataset:
        each_site = {}
        each_site['id'] = i['site_id']
        each_site['name'] = i['site_name_long']
        each_site['lat'] = i['location']['latitude']
        each_site['lon'] = i['location']['longitude']
        newdata.append(each_site)
    return json.dumps(newdata)


app = Flask(__name__)


@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/launches')
def launches():
    return format_launches()

@app.route('/sites')
def sites():
    return format_sites()

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