import json
import os
from datetime import datetime


import numpy as np


import block
import api_comm


class DataModifier:
    def __init__(self, todo_path=r'CSV\departures_todo.csv', 
                done_path=r'CSV\departures_done.csv',
                conjunctions_path=r'CSV\conjunctions.csv'):
        self.todo_path = todo_path
        self.done_path = done_path
        self.conjunctions_path = conjunctions_path
        self.todos = None
        self.done = None
        self.load_todos_and_done()

    def load_todos_and_done(self):
        """Loads open and done todos from todo_path and done_path
        Converts json format to dict and puts list of dicts into
        self.todos and self.done
        """
        self._load_todos('todo')
        self._load_todos('done')

    def _load_todos(self, done_or_todo):
        if done_or_todo == 'todo':
            path = self.todo_path
        elif done_or_todo == 'done':
            path = self.done_path

        with open(path, 'r') as f:
            todos = f.read()
            todos = todos.split('\n')

        if self._check_file_empty(path) or todos == ['','']:
            if done_or_todo == 'todo':
                self.todos = []
            elif done_or_todo == 'done':
                self.done = []
        else:
            if done_or_todo == 'todo':
                self.todos = [json.loads(todo) for todo in todos]
            elif done_or_todo == 'done':
                self.done = [json.loads(todo) for todo in todos]


    def _check_file_empty(self, path):
        if os.stat(path).st_size == 0:
            return True
        else:
            return False


    def write_todo(self, year, month, day, hour, minute, second):
        """Writes a new todo timestamp to self.todo_path csv in json format
        and appends dict to todos.
        """
        todo_dict = {'year' : year,
                    'month' : month,
                    'day' : day,
                    'hour' : hour,
                    'minute' : minute,
                    'second' : second}

        self.todos.append(todo_dict)

        todo_json = json.dumps(todo_dict)

        if self._check_file_empty(self.todo_path):
            with open(self.todo_path, 'a') as f:
                f.write(todo_json)
        else:
            with open(self.todo_path, 'a') as f:
                f.write('\n{}'.format(todo_json))

    def is_done(self):
        self.done = self.todos
        self.todos = []
        self._write_done_and_todos()
        with open(self.todo_path, 'w') as f:
            f.write('')

    def _write_done_and_todos(self):
        """
        """
        todo_json_list = [json.dumps(todo) for todo in self.todos]
        done_json_list = [json.dumps(todo) for todo in self.done]
        todo_string = '\n'.join(todo_json_list)
        done_string = '\n'.join(done_json_list)
        todo_empty = self._check_file_empty(self.todo_path)
        done_empty = self._check_file_empty(self.done_path)
        if todo_empty:
            with open(self.todo_path, 'w') as f:
                f.write(todo_string)
        else:
            with open(self.todo_path, 'a') as f:
                f.write('\n{}'.format(todo_string))
        if done_empty:
            with open(self.done_path, 'w') as f:
                f.write(done_string)
        else:
            with open(self.done_path, 'a') as f:
                f.write('\n{}'.format(done_string))

    def write_point(self,point_info_dict):
        """Takes dict with keys 'point_id', 'latitude', 'longitude',
        'conn_rightway', 'conn_wrongway' and 'name.

        Writes line to self.conjunctions_path csv
        """
        line = self._generate_line(point_info_dict)

        with open(self.conjunctions_path, 'a') as f:
            f.writelines([line])

    def _generate_line(self, point_info_dict):
        return '{},{},{},{},{},{}\n'.format(point_info_dict['point_id'],
                                            point_info_dict['latitude'],
                                            point_info_dict['longitude'],
                                            point_info_dict['conn_rightway'],
                                            point_info_dict['conn_wrongway'],
                                            point_info_dict['name']
                                            )

    def work_todos(self):
        superblock = block.Block()
        communicator = api_comm.DistanceMatrixCommunicator('google_api_key.txt')

        for todo in self.todos:
            if todo in self.done:
                continue
            dt_dict = json.loads(todo)
            dt_dict_int = {key:int(val) for key, val in dt_dict.items()}
            todo_dt = datetime(**dt_dict_int)
            communicator.departure_time = todo_dt
            for lat, lon in zip(superblock.conjunctions['latitude'].values, superblock.conjunctions['longitude'].values):
                origin = {'latitude' : lat,
                        'longitude' : lon
                        }
                communicator.origin = origin
                for connections in superblock.conjunctions['connected_right']:
                    if connections == np.nan or connections == 'nan':
                        continue
                    for con in connections:
                        if con == np.nan or connections == 'nan':
                            continue
                        destination = {'latitude' : superblock.conjunctions.at[int(con),'latitude'],
                                        'longitude' : superblock.conjunctions.at[int(con),'longitude']
                                        }
                        communicator.destination = destination
                        filename = 'CSV\\responses\\{}-{}-{}-{}-{}-{}.csv'.format(todo_dt.year,
                                                                todo_dt.month,
                                                                todo_dt.day,
                                                                todo_dt.hour,
                                                                todo_dt.minute,
                                                                todo_dt.second)
                        with open(filename, 'a') as f:
                            f.writelines(['{},{},{}\n'.format(communicator.json_response, json.dumps(origin), json.dumps(destination))])

                for connections in superblock.conjunctions['connected_wrong']:
                    if connections == np.nan or connections == 'nan':
                        continue
                    for con in connections:
                        if con == np.nan or con == 'nan':
                            continue
                        destination = {'latitude' : superblock.conjunctions.at[int(con),'latitude'],
                                        'longitude' : superblock.conjunctions.at[int(con),'longitude']
                                        }
                        communicator.destination = destination
                        filename = 'CSV\\responses\\{}-{}-{}-{}-{}-{}.csv'.format(todo_dt.year,
                                                                todo_dt.month,
                                                                todo_dt.day,
                                                                todo_dt.hour,
                                                                todo_dt.minute,
                                                                todo_dt.second)
                        with open(filename, 'a') as f:
                            f.writelines(['{},{},{}\n'.format(communicator.json_response, json.dumps(origin), json.dumps(destination))])
        

    

    
