import requests
import json
import time

#gets data about all rocket launches in each year, filters our NASA launches and gathers count in each year + launch site coordinates
def get_NASA_half(dates, yeardata, count):
    all_launches = 'https://launchlibrary.net/1.4/launch/' + dates
    r = requests.get(all_launches)

    if r.status_code == 200:
        dataset = r.json()
    else:
        print(r.status_code)
        return 'Problem obtaining data'

    for i in dataset['launches']:
        if len(i['missions']) > 0:
            if i['missions'][0]['agencies'] != None:
                if len(i['missions'][0]['agencies']) > 0:
                    if i['missions'][0]['agencies'][0]['abbrev'] == 'NASA':
                        each_launch = {}
                        each_launch['lat'] = i['location']['pads'][0]['latitude']
                        each_launch['lon'] = i['location']['pads'][0]['longitude']
                        each_launch['site'] = i['location']['pads'][0]['name']
                        yeardata.append(each_launch)
                        count += 1
    return [yeardata, count]

#gets info about SpaceX launches from all of the years and gathers count in each year while getting NASA data
def format_NASA_year(year):
    print('Formatting NASA data from ' + str(year))
    yeardata = []
    count = 0

    res = get_NASA_half(str(year) + '-01-01/' + str(year) + '-07-01', yeardata, count)
    yeardata = res[0]
    count = res[1]
    res = get_NASA_half(str(year) + '-07-01/' + str(year + 1) + '-01-01', yeardata, count)

    return [res[0], res[1]]

def format_launches():
    start_time = time.time()
    spacex_launches = 'https://api.spacexdata.com/v3/launches'
    r = requests.get(spacex_launches)

    if r.status_code == 200:
        dataset = r.json()
    else:
        print(r.status_code)
        return 'Problem obtaining data'

    mid_time = time.time()
    print('Recieved SpaceX launches in ' + str(round(mid_time - start_time, 3)) + ' seconds')

    xdata = {}
    nasadata = {}
    years = []
    first = int(dataset[0]['launch_year'])
    last = int(dataset[-1]['launch_year'])

    print('Getting NASA data')

    for i in range(first, last + 1):
        yr = str(i)
        xdata[yr] = {'count':0}
        nasadata[yr] = {}
        temp_nas_data = format_NASA_year(i)
        nasadata[yr]['info'] = temp_nas_data[0]
        nasadata[yr]['count'] = temp_nas_data[1]
        years.append(i)

    print('NASA data received in ' + str(round(time.time() - mid_time, 3)) + ' seconds')
    print('Formatting SpaceX data')

    for i in dataset:
        xdata[i['launch_year']]['count'] += 1

    send_back = {'spacex':xdata, 'nasa':nasadata, 'years':years}

    print('Sending SpaceX and NASA launch data after ' + str(round(time.time() - start_time, 3)) + ' seconds')
    return json.dumps(send_back)

#gets and combines data about SpaceX launch sites
def format_sites():
    start_time = time.time()
    spacex_sites = 'https://api.spacexdata.com/v3/launchpads'
    r = requests.get(spacex_sites)

    if r.status_code == 200:
        dataset = r.json()
    else:
        print(r.status_code)
        return 'Problem obtaining data'
    xdata = []
    for i in dataset:
        each_site = {}
        each_site['id'] = i['site_id']
        each_site['name'] = i['site_name_long']
        each_site['lat'] = i['location']['latitude']
        each_site['lon'] = i['location']['longitude']
        xdata.append(each_site)
    print('Sending SpaceX pad data after ' + str(round(time.time() - start_time, 3)) + ' seconds')
    return json.dumps(xdata)
