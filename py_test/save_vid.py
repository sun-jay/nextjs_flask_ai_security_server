# save webcam video to file using opencv
import cv2
fourcc = cv2.VideoWriter_fourcc(*'H264')

cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (width, height))
while True:
    ret, frame = cap.read()
    if not ret:
        continue
    out.write(frame)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
out.release()
cv2.destroyAllWindows()
