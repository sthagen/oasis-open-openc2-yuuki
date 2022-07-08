"""
Example Implementation of an OpenC2 HTTP Consumer
"""
from oc2_arch.transports import HttpTransport, HttpConfig
from consumer_example import consumer


http_consumer = HttpTransport(consumer=consumer, config=HttpConfig())
http_consumer.start()
