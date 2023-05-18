# %%
import pandas as pd
from datetime import datetime


times_df = pd.read_csv('../backend/times.csv')
# print(times_df.head())
convert = lambda x: time.mktime(time.strptime(x, '%Y%m%d%H%M%S'))

# convert times_df to python list of tuples
times_list = times_df.to_records(index=False).tolist()

for start,end,f in times_list:
    # convert unix timestamps to datetime objects
    start = datetime.fromtimestamp(start)
    try:
        end = datetime.fromtimestamp(end)
    except:
        pass

    # if start is less then now minus 12 hours, skip
    # if start < datetime.now() - pd.Timedelta(hours=12):
    #     continue

    # prin the date in 12 h time
    start = start.strftime('%Y-%m-%d %I:%M:%S %p')
    # end = end.strftime('%Y%m%d%H%M%S')

    print('start:', start, 'end:', end)


# %%

# !!!!!! WARNING !!!!!!
# THIS WILL DELETE ALL FILES IN ../backend/saved_streams EXCEPT times.csv !!!!!!

input('are you sure you want to delete all files in ../backend/saved_streams except times.csv? press enter to continue...')

import pandas as pd

import os
# delete all files in ../backend/saved_streams exepct times.csv
for f in os.listdir('../backend/saved_streams'):
    if f.endswith('.mp4'):
        os.remove(f'../backend/saved_streams/{f}')
# reset times.csv to empty dataframe with columns: start_time, end_time, filename
times_df = pd.DataFrame(columns=['start_time', 'end_time', 'filename'])
times_df.to_csv('../backend/saved_streams/times.csv', index=False)
# 


# %%
# record 5 seconds of stream and save to file


import time
import cv2
import os
# save 10 seconds of video to a file
front_door = 'rtsp://admin:admin@192.168.0.29:554' 

cap = cv2.VideoCapture(front_door)
fourcc = cv2.VideoWriter_fourcc(*'avc1')
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
filename = 'test_copy.mp4'

out = cv2.VideoWriter(filename, fourcc, 30.0, (width, height))
start_time = time.time()
while time.time() - start_time < 5:
    ret, frame = cap.read()
    if not ret:
        continue
    out.write(frame)
cap.release()
out.release()
# os.system(f'docker cp c2ddaf03daa7:/app/{filename}.mp4 /Users/sunnyjay/Documents/vscode/ffmpeg-docker/{filename}.mp4')
cv2.destroyAllWindows()


