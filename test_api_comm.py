from datetime import datetime, timedelta


from api_comm import DistanceMatrixCommunicator


communicator = DistanceMatrixCommunicator("google_api_key.txt")

origin = {"latitude": "47.066502", "longitude": "15.438346"}
destination = {"latitude": "47.063286", "longitude": "15.450824"}
departure_time = datetime(2020, 2, 24, 12, 36)

def test_init():
    assert isinstance(communicator._api_key, str)
    assert communicator._api_key[-1] != "\n"
    assert isinstance(communicator._api_url, str)
    assert communicator.origin == None
    assert communicator.destination == None
    assert communicator.request == None
    assert communicator._departure_time == None
    assert communicator._json_response == None


def test_getters_setters():
    communicator.origin = origin
    communicator.destination = destination
    communicator.departure_time = departure_time

    assert communicator.origin == origin
    assert communicator.destination == destination
    assert communicator.departure_time == departure_time
    assert communicator._origin == origin
    assert communicator._destination == destination
    assert communicator._departure_time == departure_time

def test_timedelta():
    departure_time
    delta_sec = communicator._get_timedelta_from_zero(departure_time)
    delta = timedelta(seconds=delta_sec)
    new_dt = datetime(1970, 1, 1, 0, 0, 0) + delta
    assert new_dt == departure_time

def test_request():
    api_url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={},{}&destinations={},{}&departure_time={}&key={}"
    assert communicator.request == api_url.format(origin['latitude'],
                                                origin['longitude'],
                                                destination['latitude'],
                                                destination['longitude'],
                                                str(communicator._get_timedelta_from_zero(departure_time))[:-2],
                                                communicator._api_key
                                                )

def test_clear():
    communicator.clear(all=True)
    assert communicator.departure_time == None
    assert communicator.origin == None
    assert communicator.destination == None
    assert communicator.request == None
    assert communicator._json_response == None