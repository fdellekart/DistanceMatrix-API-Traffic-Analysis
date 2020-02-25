import data


class Interface:

    @staticmethod
    def add_point():
        while True:
            print('Enter point information, enter "q" for id to quit')
            p_id = input('id:\n')
            if p_id == 'q':
                break
            point = input('latitude,longitude:\n')
            connected_right = input('Connected point ids right direction "point,point"\n')
            connected_wrong = input('Connected pint ids wrong direction "point,point"\n')
            name = input('Name:\n')
            
            lat = point.split(',')[0]
            lon = point.split(',')[1]
            connected_right = connected_right.split(',')
            connected_wrong = connected_wrong.split(',')

            data.DataModifier.add_point(p_id,
                                        lat,
                                        lon,
                                        connected_right,
                                        connected_wrong,
                                        name
                                        )

    @staticmethod
    def add_todo():
        while True:
            print('Write departure time information, to quit type "q" for year')
            year = input('Year:')
            if year == 'q':
                break
            month = input('Month:')
            day = input('Day:')
            hour = input('Hour:')
            minute = input('Minute:')
            second = input('Second:')

            todo_dict = {'year' : year,
                        'month' : month,
                        'day' : day,
                        'hour' : hour,
                        'minute' : minute,
                        'second' : second}

            data.DataModifier.add_todo(**todo_dict)

    @staticmethod
    def work_todos():
        modifier = data.DataModifier()
        modifier.work_todos()