import os
import datetime
import time
import pandas as pd


for file in os.listdir('saved_streams'):
    if file.endswith('.mp4'):
        os.remove(f'saved_streams/{file}')

times_df = pd.DataFrame(columns=['start_time', 'end_time', 'filename'])
times_df.to_csv('times.csv', index=False)

logs_df = pd.DataFrame(columns=['time', 'person'])
logs_df.to_csv('logs.csv', index=False)

events_df = pd.DataFrame(columns=['time','event', 'duration'])
events_df.to_csv('events.csv', index=False)

print('Cleared files at\n' + datetime.datetime.now().strftime('%Y-%m-%d %I:%M:%S %p'))