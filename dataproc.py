import pandas as pd
import datetime

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
files = [
    "2022-Q1",
    "2022-Q2",
    "2022-Q3",
    "2022-Q4",
    "2023-Q1",
]

aggregate = pd.DataFrame()
for name in files:
    oldFile = 'data/' + str(name) + '_LRTravelTimes.csv'
    newFile = 'data/LR-' + str(name) + '.csv'
    oldData = pd.read_csv(oldFile)
    print('reading csv: ' + str(name))

    newData = oldData[oldData['route_id'].str.contains('Green')]
    newData = newData[['from_stop_id', 'to_stop_id', 'service_date', 'route_id', 'start_time_sec', 'travel_time_sec']]
    newData.columns = ['from_stop_id', 'to_stop_id', 'week_day', 'route_id', 'start_time', 'travel_time']
    newData['route_id'] = newData['route_id'].map(routes)
    newData['month_day'] = pd.to_datetime(newData['week_day']).dt.day
    newData['week_day'] = pd.to_datetime(newData['week_day']).dt.weekday
    newData['stop_id'] = [stops.get((from_stop, to_stop)) for from_stop, to_stop in zip(newData['from_stop_id'], newData['to_stop_id'])]
    newData = newData.dropna(subset=['stop_id'])
    newData = newData.drop(['from_stop_id', 'to_stop_id'], axis=1)

    newData.to_csv(newFile, index=False)
    aggregate = pd.concat([aggregate, newData], ignore_index=True)
aggregate.to_csv('data/LR-aggregate.csv')