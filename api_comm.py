import requests
import json
from datetime import datetime


class DistanceMatrixCommunicator:
    def __init__(self, api_key_path):
        self._api_url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={},{}&destinations={},{}&departure_time={}&key={}"
        self._api_key = open(api_key_path, 'r').read()
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

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, d):
        self._destination = d	

    @property
    def request(self):
        if self._origin != None and self._destination != None:
            self._request = self._api_url.format(self._origin['latitude'],
                                                self._origin['longitude'],
                                                self._destination['latitude'],
                                                self._destination['longitude'],
                                                str(self._get_timedalte_from_zero(self._departure_time))[:-2],
                                                self._api_key
                                                )
            return self._request
        else:
            return self._request

    def get_response(self):
        self.response = requests.get(self.request)
        return self.response

    def _get_timedalte_from_zero(self, time_point):
        time_zero = datetime(1970, 1, 1, 0, 0, 0)
        time_delt = time_point - time_zero
        return time_delt.total_seconds()

    def _get_response(self):
        self._json_response = requests.get(self._request)

    @property
    def json_response(self):
        return self._json_response

    @property
    def dict_response(self):
        return json.loads(self._json_response)

    def clear(self):
        self._origin = None
        self._destination = None
        self._json_response = None
        self._request = None
        self._departure_time = None


    