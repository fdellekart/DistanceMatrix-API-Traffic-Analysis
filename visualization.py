import json
import cv2
import numpy as np
import pandas as pd
from bokeh.plotting import output_file, figure, save, show
from bokeh.models import ColumnDataSource
from datetime import datetime


from block import Block
from data import DataModifier


class Visualizer:
    def __init__(self, base_pic_path='superblock_base.jpg',
                        edges_path='edges.json',
                        responses_path='CSV\\responses\\',
                        conjuctions_path = 'CSV\\conjunctions.csv',
                        images_path = 'images\\',
                        time_series_path = 'CSV\\time_series.csv'):
        self.edges = self._load_edges(edges_path)
        self.base_pic = cv2.imread(base_pic_path)
        self.responses_path = responses_path
        self.block = Block(conjunctions_path=conjuctions_path)
        self.modifier = DataModifier()
        self.filename = None
        self.images_path = images_path
        self.time_series_path = time_series_path

    def _load_edges(self,edges_path):
        with open(edges_path, 'r') as f:
            edges = json.loads(f.read())
        return edges

    def show(self):
        cv2.imshow('image', self.base_pic)
        cv2.waitKey()

    @property
    def latitude_change_per_pixel(self):
        left_upper = self.edges['left_upper']['latitude']
        right_lower = self.edges['right_lower']['latitude']
        latitude_diff = left_upper - right_lower
        return latitude_diff/self.base_pic.shape[0]

    @property
    def longitude_change_per_pixel(self):
        left_upper = self.edges['left_upper']['longitude']
        right_lower = self.edges['right_lower']['longitude']
        longitude_diff = right_lower - left_upper
        return longitude_diff/self.base_pic.shape[1]

    def _pixel_position_with_coordinates(self, latitude, longitude):
        lat_diff = self.edges['left_upper']['latitude'] - latitude
        lon_diff = longitude - self.edges['left_upper']['longitude']

        lat_pixels = round(lat_diff/self.latitude_change_per_pixel)
        lon_pixels = round(lon_diff/self.longitude_change_per_pixel)

        return lat_pixels, lon_pixels

    def _color_coordinate(self, latitude, longitude, BGR):
        lat_pixel, lon_pixel = self._pixel_position_with_coordinates(latitude,
                                                                    longitude)
        for i in range(-3,3):
            for j in range(-3,3):
                BGR_point = self.base_pic[lat_pixel + i, lon_pixel + j]
                if BGR_point[0] >= 95 and BGR_point[1] >= 95 and BGR_point[2] >= 95:
                    try:
                        self.base_pic[lat_pixel + i, lon_pixel + j] = BGR
                    except ValueError:
                        self.base_pic[lat_pixel + i, lon_pixel + j] = np.array([0,255,0])

    def _color_street(self, id_origin, id_destination, BGR):
        origin_lat = self.block.conjunctions.at[int(id_origin), 'latitude']
        origin_lon = self.block.conjunctions.at[int(id_origin), 'longitude']
        destination_lat = self.block.conjunctions.at[int(id_destination), 'latitude']
        destination_lon = self.block.conjunctions.at[int(id_destination), 'longitude']

        lat_linspace = np.linspace(origin_lat, destination_lat, 700)
        lon_linspace = np.linspace(origin_lon, destination_lon, 700)

        for lat, lon in zip(lat_linspace, lon_linspace):
            self._color_coordinate(float(lat), float(lon), BGR)

    def _get_response_filename(self, timestamp):
        timestamp_list = [timestamp.year,
                        timestamp.month,
                        timestamp.day,
                        timestamp.hour,
                        timestamp.minute,
                        timestamp.second]
        date = '-'.join([str(x) for x in timestamp_list])
        return '{}{}.csv'.format(self.responses_path, date)

    def _get_speed_bgr(self, speed, origin_id, destination_id, distance):
        min_speed = distance/self.modifier.get_max_duration(origin_id, destination_id)
        max_speed = distance/self.modifier.get_min_duration(origin_id, destination_id)
        
        green_share = (speed - min_speed)/(max_speed - min_speed)
        red_share = 1 - green_share
        return np.array([0, 255*green_share, 255*red_share])

    def color_street_with_speed(self, origin_id, destination_id, timestamp):
        self.filename = self._get_response_filename(timestamp)
        data = pd.read_csv(self.filename, engine='python')
        origin = data['origin_id'] == origin_id
        destination = data['destination_id'] == destination_id
        duration_in_traffic = data[origin & destination]['duration_in_traffic']
        distance = data[origin & destination]['distance']
        speed = distance/duration_in_traffic
        bgr = self._get_speed_bgr(speed, origin_id, destination_id, distance)
        self._color_street(origin_id, destination_id, bgr)

    def color_all_streets(self,timestamp):
        connections = self.block.conjunctions.loc[:,'connected_right']
        for i, con in connections.iteritems():
            origin_id = i
            for destination_id in con:
                self.color_street_with_speed(int(origin_id), int(destination_id), timestamp)
                print('colored: origin: {}, destination: {}'.format(origin_id, destination_id))

    def bokeh_plot(self, street, start=None, stop=None, all=True):
        time_series = pd.read_csv(self.time_series_path)
        time_series = time_series.set_index('timestamp')
        time_series = time_series.sort_index()
        source = ColumnDataSource(time_series.loc[start:stop,:])
        colors = ['black', 'red', 'green', 'blue', 'orange']
        p = figure(x_axis_label='Timestamp',
                    y_axis_label='Duration in Traffic [s]',
                    x_axis_type='datetime'
                    )
        
        p.line(x='timestamp', y=street, source=source, name=street)

        show(p)

    def _time_series_str_to_datetime(self, string):
        list_ = string.split(' ')
        date = list_[0].split('-')
        time = list_[1].split(':')
        date = [int(x) for x in date]
        time = [int(x) for x in time]

        return datetime(year=date[0],
                        month=date[1],
                        day=date[2],
                        hour=time[0],
                        minute=time[1],
                        second=time[2]
                        )

    def save(self, filename):
        cv2.imwrite(self.images_path + filename, self.base_pic)

