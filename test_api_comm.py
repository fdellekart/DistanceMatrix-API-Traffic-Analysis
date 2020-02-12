from api_comm import DistanceMatrixCommunicator

communicator = DistanceMatrixCommunicator("google_api_key.txt")

def test_init():
    assert isinstance(communicator._api_key, str)
    assert communicator._api_key[-1] != "\n"
    assert isinstance(communicator._api_url, str)
    assert communicator.origin == None
    assert communicator.destination == None
    assert communicator.request == None

def test_getters_setters():
    communicator.origin = "origin"
    communicator.destination = "destination"

    assert communicator.request == communicator._api_url.format("origin",
                                                                "destination",
                                                                communicator._api_key
                                                                )