import cv2
import mediapipe as mp
import socket
import json
import time

class HandTrackingServer:
    def __init__(self, host='127.0.0.1', port=65432):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=1,
            min_detection_confidence=0.7, 
            min_tracking_confidence=0.7   
        )
        
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((host, port))
            self.server_socket.listen(1)
        except Exception as e:
            print(f"Socket error: {e}")
            raise
        
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640) 
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        if not self.cap.isOpened():
            raise RuntimeError("Could not open camera")
        
    def start(self):
        print("Waiting for Blender connection...")
        try:
            conn, addr = self.server_socket.accept()
            print(f"Connected to Blender at {addr}")

            while self.cap.isOpened():
                success, image = self.cap.read()
                if not success:
                    print("Failed to get frame")
                    continue

                image = cv2.flip(image, 1)
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = self.hands.process(image_rgb)

                height, width, _ = image.shape

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Draw landmarks with custom style
                        self.mp_drawing.draw_landmarks(
                            image,
                            hand_landmarks,
                            self.mp_hands.HAND_CONNECTIONS,
                            self.mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2),
                            self.mp_drawing.DrawingSpec(color=(255,0,0), thickness=2)
                        )

                        # Convert landmarks to list with better precision
                        landmarks_list = []
                        for idx, landmark in enumerate(hand_landmarks.landmark):
                            landmarks_list.append([
                                float(landmark.z),
                                float(landmark.x * width),
                                float(landmark.y * height)
                            ])

                        try:
                            data = {
                                'landmarks': landmarks_list,
                                'image_size': [width, height],
                                'timestamp': time.time()  
                            }
                            message = json.dumps(data) + '\n'
                            conn.sendall(message.encode())
                        except (ConnectionResetError, BrokenPipeError):
                            print("Blender connection lost")
                            return
                        except Exception as e:
                            print(f"Error sending data: {e}")
                            return

                cv2.imshow('Hand Tracking', image)
                
                key = cv2.waitKey(1) & 0xFF
                if key == 27 or key == ord('q'):
                    break

        except Exception as e:
            print(f"Error in main loop: {e}")
        finally:
            if 'conn' in locals():
                conn.close()
            self.cleanup()

    def cleanup(self):
        print("Cleaning up...")
        self.cap.release()
        cv2.destroyAllWindows()
        self.server_socket.close()
        self.hands.close()

if __name__ == "__main__":
    while True:
        try:
            server = HandTrackingServer()
            server.start()
            response = input("Server stopped. Press 'r' to restart or 'q' to quit: ")
            if response.lower() != 'r':
                break
        except Exception as e:
            print(f"Server error: {e}")
            print("Restarting in 2 seconds...")
            time.sleep(2)