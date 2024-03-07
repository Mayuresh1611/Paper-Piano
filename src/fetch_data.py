import cv2
import numpy as np
import mediapipe as mp
import os
from  src import GLOBAL



# CAPTURE TOUCHED n UNTOUCHED
# track finger
# save images

def Capture(save_folder , finger_state , finger):
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    cap = cv2.VideoCapture(GLOBAL.WEB_CAM)
    iter = 0
    with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            image = cv2.cvtColor(image , cv2.COLOR_BGR2RGB)
            copy_image = image.copy()

            image.flags.writeable = False
            results = hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            finger_tracking_frame = None # initializing region of interest

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    for finger_tip_id in finger:  # Landmark IDs for all five fingers' tips
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
                        finger_tracking_frame = copy_image[y1:y2, x1:x2]
                        
                        if finger_tracking_frame is not None and finger_tracking_frame.shape[0] > 0 and finger_tracking_frame.shape[1] > 0:
                            finger_tracking_frame = cv2.cvtColor(finger_tracking_frame , cv2.COLOR_BGR2RGB)
                            filename = os.path.join(save_folder, f'finger-{finger_state}{iter}.png')
                            cv2.imwrite(filename, finger_tracking_frame)
                            print(f'Saved touched image: {filename}')           
                            iter += 1         
                        if iter >= GLOBAL.SAMPLES:
                            cv2.destroyAllWindows()
                            return 

            cv2.imshow(f'{finger_state} SAVING', image)            
            key = cv2.waitKey(5)
            if key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                break




def clear_training_data():
    for file in os.listdir(GLOBAL.TOUCH_FOLDER):
        os.remove(f'{GLOBAL.TOUCH_FOLDER}/{file}')
        
    for file in os.listdir(GLOBAL.UNTOUCH_FOLDER):
        os.remove(f'{GLOBAL.UNTOUCH_FOLDER}/{file}')
    print("TRAINING DATA CLEARED")

def delete_model():
    model = os.listdir("models")
    if "touch_detection_model.h5" in model:
        model.remove("touch_detection_model.h5")
        print("model removed")
    else:
        print("model not present")

def Try(finger):
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    cap = cv2.VideoCapture(GLOBAL.WEB_CAM)
    with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            image = cv2.cvtColor(image , cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    for finger_tip_id in finger:  # Landmark IDs for all five fingers' tips
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
            cv2.imshow('Tocuh tracking', image)            
            key = cv2.waitKey(5)
            if key == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()


    
