import ctypes
import json
import os
import sys
from datetime import datetime
from datetime import date

import config
import checks

# Check local API connection and after how many seconds it must retry
checks.connection_check_url(config.api_url, 5)

# Check if json file exists
if os.path.exists(config.json_file):
    f = open(config.json_file, "r")
    json_object = json.load(f)
    f.close()
    if json_object["date"] == str(date.today()):
        # Exit if starttime is already set with date today
        print("Starttime already set today")
        sys.exit()

# Create starttime with data today
starttime = datetime.now().strftime("%H.%M")
data = {}
data["date"] = str(date.today())
data["start_time"] = starttime
data["end_time"] = ""
print(f"Startime is set {data}")
with open(config.json_file, 'w') as file_object:
    json.dump(data, file_object)

# Send popup message
MessageBox = ctypes.windll.user32.MessageBoxW
MessageBox(None, f'Starttime is set {starttime}', 'Workorder', 0)
