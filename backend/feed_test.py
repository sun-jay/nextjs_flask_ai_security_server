import cv2

def display_webcam_feed():
    # Create a VideoCapture object for the webcam
    cap = cv2.VideoCapture('rtsp://admin:admin@192.168.0.29:554?tcp')

    # Check if the VideoCapture object was successfully initialized
    if not cap.isOpened():
        print("Failed to open the webcam.")
        return

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()

        # Check if the frame was successfully read
        if not ret:
            print("Failed to read frame from the webcam.")
            break

        # Display the frame in a window named "Webcam Feed"
        cv2.imshow("Webcam Feed", frame)

        # Break the loop when the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the VideoCapture object and close the window
    cap.release()
    cv2.destroyAllWindows()

# Call the function to display the webcam feed
display_webcam_feed()
