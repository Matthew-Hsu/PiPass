#!/usr/bin/python

#### Imported Libraries ####

import subprocess
import urllib
import json
import time
import io

#### Configuration Variables - Adjust to your Preferences ####

# Controls the minutes between each Nintendo Zone cycle.
STREETPASS_CYCLE_MINUTES = 15

# URL where the Google Spreadsheet is located for the Nintendo Zone information. Refer to README at
# https://github.com/Matthew-Hsu/PiPass/blob/master/README.md
PIPASS_DB = "https://spreadsheets.google.com/feeds/list/1OfgyryUHeCPth76ziFT985XNLS-O5EXtjQDa0kA1L6M/2/public/values?alt=json"

# Hostapd driver for your USB WiFi dongle. If the default value does not work for
# you, you may need to research which driver is compatible. Refer to README at
# https://github.com/Matthew-Hsu/PiPass/blob/master/README.md
HOSTAPD_DRIVER = "nl80211"

#### PiPass Support - MODIFY AT YOUR OWN RISK ####

# Network configuration file path for PiPass to spoof as a Nintendo Zone.
NETWORK_CONFIGURATION = "/etc/hostapd/hostapd.conf"

# Path to the JSON file where PiPass will write to for the PiPass Dashboard to display connection information.
DASHBOARD_INFO = "/var/www/assets/json/current_state.json"

# Path to the JSON file where PiPass will write to for the 'Show Current' page on the PiPass Dashboard.
CURRENT_LIST = "/var/www/assets/json/current_list.json"

# Flag that informs PiPass that updates have been made to PIPASS_DB and to use those updates. Default value is "execute".
piPassStatus = "execute"

# Temporary flag file path for piPassStatus.
FLAG_PATH = "/tmp/pipass_flag.txt"

# Converting STREETPASS_CYCLE_MINUTES to seconds.
STREETPASS_CYCLE_SECONDS = STREETPASS_CYCLE_MINUTES * 60

# Constructing hostapd command string.
COMMAND = "timeout " + str(STREETPASS_CYCLE_SECONDS) + " hostapd " + NETWORK_CONFIGURATION

#### PiPass Main #####

print("[ PiPass - Homepass for the Nintendo 3DS ]\n")

# Ensure that hostapd is running.
subprocess.Popen("sudo service hostapd start", shell=True, stdout=subprocess.PIPE)
print("> Starting up hostapd services...")
time.sleep(5)

# Create/Overwrite flag file for piPassStatus.
fo = open(FLAG_PATH, "w")
fo.write(piPassStatus)
fo.close()

print("> PiPass is currently running...")

# This loop does not feel pity or remorse or fear and it cannot be stopped unless Half-Life 3 is released.
while "Waiting for Half-Life 3":
    # Load the Nintendo Zone information from PIPASS_DB.
    response = urllib.urlopen(PIPASS_DB)
    results = json.loads(response.read())
    
    # Write the current list being used to CURRENT_LIST.
    with io.open(CURRENT_LIST, 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(results, ensure_ascii=False)))

    # The index of the current Nintendo Zone we are visting.
    currentZoneIndex = 0

    # Begin looping through all the Nintendo Zones in the collection.
    for data in results['feed']['entry']:
        # Open the flag file and read in the value.
        fo = open(FLAG_PATH)
        piPassStatus = fo.read()
        fo.close()

        # If the user has issued an update, then reload PIPASS_DB for the updated Nintendo Zones.
        if piPassStatus == "update\n":
            # We want PiPass to keep running.
            piPassStatus = "execute"

            # Overwrite flag file for piPassStatus.
            fo = open(FLAG_PATH, "w")
            fo.write(piPassStatus)
            fo.close()

            print("\n< Update Detected! - Using new updated Nintendo Zones. >\n")

            break

        # Write the current zone information to NETWORK_CONFIGURATION.
        fo = open(NETWORK_CONFIGURATION, "w")

        # Loop variables to store Nintendo Zone information.
        zoneValues = [' ',' ',' ']
        zoneValueIndex = 0
        
        # Saves the current Nintendo Zone information.
        for label in results['feed']['entry'][currentZoneIndex]:
            if label[:3]=='gsx':
                zoneValues[zoneValueIndex] = str(data[label]['$t'].encode('utf-8'))
                zoneValueIndex = zoneValueIndex + 1

        conf = "interface=wlan0\nbridge=br0\ndriver=" + HOSTAPD_DRIVER + "\nssid=" + zoneValues[0] + "\nbssid=" + zoneValues[1] + "\nhw_mode=g\nchannel=6\nauth_algs=1\nwpa=0\nmacaddr_acl=1\naccept_mac_file=/etc/hostapd/mac_accept\nwmm_enabled=0\nignore_broadcast_ssid=0"

        fo.write(conf)
        fo.close()

        # Nintendo Zone identity acquired for PiPass spoofing.
        print("> Spoofing as " + zoneValues[1] + " on " + zoneValues[0] + " ( " + zoneValues[2] + " ) for " + str(STREETPASS_CYCLE_MINUTES) + " minute(s).")

        # Write PiPass status to DASHBOARD_INFO.
        with io.open(DASHBOARD_INFO, 'w', encoding='utf-8') as f:
            f.write(unicode('['))
            f.write(unicode(json.dumps(results['feed']['entry'][currentZoneIndex], ensure_ascii=False)))
            f.write(unicode(']'))

        currentZoneIndex = currentZoneIndex + 1

        # Run current Nintendo Zone and pause for STREETPASS_CYCLE_MINUTES until moving onto the next Nintendo Zone.
        subprocess.Popen(COMMAND, shell=True, stdout=subprocess.PIPE)
        time.sleep(STREETPASS_CYCLE_SECONDS)
