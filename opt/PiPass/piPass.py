#!/usr/bin/python

#### Imported Libraries ####

import os
import io
import time
import json
import urllib
import signal
import os.path
import logging
import datetime
import subprocess
import logging.handlers

from random import shuffle

#### Logging Support ####

LOG_FILENAME = '/opt/PiPass/logs/piPass.log'

# We only want to keep the log file of the current execution of PiPass.
if os.path.isfile(LOG_FILENAME):
    subprocess.call('sudo rm ' + LOG_FILENAME, stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'), shell=True)

# Set up a specific logger with the desired output level.
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Add the log message handler to the logger.
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1048576, backupCount=0)

# Create a logging format.
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

#### Support Functions ####

# Read and load the path to where the PiPass Dashboard is installed.
def loadDashboard():
    # Read the settings.
    try:
        with open('/opt/PiPass/config/pipass_dashboard.json', 'r') as f:
            pipass_dashboard = json.load(f)
    except IOError:
        logger.error('Unable to read the file: /opt/PiPass/config/pipass_dashboard.json.')
        updateStatus('Not Available', 'Not Available', 'PiPass is not running')
        logger.info('PiPass has been shutdown with an error.')
        exit(1)

    # Controls the location to where the PiPass Dashboard is installed.
    global DASHBOARD

    # Path to the JSON file where PiPass will write to for the PiPass Dashboard to display connection information.
    global DASHBOARD_INFO

    # Path to the JSON file where PiPass will write to for the PiPass Dashboard to calculate the time until the next Nintendo Zone.
    global CURRENT_ZONE_END_TIME

    # Path to the JSON file where PiPass will write to for the 'Show Current' page on the PiPass Dashboard.
    global CURRENT_LIST

    try:
        DASHBOARD = pipass_dashboard['DASHBOARD']
    except KeyError:
        DASHBOARD = "/var/www/"
        logger.warning('Missing the DASHBOARD key in: /opt/PiPass/config/pipass_dashboard.json. Defaulting to: ' + DASHBOARD + '.')

    DASHBOARD_INFO = DASHBOARD + "assets/json/current_state.json"
    CURRENT_ZONE_END_TIME = DASHBOARD + "assets/json/current_zone_end_time.json"
    CURRENT_LIST = DASHBOARD + "assets/json/current_list.json"

    return None

# Read and load settings stored in {DASHBOARD}assets/json/pipass_config.json.
def loadSettings():
    # Read the settings.
    try:
        with open(DASHBOARD + 'assets/json/pipass_config.json', 'r') as f:
            pipass_config = json.load(f)
    except IOError:
        logger.error('Unable to read the file: ' + DASHBOARD + 'assets/json/pipass_config.json.')
        updateStatus('Not Available', 'Not Available', 'PiPass is not running')
        logger.info('PiPass has been shutdown with an error.')
        exit(1)

    # Controls the minutes between each Nintendo Zone cycle.
    global STREETPASS_CYCLE_MINUTES

    try:
        STREETPASS_CYCLE_MINUTES = int(pipass_config['STREETPASS_CYCLE_MINUTES'])

        if STREETPASS_CYCLE_MINUTES < 1:
            STREETPASS_CYCLE_MINUTES = 30
            logger.warning('The value for the STREETPASS_CYCLE_MINUTES key in: ' + DASHBOARD + 'assets/json/pipass_config.json is less than one. Defaulting to: ' + str(STREETPASS_CYCLE_MINUTES) + '.')
    except KeyError:
        STREETPASS_CYCLE_MINUTES = 30
        logger.warning('Missing the STREETPASS_CYCLE_MINUTES key in: ' + DASHBOARD + 'assets/json/pipass_config.json. Defaulting to: ' + str(STREETPASS_CYCLE_MINUTES) + '.')
    except ValueError:
        STREETPASS_CYCLE_MINUTES = 30
        logger.warning('Invalid value for the STREETPASS_CYCLE_MINUTES key in: ' + DASHBOARD + 'assets/json/pipass_config.json. Defaulting to: ' + str(STREETPASS_CYCLE_MINUTES) + '.')

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
        logger.warning('Missing the GSX_KEY key in: ' + DASHBOARD + 'assets/json/pipass_config.json. Defaulting to: ' + GSX_KEY + '.')

    # The Google Spreadsheet's WORKSHEET that is used for PIPASS_DB.
    global GSX_WORKSHEET

    try:
        GSX_WORKSHEET = pipass_config['GSX_WORKSHEET']
    except KeyError:
        GSX_WORKSHEET = "2"
        logger.warning('Missing the GSX_WORKSHEET key in: ' + DASHBOARD + 'assets/json/pipass_config.json. Defaulting to: ' + GSX_WORKSHEET + '.')

    # Constructs the URL where the Google Spreadsheet is located for the
    # Nintendo Zone information. Refer to README at
    # https://github.com/Matthew-Hsu/PiPass/blob/master/README.md
    global PIPASS_DB
    PIPASS_DB = "https://spreadsheets.google.com/feeds/list/" + GSX_KEY + "/" + GSX_WORKSHEET + "/public/values?alt=json"

    # Controls whether PiPass should have WiFi security enabled or disabled.
    global HOSTAPD_SECURITY

    try:
        HOSTAPD_SECURITY = pipass_config['HOSTAPD_SECURITY']
    except KeyError:
        HOSTAPD_SECURITY = "0"

    # Hostapd uses a binary flag to signal if WiFi security is enabled or disabled. So, perform the conversions here.
    if HOSTAPD_SECURITY == "on":
        HOSTAPD_SECURITY = "1"
    else:
        HOSTAPD_SECURITY = "0"

    # Hostapd driver for your WiFi adapter. If the default value does not work for
    # you, you may need to research which driver is compatible. Refer to README at
    # https://github.com/Matthew-Hsu/PiPass/blob/master/README.md
    global HOSTAPD_DRIVER

    try:
        HOSTAPD_DRIVER = pipass_config['HOSTAPD_DRIVER']
    except KeyError:
        HOSTAPD_DRIVER = "nl80211"
        logger.warning('Missing the HOSTAPD_DRIVER key in: ' + DASHBOARD + 'assets/json/pipass_config.json. Defaulting to: ' + HOSTAPD_DRIVER + '.')

    return None

# Reset the PiPass Dashboard.
def updateStatus(mySSID, myMAC, myDescription):
    try:
        with io.open(DASHBOARD_INFO, 'w', encoding='utf-8') as f:
            f.write(unicode('[{"gsx$ssid": {"$t": "' + mySSID + '."}, "gsx$mac": {"$t": "' + myMAC + '."}, "gsx$description": {"$t": "' + myDescription + '."}}]'))
    except IOError:
        logger.error('Unable to write the file: ' + DASHBOARD_INFO + '.')
        logger.info('PiPass has been shutdown with an error.')
        exit(1)

    try:
        with io.open(CURRENT_ZONE_END_TIME, 'w', encoding='utf-8') as f:
            f.write(unicode('{"CURRENT_ZONE_END_TIME":"0", "STREETPASS_CYCLE_SECONDS":"0"}'))
    except IOError:
        logger.error('Unable to write the file: ' + CURRENT_ZONE_END_TIME + '.')
        logger.info('PiPass has been shutdown with an error.')
        exit(1)

    return None

# Update the end time for the current Nintendo Zone.
def updateZoneEndTime(myZoneStartTime, mySteetPassCycleSeconds):
    try:
        with io.open(CURRENT_ZONE_END_TIME, 'w', encoding='utf-8') as f:
            f.write(unicode('{"CURRENT_ZONE_END_TIME":"' + str(myZoneStartTime + mySteetPassCycleSeconds) + '", "STREETPASS_CYCLE_SECONDS":"' + str(mySteetPassCycleSeconds) + '"}'))
    except IOError:
        logger.error('Unable to write the file: ' + CURRENT_ZONE_END_TIME + '.')
        logger.info('PiPass has been shutdown with an error.')
        exit(1)

    return None

# Determines the network connectivity status of PiPass.
def isNetworkConnected():
    global isDisconnected

    while True:
        # Ping the OpenDNS server to determine if PiPass has Internet access.
        if subprocess.call('sudo ping -c 3 208.67.222.222', stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'), shell=True) == 1:
            # Ping the Google DNS server to have higher certainty that the network connectivity issue is real.
            if subprocess.call('sudo ping -c 3 8.8.8.8', stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'), shell=True) == 1:
                subprocess.call('sudo service hostapd stop', stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'), shell=True)
                isDisconnected = True
                updateStatus('Not Available', 'Not Available', 'Internet access is not available. PiPass is trying to reconnect')
                logger.warning('Internet access is not available. Trying to reconnect in one minute.')
                time.sleep(60)
            else:
                return True
        else:
            return True

# Handles SIGQUIT, which is interpreted as a request to terminate PiPass.
def sigQuit(signum, stack):
    updateStatus('Not Available', 'Not Available', 'PiPass is not running')

    # The time elapsed loop records its start time in "start". By setting to 0,
    # this forces the elapsed time to a huge number which results in advancing
    # to the next Nintendo Zone.
    global start
    start = 0

    global piPassStatus
    piPassStatus = "update"

    global doExecute
    doExecute = False

    logger.info('Stop Detected - PiPass is shutting down.')

    return None

# Handles SIGUSR1, which is interpreted as a request to update settings.
def sigUsr1(signum, stack):
    global piPassStatus
    piPassStatus = "update"

    # There is a possibility that the WiFi driver can change, so let's re-test the WiFi driver if hostapd fails.
    global doTestDriver
    doTestDriver = True

    loadDashboard()
    loadSettings()

    global currentZoneStartTime
    global STREETPASS_CYCLE_SECONDS

    updateZoneEndTime(currentZoneStartTime, STREETPASS_CYCLE_SECONDS)

    logger.info('Refresh Detected - Using the updated PiPass configuration.')

    return None

# Handles SIGUSR2, which is interpreted as a request to advance to the next Nintendo Zone.
def sigUsr2(signum, stack):
    # The time elapsed loop records its start time in "start". By setting to 0,
    # this forces the elapsed time to a huge number which results in advancing
    # to the next Nintendo Zone.
    global start
    start = 0

    logger.info('Advance Detected - Advancing to the next Nintendo Zone.')

    return None

#### Load PiPass Settings ####

# PiPass configuration variables. They will be overridden with correct values from loadDashboard() and loadSettings().
DASHBOARD = None
DASHBOARD_INFO = None
CURRENT_ZONE_END_TIME = None
CURRENT_LIST = None
STREETPASS_CYCLE_MINUTES = None
STREETPASS_CYCLE_SECONDS = None
PIPASS_SHUFFLE = None
GSX_KEY = None
GSX_WORKSHEET = None
PIPASS_DB = None
HOSTAPD_SECURITY = None
HOSTAPD_DRIVER = None

loadDashboard()
loadSettings()

#### PiPass Support - MODIFY AT YOUR OWN RISK ####

# Network configuration file path for PiPass to spoof as a Nintendo Zone.
NETWORK_CONFIGURATION = "/etc/hostapd/hostapd.conf"

# Time interval in seconds that StreetPass requires between successive visits to a Nintendo Zone.
STREETPASS_VISIT_INTERVAL = (8 * 60) * 60

# Flag that informs PiPass whether to keep running or not.
doExecute = True

# Flag that informs PiPass that updates have been made to PIPASS_DB and to use those updates. Default value is "execute".
piPassStatus = "execute"

# Indicates whether the Nintendo Zone visit records need to be cleared. It is set to
# True initially so that it initializes on the first pass.
clearVisits = True

# Flag that informs PiPass if we should test for any potential hostapd driver issues.
doTestDriver = True

# The start time for the current Nintendo Zone.
currentZoneStartTime = 0

# Flag that informs PiPass if a network disconnection has been detected.
isDisconnected = False

#### PiPass Main #####

# Lighting the beacons...
signal.signal(signal.SIGQUIT, sigQuit)
signal.signal(signal.SIGUSR1, sigUsr1)
signal.signal(signal.SIGUSR2, sigUsr2)

logger.info('PiPass is now running.')

# PiPass will keep running until it is requested to stop.
while doExecute:
    # Check to see if PiPass has a network connection.
    isNetworkConnected()

    # Load the Nintendo Zone information from PIPASS_DB.
    try:
        response = urllib.urlopen(PIPASS_DB)
    except Exception:
        logger.error('Unable to read the URL: ' + PIPASS_DB + '.')
        updateStatus('Not Available', 'Not Available', 'PiPass is not running')
        logger.info('PiPass has been shutdown with an error.')
        exit(1)

    try:
        results = json.loads(response.read())
    except ValueError:
        logger.error('Unable to parse the JSON in: ' + PIPASS_DB + '.')
        updateStatus('Not Available', 'Not Available', 'PiPass is not running')
        logger.info('PiPass has been shutdown with an error.')
        exit(1)

    # Shall we shuffle the Nintendo Zone list?
    if PIPASS_SHUFFLE == "on":
        # Shuffle results, so each list pass through is different each time.
        shuffle(results['feed']['entry'])

    # Write the current list being used to CURRENT_LIST.
    try:
        with io.open(CURRENT_LIST, 'w', encoding='utf-8') as f:
            f.write(unicode(json.dumps(results, ensure_ascii=False)))
    except IOError:
        logger.error('Unable to write the file: ' + CURRENT_LIST + '.')
        updateStatus('Not Available', 'Not Available', 'PiPass is not running')
        logger.info('PiPass has been shutdown with an error.')
        exit(1)

    # The index of the current Nintendo Zone we are visiting.
    currentZoneIndex = 0

    # Clears the Nintendo Zone visits, if needed, by redefining to an empty dictionary.
    if clearVisits:
        zoneVisits = {}

    # Indicates that the visits should be cleared on the next loop. This will be overridden if a usable Nintendo Zone is found.
    clearVisits = True

    # Begin looping through all the Nintendo Zones in the collection.
    for data in results['feed']['entry']:
        # Ensure isDisconnected is False.
        isDisconnected = False

        # If the user has issued an update, then restart with the updated Nintendo Zones.
        if piPassStatus == "update":
            piPassStatus = "execute"

            break

        # Loop variables to store Nintendo Zone information.
        zoneValues = [' ',' ',' ']
        zoneValueIndex = 0

        # Saves the current Nintendo Zone information.
        for label in results['feed']['entry'][currentZoneIndex]:
            if label[:3]=='gsx':
                zoneValues[zoneValueIndex] = str(data[label]['$t'].encode('utf-8'))
                zoneValueIndex = zoneValueIndex + 1

        # Ensure data format consistency with MAC addresses.
        zoneValues[1] = str(zoneValues[1])
        zoneValues[1] = zoneValues[1].upper().replace("-", ":")

        # Nintendo Zone visits use a key based on the SSID and the MAC address.
        visit = (zoneValues[0], zoneValues[1])

        # If the Nintendo Zone was visited too recently, skip it.
        try:
            if (datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() - zoneVisits[visit] < STREETPASS_VISIT_INTERVAL:
                logger.info('Recent Zone Detected - Trying the next Nintendo Zone.')
                continue
        except KeyError:
            pass

        # A usable Nintendo Zone was found, so visits should not get cleared on the next pass.
        clearVisits = False

        # Shut down hostapd so NETWORK_CONFIGURATION will write out properly
        # subprocess.call() will wait for the service command to finish before moving on.
        subprocess.call('sudo service hostapd stop', stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'), shell=True)
        
        # Write the current zone information to NETWORK_CONFIGURATION.
        try:
            fo = open(NETWORK_CONFIGURATION, "w")
        except IOError:
            logger.error('Unable to write the file: ' + NETWORK_CONFIGURATION + '.')
            updateStatus('Not Available', 'Not Available', 'PiPass is not running')
            logger.info('PiPass has been shutdown with an error.')
            exit(1)

        conf = "interface=wlan0\nbridge=br0\ndriver=" + HOSTAPD_DRIVER + "\nssid=" + zoneValues[0] + "\nbssid=" + zoneValues[1] + "\nhw_mode=g\nchannel=6\nauth_algs=1\nwpa=0\nmacaddr_acl=" + HOSTAPD_SECURITY + "\naccept_mac_file=/etc/hostapd/mac_accept\nwmm_enabled=0\nignore_broadcast_ssid=0"

        fo.write(conf)
        fo.close()

        # Start hostapd to use new NETWORK_CONFIGURATION.
        # Start will also save 8+ seconds as there is a sleep(8) in the restart script.
        # subprocess.call() will wait for the service command to finish before moving on.
        subprocess.call('sudo service hostapd start', stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'), shell=True)

        # Verify that hostapd is running. If it is not, there is a possible WiFi driver issue or hostapd is using an invalid MAC address.
        hostapdStatus = subprocess.check_output('sudo ps -A', shell=True)

        # When hostapd fails to startup, it can be caused by two reasons: [1] hostapd is experiencing a WiFi driver issue or
        # [2] hostapd is trying to spoof with a invalid MAC address.
        if 'hostapd' not in hostapdStatus:
            # Test for issue [1] by getting hostapd to spoof with a known good MAC address. If hostapd still fails, there is a good chance
            # that this is a potential WiFi driver issue. Although, if hostapd passes, we do not want to perform this test every time
            # since a pass means that the WiFi driver is correctly installed and configured.
            if doTestDriver:
                # Write a known valid MAC address to NETWORK_CONFIGURATION.
                try:
                    fo = open(NETWORK_CONFIGURATION, "w")
                except IOError:
                    logger.error('Unable to write the file: ' + NETWORK_CONFIGURATION + '.')
                    updateStatus('Not Available', 'Not Available', 'PiPass is not running')
                    logger.info('PiPass has been shutdown with an error.')
                    exit(1)

                conf = "interface=wlan0\nbridge=br0\ndriver=" + HOSTAPD_DRIVER + "\nssid=" + HOSTAPD_DRIVER + "\nbssid=02:00:00:00:00:01\nhw_mode=g\nchannel=6\nauth_algs=1\nwpa=0\nmacaddr_acl=" + HOSTAPD_SECURITY + "\naccept_mac_file=/etc/hostapd/mac_accept\nwmm_enabled=0\nignore_broadcast_ssid=0"

                fo.write(conf)
                fo.close()

                # Restart hostapd to ensure NETWORK_CONFIGURATION is used. Restarting hostapd will also ensure that it is running if it is currently off.
                # subprocess.call() will wait for the service command to finish before moving on.
                subprocess.call('sudo service hostapd restart', stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'), shell=True)

                # Verify that hostapd is running. If it is not, there is a possible WiFi driver issue.
                hostapdStatus = subprocess.check_output('sudo ps -A', shell=True)

                if 'hostapd' not in hostapdStatus:
                    logger.warning('A possible WiFi driver issue has been detected.')
                    logger.error('Unable to start hostapd.')
                    updateStatus('Not Available', 'Not Available', 'PiPass is not running')
                    logger.info('PiPass has been shutdown with an error.')
                    exit(1)

                doTestDriver = False

            # If we are here, we know that issue [2] is affecting hostapd.
            logger.warning('A possible invalid MAC address has been detected: ' + zoneValues[1] + '.')
            logger.error('Unable to start hostapd.')
            updateStatus('Not Available', 'Not Available', 'PiPass is not running')
            logger.info('PiPass is moving onto the next Nintendo Zone.')

            continue

        # Verify that the WiFi adapter is actually able to change MAC addresses.
        currentWirelessMAC = subprocess.check_output("sudo ifconfig wlan0 | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'", shell=True)
        currentWirelessMAC = currentWirelessMAC.upper().replace('\n', '')

        if currentWirelessMAC != zoneValues[1]:
            logger.warning('A possible incompatible hostapd WiFi chipset has been detected.')
            logger.error('Unable to change the MAC address of the WiFi adapter.')
            updateStatus('Not Available', 'Not Available', 'PiPass is not running')
            logger.info('PiPass has been shutdown with an error.')
            exit(1)

        # Note the current time for the current visit to the Nintendo Zone.
        zoneVisits[visit] = (datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds()

        # Prepare to calculate the end time for the current Nintendo Zone.
        currentZoneStartTime = zoneVisits[visit]
        updateZoneEndTime(currentZoneStartTime, STREETPASS_CYCLE_SECONDS)

        # Nintendo Zone identity acquired for PiPass spoofing.
        logger.info('Spoofing as ' + zoneValues[1] + ' on ' + zoneValues[0] + ' ( ' + zoneValues[2] + ' ) for ' + str(STREETPASS_CYCLE_MINUTES) + ' minute(s).')

        # Write PiPass status to DASHBOARD_INFO.
        try:
            with io.open(DASHBOARD_INFO, 'w', encoding='utf-8') as f:
                f.write(unicode('['))
                f.write(unicode(json.dumps(results['feed']['entry'][currentZoneIndex], ensure_ascii=False)))
                f.write(unicode(']'))
        except IOError:
            logger.error('Unable to write the file: ' + DASHBOARD_INFO + '.')
            updateStatus('Not Available', 'Not Available', 'PiPass is not running')
            logger.info('PiPass has been shutdown with an error.')
            exit(1)

        currentZoneIndex = currentZoneIndex + 1

        # Receiving SIGUSR1 or SIGUSR2 will interrupt the time.sleep call. The loop allows
        # for sleep to be resumed up to the current cycle setting.
        start = (datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds()
        while (datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() - start < STREETPASS_CYCLE_SECONDS:
            # Verify network connection. If network connectivity is lost, we want to halt StreetPass cycling and attempt to reconnect.
            # Once reconnected, move to the next Nintendo Zone in the list.
            if isNetworkConnected() and isDisconnected:
                break

            time.sleep(5)

logger.info('PiPass has been shutdown successfully.')

exit(0)
