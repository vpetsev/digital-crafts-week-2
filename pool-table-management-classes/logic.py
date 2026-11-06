import os
import json
import view
from datetime import timedelta, date, datetime


class Table:
    def __init__(self, table_number):
        self.table_number = table_number
        self.is_occupied = "Not Occupied"
        self.start_time = None
        self.end_time = None
        self.total_minutes_played_today = 0.0
        self.revenue_from_today = 0.0

    def open_table(self):
        chosen_table = view.pool_hall_tables[self.table_number - 1]
        if chosen_table['is_occupied'] == "Not Occupied":
            self.is_occupied = "Occupied"
            chosen_table['is_occupied'] = self.is_occupied
            chosen_table["start_time"] = self.format_datetime_to_str(datetime.now())
            return True
        else:
            print(f'Table {self.table_number} is already occupied')
            return False
    
    def close_table(self):
        chosen_table = view.pool_hall_tables[self.table_number - 1]
        if chosen_table["is_occupied"] == "Occupied":
            chosen_table['is_occupied'] = 'Not Occupied'
            chosen_table["end_time"] = self.format_datetime_to_str(datetime.now())
            self.min_played()
        else:
            print('no match')

    def min_played(self):
        chosen_table = view.pool_hall_tables[self.table_number - 1]
        try:
            end_time_td = datetime.fromisoformat(chosen_table['end_time'])
        except ValueError:
            end_time_td = datetime.combine(date.today(), datetime.strptime(chosen_table['end_time'], '%H:%M:%S').time())
        try:
            start_time_td = datetime.fromisoformat(chosen_table['start_time'])
        except ValueError:
            # Older saved rows only have a clock time; retain support for them.
            start_time_td = datetime.combine(end_time_td.date(), datetime.strptime(chosen_table['start_time'], '%H:%M:%S').time())
            if start_time_td > end_time_td:
                start_time_td -= timedelta(days=1)
        timediff_to_add = end_time_td - start_time_td
        if timediff_to_add < timedelta(0):
            raise ValueError('Table start time is after its end time')
        value_of_table = chosen_table["total_minutes_played_today"]
        time_in_min = timediff_to_add / timedelta(minutes=1)
        value_of_table += float(time_in_min)
        chosen_table["total_minutes_played_today"] = value_of_table
        chosen_table['start_time'] = None
        chosen_table["end_time"] = None


    def format_datetime_to_str(self, input_value):
        return input_value.isoformat(timespec='seconds')

    def toDict(self):
        return {
            "table_number": self.table_number,
            "is_occupied": "Not Occupied",
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_minutes_played_today": self.total_minutes_played_today
        }


class PoolHall:

    def __init__(self, tables):
        self.all_tables = tables

    def view_tables_in_hall(self):
        for i in range(0, len(view.pool_hall_tables)):
            tbl = view.pool_hall_tables[i]
            print(f'''
                Table_number: {tbl["table_number"]}
                Occupied: {tbl["is_occupied"]}
                Start time: {tbl["start_time"]}
                End time: {tbl["end_time"]}
                Total Time Played: {tbl["total_minutes_played_today"]}
            ''')

    def end_of_day_date_adder(self):
        today = date.today()
        return today.strftime("%B %d, %Y")
