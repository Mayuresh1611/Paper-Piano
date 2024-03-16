import cv2 
import mediapipe as mp 
import os 
import time
from src import fetch_data , train_model, GLOBAL , piano
from models import model  
 
FINGER = [GLOBAL.INDEX_FINGER]

def RUN(finger): 
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
                        finger_tracking_frame = copy_image[y1:y2, x1:x2]
                        color = (0, 0, 255)
                        if finger_tracking_frame is not None and finger_tracking_frame.shape[0] > 0 and finger_tracking_frame.shape[1] > 0:
                            finger_tracking_frame = cv2.cvtColor(finger_tracking_frame , cv2.COLOR_BGR2RGB)
                            pred = model.Predict(finger_tracking_frame)
                            if pred:
                                color=(0, 255, 0)
                            else:
                                if color == (0, 255, 0):
                                    pass
                                else:
                                    color = (0, 0, 255)
                            image = cv2.circle(image, (250 , 300), 2, color, 20)
            cv2.imshow('Tocuh tracking', image)            
            key = cv2.waitKey(5)
            if key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                break


def fetch_train_data():
    print("The First window is try window so that you can adjust the finger position, adjust hand position so that box will cover  finger tip and finger tip\n1. Window after try will be touch train window\n\t do not lift any finger, move fingers slowly on the paper to get all angles\n2. After this window untouch train window will pop up\n\t lift fingers so that it can take pics of finger tips for training\n\t Then model will be trained and you should see the prediction window for Index finger")
    print("Press Y to move for training stage")
    while 1:
        key = input(">> ")
        if key.lower() == 'y':
            break
    time.sleep(2)
    fetch_data.Try(FINGER) 
    time.sleep(2)
    fetch_data.Capture(GLOBAL.TOUCH_FOLDER , "touched" , FINGER) 
    time.sleep(2)
    fetch_data.Capture(GLOBAL.UNTOUCH_FOLDER , "untouched" , FINGER) 

    train_model.start_training() 

    print("Model Training Complete")
    time.sleep(3)

    RUN(GLOBAL.INDEX_FINGER)

print("welcome to Paper Piano")
# fetch_data.delete_model()
run = True

fetch_data.clear_training_data()

while run:
    model_list = os.listdir("models")
    if "touch_detection_model.h5" not in model_list:
        print("We need to train model on your finger's data")
        fetch_data.clear_training_data()
        fetch_train_data()
        
    else:

        print("-------------*MENU*-------------\n[1] Retrain model\n[2] Start Paper Piano\n[3] Exit")
        check = True
        while check:
            opt = int(input())
            if opt == 1:
                check = False
                fetch_data.clear_training_data()
                fetch_train_data()
            elif opt == 2:
                check = False
                print("Adjust paper accordingly until you see mesh of keys and press 'q'")
                time.sleep(3)
                piano.start_piano(GLOBAL.INDEX_FINGER)
            elif opt==3:
                check = False
                run = False
