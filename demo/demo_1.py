import cv2
import mediapipe as mp
import sys


def detect_hand(input_img, output_img):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)

    img = cv2.imread(input_img)
    # Convert from BGR to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for idx, landmark in enumerate(hand_landmarks.landmark):
                height, width, _ = img.shape
                cx, cy = int(landmark.x * width), int(landmark.y * height)
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

                print(idx)
                print(landmark)

            landmarks = hand_landmarks.landmark
            connections = mp_hands.HAND_CONNECTIONS
            for connection in connections:
                x0, y0 = int(landmarks[connection[0]].x * width), int(landmarks[connection[0]].y * height)
                x1, y1 = int(landmarks[connection[1]].x * width), int(landmarks[connection[1]].y * height)
                cv2.line(img, (x0, y0), (x1, y1), (0, 0, 255), 2)
    
    cv2.imwrite(output_img, img)
    hands.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 detect_hand_in_img.py [input_image] [output_image]")
    else:
        detect_hand(sys.argv[1], sys.argv[2])
