import time
import datetime
from wakepy import keepawake
import os
import signal
import subprocess


ffmpeg_command = [
    'ffmpeg',
    '-rtsp_transport', 'tcp',
    '-i', 'rtsp://admin:admin@192.168.0.29:554?tcp',
    '-c:v', 'copy',
    '-c:a', 'copy',
    '-map', '0',
    '-f', 'segment',
    '-segment_time', '60',
    '-segment_format', 'mp4',
    '-strftime', '1',
    '-reset_timestamps', '1',
    'outfile_%Y%m%d%H%M%S.mp4'
]

# Function to stop the FFmpeg process
with keepawake(keep_screen_awake=False): 
    def start_ffmpeg():
        # Start the FFmpeg process
        return subprocess.Popen(ffmpeg_command)
    def stop_ffmpeg(command):
        pid_list = subprocess.Popen('wmic process where "name=\'ffmpeg.exe\'" get ProcessId', stdout=subprocess.PIPE, shell=True).communicate()[0]
        pid_list = pid_list.decode().strip().split('\n')[1:]  # Remove header and split into lines
        for pid in pid_list:
            subprocess.Popen(f'taskkill /F /PID {pid.strip()}', shell=True).wait()
        print(command)
        if command == None:
            return
        command.terminate()

    def get_size_mp4s():
        total_size = 0

        for file in os.listdir():

            if file.endswith(".mp4"):
                total_size += os.path.getsize(file)

        return total_size

    prev_size = get_size_mp4s()
    print('\n\nprev_size',prev_size)
    command = start_ffmpeg()
    while True:
        time.sleep(20)
        curr_size = get_size_mp4s()
        print('\n\ncurr_size',curr_size)
        if curr_size <= prev_size:
            stop_ffmpeg(command)
            print('\n\n STARTING NEW FFMPEG PROCESS \n\n')
            print('time',datetime.datetime.now().strftime("%I:%M:%S %p"))
            command = start_ffmpeg()
        prev_size = curr_size

# %%
# import os
# def get_size_mp4s():
#     total_size = 0

#     for file in os.listdir():

#         if file.endswith(".mp4"):
#             total_size += os.path.getsize(file)

#     return total_size

# print(get_size_mp4s())
    #   
    # command = None
    # while F:
    #     # Stop the FFmpeg process
    #     stop_ffmpeg(command)

    #     # Start a new FFmpeg process
    #     command = start_ffmpeg()
    #     print('\n\n STARTING NEW FFMPEG PROCESS \n\n')
    #     print('time',datetime.datetime.now().strftime("%I:%M:%S %p"))
    #     # Wait for 10 minutes
    #     # time.sleep(60*30)
    #     time.sleep(10)


import os


    




