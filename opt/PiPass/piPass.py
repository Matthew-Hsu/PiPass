#!/usr/bin/python

#### Imported Libraries ####

from random import shuffle
import subprocess
import signal
import urllib
import json
import time
import io

#### Support Functions ####

# Read and load settings stored in /var/www/assets/json/pipass_config.json.
def loadSettings():
    # Read the settings.
    with open('/var/www/assets/json/pipass_config.json', 'r') as f:
        pipass_config = json.load(f)
        
    # Controls the minutes between each Nintendo Zone cycle.
    global STREETPASS_CYCLE_MINUTES

    try:
        STREETPASS_CYCLE_MINUTES = int(pipass_config['STREETPASS_CYCLE_MINUTES'])
    except (KeyError, ValueError):
        STREETPASS_CYCLE_MINUTES = 15

    # Converting STREETPASS_CYCLE_MINUTES to seconds.
    global STREETPASS_CYCLE_SECONDS
    STREETPASS_CYCLE_SECONDS = STREETPASS_CYCLE_MINUTES * 60

    # Controls whether PiPass should shuffle the Nintendo Zone list or not.
    global PIPASS_SHUFFLE

    try:
        PIPASS_SHUFFLE = pipass_config['PIPASS_SHUFFLE']
    except KeyError:
        PIPASS_SHUFFLE = "off"

    # The Google Spreadsheet's KEY that is used for PIPASS_DB.
    global GSX_KEY

    try:
        GSX_KEY = pipass_config['GSX_KEY']
    except KeyError:
        GSX_KEY = "1OfgyryUHeCPth76ziFT985XNLS-O5EXtjQDa0kA1L6M"

    # The Google Spreadsheet's WORKSHEET that is used for PIPASS_DB.
    global GSX_WORKSHEET

    try:
        GSX_WORKSHEET = pipass_config['GSX_WORKSHEET']
    except KeyError:
        GSX_WORKSHEET = "2"

    # Contructs the URL where the Google Spreadsheet is located for the
    # Nintendo Zone information. Refer to README at
    # https://github.com/Matthew-Hsu/PiPass/blob/master/README.md
    global PIPASS_DB
    PIPASS_DB = "https://spreadsheets.google.com/feeds/list/" + GSX_KEY + "/" + GSX_WORKSHEET + "/public/values?alt=json"

    # Hostapd driver for your USB WiFi dongle. If the default value does not work for
    # you, you may need to research which driver is compatible. Refer to README at
    # https://github.com/Matthew-Hsu/PiPass/blob/master/README.md
    global HOSTAPD_DRIVER

    try:
        HOSTAPD_DRIVER = pipass_config['HOSTAPD_DRIVER']
    except KeyError:
        HOSTAPD_DRIVER = "nl80211"

    return None

# Handles SIGUSR1, which is interpreted as a request to update settings.
def sigUsr1(signum, stack):
    global piPassStatus
    piPassStatus = "update"

    loadSettings()

    print("\n< Update Detected! - Using the updated configuration. >\n")

    return None

# Handles SIGUSR2, which is interpreted as a request to advance to the next Nintendo Zone.
def sigUsr2(signum, stack):
    # The time elapsed loop records its start time in "start". By setting to 0,
    # this forces the elapsed time to a huge number which results in advancing
    # to the next Nintendo Zone.
    global start
    start = 0

    print("\n< Advance Detected! - Advancing to the next Nintendo Zone. >\n")

    return None

#### Load PiPass Settings ####

# PiPass configuration variables. They will be overidded with correct values from loadSettings().
STREETPASS_CYCLE_MINUTES = None
STREETPASS_CYCLE_SECONDS = None
PIPASS_SHUFFLE = None
GSX_KEY = None
GSX_WORKSHEET = None
PIPASS_DB = None
HOSTAPD_DRIVER = None

loadSettings()

#### PiPass Support - MODIFY AT YOUR OWN RISK ####

# Network configuration file path for PiPass to spoof as a Nintendo Zone.
NETWORK_CONFIGURATION = "/etc/hostapd/hostapd.conf"

# Path to the JSON file where PiPass will write to for the PiPass Dashboard to display connection information.
DASHBOARD_INFO = "/var/www/assets/json/current_state.json"

# Path to the JSON file where PiPass will write to for the 'Show Current' page on the PiPass Dashboard.
CURRENT_LIST = "/var/www/assets/json/current_list.json"

# Time interval in seconds that StreetPass requires between successive visits to a Nintendo Zone.
STREETPASS_VISIT_INTERVAL = 8 * 60 * 60

# Flag that informs PiPass that updates have been made to PIPASS_DB and to use those updates. Default value is "execute".
piPassStatus = "execute"

#### PiPass Main #####

print("[ PiPass - Homepass for the Nintendo 3DS ]\n")

# Lighting the beacons...
signal.signal(signal.SIGUSR1, sigUsr1)
signal.signal(signal.SIGUSR2, sigUsr2)

print("> PiPass is currently running...")

# Indicates whether the Zone visit records need to be cleared. It is set to
# True initially so that it initializes on the first pass.
clearVisits = True

# This loop does not feel pity or remorse or fear and it cannot be stopped unless Half-Life 3 is released.
while "Waiting for Half-Life 3":
    # Load the Nintendo Zone information from PIPASS_DB.
    response = urllib.urlopen(PIPASS_DB)
    results = json.loads(response.read())
    
    # Shall we shuffle the Nintendo Zone list?
    if PIPASS_SHUFFLE == "on":
        # Shuffle results, so each list pass through is different each time.
        shuffle(results['feed']['entry'])

    # Write the current list being used to CURRENT_LIST.
    with io.open(CURRENT_LIST, 'w', encoding='utf-8') as f:
        f.write(unicode(json.dumps(results, ensure_ascii=False)))

    # The index of the current Nintendo Zone we are visting.
    currentZoneIndex = 0

    # Clear the Zone visits if needed by redefining to an empty dictionary.
    if clearVisits:
        zoneVisits = {}

    # Indicate the the visits should be cleared on the next loop. This will be
    # overridden if a usable Zone is found.
    clearVisits = True

    # Begin looping through all the Nintendo Zones in the collection.
    for data in results['feed']['entry']:
        # If the user has issued an update, then restart with the updated Nintendo Zones.
        if piPassStatus == "update":
            piPassStatus = "execute"

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

	# Zone visits use a key based on the SSID and the MAC address. The MAC
	# address is forced to uppercase to detect duplicates that might vary
	# by case.
        visit = (zoneValues[0], zoneValues[1].upper())

        # If the Zone was visited too recently, skip it.
        try:
            if time.time() - zoneVisits[visit] < STREETPASS_VISIT_INTERVAL:
                continue
        except KeyError:
            pass

        # A usable zone was found, so visits should not get cleared on the next pass.
        clearVisits = False

        # Note the current time for the current visit to the zone.
        zoneVisits[visit] = time.time()

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

        # Restart hostapd to ensure NETWORK_CONFIGURATION is used and pause for STREETPASS_CYCLE_MINUTES until moving onto the next Nintendo Zone.
        # Restarting hostapd will also ensure that it is running if it is currently off.
        subprocess.Popen('sudo service hostapd restart', shell=True, stdout=subprocess.PIPE)

        # Receiving SIGUSR1 or SIGUSR2 will interrupt the time.sleep call. The loop allows
        # for sleep to be resumed up to the current cycle setting.
        start = time.time()
        while time.time() - start < STREETPASS_CYCLE_SECONDS:
            time.sleep(5)
