import cv2
import numpy as np
from imutils.video import VideoStream
import datetime
import pymongo
from pymongo import MongoClient
import time

# MongoDB Setup
client = pymongo.MongoClient("mongodb+srv://username:password@cluster0.lccx6km.mongodb.net/Cluster()")
db = client["fridgerator"]
collection = db["doorStatus"]

# Function to write data to MongoDB
def log_door_status(status):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = {
        "timestamp": timestamp,
        "status": status
    }
    collection.insert_one(data)
    print(f"{status.capitalize()} at {timestamp}")

# Initialize the video capture object with the first camera (index 0 for built-in webcam, 1 for USB camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video device.")
else:
    print("Video device opened successfully.")

# Set properties
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Variables to keep track of door status
door_open = False
last_status = "closed"

# Threshold for detecting brightness changes
brightness_threshold = 50

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image.")
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calculate the average brightness of the frame
    avg_brightness = np.mean(gray)

    # Determine door status based on brightness
    if avg_brightness > brightness_threshold:
        current_status = "open"
    else:
        current_status = "closed"

    # Log status change if there is any
    if current_status != last_status:
        log_door_status(current_status)
        last_status = current_status

    # Display the resulting frame
    cv2.imshow('USB Camera Feed', frame)

    # Press 'q' to exit the video feed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()