import os
import json
from datetime import date, datetime, timedelta

table_list = []
total_time_played = 0

def table_maker():
    for i in range(0, 12):
        table_dict = {
            "table_number": None,
            "occupied": 'Not Occupied',
            "start_time": None,
            "end_time": None,
            "num_minutes_played": None
        }
        table_dict['table_number'] = i + 1
        table_list.append(table_dict)

def view_tables(table_to_check):
    for i in range(0, len(table_list)):
        tbl = table_list[i]
        print(f'''
            Table_number: {tbl["table_number"]}
            Occupied: {tbl["occupied"]}
            Start time: {tbl["start_time"]}
            End time: {tbl["end_time"]}
            Minutes Played: {tbl["num_minutes_played"]}
        ''')

def time_adder():
    return datetime.now().isoformat(timespec='seconds')

def mark_as_occupied(table_num):
    for i in range(0, len(table_list)):
        tbl = table_list[i]
        if (tbl["table_number"] == table_num) and (tbl["occupied"] != "Occupied"):
            tbl["occupied"] = 'Occupied'
            tbl["start_time"] = time_adder()
            print(f'Table: {table_num} is now {tbl["occupied"]}')
        elif (tbl["table_number"] == table_num) and (tbl["occupied"] == 'Occupied'):
            print(f'Table {table_num} is already occupied')

def mark_as_unoccupied(table_num):
    tbl = next((table for table in table_list if table['table_number'] == table_num), None)
    if tbl is None or tbl['occupied'] != 'Occupied':
        return False
    end_time = time_adder()
    end = datetime.fromisoformat(end_time)
    try:
        start = datetime.fromisoformat(tbl['start_time'])
    except ValueError:
        # Existing JSON files contain time-only values; assume the latest occurrence.
        start = datetime.combine(end.date(), datetime.strptime(tbl['start_time'], '%H:%M:%S').time())
        if start > end:
            start -= timedelta(days=1)
    minutes_played = (end - start).total_seconds() / 60
    if minutes_played < 0:
        raise ValueError('Table start time is after its end time')
    tbl['end_time'] = end_time
    tbl['occupied'] = 'Not Occupied'
    table_reset(table_num, minutes_played)
    print(f'Table occupied for {minutes_played} minutes')
    return True
        

def table_reset(table_to_reset, min_played):
    global total_time_played
    table = next(table for table in table_list if table['table_number'] == table_to_reset)
    table['num_minutes_played'] = min_played
    total_time_played += min_played

def end_of_day_date_adder():
    today = date.today()
    return today.strftime("%B %d, %Y")
    
file_path = 'tables.json'

def is_file_empty(file_path):
    return os.path.exists(file_path) and os.stat(file_path).st_size == 0

is_empty = is_file_empty(file_path)

if is_empty:
    print("file is empty")
    table_maker()
else:
    with open('tables.json', 'r') as file:
        saved_tables = json.load(file)

    for i in range(0, len(saved_tables)):
        table_list.append(saved_tables[i])


