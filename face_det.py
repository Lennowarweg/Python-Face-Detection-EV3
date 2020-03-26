from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
import EV3BT
import serial


EV3 = serial.Serial("COM3")


print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(prototxt="deploy.prototxt.txt", caffeModel="res10_300x300_ssd_iter_140000.caffemodel")

print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

while True:
	frame = vs.read()
	frame = imutils.resize(frame, width=400)


	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
		(300, 300), (104.0, 177.0, 123.0))


	camwith = int(w / 2)
	camheight = int(h / 2)

	net.setInput(blob)
	detections = net.forward()




	for i in range(0, detections.shape[2]):

		confidence = detections[0, 0, i, 2]


		if confidence < 0.5:
			continue


		box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		(startX, startY, endX, endY) = box.astype("int")

		m_width = int((startX + endX) / 2)
		m_height = int((startY + endY) / 2)

		y = startY - 10 if startY - 10 > 10 else startY + 10
		cv2.rectangle(frame, (startX, startY), (endX, endY),
					  (255, 0, 0), 2)

		distance_x = m_width - camwith
		distance_y = m_height - camheight

		if distance_x > 20:
			right = 10
			r = True
			s = EV3BT.encodeMessage(EV3BT.MessageType.Logic, "true", r)
			EV3.write(s)
			s = EV3BT.encodeMessage(EV3BT.MessageType.Numeric, "right", right)
			EV3.write(s)
			left = -10
			l = False
			s = EV3BT.encodeMessage(EV3BT.MessageType.Logic, "false", l)
			EV3.write(s)
			s = EV3BT.encodeMessage(EV3BT.MessageType.Numeric, "left", left)
			EV3.write(s)

		if distance_x < -20:
			right = -10
			r = False
			s = EV3BT.encodeMessage(EV3BT.MessageType.Logic, "false", r)
			EV3.write(s)
			s = EV3BT.encodeMessage(EV3BT.MessageType.Numeric, "right", right)
			EV3.write(s)
			left = 10
			l = True
			s = EV3BT.encodeMessage(EV3BT.MessageType.Logic, "true", l)
			EV3.write(s)
			s = EV3BT.encodeMessage(EV3BT.MessageType.Numeric, "left", left)
			EV3.write(s)

		if -20 < distance_x < 20:
			right = 0
			left = 0
			l = True
			r = False
			s = EV3BT.encodeMessage(EV3BT.MessageType.Logic, "false", r)
			EV3.write(s)
			f = EV3BT.encodeMessage(EV3BT.MessageType.Logic, "true", l)
			EV3.write(f)
			s = EV3BT.encodeMessage(EV3BT.MessageType.Numeric, "right", right)
			EV3.write(s)
			s = EV3BT.encodeMessage(EV3BT.MessageType.Numeric, "left", left)
			EV3.write(s)

		if distance_y > 10:
			down = -20
			d = True
			f = EV3BT.encodeMessage(EV3BT.MessageType.Logic, "d", d)
			EV3.write(f)
			s = EV3BT.encodeMessage(EV3BT.MessageType.Numeric, "down", down)
			EV3.write(s)

		if distance_y < 10:
			down = 20
			d = False
			f = EV3BT.encodeMessage(EV3BT.MessageType.Logic, "d", d)
			EV3.write(f)
			s = EV3BT.encodeMessage(EV3BT.MessageType.Numeric, "down", down)
			EV3.write(s)

		if -10 < distance_y < 10:
			down = 0
			s = EV3BT.encodeMessage(EV3BT.MessageType.Numeric, "down", down)
			EV3.write(s)

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
 

	if key == ord("q"):
		break


cv2.destroyAllWindows()
vs.stop()
