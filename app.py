from flask import request
from flask_api import FlaskAPI
import subprocess
from threading import Thread
import json

app = FlaskAPI(__name__)


def call_mavproxy(mav, src, addr):
    subprocess.run(["screen", "-dmS", "mav", "%s" %
                    mav, "--master", "%s" % src, "--out=%s" % addr])


def get_iot_sample(droneId, server_ip, server_port, username, password, sensorType, interval, number):
    cmd = ["python3", "iot/iot_collector.py", "-d", "{}".format(droneId), "-s", server_ip,
           "-p", server_port, "-u", username, "-w", password, "-t", "%s" % sensorType]
    if interval:
        cmd.append("-i")
        cmd.append("%s" % interval)
    if number:
        cmd.append("-n")
        cmd.append("%s" % number)
    subprocess.run(cmd)


@app.route("/test/", methods=['GET'])
def get_test():
    return "Test available"


@app.route("/cmds/", methods=['POST'])
def exec_cmds():
    cmds = json.loads(request.data["o"])
    error_messges = []
    for cmd in cmds:
        if cmd["cmd"] == "mav":
            token = None
            addr = None
            mav = "/home/pi/.local/bin/mavproxy.py"
            src = "/dev/ttyACM0"
            if "addr" in cmd["body"]:
                addr = cmd["body"]["addr"]
                if "token" in cmd["body"]:
                    token = cmd["body"]["token"]
                if "mav" in cmd["body"]:
                    mav = cmd["body"]["mav"]
                if "src" in cmd["body"]:
                    src = cmd["body"]["src"]
                Thread(target=call_mavproxy, args=(mav, src, addr,)).start()
            else:
                error_messges.append('Missing controller addr')
        elif cmd["cmd"] == "iot":
            token = None
            sensorType = None
            interval = None
            number = None
            if "id" in cmd["body"] and "type" in cmd["body"] and "server" in cmd["body"] and "port" in cmd["body"] and "username" in cmd["body"] and "password" in cmd["body"]:
                droneId = cmd["body"]["id"]
                sensorType = cmd["body"]["type"]
                server_ip = cmd["body"]["server"]
                server_port = cmd["body"]["port"]
                username = cmd["body"]["username"]
                password = cmd["body"]["password"]
                if "token" in cmd["body"]:
                    token = cmd["body"]["token"]
                if "interval" in cmd["body"]:
                    interval = cmd["body"]["interval"]
                if "number" in cmd["body"]:
                    number = cmd["body"]["number"]
                Thread(target=get_iot_sample, args=(droneId, server_ip, server_port,
                                                    username, password, sensorType, interval, number,)).start()
            else:
                error_messges.append('Missing required arguments')
    if len(error_messges) > 0:
        return "\n".join(error_messges), 400
    else:
        return {"started": True}


@app.route("/start_uav/", methods=['POST'])
def start_uav():
    token = None
    addr = None
    mav = "/home/pi/.local/bin/mavproxy.py"
    src = "/dev/ttyACM0"
    if "addr" in request.data:
        addr = request.data["addr"]
        if "token" in request.data:
            token = request.data["token"]
        if "mav" in request.data:
            mav = request.data["mav"]
        if "src" in request.data:
            src = request.data["src"]
        Thread(target=call_mavproxy, args=(mav, src, addr,)).start()
        return {"started": True}
    else:
        return 'Controller address (addr) is not specified in QR-code', 400


@app.route("/get_iot_data/", methods=['POST'])
def get_iot_data():
    token = None
    sensorType = None
    interval = None
    number = None
    if "type" in request.data:
        sensorType = request.data["type"]
        if "token" in request.data:
            token = request.data["token"]
        if "interval" in request.data:
            interval = request.data["interval"]
        if "number" in request.data:
            number = request.data["number"]
        Thread(target=get_iot_sample, args=(
            sensorType, interval, number,)).start()
        return {"started": True}
    else:
        return 'Sensor type (type) is not specified in QR-code', 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)
