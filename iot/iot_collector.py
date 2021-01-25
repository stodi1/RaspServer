import getopt
import sys
from iot import IoT
import time
import datetime
import paho.mqtt.client as mqtt
import json
from Publisher import Publisher


class Collector:
    def __init__(self):

        self.drone_id = None
        self.sensor_type = None
        self.server_ip = None
        self.server_port = None
        self.username = None
        self.password = None
        self.interval = 0
        self.count = -1
        argument_list = sys.argv[1:]
        short_options = "hn:i:t:s:p:d:u:w:"
        long_options = ["help", "number=", "interval=", "type=", "server=", "port=", "drone=", "username=", "password="]

        try:
            arguments, values = getopt.getopt(
                argument_list, short_options, long_options)
        except getopt.error as err:
            print(str(err))
            sys.exit(2)
        for current_argument, current_value in arguments:
            if current_argument in ("-d", "--drone"):
                print("Collecting data of drone with id %s" % (current_value))
                self.drone_id = current_value
            if current_argument in ("-t", "--type"):
                print("Collecting data from %s sensor" % (current_value))
                self.sensor_type = current_value
            if current_argument in ("-s", "--server"):
                print("Sending data to server %s" % (current_value))
                self.server_ip = current_value
            if current_argument in ("-p", "--port"):
                print("Sending data to server at port %s" % (current_value))
                self.server_port = int(current_value)
            if current_argument in ("-u", "--username"):
                self.username = current_value
            if current_argument in ("-w", "--password"):
                self.password = current_value
            if current_argument in ("-n", "--number"):
                print("Sending limited (%s) data" % (current_value))
                if int(current_value) > 0:
                    self.count = int(current_value)
                else:
                    print("Invalid number of data (%s). Ignoring this flag .." % (
                        current_value))
            elif current_argument in ("-i", "--interval"):
                print(("Setting an interval of %ss") % (current_value))
                if int(current_value) > 0:
                    self.interval = int(current_value)
                else:
                    print("Invalid interval time (%s). Ignoring this flag .." %
                          (current_value))
            elif current_argument in ("-h", "--help"):
                print("Displaying help")
        if self.drone_id == None:
            print("Please specify drone id using --drone flag")
        elif self.sensor_type == None:
            print("Please specify sensor type using --type flag")
        elif self.server_ip == None:
            print("Please specify server ip using --server flag")
        elif self.server_port == None:
            print("Please specify server port using --port flag")
        elif self.username == None:
            print("Please specify username using --username flag")
        elif self.password == None:
            print("Please specify password using --password flag")
        else:
            self.start_collection()

    def send_data(self, data):
        i = 0
        for value in data:
            print("{}: {}".format(self.sensor_type.split("_and_")[i], value))
            body = {
                "time": str(datetime.datetime.now()),
                "type": self.sensor_type.split("_and_")[i],
                "value": value,
                "drone_id": self.drone_id
            }
            self.publisher.publish(json.dumps(body))
            i += 1

    def start_collection(self):
        iot = IoT()
        self.publisher = Publisher(self.drone_id, self.server_ip, self.server_port, self.username, self.password)
        sensor = iot.get_sensor(self.sensor_type)
        while True:
            self.send_data(sensor.get_data())
            self.count -= 1
            if self.count == 0:
                break
            time.sleep(self.interval)


collector = Collector()
