from datetime import datetime
datetime_list = [
    datetime(2019, 7, 7, 18, 59, 6),
    datetime(2019, 7, 7, 19, 0, 2),
    datetime(2019, 7, 7, 19, 1, 4)
]
report_seconds = []
for dt_end in datetime_list:
    report_seconds.append(dt_end.second)
print(report_seconds)

total_time = sum(report_seconds)
print(total_time)


