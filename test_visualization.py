import json
from datetime import datetime


from visualization import Visualizer


visualizer = Visualizer()


def test_load_edges():
    assert visualizer.edges == json.loads(open('edges.json').read())

def test_changes():
    assert isinstance(visualizer.latitude_change_per_pixel, float)
    assert isinstance(visualizer.longitude_change_per_pixel, float)
    left_upper_lat = visualizer.edges['left_upper']['latitude'] 
    right_lower_lat = visualizer.edges['right_lower']['latitude']
    latitude_diff = left_upper_lat-right_lower_lat
    left_upper_lon = visualizer.edges['left_upper']['latitude'] 
    right_lower_lon = visualizer.edges['right_lower']['latitude']
    longitude_diff = right_lower_lon - left_upper_lon
    shape = visualizer.base_pic.shape
    assert round(visualizer.latitude_change_per_pixel) == round(latitude_diff/shape[0])
    assert round(visualizer.longitude_change_per_pixel) == round(longitude_diff/shape[1])

def test_color_streets_with_speed():
    visualizer.color_street_with_speed(4,16,datetime(2020,3,3,15,0,0))
    visualizer.color_all_streets(datetime(2020,3,2,9,30,0))
    visualizer.show()
