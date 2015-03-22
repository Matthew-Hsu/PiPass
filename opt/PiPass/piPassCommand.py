#!/usr/bin/python

#### Imported Libraries ####

from xml.dom.minidom import Document
import xml.dom.minidom
import subprocess
import sys

#### Configuration Variables - Adjust to your Preferences ####

# Path to the XML file where PiPass will write to for the PiPass Dashboard to display connection information.
DASHBOARD_INFO = "/var/www/assets/xml/current_state.xml"

#### Support Functions ####

# Write PiPass status to DASHBOARD_INFO.
def updateStatus():
    doc = Document()
    root = doc.createElement("PI_PASS_STATUS")
    stateXML = {'STATE':'Not running', 'MAC':'None', 'SSID':'None', 'DESCRIPTION':'None'}

    doc.appendChild(root)

    for value in stateXML:
        # Create Element
        tempChild = doc.createElement(value)
        root.appendChild(tempChild)

        # Write Text
        nodeText = doc.createTextNode(stateXML[value].strip())
        tempChild.appendChild(nodeText)

    doc.writexml(open(DASHBOARD_INFO, 'w'), indent="  ", addindent="  ", newl='\n')
    doc.unlink()

    return None

# Print out command interface.
def printCommandInterface():
    print("\nupdate : PiPass will use updated Nintendo Zone list.")
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
    subprocess.Popen('sudo echo "update" > /tmp/pipass_flag.txt', shell=True, stdout=subprocess.PIPE)
    print("Using updated Nintendo Zone list.\n")
elif command == "stop":
    # Web GUI: PiPass -> Stop
    updateStatus()
    subprocess.Popen('sudo pkill -f piPass.py', shell=True, stdout=subprocess.PIPE)
    subprocess.Popen('sudo service hostapd stop', shell=True, stdout=subprocess.PIPE)
    subprocess.Popen('sudo killall hostapd', shell=True, stdout=subprocess.PIPE)
    print("PiPass stopped.\n")
elif command == "start":
    # Web GUI: PiPass -> Start
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
