from bokeh.plotting import output_file, figure, show, save
from bokeh.models import ColumnDataSource
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd

series = pd.read_csv('CSV\\time_series_duration.csv')

series.timestamp = pd.to_datetime(series.timestamp)
series.set_index('timestamp', inplace=True)
series = series.sort_index()
series = series.loc['2020-3-3 04:00:00':'2020-3-3 22:30:00', :]

response = pd.read_csv('CSV\\responses\\2020-3-3-5-0-0.csv', engine='python')

index = pd.MultiIndex.from_frame(response.loc[:,['origin_id','destination_id']])

response.drop(['origin_id', 'destination_id'], axis=1, inplace=True)

response.index = index


distance1 = response.loc[(1, 2), 'distance'] + response.loc[(2, 3), 'distance']
distance2 = distance1 + response.loc[(3, 4), 'distance'] + response.loc[(4, 5), 'distance'] + response.loc[(5, 6), 'distance']
muenzgraben = 3.6*distance1/(series.loc[:,'1-2'] + series.loc[:,'2-3'])# + series.loc[:,'3-4'] + series.loc[:,'4-5'] + series.loc[:,'5-6'])
muenzgraben_reverse = 3.6*distance2/(series.loc[:,'1-2'] + series.loc[:,'2-3'] + series.loc[:,'3-4'] + series.loc[:,'4-5'] + series.loc[:,'5-6'])
series['muenzgraben'] = muenzgraben
series['reverse'] = muenzgraben_reverse
source = ColumnDataSource(series)
print(series.info())

p = figure(x_axis_label='Timestamp',
            y_axis_label='Traffic Speed [km/h]',
            x_axis_type='datetime',
            title='Grazbachgasse, 3.3.2020'
            )

p.line(x='timestamp', y='muenzgraben', source=source, legend_label='Grazbachgasse ohne Dietrichsteinplatz')
p.line(x='timestamp', y='reverse', source=source, legend_label='Grazbachgasse mit Dietrichsteinplatz', color='red')

show(p)

# sns.set()

# sns.pairplot(series.loc[:,['30-27', '28-24', '27-26', '24-25']])

# plt.show()