import time
import face_recognition
import cv2
import numpy as np
import pymongo
from pymongo import MongoClient
import datetime

# MongoDB Setup
client = pymongo.MongoClient("mongodb+srv://Admin:Domusa96lewe-@cluster0.xf9oyhe.mongodb.net/test")
db = client["IoT"]
collection = db["Door status"]

# ----------------- Door Status Detection -----------------
# Initialize the video capture object with the first camera (index 0 for built-in webcam, 1 for USB camera)
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Error: Could not open video device.")
else:
    print("Video device opened successfully.")

# Set properties
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Threshold for detecting brightness changes
brightness_threshold = 50

# Function to save data status open
def log_door_status_open(status):
    global dataOpen
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dataOpen = {
        "status": status,
        "timestamp": timestamp,
    }

# Function to save data status close
def log_door_status_close(status):
    global dataClose
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dataClose = {
        "status": status,
        "timestamp": timestamp,
    }

# ----------------- Facial Recognition -----------------
known_face_encodings = []
known_face_names = []

def facial_rec():
    global known_face_encodings, known_face_names
    elias_image = face_recognition.load_image_file("elias.jpg")
    elias_face_encoding = face_recognition.face_encodings(elias_image)[0]

    florian_image = face_recognition.load_image_file("florian.jpg")
    florian_face_encoding = face_recognition.face_encodings(florian_image)[0]

    oliver_image = face_recognition.load_image_file("oliver.jpg")
    oliver_face_encoding = face_recognition.face_encodings(oliver_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        elias_face_encoding,
        florian_face_encoding,
        oliver_face_encoding
    ]
    known_face_names = [
        "Elias",
        "Florian",
        "Oliver"
    ]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# Call the facial recognition setup function
facial_rec()

# ----------------- Log -----------------
# Function to write data to MongoDB
dataOpen = {}
dataClose = {}
persons = []
previous_status = "closed"

def log_door_status(status):
    global previous_status, persons

    if previous_status == "closed" and status == "open":
        log_door_status_open(status)
    elif previous_status == "open" and status == "closed":
        log_door_status_close(status)

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "open": dataOpen,
            "close": dataClose,
            "persons": persons if persons else ["Unknown"],
            "timestamp": timestamp
        }
        collection.insert_one(data)
        print(dataOpen)
        print(dataClose)
        print(f"{status.capitalize()} at {timestamp}")

    previous_status = status  # Update the previous status

# ----------------- Script -----------------
# Variables to keep track of door status
last_status = "closed"

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

    if current_status != last_status:
        log_door_status(current_status)
        last_status = current_status

        if current_status == "closed":
            persons = []
    elif current_status == "open":
        # Only process every other frame of video to save time
        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            persons.clear()
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                persons.append(name)

            if not persons:
                persons.append("Unknown")

        process_this_frame = not process_this_frame

# Release handle to the webcam
cap.release()
cv2.destroyAllWindows()
