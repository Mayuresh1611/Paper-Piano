import cv2
from tensorflow.keras.models import load_model
import numpy as np
import sys
sys.path.append("src")
import GLOBAL
import os


model_list = os.listdir("models")
if "touch_detection_model.h5" not in model_list:
    print("We need to train model on your finger's data")
else:
    model = load_model("models/touch_detection_model.h5")

def Predict(img):
  resized_img = cv2.resize(img, GLOBAL.TRACKING_BOX_RESOLUTION)
  # Add the batch dimension and normalize pixel values
  data = np.expand_dims(resized_img/255, axis=0)
  # Make the prediction
  prediction = model.predict(data)  
  print(prediction)
  if prediction > 0.502:
      return 0
  else:
      return 1