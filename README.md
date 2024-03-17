# PAPER PIANO

### Now we don't need to buy a Piano if we want to play music. We can play piano on paper, although it may not give a feeling of pressing keys on the piano but it gets work done!

https://github.com/Mayuresh1611/Paper-Piano/assets/103099867/c2b0b4f1-3b6b-4eed-927d-91c5b5c91708

**Currently it only supports a maximum of 2 fingers** (1 finger of both hands). Support for more fingers and a highly susceptible training model is on the way.

1. [Setting up project](#setting-up-project)
2. [How to Use](#how-to-use)
3. [Training and Adjusting ](#training-and-adjusting)
4. [Contributing to this project](#contributing-to-this-project)
   
## SETTING UP PROJECT
Python version 3.11 and above
1.  Clone the repository ```git clone https://github.com/Mayuresh1611/Paper-Piano.git```
2. run command ```pip install -r requirements.txt``` in the command line.
3. Execute ```run.py``` file

## HOW TO USE   
This is a little trickier part as the project requires you to set up a webcam in a specific angle at a specific height and distance. Also  stronger the light, the better the performance. 
#### STUFF YOU WILL REQUIRE 
1. webcam or you can use third-party tools for webcam. 
2. Two A4-sized white paper, horizontally joined together. 2 rectangles need to be drawn at both ends of the paper with a black marker, thicker lines yield better results. 
3. The recommended position for the webcam will be such that it can capture the finger and shadow beneath the finger and should have both boxes we drew on joined paper in the FOV of the camera.
Just like shown in the demo video.
4. A light source in front, ie. behind the camera would be preferred. Casting sharp shadows.
4. Hand with all fingers.

#### TRAINING AND ADJUSTING
* During training the model on your finger, the first window will appear where the box will be drawn around the tip of the finger. If the box does not cover the complete finger and little surrounding of the finger. Adjust the camera accordingly.
* In the training stage, do not move your finger furiously, move it slowly giving out every angle.
* While training, during the touched finger state, do press the finger but not too hard. In an untouched finger state, do not touch paper, you can get near paper but not too close. Lift the finger high like you would normally do.
* CNN has been used to train over the data, it distinguishes the touched and untouched finger, if the results are not satisfactory, retrain the model.    
## CONTRIBUTING TO THIS PROJECT
If we make this project into a complete working piano on paper. It would give access to pianos and instruments for those who cannot afford them. ```like me :)``` 

* There are no set rules or code of conduct as of now. Anyone with better ideas and improvement is welcomed. 
* The only rules are
1. The name of the function should match the functionality it is doing.
2. Use comments only when required. 
3. Share with the ones who can improve this project even more.

