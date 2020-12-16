# RaspServer: a Flask-based webserver for drone's Raspberry PI
This project is a webserver that is used to expose a REST API in the Raspberry PI to get commands from the client (mobile application). The Raspberry PI is supposed to be attached to a flight controller in a drone.

The server supports two kind of commands:

## 1. Start telemtrying drone data
Using the GCS software (Ground Control Station) installed on the Rspberry PI, the webserver can trigger the command that forwards telemetry packets to a remote host (named the UAV-controller). If you don't have a GCS installed in your Raspberry PI, we recommand that you install [MAVProxy](https://ardupilot.org/mavproxy/docs/getting_started/download_and_installation.html#mavproxy-downloadinstalllinux), it's a widly used open-source GCS.

## 2. Start collecting data from IoT on-board the drone
The drone can carry a wide-range of IoTs, the webserver expose an interface to trigger the process of collecting data from the IoTs on-board.

# Installation process
1. Download this project to your Raspberry PI by following one of these two methods:
a. if you have [Git](https://linuxize.com/post/how-to-install-git-on-raspberry-pi/) installed on the Raspberry PI, you can clone this project
```sh
$ git clone git@github.com:stodi1/RaspServer.git
```
b. Download the project to your computer and copy the files to your Raspberry PI (for instance, using scp).
```sh
scp -r <PATH_TO_DOWNLOADED_PROJECT> <DIR_IN_THE_RASPBERRY>
```

2. Access your Raspberry PI (using SSH), change directory to the project folder and trigger the installation process with
```sh
./install.sh
```

More information about the mobile application and the platform will be provided later.