import os
from datetime import datetime


import pandas as pd


from block import Block


def response_filename_to_datetime(filename):
    name_list = [int(x) for x in filename[:-4].split('-')]

    return datetime(year=name_list[0],
                    month=name_list[1],
                    day=name_list[2],
                    hour=name_list[3],
                    minute=name_list[4],
                    second=name_list[5]
                    )


superblock = Block()

responses_path = "CSV\\responses\\"

columns = ['timestamp',]

for row in superblock.conjunctions.iterrows():
    for dest in row[1]['connected_right']:
        connection_string = '-'.join([str(row[0]), str(dest)])
        columns.append(connection_string)

responses_files = os.listdir(responses_path)


time_series_df = pd.DataFrame(columns=columns)
time_series_df.set_index('timestamp')



for filename in responses_files:
    timestamp = response_filename_to_datetime(filename)
    resp_csv = pd.read_csv(responses_path + filename, engine='python')
    duration_list = [timestamp,]
    for row in resp_csv.iterrows():
        origin_id = row[1]['origin_id']
        destination_id = row[1]['destination_id']
        duration = row[1]['duration_in_traffic']
        key = '-'.join([str(origin_id), str(destination_id)])
        duration_list.append(duration)
    row_df = pd.DataFrame(data=[duration_list], columns=columns)
    time_series_df = time_series_df.append(row_df)
    print(row_df)

time_series_df = time_series_df.set_index('timestamp')
time_series_df.to_csv('CSV\\time_series.csv')