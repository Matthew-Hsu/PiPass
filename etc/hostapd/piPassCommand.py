#!/usr/bin/python

#### Imported Libraries ####
import sys
import subprocess

#### PiPass Command Main ####

# Read in the first argument from the command line.
if len(sys.argv) < 2:
    print("\nupdate : PiPass will use updated Nintendo Zone list.")
    print("stop : Stops PiPass.")
    print("start : Starts PiPass.")
    print("piRestart : Restarts the Raspberry Pi.")
    print("piOff : Shutdown the Raspberry Pi.")
    print("e.g., python piPassCommand.py start\n")
    sys.exit(1)

command = sys.argv[1]

# Command switchboard for PiPass commands.
if command == "update":
    # Web GUI: PiPass -> Refresh
    subprocess.Popen('sudo echo "update" > /tmp/pipass_flag.txt', shell=True, stdout=subprocess.PIPE)
    print("Using updated Nintendo Zone list.\n")
elif command == "stop":
    # Web GUI: PiPass -> Stop
    subprocess.Popen('sudo pkill -f piPass.py', shell=True, stdout=subprocess.PIPE)
    subprocess.Popen("sudo service hostapd stop", shell=True, stdout=subprocess.PIPE)
    subprocess.Popen("sudo killall hostapd", shell=True, stdout=subprocess.PIPE)
    print("PiPass stopped.\n")
elif command == "start":
    # Web GUI: PiPass -> Start
    subprocess.Popen('sudo pkill -f piPass.py', shell=True, stdout=subprocess.PIPE)
    subprocess.Popen('sudo python /etc/hostapd/piPass.py', shell=True, stdout=subprocess.PIPE)
    print("PiPass started.\n")
elif command == "piRestart":
    # Web GUI: Raspberry Pi -> Restart
    subprocess.Popen('sudo /sbin/shutdown -r now', shell=True, stdout=subprocess.PIPE)
elif command == "piOff":
    # Web GUI: Raspberry Pi -> Shutdown
    subprocess.Popen('sudo /sbin/shutdown -h now', shell=True, stdout=subprocess.PIPE)
else:
    # Print out command interface.
    print("\nupdate : PiPass will use updated Nintendo Zone list.")
    print("stop : Stops PiPass.")
    print("start : Starts PiPass.")
    print("piRestart : Restarts the Raspberry Pi.")
    print("piOff : Shutdown the Raspberry Pi.")
    print("e.g., python piPassCommand.py start\n")
