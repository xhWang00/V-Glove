import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm


# Initialize MediaPipe Hands.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# Define connections between landmarks.
HAND_CONNECTIONS = [
    [2, 1], [1, 0], [2, 3], [3, 4], [5, 6], [6, 7], [7, 8], [9, 10], [10, 11], [11, 12], [13, 14], [14, 15], [15, 16], [17, 18], [18, 19], [19, 20]
]

# Setup OpenCV.
cap = cv2.VideoCapture(0)
fig = plt.figure("3D plotting")
plt.axis('off')
ax = fig.add_subplot(111, projection='3d')
ax.view_init(elev=45, azim=120, roll=0)


while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert the image from BGR to RGB.
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Process the frame.
    results = hands.process(rgb_frame)
    # Clear previous frame.
    ax.clear()
    
    # If a hand is detected.
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmark_coords = np.array([[landmark.x, landmark.y, landmark.z] for landmark in hand_landmarks.landmark])
            
            # Plot hand connections
            for connection in HAND_CONNECTIONS:
                point1 = landmark_coords[connection[0]]
                point2 = landmark_coords[connection[1]]
                ax.plot([point1[0], point2[0]], [point1[1], point2[1]], [point1[2], point2[2]], c='k', linewidth=5)
            
            # Plot landmark points.
            ax.scatter(landmark_coords[:, 0], landmark_coords[:, 1], landmark_coords[:, 2], c='r', marker='o', s=10)

            # Plot the palm
            surface_points = landmark_coords[[1, 2, 5, 9, 13, 17, 0], :]
            X, Y, Z = surface_points[:, 0], surface_points[:, 1], surface_points[:, 2]
            ax.plot_trisurf(X, Y, Z, color='k')
    
    # Set plot limits and labels
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    
    # Display the plot
    plt.pause(0.001)
    