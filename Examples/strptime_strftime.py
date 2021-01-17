from datetime import datetime, timedelta
date_string = '2019-07-07T18:59:33'
dt = datetime.strptime(date_string,'%Y-%m-%dT%H:%M:%S')
date_format = dt.strftime("%d.%m.%Y")
print(date_format)
