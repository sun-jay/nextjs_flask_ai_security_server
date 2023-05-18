
import mediapipe as mp
from flask import Flask, Response, request
import cv2
import threading
import base64
from flask import Flask, send_file
from flask_sse import sse
from imutils.video import VideoStream
import pandas as pd
from datetime import datetime, timedelta
import sys
from flask_cors import CORS


app = Flask(__name__)
app.config['REDIS_URL'] = 'redis://localhost:6379'
app.register_blueprint(sse, url_prefix='/stream')
CORS(app)

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
    return Response(gen_with_VideoStream('rtsp://admin:admin@192.168.0.29:554'), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route('/test', methods=['GET'])
def test():
    response_body = {
        "name": "Nagato",
        "about": "Hello! I'm a full stack developer that loves python and javascript"
    }
    return response_body


    
@app.route('/video')
def video():
    times = pd.read_csv('times.csv')
    unix_timestamp = request.args.get('time')

    # if the unix_timestamp greater than the greatest end_time in the times.csv, return an http response with a 404 status code
    if float(unix_timestamp) > times['end_time'].max():
        return "Requested time is too early, please wait", 404

    # print the unix_timestamp in 12 hour time readable format
    print(datetime.fromtimestamp(float(unix_timestamp)).strftime("%I:%M:%S %p"), file=sys.stderr)
    # print(unix_timestamp, file=sys.stderr)

    # filter the dataframe to only include rows that have a start_time
    # that is less than the unix_timestamp and an end_time that is greater
    # than the unix_timestamp
    filtered_df = times[(times['start_time'] <= float(unix_timestamp)) & (times['end_time'] >= float(unix_timestamp))]

    filenames = filtered_df['filename'].tolist()
    response = send_file("saved_streams/"+filenames[0], as_attachment=True)
    response.headers['Content-Disposition'] = filtered_df['start_time'].tolist()[0]
    print(filenames[0], file=sys.stderr)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
    return response

@app.route('/events')
def events():
    events_df = pd.read_csv('events.csv')
    events_arr = events_df.to_dict('records')
    return events_arr

def gen_with_VideoStream(url):
    vc = VideoStream(url).start()
    while True:
        frame = vc.read()
        if frame is None:
            continue
        # Encode the frame as a binary JPEG image
        frame = cv2.imencode('.jpg', frame)[1].tobytes()
        # yield the output frame in the byte format
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(frame) + b'\r\n')

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


if __name__ == '__main__':
    app.run(host="192.168.1.101",port="5000", debug=True)
