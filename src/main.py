import cv2
import mediapipe as mp
import numpy as np


# Initialize MediaPipe Hands.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# Setup setup.
cap = cv2.VideoCapture(0)
cv2.namedWindow("Hand Tracking", cv2.WINDOW_NORMAL)
cv2.namedWindow("Landmark Coordinates", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Landmark Coordinates", 300, 650) 


while cap.isOpened():
    ret, frame = cap.read()
    landmark_frame = 255 * np.zeros((650, 300, 3), dtype=np.uint8)
    if not ret:
        break
    
    # Convert the image from BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Process the frame
    results = hands.process(rgb_frame)
    
    # If a hand is detected.
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            for idx, landmark in enumerate(hand_landmarks.landmark):
                # Plot and how the landmarks on the real-time footage.
                h, w, c = frame.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv2.putText(frame, f"{idx}", (cx, cy + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                # Display the X Y Z coordinates.
                text = f"{idx}: (X: {landmark.x:.2f}, Y: {landmark.y:.2f}, Z: {landmark.z:.2f})"
                cv2.putText(landmark_frame, text, (10, 30*(idx+1)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    
    # Display the frame.
    cv2.imshow("Hand Tracking", frame)
    cv2.imshow("Landmark Coordinates", landmark_frame)
    
    # Check for ESC key to exit.
    key = cv2.waitKey(1)
    if key == 27:
        break


# Release resources.
cap.release()
cv2.destroyAllWindows()