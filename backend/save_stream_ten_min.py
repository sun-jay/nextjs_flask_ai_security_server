import cv2
import time
import pandas as pd

# initialize video capture object

side = 'rtsp://admin:admin@192.168.0.17:554'
driveway = 'rtsp://admin:admin@192.168.0.28:554' 
garage = 'rtsp://admin:admin@192.168.0.26:554' 
front_door = 'rtsp://admin:admin@192.168.0.29:554' 

cap = cv2.VideoCapture(front_door)

# initialize video writer object and other variables
file_duration_secs = 30 # 30 seconds
file_counter = 0
fourcc = cv2.VideoWriter_fourcc(*'avc1')
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = out = cv2.VideoWriter("first.mp4", fourcc, 30.0, (width, height))
# open times.csv with pandas
times_df = pd.read_csv('saved_streams/times.csv')

# loop through frames and write to file
start_time = time.time()
print('Recording and saving stream to saved_streams...')
while True:
    ret, frame = cap.read()
    if not ret:
        continue
    
    # check if it's time to start a new file
    if time.time() - start_time > file_duration_secs:
        # print readbale time
        print('Starting new file at', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        # release previous video writer object, if any
        if out !=  None:
            out.release()
        # create new video writer object for new file
        filename = f'saved_streams\\output_video~{start_time}~{time.time()}~{file_counter}.mp4'
        out = cv2.VideoWriter(filename, fourcc, 30.0, (width, height))
        file_counter += 1
        # update times.csv 
        times_df = times_df.append({'start_time': start_time, 'end_time': time.time(), 'filename': filename}, ignore_index=True)
        times_df.to_csv('saved_streams/times.csv', index=False)
        # reset start_time
        start_time = time.time()
    

    if cv2.waitKey(1) == ord('q'):
        break

    out.write(frame)

# release resources
cap.release()
out.release()
cv2.destroyAllWindows()

