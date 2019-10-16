import csv
from datetime import datetime
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pdb
import pandas as pd

# Gspread setup
scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('Calaxy Clock-80a46774c131.json', scope)
gc = gspread.authorize(credentials)
wks1 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1oTscuN5JqshsnnwVKfyHL8WXnBAVFeMgwlHb_N21AQM/edit#gid=51388084').worksheet('raw data')
wks2 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1oTscuN5JqshsnnwVKfyHL8WXnBAVFeMgwlHb_N21AQM/edit#gid=51388084').worksheet('processed stamps')

raw_timestamps = wks1.get_all_values()
raw_timestamps = raw_timestamps[1:]

for timestamp in raw_timestamps:
    time_and_date = timestamp[0].split()
    timestamp[0] = time_and_date[0]
    timestamp.append(time_and_date[1])

problematic_timecard = any('' in sublists for sublists in raw_timestamps)
if problematic_timecard:
    print('Timecard has blank spot')
    sys.exit()
if raw_timestamps[0][3] == "Out":
    print('First timestamp is out')
    sys.exit()

for current_entry_index,timestamp in enumerate(raw_timestamps):
    name = timestamp[1]
    found_another_name = 0;
    incremented_next_entry = 0;
    if timestamp[4] == "Out":
        print(name + ' didnt clock in before' + str(timestamp))
        sys.exit()
    for next_entry_index, otherstamps in enumerate(raw_timestamps[current_entry_index+1:]):
        if found_another_name == 0:
            try:
                otherstamps.index(name);
            except:
                continue
            found_another_name = 1;
        else:
            incremented_next_entry = 1;
            break
    if incremented_next_entry == 0:
        next_entry_index += 1
    if found_another_name == 0:
        print(name + ' didnt clock out after' + str(timestamp))
        sys.exit()
    next_entry_index = next_entry_index + current_entry_index
    if next_entry_index > len(raw_timestamps):
        continue
    if raw_timestamps[next_entry_index][4] != "Out":
        print(name + ' didnt clock out after' + str(timestamp))
        sys.exit()

    timestamp[4] = timestamp[5]
    timestamp.pop(5)
    timestamp.append(raw_timestamps[next_entry_index][5])
    raw_timestamps.pop(next_entry_index)

    timestamp.append((datetime.strptime(timestamp[5], '%H:%M:%S')-datetime.strptime(timestamp[4], '%H:%M:%S')).total_seconds()/3600)
    timestamp[6] = abs(round(timestamp[6]*4)/4)
    #NEED TO FIX PROGRAM SO DON"T NEED ABS

raw_timestamps_with_headers = [['date', 'user', 'job', 'division', 'in', 'out', 'hours']]
raw_timestamps_with_headers.extend(raw_timestamps)
with open("out.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(raw_timestamps_with_headers)

range_string = "A2:G" + str(len(raw_timestamps)+1)
cell_list = wks2.range(range_string)
current_row = 0
current_column = 0
for cell in cell_list:
    cell.value = raw_timestamps[current_row][current_column]
    current_column +=1
    if current_column == 7:
        current_row +=1
        current_column = 0
wks2.update_cells(cell_list)
