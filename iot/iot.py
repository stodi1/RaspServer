import importlib

class IoT:
    def get_sensor(self, sensor_type):
        module = importlib.import_module("classes.{}".format(sensor_type))
        sensor_class = getattr(module, sensor_type)
        return sensor_class()