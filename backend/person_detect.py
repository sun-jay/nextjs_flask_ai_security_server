import cv2
import mediapipe as mp
import time
import datetime
import pandas as pd


# RTSP stream URL
rtsp_url = 'rtsp://admin:admin@192.168.0.29:554?tcp'
# Create the MediaPipe Pose Estimator
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.9, model_complexity=0)


def detect_pose():
    # Create a VideoCapture object
    cap = cv2.VideoCapture(rtsp_url)
    # Check if the VideoCapture object was successfully initialized
    if not cap.isOpened():
        print("Failed to open the RTSP stream.")
        return None
    # Read one frame from the stream
    ret, frame = cap.read()
    # Check if the frame was successfully read
    if not ret:
        print("Failed to grab frame from the stream.")
        return None
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
# open logs.csv

# while True:
#     logs = pd.read_csv('logs.csv')
#     output = detect_pose()

#     if output != 'err' and output is not None:
#         print('!!!PERSON DETECTED!!!', 'time', datetime.datetime.now().strftime("%I:%M:%S %p"))
#         logs = logs.append({'time': time.time(), 'person': 1}, ignore_index=True)
#     elif output != 'err':
#         print('NO PERSON DETECTED', 'time', datetime.datetime.now().strftime("%I:%M:%S %p"))
#         logs = logs.append({'time': time.time(), 'person': 0}, ignore_index=True)

#     logs.to_csv('logs.csv', index=False)

#     time.sleep(1)



# i think we want to remake this, rather than printing out all the logs and then converting it to events,
# we should make it so we write events directly
# to do this, we will have to keep a buffer of the last minute of logs, and then write any events that occur
# to the events.csv file.
# we have to make sure that were not writing the same event over and over again, so we should keep a list of
# events that have already been written, and then check if the event has already been written before writing it
# each event should have a duration, so we should keep track of the start time of the event, and then when the
# event ends, we can calculate the duration and write it to the events.csv file
# lets start by making a function that takes in a list of logs, and then returns a list of events


# actually, what if we made it so if theres a streak of person detected, we start writing a buffer of logs
# this buffer is stored locally in ram as we want to get rid of the need for a logs.csv file
# then, when the person is no longer detected, we write the start and end time of the buffer to the events.csv file
# remember, we need to include a "falt tolerance" of 4 iterations, so if the person is detected, and then not detected
# for 4 iterations, we want to continue writing the same buffer rather than starting a new one
# code:

buffer = []
while True:
    events = pd.read_csv('events.csv')
    # the only time any code is executed in this loop is when the buffer is empty, or when there is a person detected
    if buffer:

        if detect_pose() != None :
            buffer.append({'time': time.time(), 'person': 1})
        else:
            buffer.append({'time': time.time(), 'person': 0})
        
        # if the last 4 iterations of the buffer are 0, write the buffer to the events.csv file
        if buffer[-1]['person'] == 0 and buffer[-2]['person'] == 0 and buffer[-3]['person'] == 0 and buffer[-4]['person'] == 0:
            events = events.append({'time': buffer[0]['time'], 'event': 'person detected', 'duration': buffer[-4]['time'] - buffer[0]['time']}, ignore_index=True)
            events.to_csv('events.csv', index=False)
            buffer = []
            print('event detected and ended, writing to events.csv')
    else:
        if detect_pose():
            buffer.append({'time': time.time(), 'person': 1})

    time.sleep(1)

    


# Release the resources
pose.close()
cv2.destroyAllWindows()
