#!/usr/bin/env python3

from flask import Flask, Response, render_template_string
import cv2
import argparse
import threading
import time
import copy
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Argument parser setup
parser = argparse.ArgumentParser(description="Video stream server.")
parser.add_argument("--device", type=int, default=0, help="Video device number (e.g., 0). Use 'v4l2-ctl --list-devices' to list all devices.")
args = parser.parse_args()

app = Flask(__name__)

# Lock for thread-safe frame updates
frame_lock = threading.Lock()
latest_frame = None

def capture_frames(device_id):
    global latest_frame
    cap = cv2.VideoCapture(device_id)
    if not cap.isOpened():
        logging.error(f"Could not open video device {device_id}")
        return
    
    while True:
        success, frame = cap.read()
        if not success:
            logging.warning("Failed to read frame from camera")
            break
        height = frame.shape[0]
        frame = frame[:height // 2, :]

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        with frame_lock:
            latest_frame = frame_bytes

    cap.release()

def generate_frames():
    global latest_frame
    while True:
        with frame_lock:
            while latest_frame is None:
                time.sleep(0.1)  # wait for the first frame
            frame_copy = copy.deepcopy(latest_frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_copy + b'\r\n')
        time.sleep(0.1)  # reduce CPU usage

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Video Stream</title>
    <style>
        body, html {
            height: 100%;
            margin: 0;
            padding: 0;
            background-color: black; /* Set background to black */
            display: flex;
            align-items: center; /* Center vertically */
            justify-content: center; /* Center horizontally */
            overflow: hidden; /* Prevents scroll bars */
        }
        img {
            width: 100vw;  /* 100% of the viewport width */
            height: 100vh; /* 100% of the viewport height */
            object-fit: contain; /* Ensures the image is fully visible */
        }
    </style>
</head>
<body>
    <img src="{{ url_for('video_feed') }}">
</body>
</html>
    ''')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    threading.Thread(target=capture_frames, args=(args.device,), daemon=True).start()
    app.run(host='0.0.0.0', port=5001, threaded=True)
