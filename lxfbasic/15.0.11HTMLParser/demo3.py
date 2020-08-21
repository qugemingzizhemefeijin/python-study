from html.parser import HTMLParser
from html.entities import name2codepoint
from urllib import request
from datetime import datetime
from pytz import utc
from pytz import timezone

utc_tz = timezone('UTC')
cst_tz = timezone('Asia/Shanghai')

dt = datetime.strptime('2020-03-02T15:27:00', '%Y-%m-%dT%H:%M:%S')
print(dt)
dt_utc = dt.replace(tzinfo=utc_tz)
print(dt_utc)
dt_sh = dt.astimezone(cst_tz)
print(dt_sh)