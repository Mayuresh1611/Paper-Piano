# PAPER PIANO

### Now we don't need to buy Piano if we want to play music. We can play piano on paper, although it may not give feeling of pressing keys on piano but it gets work done!

https://github.com/Mayuresh1611/Paper-Piano/assets/103099867/c2b0b4f1-3b6b-4eed-927d-91c5b5c91708

**Currently it only supports maximum 2 fingers** (1 finger of both hands). Support for more fingers and highly susceptible training model is on the way.

1. [Setting up project](#setting-up-project)
2. [How to Use](#how-to-use)
3. [Training and Adjusting ](#training-and-adjusting)
4. [Contributing to this project](#contributing-to-project)
   
## SETTING UP PROJECT
Python version 3.11 and above
1.  Clone the repository ```git clone https://github.com/Mayuresh1611/Paper-Piano.git```
2. run command ```pip install requirements.txt``` in command line.
3. Execute ```run.py``` file

## HOW TO USE   
This is little trickier part as the project requires you to set up webcam in specific angle at specifih heigh and distance. Also  stronger the ligth, better the performance. 
#### STUFF YOU WILL REQUIRE 
1. webcam or you can use third-party tools for webcam. 
2. Two A4 sized white paper, horizontally joined together. 2 rectangle need to be drawn at both end of paper with black marker, thicker line yeild better result. 
3. Recommended position for webcam will be scuh that it can capture the finger and shadow beneath the finger and should have both boxes we drew on joined paper in the FOV of camera.
Just like shown in the demo video.
4. Light source in front, ie. behind the camera would be preffered. Casting sharp shadows.
4. Hand with all fingers.

#### TRAINING AND ADJUSTING
* During training the model on your finger, first window will appear where box will be drawn around the tip of the finger. If the box does not cover complete finger and little surrounding of the finger. Adjust the camera accordingly.
* While training stage, do not move finger furiously, move it slowly giving out every angle.
* While training, during touched finger state, do press finger but not too hard. In untouched finger state, do not touch paper, you can get near paper but not too close. Lift the finger high like you would normally do.
* CNN has been used to train over the data, it distinguishes the touched and untouched finger, if the results are not satisfactory, retrain the model.    
## CONTRIBUITING TO THIS PROJECT
If we make this project into complete working piano on paper. It would give access of piano and instruments for those who cannot afford it. ```like me :)``` 

* There are no set rules or code of conduct as of now. Anyone wtih better ideas and improvement is welcomed. 
* The only rules are
1. Name of the function should match the functionality it is doing.
2. Use comments only when required. 
3. Share with the ones who can improve this project even more.

