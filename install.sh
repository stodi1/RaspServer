#Extremly important parameters.
#Do not change these values unless you are very confident about what are you doing
pythonDir=$(which python3)
workDir=$(pwd)
currentUser=$(whoami)

sudo apt-get install screen python3-pip
pip3 install -r requirements.txt
printf "[Unit]\nAfter=network-online.target\n[Service]" > initializer.service
printf "\nWorkingDirectory="$workDir >> initializer.service
printf "\nExecStart="$pythonDir >> initializer.service
printf " "$workDir"/app.py" >> initializer.service
printf "\nRestart=always\nStandardOutput=syslog\nStandardError=syslog\nSyslogIdentifier=initializer\nUser="$currentUser >> initializer.service
printf "\n[Install]\nWantedBy=multi-user.target" >> initializer.service
sudo cp initializer.service /etc/systemd/system/
sudo chmod u+r /etc/systemd/system/initializer.service
sudo systemctl enable initializer
sudo systemctl start initializer

echo "webserver installed successfully."