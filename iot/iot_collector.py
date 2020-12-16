import getopt, sys
from iot import IoT
import time

class Collector:
    def __init__(self):
        self.sensor_type = None
        self.interval = 0
        self.count = -1
        argument_list = sys.argv[1:]
        short_options = "hn:i:t:"
        long_options = ["help", "number=", "interval=", "type="]

        try:
            arguments, values = getopt.getopt(argument_list, short_options, long_options)
        except getopt.error as err:
            print (str(err))
            sys.exit(2)
        for current_argument, current_value in arguments:
            if current_argument in ("-t", "--type"):
                print ("Collecting data from %s sensor" % (current_value))
                self.sensor_type = current_value
            if current_argument in ("-n", "--number"):
                print ("Sending limited (%s) data" % (current_value))
                if int(current_value) > 0:
                    self.count = int(current_value)
                else:
                    print("Invalid number of data (%s). Ignoring this flag .." %(current_value))
            elif current_argument in ("-i", "--interval"):
                print (("Setting an interval of %ss") % (current_value))
                if int(current_value) > 0:
                    self.interval = int(current_value)
                else:
                    print("Invalid interval time (%s). Ignoring this flag .." %(current_value))
            elif current_argument in ("-h", "--help"):
                print ("Displaying help")
        if self.sensor_type == None:
            print ("Please specify sesor type using --type flag")
        else:
            self.start_collection()

    def send_data(self, data):
        i = 0
        for value in data:
            print("{}: {}".format(self.sensor_type.split("_and_")[i], value))
            i += 1

    def start_collection(self):
        iot = IoT()
        sensor = iot.get_sensor(self.sensor_type)
        while True:
            self.send_data(sensor.get_data())
            self.count -= 1
            if self.count == 0:
                break
            time.sleep(self.interval)

collector = Collector()