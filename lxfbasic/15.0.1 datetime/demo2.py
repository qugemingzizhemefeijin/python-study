import re
from datetime import datetime, timezone, timedelta

###假设你获取了用户输入的日期和时间如2015-1-21 9:01:30，以及一个时区信息如UTC+5:00，均是str，请编写一个函数将其转换为timestamp：

def to_timestamp(dt_str, tz_str):
	hours = int(re.match(r'^UTC([-\+][0-9]+):00$', tz_str).group(1))
	tz_utc = timezone(timedelta(hours=hours))
	dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
	utc_dt = dt.replace(tzinfo=tz_utc)
	return utc_dt.timestamp()


# 测试:
t1 = to_timestamp('2015-6-1 08:10:30', 'UTC+07:00')
assert t1 == 1433121030.0, t1

t2 = to_timestamp('2015-5-31 16:10:30', 'UTC-09:00')
assert t2 == 1433121030.0, t2

print('ok')
