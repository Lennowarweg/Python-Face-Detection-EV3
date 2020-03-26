# Python-Facedetection-EV3
Enables you to use your EV3 as a facetracker. Uses the Dnn method of OpenCv and an external script (EV3BT) found in an Geek Droppings article written by Maksym Shyte. 

How to use it:
Put an Usb-Webcam onto the robot, which should be able to move in x- and y-direction, and connect both, the Cam and the EV3, to your PC. You need to enter the right COM Port of your connected EV3 (face_det.py line 10) in order to connect to it. Connecting to EV3 gives strange errors sometimes, in this case check if the COM Port is right and restart the code.
