import pika
import json

class Publisher:
    def __init__(self, id, server, port, username, password):
        self.credentials = pika.PlainCredentials(
            username, password)
        self.parameters = pika.ConnectionParameters(
            server, port, '/', self.credentials)
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange='telemetry_topic', exchange_type='topic')
        self.routing_key = "iot."+str(id)+"."

    def publish(self, data):
        iot_type = json.loads(data)["type"]
        # to_send = json.dumps(json_data)
        try:
            self.channel.basic_publish(
                exchange='telemetry_topic', routing_key=self.routing_key+iot_type, body=data)
        except Exception as ex:
            print(str(ex))
            self.connection = pika.BlockingConnection(self.parameters)
            self.channel = self.connection.channel()
            self.channel.exchange_declare(
                exchange='telemetry_topic', exchange_type='topic')