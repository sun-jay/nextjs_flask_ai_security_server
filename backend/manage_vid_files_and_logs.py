import time
import pandas as pd
import os 
from wakepy import keepawake
import datetime


def manage_video_files():
    print('Updated times.csv in accordance with saved_streams at\n' +  datetime.datetime.now().strftime('%Y-%m-%d %I:%M:%S %p'))

    times_df = pd.DataFrame(columns=['start_time','end_time', 'filename'])

    files = os.listdir('saved_streams')
    i = 0

    for file in files:
        if file.endswith('.py'):
            files.remove(file)
            break

    convert = lambda x: time.mktime(time.strptime(x, '%Y%m%d%H%M%S'))

    while i < len(files):
        start_time = files[i].split('_')[1].split('.')[0]
        # start time is of the format Y%m%d%H%M%S, i need to convert to unix time
        start_time = convert(start_time)
        end_time = None

        if i != len(files) - 1:
            end_time = files[i+1].split('_')[1].split('.')[0]
            end_time = convert(end_time)
        
        times_df = times_df.append({'start_time': start_time, 'end_time': end_time, 'filename': files[i]}, ignore_index=True)
        i += 1
    # save times_df
    times_df.to_csv('times.csv', index=False)

def convert_logs_to_events():


    print('Converted logs to events at\n'+  datetime.datetime.now().strftime('%Y-%m-%d %I:%M:%S %p'))

    # open logs.csv
    logs_df = pd.read_csv('logs.csv')
    # convert logs_df to python list of tuples
    logs_list = logs_df.to_records(index=False).tolist()

    def extract_streaks_of_ones(lst, max_zeroes):
        streaks = []
        start_time = None
        streak_duration = 0

        for i, (time, num) in enumerate(lst):
            if num == 1:
                if start_time is None:
                    start_time = time
                streak_duration += 1
            elif start_time is not None and num == 0 and streak_duration <= max_zeroes:
                streak_duration += 1
            elif start_time is not None:
                streaks.append((start_time, streak_duration))
                start_time = None
                streak_duration = 0

        if start_time is not None:
            streaks.append((start_time, streak_duration))

        return streaks
    
    # extract streaks of 1s from logs_list, with 2 seconds of faulty detection tolerance
    streaks = extract_streaks_of_ones(logs_list, 1)
    # open events.csv
    events_df = pd.DataFrame(columns=['time', 'event', 'duration'])
    # append a log for each streak
    for start_time, duration in streaks:
        events_df = events_df.append({'time': start_time, 'event': "Person Detected", 'duration': duration}, ignore_index=True)

    # save logs_df
    events_df.to_csv('events.csv', index=False)
# %%

# this is not the most efficient way to do this, but it works
# the corrent way to do this would be to leverage the sorted nature of times.csv and events.csv,
# and utilize binary search to query both times_df and events_df rather than iterating through them
def del_old_vids():
    print('Deleted old videos at\n' + datetime.datetime.now().strftime('%Y-%m-%d %I:%M:%S %p'))
    times_df = pd.read_csv('times.csv')
    events = pd.read_csv('events.csv')

    # we want to select videos that start within 24 hours and/or are within 5 minutes of an event, and delete the rest
    for row in times_df.itertuples():
        start_time = row.start_time
        filename = row.filename
        # if row.end_time is not None:
        #     end_time = row.end_time
        # else:
        #     end_time = time.time()

        # if the video is within 24 hours of now, or within 5 minutes of an event, we keep it
        for event in events.itertuples():
            event_time = event.time
            if event_time - 300 <= start_time <= event_time + 300:
                break
        else:
            # if we didn't break out of the loop, then the video is not within 5 minutes of an event
            # so if this code is reached, we check if the video is within 24 hours of now
            if start_time > time.time() - 86400:
                continue
            else:
                # if this code is reached, the video is not within 24 hours of now, and not within 5 minutes of an event
                print(f'Deleting {filename}...')
                os.remove(f'saved_streams/{filename}')
                # manage_video_files() will be called in the main loop, so we don't need to update times.csv here
# %%


with keepawake(keep_screen_awake=False): 
    print('Updating times.csv in accordance with saved_streams...')
    count = 0
    while True:
        manage_video_files()
        # convert_logs_to_events()

        #this will run 5 times a day; 17280 iterations a day`` 
        if count == 17280/5:
            del_old_vids()
            count = 0
        count += 1

        # wait 15 seconds until we update times.csv again
        time.sleep(5)
