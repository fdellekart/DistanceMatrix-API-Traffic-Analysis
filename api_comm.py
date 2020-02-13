import requests
import json


class DistanceMatrixCommunicator:
    def __init__(self, api_key_path):
        self._api_url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={}&destinations={}&key={}"
        self._api_key = open(api_key_path, 'r').read()
        self._origin = None
        self._destination = None
        self._request = None

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
            self._request = self._api_url.format(self._origin, 
                                                self._destination,
                                                self._api_key
                                                )
            return self._request
        else:
            return self._request

    def get_response(self):
        self.response = requests.get(self.request)
        return self.response