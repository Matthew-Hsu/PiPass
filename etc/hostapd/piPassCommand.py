#!/usr/bin/python

#### Imported Libraries ####
import sys
import subprocess

#### PiPass Command Main ####

# Read in the first argument from the command line.
command = sys.argv[1]

# Command switchboard for PiPass commands.
if command == "update":
    # Web GUI: PiPass -> Refresh
    subprocess.Popen('sudo echo "update" > /tmp/pipass_flag.txt', shell=True, stdout=subprocess.PIPE)
elif command == "stop":
    # Web GUI: PiPass -> Stop
    subprocess.Popen('sudo echo "stop" > /tmp/pipass_flag.txt', shell=True, stdout=subprocess.PIPE)
elif command == "start":
    # Web GUI: PiPass -> Start
    subprocess.Popen('sudo pkill -f piPass.py', shell=True, stdout=subprocess.PIPE)
    subprocess.Popen('sudo python /etc/hostapd/piPass.py', shell=True, stdout=subprocess.PIPE)
elif command == "piRestart":
    # Web GUI: Raspberry Pi -> Restart
    subprocess.Popen('sudo /sbin/shutdown -r now', shell=True, stdout=subprocess.PIPE)
elif command == "piOff":
    # Web GUI: Raspberry Pi -> Shutdown
    subprocess.Popen('sudo /sbin/shutdown -h now', shell=True, stdout=subprocess.PIPE)
