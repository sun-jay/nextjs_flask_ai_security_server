# %%
import pandas as pd
from datetime import datetime

times_df = pd.read_csv('../backend/saved_streams/times.csv')
# print(times_df.head())

# convert times_df to python list of tuples
times_list = times_df.to_records(index=False).tolist()

for start,end,f in times_list:
    # convert unix timestamps to datetime objects
    start = datetime.fromtimestamp(start)
    end = datetime.fromtimestamp(end)

    # if start is less then now minus 12 hours, skip
    if start < datetime.now() - pd.Timedelta(hours=12):
        continue

    # convert datetime objects to strings of am/pm time (12 hour clock, not 24 hour)
    start = start.strftime("%I:%M:%S %p")
    end = end.strftime("%I:%M:%S %p")

    print('start:', start, 'end:', end)


# %%
import cv2

build_info = cv2.getBuildInformation()

print(build_info)
