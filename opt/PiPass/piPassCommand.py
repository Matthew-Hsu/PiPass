#!/usr/bin/python

#### Imported Libraries ####

import subprocess
import json
import sys
import io

#### PiPass Command Support - MODIFY AT YOUR OWN RISK ####

# Path to the JSON file where PiPass will write to for the PiPass Dashboard to display connection information.
DASHBOARD_INFO = "/var/www/assets/json/current_state.json"

#### Support Functions ####

# Write PiPass status to DASHBOARD_INFO.
def updateStatus():
    with io.open(DASHBOARD_INFO, 'w', encoding='utf-8') as f:
        f.write(unicode('[{"gsx$ssid": {"$t": "Not Available."}, "gsx$mac": {"$t": "Not Available."}, "gsx$description": {"$t": "PiPass not running."}}]'))

    return None

# Print out command interface.
def printCommandInterface():
    print("\nupdate : PiPass will use updated Nintendo Zone list.")
    print("advance : Advances PiPass to next entry in list.")
    print("stop : Stops PiPass.")
    print("start : Starts PiPass.")
    print("piRestart : Restarts the Raspberry Pi.")
    print("piOff : Shutdown the Raspberry Pi.")
    print("e.g., python piPassCommand.py start\n")

    return None

#### PiPass Command Main ####

# Validate execution.
if len(sys.argv) < 2:
    printCommandInterface()
    sys.exit(1)

# Read in the first argument from the command line.
command = sys.argv[1]

# Command switchboard for PiPass commands.
if command == "update":
    # Web GUI: PiPass -> Refresh
    subprocess.Popen('sudo pkill --signal SIGUSR1 -f piPass.py', shell=True, stdout=subprocess.PIPE)
    print("Using updated Nintendo Zone list.\n")
elif command == "advance":
    subprocess.Popen('sudo pkill --signal SIGUSR2 -f piPass.py', shell=True, stdout=subprocess.PIPE)
    print("PiPass advanced to next entry.\n")
elif command == "stop":
    # Web GUI: PiPass -> Stop
    updateStatus()
    subprocess.Popen('sudo pkill -f piPass.py', shell=True, stdout=subprocess.PIPE)
    subprocess.Popen('sudo service hostapd stop', shell=True, stdout=subprocess.PIPE)
    subprocess.Popen('sudo killall hostapd', shell=True, stdout=subprocess.PIPE)
    print("PiPass stopped.\n")
elif command == "start":
    # Web GUI: PiPass -> Start
    updateStatus()
    subprocess.Popen('sudo pkill -f piPass.py', shell=True, stdout=subprocess.PIPE)
    subprocess.Popen('sudo python /opt/PiPass/piPass.py', shell=True, stdout=subprocess.PIPE)
    print("PiPass started.\n")
elif command == "piRestart":
    # Web GUI: Raspberry Pi -> Restart
    updateStatus()
    subprocess.Popen('sudo /sbin/shutdown -r now', shell=True, stdout=subprocess.PIPE)
elif command == "piOff":
    # Web GUI: Raspberry Pi -> Shutdown
    updateStatus()
    subprocess.Popen('sudo /sbin/shutdown -h now', shell=True, stdout=subprocess.PIPE)
else:
    printCommandInterface()
