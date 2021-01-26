import numpy as np
import cv2
import paho.mqtt.client as mqtt

LOCAL_MQTT_HOST="broker"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="face_detection"

# create a new mosquitto client named local mqtt
client = mqtt.Client()

# connect to mqtt broker 
client.connect(LOCAL_MQTT_HOST)

# the index depends on your camera setup and which one is your USB camera
cap = cv2.VideoCapture(0)

# face classifier
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# start stream
client.loop_start()

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 2)

    for (x, y, w, h) in faces:
        face = gray[y:y+h, x:x+w]
        rc, png = cv2.imencode('.png', face)
        msg = png.tobytes()
        client.publish(LOCAL_MQTT_TOPIC, msg)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# stop the loop and disconnect from the client
client.loop_stop()
client.disconnect()

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
