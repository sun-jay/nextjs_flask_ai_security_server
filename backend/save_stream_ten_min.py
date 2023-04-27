import cv2
import time
import pandas as pd

# initialize video capture object
cap = cv2.VideoCapture(0)

# initialize video writer object and other variables
file_duration_secs = 10  # 10 seconds in this example
file_counter = 0
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 25.0, (640, 480))

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
        # release previous video writer object, if any
        if out is not None:
            out.release()
        # create new video writer object for new file
        filename = f'saved_streams/output_video~{start_time}~{time.time()}~{file_counter}.mp4'
        out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))
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

