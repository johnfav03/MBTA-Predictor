import requests
from datetime import datetime, timedelta, timezone
import pandas as pd

stops = {
    #kenmore - hynes
    (71150, 70152): '0',
    #hynes - copley
    (70152, 70154): '1',
    #copley - arlington
    (70154, 70156): '2',
    #arlington - boylston
    (70156, 70158): '3',
    #boylston - park st
    (70158, 70200): '4',
    #park st - govt ctr
    (70200, 70201): '5',
    #govt ctr - park st
    (70202, 70196): '6',
    #park st - boylston
    (70196, 70159): '7',
    #boylston - arlington
    (70159, 70157): '8',
    #arlington - copley
    (70157, 70155): '9',
    #copley - hynes
    (70155, 70153): '10',
    #hynes - kenmore
    (70153, 71151): '11',
}
routes = {
    'Green-B': '0',
    'Green-C': '1',
    'Green-D': '2',
    'Green-E': '3',
}
outbound = [71150, 70152, 70154, 70156, 70158, 70200, 70201]
inbound = [70202, 70196, 70159, 70157, 70155, 70153, 71151]

prev_day = (datetime.now(timezone(timedelta(hours=-5))) - timedelta(days=1))
beg_time = int(prev_day.replace(hour=4, minute=0, second=0, microsecond=0).timestamp())
end_time = int(prev_day.replace(hour=23, minute=59, second=0, microsecond=0).timestamp())

print(beg_time)
print(end_time)

month_day = prev_day.day
week_day = prev_day.weekday()

api_key = 'wX9NwuHnZU2ToO7GmGR9uw'
url_base=f'https://realtime.mbta.com/developer/api/v2.1/traveltimes?api_key={api_key}&from_datetime={beg_time}&to_datetime={end_time}&format=json'

#week_day,route_id,start_time,travel_time,month_day,stop_id
yesterday = pd.DataFrame(columns=['week_day','route_id','start_time','travel_time','month_day','stop_id'])
for i in range(6):
    suffix = f'&from_stop={outbound[i]}&to_stop={outbound[i+1]}'
    url = url_base + suffix
    response = requests.get(url)
    data = response.json()['travel_times']
    for d in data:
        route_id = routes[d['route_id']]
        epoch_time = datetime.fromtimestamp(int(d['dep_dt']))
        start_time = int((epoch_time - epoch_time.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds())
        travel_time = d['travel_time_sec']
        stop_id = stops.get((outbound[i], outbound[i+1]))
        row = pd.DataFrame([{
            'week_day': week_day, 
            'route_id': route_id, 
            'start_time': start_time, 
            'travel_time': travel_time,
            'month_day': month_day,
            'stop_id': stop_id,
        }])
        yesterday = pd.concat([yesterday, row], ignore_index=True)
for i in range(6):
    suffix = f'&from_stop={inbound[i]}&to_stop={inbound[i+1]}'
    url = url_base + suffix
    response = requests.get(url)
    data = response.json()['travel_times']
    for d in data:
        route_id = routes[d['route_id']]
        epoch_time = datetime.fromtimestamp(int(d['dep_dt']))
        start_time = int((epoch_time - epoch_time.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds())
        travel_time = d['travel_time_sec']
        stop_id = stops.get((inbound[i], inbound[i+1]))
        row = pd.DataFrame([{
            'week_day': week_day, 
            'route_id': route_id, 
            'start_time': start_time, 
            'travel_time': travel_time,
            'month_day': month_day,
            'stop_id': stop_id,
        }])
        yesterday = pd.concat([yesterday, row], ignore_index=True)
yesterday.to_csv('data/LR-yesterday.csv')

print(f'Lines: {len(yesterday)}')