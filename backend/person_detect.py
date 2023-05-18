import cv2
import mediapipe as mp
import time
import datetime

# RTSP stream URL
rtsp_url = 'rtsp://admin:admin@192.168.0.29:554?tcp'
# Create the MediaPipe Pose Estimator
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.7, model_complexity=0)


def detect_pose():
    # Create a VideoCapture object
    cap = cv2.VideoCapture(rtsp_url)
    # Check if the VideoCapture object was successfully initialized
    if not cap.isOpened():
        print("Failed to open the RTSP stream.")
        return "err"
    # Read one frame from the stream
    ret, frame = cap.read()
    # Check if the frame was successfully read
    if not ret:
        print("Failed to grab frame from the stream.")
        return "err"
    # resize the frame to fit the screen
    # frame = cv2.resize(frame, ((int(1920*(2/3)), int(1080*(2/3)))))
    # Load the grabbed image
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Process the image with the Pose Estimator
    results = pose.process(image)
    # # Draw the pose landmarks on the image
    # mp_drawing = mp.solutions.drawing_utils
    # annotated_image = image.copy()
    # mp_drawing.draw_landmarks(annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    # # Convert the image back to BGR format
    # annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
    # # Display the annotated image
    # cv2.imshow("Pose Estimation", annotated_image)
    # # Wait for keypress to exit
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    return results.pose_landmarks

# Call the function to display the webcam feed
import pandas as pd
# open logs.csv
logs = pd.read_csv('logs.csv')

while True:
    logs = pd.read_csv('logs.csv')
    output = detect_pose()

    if output != 'err' and output is not None:
        print('!!!PERSON DETECTED!!!', 'time', datetime.datetime.now().strftime("%I:%M:%S %p"))
        logs = logs.append({'time': time.time(), 'person': 1}, ignore_index=True)
    elif output != 'err':
        print('NO PERSON DETECTED', 'time', datetime.datetime.now().strftime("%I:%M:%S %p"))
        logs = logs.append({'time': time.time(), 'person': 0}, ignore_index=True)

    logs.to_csv('logs.csv', index=False)

    time.sleep(1)


# Release the resources
pose.close()
cv2.destroyAllWindows()
