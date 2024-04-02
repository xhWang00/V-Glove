import cv2
import mediapipe as mp
from flask import Flask, jsonify
import threading

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)

# Initialize Flask
app = Flask(__name__)

# Initialize hand landmarks
hand_landmarks = None

# Capture video from the webcam
cap = cv2.VideoCapture(0)

def update_hand_landmarks():
    global hand_landmarks
    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame horizontally for selfie view
        frame = cv2.flip(frame, 1)

        # Convert the BGR image to RGB
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image and get hand landmarks
        results = hands.process(rgb_image)

        # Update hand landmarks
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

@app.route('/landmarks')
def get_landmarks():
    global hand_landmarks
    if hand_landmarks is None:
        return jsonify(None)
    else:
        landmarks = [{'x': landmark.x, 'y': landmark.y, 'z': landmark.z} for landmark in hand_landmarks.landmark]
        return jsonify(landmarks)

if __name__ == '__main__':
    # Start a thread to update hand landmarks
    threading.Thread(target=update_hand_landmarks).start()

    # Start the Flask app
    app.run(host='0.0.0.0', port=5000)
