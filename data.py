import json
import os
from datetime import datetime


import numpy as np
import pandas as pd


import block
import api_comm
import block


class DataModifier:
    def __init__(self, todo_path=r'CSV\departures_todo.csv', 
                done_path=r'CSV\departures_done.csv',
                conjunctions_path=r'CSV\conjunctions.csv'):
        self.todo_path = todo_path
        self.done_path = done_path
        self.conjunctions_path = conjunctions_path
        self.todos = None
        self.done = None
        self.trip_data = pd.DataFrame(columns=['origin',
                                        'destination',
                                        'departure_time',
                                        'distance',
                                        'time_in_traffic'
                                        ])
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
        """sets done to todos and todos to empty list
        writes done to done_path and empties todo_path
        """
        for todo in self.todos:
            self.done.append(todo)
        self.todos = []
        print('todos in done:{}'.format(self.todos))
        print('done in done:{}'.format(self.done))
        self._write_done_and_todos()
        with open(self.todo_path, 'w') as f:
            f.write('')
        self.load_todos_and_done()

    def _write_done_and_todos(self):
        todo_json_list = [json.dumps(todo) for todo in self.todos]
        done_json_list = [json.dumps(todo) for todo in self.done]
        todo_string = '\n'.join(todo_json_list)
        done_string = '\n'.join(done_json_list)
        with open(self.todo_path, 'w') as f:
            f.write(todo_string)
        
        with open(self.done_path, 'w') as f:
            f.write(done_string)

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

    def get_data(self):
        superblock = block.Block()
        for todo in self.todos:
            todo_dt = datetime(todo['year'],
                                todo['month'],
                                todo['day'],
                                todo['hour'],
                                todo['minute'],
                                todo['second']
                                )
            todo_file_path = self._todo_filename(todo_dt)
            self._write_response_csv_header(todo_file_path)
            for origin_id in superblock.conjunctions.index:
                for destination_id in superblock.conjunctions.at[origin_id, 'connected_right']:
                    dict_response = self._get_data_one_point(int(origin_id),
                                                            int(destination_id),
                                                            todo_dt,
                                                            superblock)
                    dict_response_unpacked = self._unpack_api_response(dict_response)
                    csv_line = self._generate_response_csv_line(dict_response_unpacked,
                                                                origin_id,
                                                                destination_id
                                                                )
                    self._write_response(csv_line, todo_file_path)
        self.is_done()

    def _write_response(self, csv_line, file_path):
        with open(file_path, 'a') as f:
            f.write(csv_line)

    def _generate_response_csv_line(self, dict_response, origin_id, destination_id):
        info_list = [origin_id,
                    destination_id,
                    dict_response['origin_adress'],
                    dict_response['destination_adress'],
                    dict_response['distance'],
                    dict_response['duration'],
                    dict_response['duration_in_traffic']
                    ]
        return '\n' + ','.join([str(x) for x in info_list])

    def _write_response_csv_header(self, file_path):
        header = 'origin_id,destination_id,origin_adress,destination_adress,distance,duration,duration_in_traffic'
        with open(file_path, 'w') as f:
            f.write(header)

    def _get_data_one_point(self, origin_id, destination_id, todo_dt, conj_block):
        communicator = api_comm.DistanceMatrixCommunicator('google_api_key.txt')

        origin_lat = conj_block.conjunctions.at[origin_id, 'latitude']
        origin_lon = conj_block.conjunctions.at[origin_id, 'longitude']
        destination_lat = conj_block.conjunctions.at[destination_id, 'latitude']
        destination_lon = conj_block.conjunctions.at[destination_id, 'longitude']

        origin = {'latitude' : origin_lat, 'longitude' : origin_lon}
        destination = {'latitude' : destination_lat, 'longitude': destination_lon}

        communicator.origin = origin
        communicator.destination = destination
        communicator.departure_time = todo_dt

        return communicator.dict_response

    #{'destination_addresses': ['Grazbachgasse 34, 8010 Graz, Austria'],
    # 'origin_addresses': ['Grazbachgasse 40, 8010 Graz, Austria'],
    # 'rows': [{'elements': [{'distance': {'text': '80 m', 'value': 80},
    #                           'duration': {'text': '1 min', 'value': 14},
    #                           'duration_in_traffic': {'text': '1 min', 'value': 13},
    #                            'status': 'OK'}]}], 'status': 'OK'}

    def _unpack_api_response(self, dict_response):
        print(dict_response)
        destination_adress = dict_response['destination_addresses'][0]
        origin_adress = dict_response['origin_addresses'][0]
        info = dict_response['rows'][0]['elements'][0]
        distance = info['distance']['value']
        duration = info['duration']['value']
        duration_in_traffic = info['duration_in_traffic']['value']

        return {'destination_adress' : destination_adress,
                'origin_adress' : origin_adress,
                'distance' : distance,
                'duration' : duration,
                'duration_in_traffic' : duration_in_traffic
                }

    def _todo_filename(self, todo_dt):
        name = '-'.join([str(x) for x in [todo_dt.year,
                        todo_dt.month,
                        todo_dt.day,
                        todo_dt.hour,
                        todo_dt.minute,
                        todo_dt.second
                        ]])
        return 'CSV\\responses\\' + name + '.csv'
