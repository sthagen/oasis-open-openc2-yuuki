"""
Example Implementation of an OpenC2 MQTT Consumer
"""
from yuuki.transports import (
    MqttTransport, MqttConfig, MQTTAuthorization, MQTTAuthentication, BrokerConfig, Publication, Subscription
)

from yuuki import Consumer
# import actuator profiles for your consumer


from actuators.slpf import slpf

consumer = Consumer(rate_limit=60, versions=['1.0'], actuators=[slpf])

host = "test.mosquitto.org"
port = 1883
topics = ['oc2/cmd', 'oc2/cmd/ap/slpf']

mqtt_config = MqttConfig(
    broker=BrokerConfig(
        host=host,
        port=port,
        client_id='',
        keep_alive=300,
        authorization=MQTTAuthorization(
            enable=False,
            username='plug',
            password='fest'
        ),
        authentication=MQTTAuthentication(
            enable=False,
            certfile=None,
            keyfile=None,
            ca_certs=None
        )
    ),
    subscriptions=[Subscription(topic=t, qos=1) for t in topics],
    publications=[
        Publication(
            topic='oc2/rsp',
            qos=1
        )
    ]
)

mqtt_consumer = MqttTransport(consumer=consumer, config=mqtt_config)
print("starting consumer")
mqtt_consumer.start()
