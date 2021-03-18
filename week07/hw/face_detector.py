from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from torch.utils.data import DataLoader
from torchvision import datasets
import numpy as np
import pandas as pd
import os
from PIL import Image
import numpy as np
import cv2
import paho.mqtt.client as mqtt

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
print('Running on device: {}'.format(device))

# the index depends on your camera setup and which one is your USB camera
cap = cv2.VideoCapture(0)

# Create face detector
mtcnn = MTCNN(keep_all=True, device=device)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(img)

    # Detect face
    boxes, probs, landmarks = mtcnn.detect(image, landmarks=True)

    # Our operations on the frame come here
    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x, y), (x2, y2), (0, 255, 0), 5)
        #face = gray[y:y+h, x:x+w]
        face_extract = frame[y:y2, x:x2]
        rc, png = cv2.imencode('.png', face_extract)
        msg = png.tobytes()
        client.publish(LOCAL_MQTT_TOPIC, msg)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
