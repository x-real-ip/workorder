import json
import os
import re

values_filename = ("values.json")
values_filelocation = os.path.abspath(values_filename)

try:
  with open(values_filelocation) as values_file:
    objects_values = json.load(values_file)
    values_file.close()
except FileNotFoundError as e:
    print(e)

## date

date = objects_values["date"]
print(date)

## start time
start_time = re.split("\D",objects_values["start_time"])
start_hrs = int(start_time[0])
start_min = int(start_time[1])

if start_min <= 15:
    start_min = 00
elif start_min <= 30 >= 15:
    start_min = 15
elif start_min <= 45 >= 30:
    start_min = 30
elif start_min <= 59 >= 45:
    start_min = 45

print(f"Start time is: {start_hrs:02d}:{start_min:02d}")

## end time
end_time = re.split("\D",objects_values["end_time"])
end_hrs = int(end_time[0])
end_min = int(end_time[1])

if end_min <= 15 >= 00:
    end_min = 15
elif end_min <= 30 >= 15:
    end_min = 30
elif end_min <= 45 >= 30:
    end_min = 45
elif end_min <= 59 >= 45:
    end_min = 00
    end_hrs += 1
    if end_hrs == 24:
      end_hrs = 00

print(f"End time is: {end_hrs:02d}:{end_min:02d}")
