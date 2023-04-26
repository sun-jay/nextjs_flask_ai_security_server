
import mediapipe as mp
from flask import Flask, Response
import cv2
import threading
import base64
from flask import Flask, send_file
from flask_sse import sse

app = Flask(__name__)
app.config['REDIS_URL'] = 'redis://localhost:6379'
app.register_blueprint(sse, url_prefix='/stream')


# initialize a lock used to ensure thread-safe
# exchanges of the frames (useful for multiple browsers/tabs
# are viewing tthe stream)
lock = threading.Lock()


@app.route('/stream1', methods=['GET'])
def stream1():
    return Response(generate('rtsp://admin:admin@192.168.0.17:554'), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route('/stream2', methods=['GET'])
def stream2():
    return Response(generate('rtsp://admin:admin@192.168.0.28:554'), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route('/stream3', methods=['GET'])
def stream3():
    return Response(generate('rtsp://admin:admin@192.168.0.26:554'), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route('/stream4', methods=['GET'])
def stream4():
    return Response(person_detect('rtsp://admin:admin@192.168.0.29:554'), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route('/test', methods=['GET'])
def test():
    response_body = {
        "name": "Nagato",
        "about": "Hello! I'm a full stack developer that loves python and javascript"
    }
    return response_body

@app.route('/video')
def video():
    filename = 'Title@2022-10-23@02-29-38.mp4'
    return send_file(filename, as_attachment=True)



mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


def person_detect(url):
    # grab global references to the lock variable
    global lock
    # initialize the video stream
    vc = cv2.VideoCapture(url)

    # check camera is open
    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False

    # while streaming
    count = 0 
    while rval:
        # wait until the lock is acquired
        with lock:
            # read next frame
            rval, frame = vc.read()
            # if blank frame
            if frame is None:
                continue

            if count %10 == 0:
                with mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.5) as pose:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame.flags.writeable = False
                    results = pose.process(frame)
                    frame.flags.writeable = True
                    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(
                                        color=(0, 0, 0), thickness=2, circle_radius=4),
                                    mp_drawing.DrawingSpec(color=(245, 245, 245), thickness=2, circle_radius=4))
            count += 1


        (flag, encodedImage) = cv2.imencode(".jpg", frame)

        # ensure the frame was successfully encoded
        if not flag:
            continue

        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
    # release the camera
    vc.release()

def generate(url):
    # grab global references to the lock variable
    global lock
    # initialize the video stream
    vc = cv2.VideoCapture(url)

    # check camera is open
    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False

    # while streaming
    while rval:
        # wait until the lock is acquired
        with lock:
            # read next frame
            rval, frame = vc.read()
            # if blank frame
            if frame is None:
                continue

            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", frame)

            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')
    # release the camera
    vc.release()

def generate_video():
    video_file = cv2.VideoCapture(0)
    while True:
        ret, frame = video_file.read()
        if not ret:
            break
        # Encode the frame as a binary JPEG image
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        # Send the frame as a binary SSE event
        yield f'data: {frame}\n\n'

if __name__ == '__main__':
    app.run(debug=True)
