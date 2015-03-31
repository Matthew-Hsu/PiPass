# Status Update - 03/30/2015
There is a small unecessary update to PiPass 1.1. PiPass will traverse the current list being used in random order now. If this feature is useful to you, you can download piPass.py from the master branch and overwrite it with piPass.py that exists in PiPass 1.1. This feature does not warrant a version change yet and will be included PiPass 1.2. Right now, I want the Dashboard to provide a grapical interface for those who want to fine tune some configurations. (e.g., StreetPass Cycle Time, Google SpreadSheets URL). Refer to 'Updating PiPass Manually' if you want more information on how to update PiPass to currently in developed features.

# PiPass - Nintendo 3DS Homepass for the Raspberry Pi
PiPass turns your Raspberry Pi into a Nintendo 3DS Homepass Relay Station. The PiPass Dashboard can be accessed through a computer or mobile device. It can manage features without the need of opening up any files manually. However, fine tuning of the database source and network configuration will require getting your hands 'dirty'. Though the process is relatively fast and easy.

# What's New in Version 1.1
PiPass now pulls data from Google Spreadsheets. PiPass uses a custom Spreadsheet instead because the data on http://www.homepass.info is a little bit more difficult to parse with additional comments and formatting.

The base installation will default to using the extended MACs found on FatMagic's database. The custom spreadsheet that PiPass is using won't be updated regulary, unless it needs to be fixed. It is good for general purpose Homepass usage.

Moving to Google Spreadsheets allows for the possilibty of viewing and pulling data from FatMagic's database when the data inputs follow a standard convention. The intention to move to Google Spreadsheets is to allow for easier maintenance of custom Nintendo Zone databases that is both user friendly and to leverage online backups.

# Testing Environment
Development and testing was done using all the components from the Canakit Raspberry Pi 2 Complete Starter Kit with WiFi. A -=new=- Nintendo 3DS XL with the 9.6.0-24 U firmware was used to verify functionality of 'Homepass'.

PiPass has drivers preinstalled for Ralink, ZyDAS ZD1211/1211B, and Atheros AR5007UG chipsets. The WiFi chipset that I tested on was the Ralink RT5370. These chipsets were tested to be working for 'Homepass', so I've loaded the drivers for these other chipsets as well.

# Installation
PiPass can be installed by downloading a pre-made image for your Raspberry Pi or by downloading the source files here on GitHub and setting it up manually. Manual setup will be more work, but it has the advantage of being able to use PiPass on most Linux based operating systems that are not just limited to the Raspberry Pi.

<b>PiPass Premade Image</b>

PiPass can be downloaded through these mirrors:

* <a href="https://drive.google.com/folderview?id=0B8bbfqFbkJvVfk55dzhwWUZNUkNpQ2lXMHk3bnZXOUl5V2FlOTZqX2RmZE9OQWZQOEJZYjA&usp=sharing" target="_blank">Mirror 1 @ Google Drive</a>.
* <a href="https://www.dropbox.com/sh/91rdhi212d1vqnj/AADKzZCSQg89t68nU5R_quu9a?dl=0" target="_blank">Mirror 2 @ Dropbox</a>.

The PiPass image was built using <a href="https://minibianpi.wordpress.com/" target="_blank">Minibian</a>, a light weight image based on the Raspbian operating system. I have not tested PiPass on the Raspberry Pi B and the Raspberry Pi B+ models, but Minibian is backwards compatible and PiPass should be fine. The smallest SD card at my availability was 4GB, so a 4GB SD card will be required at minimum. The actual "real" size of everything is just a little over 500MB.

If you are not sure on how to install an image onto your SD card, the following guide here does an excellent job in explaining how to do this for all three major platforms:
* <a href="http://www.raspberrypi.org/documentation/installation/installing-images/" target="_blank">Installing Images</a>.

Once you have the PiPass image onto your SD card, you can now load PiPass into your Raspberry Pi. Depending on how you will be operating your Raspberry Pi, the following guide is good if you will be accessing your Raspberry Pi remotely through another computer:
* <a href="http://www.raspberrypi.org/documentation/remote-access/ssh/README.md" target="_blank">Using SSH</a>.
* <a href="http://www.raspberrypi.org/documentation/troubleshooting/hardware/networking/ip-address.md" target="_blank">Finding Your IP Address</a>.

Root access is only configured and the username and password is:

    +   Username:   root
    +   Password:   PiPass

For security sake, PiPass will only work on the Nintendo 3DS that you authorize. Type in the following command:

    ->  nano /etc/hostapd/mac_accept

This file will contain the list of all devices that are authorized to work with PiPass. Go to your Nintendo 3DS and open up your connection settings to find out your 3DS' MAC address. Once you have your MAC address, you can add it to the file. Each MAC address should be on its own seperate line.

The PiPass image uses your router's DHCP to handle the networking aspect. Type in the following command:

    ->  service hostapd status

Generally speaking, if hostapd services are running, you should be OK. If you have a mobile device or a computer with WiFi, check to see any available networks. If the SSID of "attwifi" or "NZ@McD1" show up, you are in luck. If both these things look good, your 3DS could have some Streetpasses already. To connect to the PiPass Dashboard, type in your Raspberry Pi's IP address in your browser or mobile device to begin.

If things don't look good, there could be some issues with your WiFi driver. PiPass has drivers preinstalled for Ralink, ZyDAS ZD1211/1211B, and Atheros AR5007UG chipsets. Check to see if your WiFi adapter is based on one of these chipsets and make sure that it can function as an "Access Point".

If problems persist, refer to the manual guide down below for some extra help. If it is a driver problem, there might be some changes that you will need to do. I've tried to make these changes easy, so if it is a driver issue, you may want to change the value of "driver=" in these two files down below:

    +   /etc/hostapd/hostapd.conf
    +   /opt/PiPass/piPass.py

<b>Manually Installing PiPass</b>

Before you begin, there is a great guide that explains in detail on how to setup a Homepass Relay Station. It is a good read and I encourage everyone to take a look at it. It is especially helpful to those who are having WiFi driver issues. The guide, written by Semperverus, can be found <a href="https://docs.google.com/document/d/1EvmIwTIjPva5MHSFEIN0qsHtRmdRRiX3WNHu_ThxnOs/edit" target="_blank">here</a>. The following instructions will assume you are familiar with Linux and will briefly explain where everything is.

Here is a list of dependencies needed for PiPass, so install the following packages through these commands:

    ->  sudo apt-get install python -y
    ->  sudo apt-get install apache2 -y
    ->  sudo apt-get install php5 -y
    ->  sudo apt-get install hostapd -y
    ->  sudo apt-get install bridge-utils -y

Download PiPass from the 1.1 branch as a zip file and extract the contents on your local machine. You will notice three directories inside PiPass: etc, opt, and var. These three directories are the locations where you want to install PiPass (e.g., Linux root locations would be /etc/, /opt/, and /var/). Go ahead and merge the directories and it will be safe to overwrite the files with PiPass' configuration files.

As a security measure, add the MAC address of your Nintendo 3DS by entering the following command:

    ->  sudo nano /etc/hostapd/mac_accept
    
Each MAC address should be on a new line.

Most of the features controlled by PiPass can actually be ran through the PiPass Dashboard. Since your Raspberry Pi will act as a web server as well, you will need to make sure it has the permissions to do so. The following commands can grant execution:

    ->  sudo chmod -R 755 /var/www/
    ->  sudo chmod -R 755 /opt/PiPass/

Now this part is a little more involved as we will need to grant the Dashboard some rights for execution. Typically, you would not want to do this on a public webpage, but since PiPass is ran locally and that we have some security measures in place, it should be fine. We'll need root access, so run the following commands:

    ->  su
    ->  visudo -f /etc/sudoers
    
Now add the following line at the end of the file:

    +   www-data ALL=(ALL:ALL) NOPASSWD: ALL
    
If you are experiencing WiFi driver problems, there might be some changes that you will need to do. I've tried to make these changes easy, so if it is a driver issue, you may want to change the value of "driver=" in these two files down below:

    +   /etc/hostapd/hostapd.conf
    +   /opt/PiPass/piPass.py

Semperverus' guide is a excellent resource for troubleshooting. With luck, you should have PiPass working manually.

# Using PiPass

<b>The PiPass Dashboard</b>

The PiPass Dashboard can be accessed on a device on your network by typing in your Raspberry Pi's IP address on your computer's or mobile device's browser. Most of what you need can be accessed through the Dashboard. However, if you want to customize PiPass, you'll have to edit some files manually.

<b>PiPass Command</b>

If you prefer to run PiPass through the terminal, instead of the dashboard, PiPass Command has a basic functional command line interface. Run the following command to see a list of options:

    ->  sudo python /opt/PiPass/piPassCommand.py

Like the dashboard, if you want to customize PiPass, you'll have to edit some files manually.

# PiPass Customization
<b>Customizing Database Source</b>

The baseline database will use the Nintendo Zones worksheet found on FatMagic's database. This section will show you how to set up a custom source where you can easily define multiple custom configurations and load them on demand.

    +   Use your own or create a Google account to store your database.

Now, make a copy of this <a href="https://drive.google.com/open?id=1OfgyryUHeCPth76ziFT985XNLS-O5EXtjQDa0kA1L6M&authuser=0" target="_blank">spreadsheet</a> and save it on Google Drive. 

    +   You can copy the spreadsheet easily by clicking "File" -> "Make a copy...".
    
Publish your spreadsheet to the Web by clicking:

    +   "File" -> "Publish to the web..."
    +   "Publish"
    
Also, make sure to copy the URL link of that spreadsheet. Now, open up piPass.py on your Raspberry Pi:

    ->  sudo nano /opt/PiPass/piPass.py

Near the top, you will see the variable PIPASS_DB. Take your spreadsheet's KEY and replace the previous KEY value. For example, the URL you just copied would look something like this:

    +   https://docs.google.com/spreadsheets/d/1OfgyryUHeCPth76ziFT985XNLS-O5EXtjQDa0kA1L6M/pubhtml

The KEY would be the value 1OfgyryUHeCPth76ziFT985XNLS-O5EXtjQDa0kA1L6M between /d/ and /pubhtml. So copy that KEY value and replace it with the previous KEY value in piPass.py:

    +   PIPASS_DB = "https://spreadsheets.google.com/feeds/list/KEY_VALUE_GOES_HERE/1/public/values?alt=json"

Save piPass.py. PiPass will now use your custom database. If problems arise, ensure that you have published your spreadsheet to the Web. This is different from sharing your spreadsheet to others.

You will also notice that in PIPASS_DB, there is a /1/ after KEY_VALUE_GOES_HERE. Changing that number, would control which worksheet you want to use. The default value of 1 selects the very first worksheet and the value of 2 selects the second worksheet. For example:

    +   PIPASS_DB = "https://spreadsheets.google.com/feeds/list/KEY_VALUE_GOES_HERE/2/public/values?alt=json"

This would use the "nintendo_zones" worksheet in the templated spreadsheet that you just copied.

<b>PiPass Nintendo Zone Cycle Time</b>

By default, PiPass will be a particular Nintendo Zone for 15 minutes, before moving onto the next one. This should give you enough time to play all the mini-games before you get your next batch. If this time is too long or too short for you, you can edit the Python script here:

    ->  sudo nano /opt/PiPass/piPass.py
    
Be careful though and try to limit your changes to the STREETPASS_CYCLE_MINUTES variable.

# Updating PiPass Manually
Updating PiPass manually is easy as you just need to download the files from the Master branch and overwrite /var/www/ and /opt/PiPass/ with the new files.

For example (On your Raspberry Pi):

    ->  sudo rm -rf /var/www/
    ->  sudo rm -rf /opt/PiPass/

Copy over the new /var/www/ and /opt/PiPass/ from your computer to your Raspberry Pi.
    
# Hardware
I have listed some kits that are quite good if you will be purchasing a Raspberry Pi for the first time. I'm not asking for any donations, but if you will be purchasing any hardware, these Amazon referal links should be helpful. The pricing on these items are exactly the same as a non-referal.

Please let me know if any other hardware is compatible and I will add them to this list.

<b>Canadian Links</b>

<a href="http://www.amazon.ca/gp/product/B00GWTNYJW/ref=as_li_ss_tl?ie=UTF8&camp=15121&creative=390961&creativeASIN=B00GWTNYJW&linkCode=as2&tag=matthew084-20">CanaKit Raspberry Pi 2 (1GB) Ultimate Starter Kit (Over 40 Components: New Raspberry Pi 2 + WiFi Dongle + 8GB SD Card + Case + Power Supply and many more)</a><img src="http://ir-ca.amazon-adsystem.com/e/ir?t=matthew084-20&l=as2&o=15&a=B00GWTNYJW" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />

<b>United States of America Links</b>

<a href="http://www.amazon.com/gp/product/B008XVAVAW/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B008XVAVAW&linkCode=as2&tag=matthew08b-20&linkId=IN557BBG3PJEAU7M">CanaKit Raspberry Pi 2 Complete Starter Kit with WiFi (Latest Version Raspberry Pi 2 + WiFi + Original Preloaded 8GB SD Card + Case + Power Supply + HDMI Cable)</a><img src="http://ir-na.amazon-adsystem.com/e/ir?t=matthew08b-20&l=as2&o=1&a=B008XVAVAW" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />

<a href="http://www.amazon.com/gp/product/B008OF9Z54/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B008OF9Z54&linkCode=as2&tag=matthew08b-20&linkId=B56OIMZL6L43DVYE">Mini USB 2.0 WiFi Wireless Adapter with Antenna, 802.11 n/g/b, 150M LAN Adapter</a><img src="http://ir-na.amazon-adsystem.com/e/ir?t=matthew08b-20&l=as2&o=1&a=B008OF9Z54" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />

# Future Features
I want to expand the functionality of PiPass by adding the following:

    +   Adding/Removing Accepted MAC Addresses through the Dashboard.
    +   Configuration for piPass.py and piPassCommands.py and control of those settings through the Dashboard.
    +   Randomized Visiting of Nintendo Zones.

# Support
If you have any problems with PiPass, please let me know through my GitHub. I will do my best to help you out. Thanks for trying out PiPass!
