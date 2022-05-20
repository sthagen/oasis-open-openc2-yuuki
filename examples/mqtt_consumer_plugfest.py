"""
Example Implementation of an OpenC2 MQTT Consumer
"""
import argparse

from yuuki.transports import (
    MqttTransport,
    MqttConfig,
    MQTTAuthorization,
    MQTTAuthentication,
    BrokerConfig,
    Publication,
    Subscription
)

from yuuki import Consumer
from actuators.SBOM import SBOM
from actuators.database import database
from actuators.slpf import slpf

consumer = Consumer(rate_limit=60, versions=['1.0'], actuators=[slpf, SBOM, database])

parser = argparse.ArgumentParser(description="MQTT Consumer")
parser.add_argument("--host", help="MQTT Broker host")
parser.add_argument("--port", type=int, help="MQTT Broker port")
args = parser.parse_args()

host = '35.221.11.97'
port = 1883

mqtt_config = MqttConfig(
    broker=BrokerConfig(
        host=host,
        port=port,
        client_id='',
        keep_alive=300,
        authorization=MQTTAuthorization(
            enable=True,
            username='plug',
            password='fest'),
        authentication=MQTTAuthentication(
            enable=False,
            certfile=None,
            keyfile=None,
            ca_certs=None)),
    subscriptions=[
        Subscription(
            topic='oc2/cmd',
            qos=1),
        Subscription(
            topic='oc2/cmd/ap/slpf',
            qos=1),
        Subscription(
            topic='oc2/cmd/ap/database',
            qos=1),
        Subscription(
            topic='oc2/cmd/ap/sbom',
            qos=1)
    ],
    publications=[
        Publication(
            topic='oc2/rsp',
            qos=1
        )]
)

mqtt_consumer = MqttTransport(consumer=consumer, config=mqtt_config)
mqtt_consumer.start()
