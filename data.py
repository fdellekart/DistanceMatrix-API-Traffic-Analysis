import json


class DataModifier:

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

