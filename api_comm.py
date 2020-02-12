
#units=imperial&origins=Washington,DC&destinations=New+York+City,NY&key=YOUR_API_KEY

origin = {"latitude": "47.066502", "longitude": "15.438346"}
destination = {"latitude": "47.063286", "longitude": "15.450824"}

class APICommunicator:
    def __init__(self, api_key_path):
        self.api_url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
        self.api_key = open(api_key_path, 'r').read()
