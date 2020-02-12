from api_comm import APICommunicator

communicator = APICommunicator("google_api_key.txt")

def test_init():
    assert isinstance(communicator.api_key, str)
    assert communicator.api_key[-1] != "\n"
    assert isinstance(communicator.api_url, str)