#!/usr/bin/python

#### Imported Libraries ####

from xml.dom.minidom import parse
import xml.dom.minidom
import time

#### Configuration Variables - Adjust to your Preferences ####

# Controls the minutes between each Nintendo Zone cycle.
STREETPASS_CYCLE_MINUTES = 1

# Path to the list of current Nintendo Zones being used.
NINTENDO_ZONES = "/Applications/XAMPP/htdocs/PiPass/wwwroot/assets/xml/current_zones.xml"

# Network configuration file path for PiPass to spoof as a Nintendo Zone.
NETWORK_CONFIGURATION = "/tmp/test_configuration.txt"

#### PiPass Support - MODIFY AT YOUR OWN RISK ####

# Flag that informs PiPass that updates have been made to current_zones.xml and to use those updates. Default value is "execute".
piPassStatus = "execute"

# Temporary flag file path for piPassStatus.
FLAG_PATH = "/tmp/pipass_flag.txt"

#### PiPass Main #####

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

		conf = "interface=wlan0\nssid=attwifi\nbssid=" + currentMAC + "\nbridge=br0\ndriver=nl80211\nssid=" + currentSSID + "\nctrl_interface=wlan0\nctrl_interface_group=0\nhw_mode=g\nchannel=5\nwpa=0\nrsn_pairwise=CCMP\nbeacon_int=100\nauth_algs=3\nmacaddr_acl=1\naccept_mac_file=/etc/hostapd/accept\nwmm_enabled=0\neap_reauth_period=360000000"

		fo.write(conf)
		fo.close()

		# Nintendo Zone identity acquired for PiPass spoofing.
		print("Spoofing as " + currentMAC + " on " + currentSSID + " ( " + currentDesc + ") for " + str(STREETPASS_CYCLE_MINUTES) + " minute(s).")

		# Pause PiPass before moving onto the next Nintendo Zone. Get those Mii's! Sleep takes in seconds so multiply by 60 to convert to minutes.
		time.sleep(STREETPASS_CYCLE_MINUTES * 60)

	# If the user has issued a stop, then exit out of PiPass.
	if piPassStatus == "stop\n":
		break

print("\n[ Stop Detected! - PiPass has exited successfully. ]\n")
