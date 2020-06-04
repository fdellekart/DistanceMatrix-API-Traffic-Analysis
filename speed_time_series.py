import pandas as pd

duration_df = pd.read_csv('CSV\\time_series_duration.csv')

response = pd.read_csv('CSV\\responses\\2020-3-3-5-0-0.csv', engine='python')

index = pd.MultiIndex.from_frame(response.loc[:,['origin_id','destination_id']])

response.drop(['origin_id', 'destination_id'], axis=1, inplace=True)

response.index = index

print(duration_df)

for connection in duration_df.columns:
    if connection == 'timestamp':
        continue
    tuple_ = tuple(connection.split('-'))
    tuple_ = (int(tuple_[0]), int(tuple_[1]))

    distance = response.at[tuple_, 'distance']

    duration_df[connection] = (1/duration_df.loc[:,connection])*distance

duration_df.set_index('timestamp', inplace=True)
duration_df.to_csv('CSV\\time_series_speed.csv')