#!/usr/bin/python

#### Imported Libraries ####

from xml.dom.minidom import parse
import xml.dom.minidom
import subprocess
import time

#### Configuration Variables - Adjust to your Preferences ####

# Controls the minutes between each Nintendo Zone cycle.
STREETPASS_CYCLE_MINUTES = 15

# Path to the list of current Nintendo Zones being used.
NINTENDO_ZONES = "/var/www/assets/xml/current_zones.xml"

# Network configuration file path for PiPass to spoof as a Nintendo Zone.
NETWORK_CONFIGURATION = "/etc/hostapd/hostapd.conf"

#### PiPass Support - MODIFY AT YOUR OWN RISK ####

# Flag that informs PiPass that updates have been made to current_zones.xml and to use those updates. Default value is "execute".
piPassStatus = "execute"

# Temporary flag file path for piPassStatus.
FLAG_PATH = "/tmp/pipass_flag.txt"

# Converting STREETPASS_CYCLE_MINUTES to seconds.
STREETPASS_CYCLE_SECONDS = STREETPASS_CYCLE_MINUTES * 60

# Constructing hostapd command string.
COMMAND = "timeout " + str(STREETPASS_CYCLE_SECONDS) + " hostapd " + NETWORK_CONFIGURATION

#### PiPass Main #####

# Ensure that hostapd is not running.
subprocess.Popen("sudo service hostapd stop", shell=True, stdout=subprocess.PIPE)
subprocess.Popen("sudo killall hostapd", shell=True, stdout=subprocess.PIPE)

# Create/Overwrite flag file for piPassStatus.
fo = open(FLAG_PATH, "wb")
fo.write(piPassStatus)
fo.close()

# Open current_zones.xml using minidom parser.
DOMTree = xml.dom.minidom.parse(NINTENDO_ZONES)
collection = DOMTree.documentElement

print("PiPass is currently running...")

# This loop does not feel pity or remorse or fear and it cannot be stopped unless Half-Life 3 is released.
while "Waiting for Half-Life 3":
	# Get all the Nintendo Zones in the collection.
	zones = collection.getElementsByTagName("ZONE")

	# Begin looping through all the Nintendo Zones in the collection.
	for currentZone in zones:
		# Open the flag file and read in the value.
		fo = open(FLAG_PATH)
		piPassStatus = fo.read()
		fo.close()

		# If the user has issued an update, then reload current_zones.xml for the updated Nintendo Zones.
		if piPassStatus == "update\n":
			# current_zones.xml has been changed, so reload it.
			DOMTree = xml.dom.minidom.parse(NINTENDO_ZONES)
			collection = DOMTree.documentElement

			# We want PiPass to keep running.
			piPassStatus = "execute"

			# Overwrite flag file for piPassStatus.
			fo = open(FLAG_PATH, "wb")
			fo.write(piPassStatus)
			fo.close()

			print("\n[ Update Detected! - Using new updated Nintendo Zones. ]\n")

			break

		# If the user has issued a stop, then exit out of PiPass. NOTE: PiPass will stop after the current Nintendo Zone is finished.
		if piPassStatus == "stop\n":
			break

		# Write the current zone information to NETWORK_CONFIGURATION.
		fo = open(NETWORK_CONFIGURATION, "wb")

		currentMAC = currentZone.getElementsByTagName("MAC")[0]
		currentMAC = currentMAC.childNodes[0].data

		currentSSID = currentZone.getElementsByTagName("SSID")[0]
		currentSSID = currentSSID.childNodes[0].data

		currentDesc = currentZone.getElementsByTagName("DESCRIPTION")[0]
		currentDesc = currentDesc.childNodes[0].data

		conf = "interface=wlan0\nbridge=br0\ndriver=nl80211\nssid=" + currentSSID + "\nbssid=" + currentMAC + "\nhw_mode=g\nchannel=6\nauth_algs=1\nwpa=0\nmacaddr_acl=1\naccept_mac_file=/etc/hostapd/mac_accept\nwmm_enabled=0\nignore_broadcast_ssid=0"

		fo.write(conf)
		fo.close()

		# Nintendo Zone identity acquired for PiPass spoofing.
		print("Spoofing as " + currentMAC + " on " + currentSSID + " ( " + currentDesc + ") for " + str(STREETPASS_CYCLE_MINUTES) + " minute(s).")

		# Run current Nintendo Zone and pause for STREETPASS_CYCLE_MINUTES until moving onto the next Nintendo Zone.
		subprocess.Popen(COMMAND, shell=True, stdout=subprocess.PIPE)
		time.sleep(STREETPASS_CYCLE_SECONDS)

	# If the user has issued a stop, then exit out of PiPass.
	if piPassStatus == "stop\n":
		break

print("\n[ Stop Detected! - PiPass has exited successfully. ]\n")
