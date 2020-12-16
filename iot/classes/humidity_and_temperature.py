import Adafruit_DHT

class humidity_and_temperature:
    def __init__(self):
        self.DHT_SENSOR = Adafruit_DHT.DHT22
        self.DHT_PIN = 22

    def get_data(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.DHT_PIN)
        return [humidity, temperature]

