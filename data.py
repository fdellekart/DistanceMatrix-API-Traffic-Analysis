import json
from datetime import datetime


import numpy as np


import block
import api_comm


class DataModifier:
    def __init__(self, todo_path=r'CSV\departures_todo.csv', done_path=r'CSV\departures_done.csv'):
        self.todo_path = todo_path
        self.done_path = done_path
        self.todos = None
        self.done = None
        self.load_todos()

    @staticmethod
    def add_point(point_id, latitude, longitude, conn_rightway, conn_wrongway, name, file_path=r'CSV\conjunctions.csv'):
        header = 'id,latitude,longitude,connected_right,connected_wrong\n'
        line = '{},{},{},{},{},{}\n'.format(point_id,
                                            latitude,
                                            longitude,
                                            '-'.join(conn_rightway),
                                            '-'.join(conn_wrongway),
                                            name
                                            )

        try:
            with open(file_path, 'a') as f:
                f.writelines([line])
        except IOError:
            with open(file_path, 'r') as f:
                f.writelines([header, line])

    @staticmethod
    def add_todo(year, month, day, hour, minute, second, file_path=r'CSV\departures_todo.csv'):
        todo_dict = {'year' : year,
                    'month' : month,
                    'day' : day,
                    'hour' : hour,
                    'minute' : minute,
                    'second' : second}

        todo_json = json.dumps(todo_dict)

        with open(file_path, 'a') as f:
            f.writelines(['{}\n'.format(todo_json)])

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
                    
        self.write_done()

    def load_todos(self):
        with open(self.todo_path, 'r') as f:
            todos = f.read()
        self.todos = todos.split('\n')

        with open(self.done_path, 'r') as f:
            todos = f.read()
        self.done = todos.split('\n')

    def write_done(self):
        with open(self.done_path, 'a') as f:
            string = '\n'.join(self.done)
            f.write('{}\n'.format(string))
        self.todos = None
        with open(self.todo_path, 'w') as f:
            f.write('')
