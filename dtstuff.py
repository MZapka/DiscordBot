from datetime import datetime
from dateutil.tz import *
# This contains the local timezone 
local = tzlocal()
now = datetime.now()
now = now.replace(tzinfo = local)

# Handles the Local Timezone Information
readable_event_date_local = (now).strftime('%a, %b %d %Y %I:%M:%S %p')
print('Local Time:  ' + readable_event_date_local)

# Handles the Server Timezone Information
utc = tzutc()
utc_now = now.astimezone(utc)
readable_event_date_server = (utc_now).strftime('%a, %b %d %Y %I:%M:%S %p')
print('Server Time: ' + readable_event_date_server)