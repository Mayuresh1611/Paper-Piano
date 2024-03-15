import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
from src.mapping import analyse, draw_over_image
import os
from shapely.geometry import Point, Polygon
import threading
import queue
import pygame
from src import GLOBAL

from models.model import Predict


cols = 0
polys = []

snd_list = os.listdir("piano_keys")
sounds = [f"piano_keys/{sound}" for sound in snd_list] 



def play_sound(sound_path):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue

def predict_worker(img_queue, result_queue, stop_event):

    while not stop_event.is_set():
        img = img_queue.get()
        if img is None:
            break

        prediction = Predict(img)
        result_queue.put(prediction)

    print("Worker thread stopped.")

def start_piano(finger):
    stop_event = threading.Event()
    img_queue = queue.Queue()
    result_queue = queue.Queue()
    predict_thread = threading.Thread(target=predict_worker, args=(img_queue, result_queue, stop_event))
    predict_thread.start()

    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue
            image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            cols , polys = analyse(image)
            image = draw_over_image(image , cols , polys)
            cv2.imshow('analyse', image)
            key = cv2.waitKey(5)
            if key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                break
        
    print(cols , polys)
    cnvrt_poly = [Polygon(polygon_coords) for polygon_coords in polys]
    prev = None

    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            success, image = cap.read() 

            if not success:
                print("Ignoring empty camera frame.")
                continue
            image = cv2.cvtColor(image , cv2.COLOR_BGR2RGB)
            frame = image.copy()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            roi = None  # Initialize roi outside the loop

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    
                
                    for finger_tip_id in [finger]:  # Landmark IDs for all five fingers' tips
                        finger_tip = hand_landmarks.landmark[finger_tip_id]
                        height, width, _ = image.shape
                        tip_x, tip_y, tip_z = int(finger_tip.x * width), int(finger_tip.y * height), finger_tip.z

                        box_size = int(GLOBAL.BOX_SIZE // 2)  # Adjust the size of the box as needed
                        box_color = (0, 255, 0)  # Green color

                        # Coordinates of the rectangle
                        x1, y1 = tip_x - box_size, tip_y - box_size
                        x2, y2 = tip_x + box_size, tip_y + box_size

                        # Draw a square box around the finger tip
                        cv2.rectangle(image, (x1, y1), (x2, y2), box_color, 2)
                        
                        # Crop the region of interest (ROI)
                        roi = frame[y1:y2, x1:x2]

                        # Save the cropped image to the 'touched' folder
                        color = (0, 0, 255)
                        touched = False
                        if roi is not None and roi.shape[0] > 0 and roi.shape[1] > 0:
                            
                            img_queue.put(roi)

                            try:
                                prediction = result_queue.get(timeout=0.1)

                            except queue.Empty:
                                prediction = None

                            if prediction is not None:
                                if prediction > 0.5:
                                    color = (0, 255, 0)
                                    touched = True
                                else:
                                    if touched:
                                        pass
                                    else:
                                        color = (0, 0, 255)
                            image = cv2.circle(image, (50, 50), 10, color, 20)
                        
                        
                        point = Point(tip_x , tip_y)
                        for poly in cnvrt_poly:
                            is_inside = point.within(poly)
                            
                            if is_inside:
                                
                                text = cnvrt_poly.index(poly) + 1
                                
                                cv2.putText(image , str(text) , (100 , 50) , cv2.FONT_HERSHEY_SIMPLEX, 2, color, 2)
                                if touched:
                                    if text != prev:
                                        sound_path = sounds[text - 1]
                                        sound_thread = threading.Thread(target=play_sound, args=(sound_path,))
                                        sound_thread.start()
                                        prev = text
                                else:
                                    prev = None

                                break
                # Your remaining code
                
            image = draw_over_image(image , cols , polys)
            image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            cv2.imshow('MediaPipe Hands', image)
            cv2.imshow('Original', frame)
            key = cv2.waitKey(5)
            if key == ord('q'):
                img_queue.put(None)
                stop_event.set()
                predict_thread.join()
                cap.release()
                cv2.destroyAllWindows()
                break 

