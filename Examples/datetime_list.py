from datetime import datetime, timedelta
dt_list = ['2019-07-07T18:59:06', '2019-07-07T19:00:02', '2019-07-07T19:01:04']
datetime_list = []
for currStr in dt_list:
    dt = datetime.strptime(currStr, '%Y-%m-%dT%H:%M:%S')
    datetime_list.append(dt)
print(datetime_list)
