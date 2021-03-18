import paho.mqtt.client as mqtt
import numpy as np
import tempfile
import cv2
from datetime import datetime

LOCAL_MQTT_HOST = "13.52.218.185"
LOCAL_MQTT_PORT = 1883
LOCAL_MQTT_TOPIC = "remote_face_processor"

def on_connect_local(client, userdata, flags, rc):
    print("connected to local broker with rc: " + str(rc))
    client.subscribe(LOCAL_MQTT_TOPIC)

def on_message(client,userdata, msg):
  try:
    msg = np.frombuffer(msg.payload, dtype='uint8')
    img = cv2.imdecode(msg, flags=1)
    filename = "/mnt/mountpoint/" + str(datetime.timestamp(datetime.now())).replace('.', '-', 1) + ".png"
    cv2.imwrite(filename, img)
    print("message received!")
  except:
    print("Unexpected error:", sys.exc_info()[0])

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_message = on_message

# go into a loop
local_mqttclient.loop_forever()
