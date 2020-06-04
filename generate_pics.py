import os
from datetime import datetime


from visualization import Visualizer


responses_path = "CSV\\responses\\"
images_path = "images\\"

existing_images = os.listdir(images_path)
responses = os.listdir(responses_path)

responses_timestamps = [x[:-4] for x in responses]

responses_lists = [x.split('-') for x in responses_timestamps]

responses_datetimes = [datetime(year=int(x[0]),month=int(x[1]),day=int(x[2]),hour=int(x[3]),minute=int(x[4]),second=int(x[5])) for x in responses_lists]

for dt, response in zip(responses_datetimes, responses):
    if not (response[:-4]+'.jpg' in existing_images):
        visualizer = Visualizer()
        print(response[:-4])
        visualizer.color_all_streets(dt)
        visualizer.save(response[:-4]+'.jpg')


