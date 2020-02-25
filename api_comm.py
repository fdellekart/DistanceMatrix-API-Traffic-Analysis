import requests
import json
from datetime import datetime, timedelta


class DistanceMatrixCommunicator:
    def __init__(self, api_key=None, file_path=True):
        self._api_url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={},{}&destinations={},{}&departure_time={}&key={}"
        if file_path:
            self._api_key = open(api_key, 'r').read()
        else:
            self._api_key = api_key
        self._origin = None
        self._destination = None
        self._request = None
        self._departure_time = None
        self._json_response = None

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, o):
        self._origin = o
        self.clear()
        self._request = self.request

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, d):
        self._destination = d
        self.clear()
        self._request = self.request

    @property
    def departure_time(self):
        return self._departure_time
    
    @departure_time.setter
    def departure_time(self, dt):
        self._departure_time = dt
        self.clear()
        self._request = self.request

    @property
    def request(self):
        if self._origin != None and self._destination != None and self._departure_time != None:
            request = self._api_url.format(self._origin['latitude'],
                                                self._origin['longitude'],
                                                self._destination['latitude'],
                                                self._destination['longitude'],
                                                str(self._get_timedelta_from_zero(self._departure_time))[:-2],
                                                self._api_key
                                                )
            return request
        else:
            return None

    def _get_timedelta_from_zero(self, time_point):
        delta = time_point.date() - datetime(1970, 1, 1, 0, 0, 0).date()
        day_delta = delta.days
        delta_dict = {'days' : day_delta,
                    'hours' : time_point.hour,
                    'minutes' : time_point.minute,
                    'seconds' : time_point.second
                    }
        time_delt = timedelta(**delta_dict)
        return time_delt.total_seconds()

    def _get_response(self):
        response = self._json_response = requests.get(self._request)
        print('Performed GET request to Distance Matrix API')
        return response

    @property
    def json_response(self):
        """Returns response in json formatted string.
        """
        if self._json_response == None:
            resp = self._get_response().json()
            self._json_response = resp
            return resp
        return self._json_response

    @property
    def dict_response(self):
        """Returns response as dict.
        """
        if self._json_response == None:
            resp = self._get_response().json()
            self._json_response = resp
        return json.loads(resp.json())

    def clear(self, all=False):
        """Sets  _json_response, _request in self to None.
        Parameters:
        all=False
            _origin, _destination, _departure_time also set
            to None if True
        """
        self._json_response = None
        self._request = None
        if all:
            self._origin = None
            self._destination = None
            self._departure_time = None

    @staticmethod
    def point_adder(file_path):
        header = 'id,latitude,longitude,connected_right,connected_wrong'
        while True:
            point_id = input('id:\n')
            if point_id == 'q':
                break
            point = input('latitude,longitude:\n')
            connected_right = input('Connected point ids right direction "point,point"\n')
            connected_wrong = input('Connected pint ids wrong direction "point,point"\n')
            name = input('Name:\n')
            latitude = point.split(',')[0]
            longitude = point.split(',')[1]
            connected_right = connected_right.split(',')
            connected_wrong = connected_wrong.split(',')

            line = '{},{},{},{},{},{}\n'.format(point_id,
                                                latitude,
                                                longitude,
                                                '-'.join(connected_right),
                                                '-'.join(connected_wrong),
                                                name
                                                )

            try:
                with open(file_path, 'a') as f:
                    f.writelines([line])
            except FileNotFoundError:
                with open(file_path, 'r') as f:
                    f.writelines([header, line])

