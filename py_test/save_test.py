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
while time.time() - start_time < 30:
    ret, frame = cap.read()
    if not ret:
        continue
    out.write(frame)
cap.release()
out.release()
# os.system(f'docker cp c2ddaf03daa7:/app/{filename}.mp4 /Users/sunnyjay/Documents/vscode/ffmpeg-docker/{filename}.mp4')
cv2.destroyAllWindows()