import cv2
import mediapipe as mp
import json
from http.server import BaseHTTPRequestHandler, HTTPServer


# Initialize MediaPipe Hands.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)


# Define a HTTP handler.
class HandLandmarksHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cap.release()

            # Detect hand landmarks.
            landmarks = self.detect_hand_landmarks(frame)

            # Send the response.
            self._set_headers()
            self.wfile.write(json.dumps({'hand_landmarks': landmarks}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def detect_hand_landmarks(self, frame):
        # Convert the BGR image to RGB.
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb_frame)

        landmarks = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for landmark in hand_landmarks.landmark:
                    landmarks.append({
                        'x': landmark.x,
                        'y': landmark.y,
                        'z': landmark.z
                    })
        return landmarks

def run_server(server_class=HTTPServer, handler_class=HandLandmarksHandler):
    server_address = (HOST, PORT)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on {HOST}:{PORT}...')
    httpd.serve_forever()


# Start the server.
if __name__ == '__main__':
    # Define the server parameters.
    HOST = 'localhost'
    PORT = 8080

    run_server()
