from datetime import date
from textwrap import dedent
import json
import random
import os

tables = []

running = True


class InitializeTable:
    def __init__(self, table_number):
        self.table_number = table_number
        self.is_occupied = False
        self.start_time = None
        self.end_time = None
        self.number_of_minutes_played = 0

class PoolHall:
    def __init__(self, tables):
        self.tables = tables

tables = []

for index in range(0, 12):
    new_table = InitializeTable(index + 1)
    tables.append(new_table)

my_poolhall = PoolHall(tables)   

def table_viewer():
    for table in my_poolhall.tables:
        print(f'''Table number: {table.table_number}
Occupied: {table.is_occupied}
Start time: {table.start_time}
End time: {table.end_time}
Minutes Played: {table.number_of_minutes_played}''')

# my_poolhall.viewAllTables()




    # - As an admin you should be able to see all the tables(12)
    # - As an admin each table in the list should show, whether the table is OCCUPIED or NOT OCCUPIED.
    # - As an admin if the table is OCCUPIED then show the start time of the table, number of minutes played.
# logic.table_maker()


while running:
    print("Menu options (1/2/3/q): ")
    print("1. Mark a table as occupied")
    print("2. See all active tables")
    print("3. Total revenue")
    print("q. Press q to quit")
    choice = input()
    if choice == '1':
        table_num = input("Choose a table to mark occupied.")
        # logic.mark_as_occupied(table_num)
    elif choice == '2':
        table_viewer()
    if choice == 'q':
        break

# # class InitializeTable:
# #       def __init__(self, table_number):
# #           self.table_number = table_number
# #           self.occupied: False
# #           self.start_time: 0
# #           self.end_time: 0
# #           self.number_of_minutes_played: 0

# #       def markAsOccupied(self):
# #           pass

# # while running:
# #     for i in range(0, 12):
# #         table = InitializeTable(i)
# #         print(f"Table stored as: Table {table.table_number}")


# # table_list.append(table)
# # print(table_list)

# # def print_tables():
# #     for i in range(0, len(table_list)):
# #         print(f'''
# #         Table_number: {table_list[i]["table_number"]}
# #         ''')
# #         # Occupied: {table_list[i]["occupied"]}
# #         # Start time = {table_list[i]["start_time"]}
# #         # End time = {table_list[i]["end_time"]}
# #         # Minutes Played = {table_list[i]["num_minutes_played"]}
# #         # ''')

# # print(len(table_list))
# # print(table_list)
# # print_tables()


# # # Populate an array holding the tables
