#!/usr/bin/env python3

from flask import Flask, Response, render_template_string
import cv2
import argparse
import threading
import time
import copy
import logging
import numpy as np
import textwrap

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

def generate_error_image(message):
    if not message:
        message = "An unknown error occurred"

    image = np.zeros((192, 256, 3), dtype=np.uint8)  # create a black image
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.5
    font_thickness = 1
    text_color = (255, 255, 255)

    # calculate the width of a character
    char_size, _ = cv2.getTextSize('a', font, font_scale, font_thickness)
    char_width = char_size[0]

    # calculate the maximum number of characters that can fit in the image
    max_chars = image.shape[1] // char_width

    # wrap the text
    wrapped_text = textwrap.wrap(message, width=max_chars)

    if not wrapped_text:  # if the message is too long to fit in the image
        font_scale = 0.4  # reduce the font size
        wrapped_text = textwrap.wrap(message, width=max_chars)

    line_height = char_size[1] + 5  # 5 pixels for spacing between lines
    y = image.shape[0] // 2 - (line_height * len(wrapped_text)) // 2  # start drawing at this height

    for line in wrapped_text:
        text_size, _ = cv2.getTextSize(line, font, font_scale, font_thickness)
        line_x = (image.shape[1] - text_size[0]) // 2  # center the line
        cv2.putText(image, line, (line_x, y), font, font_scale, text_color, font_thickness, cv2.LINE_AA)
        y += line_height  # move to the next line

    ret, buffer = cv2.imencode('.jpg', image)
    if not ret:  # if the image encoding failed
        raise ValueError("Failed to encode image")

    return buffer.tobytes()

def capture_frames(device_id):
    global latest_frame
    while True:
        cap = cv2.VideoCapture(device_id)
        if not cap.isOpened():
            logging.error(f"Could not open video device {device_id}")
            error_image = generate_error_image(f"Could not open video device {device_id}")
            with frame_lock:
                latest_frame = error_image
            time.sleep(5)  # wait for 5 seconds before trying again
            continue

        while True:
            success, frame = cap.read()
            if not success:
                logging.warning("Failed to read frame from camera")
                error_image = generate_error_image("Failed to read frame from camera")
                with frame_lock:
                    latest_frame = error_image
                break
            height = frame.shape[0]
            frame = frame[:height // 2, :]

            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            with frame_lock:
                latest_frame = frame_bytes

        cap.release()
        time.sleep(1)  # wait for 1 second before trying to reopen the device

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
