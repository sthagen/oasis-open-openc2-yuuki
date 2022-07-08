import json

from paho.mqtt import client as mqtt
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.subscribeoptions import SubscribeOptions

import openc2_command

host = '35.221.11.97'
port = 1883

oc2_properties = Properties(PacketTypes.PUBLISH)
oc2_properties.PayloadFormatIndicator = 1
oc2_properties.ContentType = "application/openc2"
oc2_properties.UserProperty = [("msgType", "req"), ("encoding", "json")]


def on_message(client, userdata, msg):
    print(json.dumps(json.loads(msg.payload), indent=2))
    client.disconnect()


#try making this pull from a file later
mqtt_client = mqtt.Client(protocol=mqtt.MQTTv5)
mqtt_client.username_pw_set(
    username='plug',
    password='fest'
)
mqtt_client.on_message = on_message
mqtt_client.connect(host=host, port=port, keepalive=60, clean_start=False)
mqtt_client.subscribe(
    topic="oc2/rsp",
    options=SubscribeOptions(qos=1, noLocal=True, retainAsPublished=True, retainHandling=0)
)
mqtt_client.publish(
    topic="oc2/cmd",
    # enter your OpenC2 Command here!
    # we reference a file with query_database, query_sbom, and query_features,
    # but as long as you set payload to a json OC2 cmd, you should be good to go
    payload=json.dumps(openc2_command.query_features),
    qos=1,
    retain=False,
    properties=oc2_properties
)
mqtt_client.loop_forever()
