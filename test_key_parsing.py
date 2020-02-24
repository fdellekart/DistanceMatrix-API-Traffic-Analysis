from api_comm import DistanceMatrixCommunicator

communicator = DistanceMatrixCommunicator('somerandomkey', file_path=False)

def test_key_parsing():
    assert communicator._api_key == 'somerandomkey'