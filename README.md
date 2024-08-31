# PiPass - Nintendo 3DS Homepass for the Raspberry Pi

# This project is unfortunately useless now that [Nintendo have shut down StreetPass Relay servers](https://www.nintendo.co.jp/support/information/2018/0228.html)

## Table of Contents
- [About PiPass](#about-pipass)
- [Master Branch Updates](#master-branch-updates)
- [What's New in Version 1.6](#whats-new-in-version-16)
- [Known Behaviours](#known-behaviours)
- [Helpful Information](#helpful-information)
    - [RTL8188CUS Chipset](#rtl8188cus-chipset)
    - [Receiving StreetPasses](#receiving-streetpasses)
- [Testing Environment](#testing-environment)
- [Installation](#installation)
    - [PiPass Pre-made Image](#pipass-pre-made-image)
    - [Automatic Installer](#automatic-installer)
    - [Manually Installing PiPass](#manually-installing-pipass)
- [Using PiPass](#using-pipass)
    - [The PiPass Dashboard](#the-pipass-dashboard)
- [PiPass Customization](#pipass-customization)
    - [StreetPass Cycle Time](#streetpass-cycle-time)
    - [Shuffle Zones](#shuffle-zones)
    - [Database Source Customization](#database-source-customization)
    - [Hostapd Security](#hostapd-security)
    - [3DS Authentication](#3ds-authentication)
    - [Hostapd Driver](#hostapd-driver)
    - [Dashboard Path](#dashboard-path)
- [PiPass Maintenance](#pipass-maintenance)
    - [Updating PiPass](#updating-pipass)
    - [Reset Network](#reset-network)
- [Hardware](#hardware)
    - [Canadian Links](#canadian-links)
    - [United States of America Links](#united-states-of-america-links)
- [Future Features](#future-features)
- [Support](#support)

## About PiPass
PiPass turned your Raspberry Pi into a Nintendo 3DS Homepass Relay Station. The PiPass Dashboard can be accessed through a computer or mobile device. It can manage features without the need of opening up any files manually. However, some fine-tuning may require getting your hands 'dirty'. Though the process is relatively fast and easy.

This video does not showcase a complete list of features, but it shows what PiPass looks like and how it operates: <a href="https://www.youtube.com/watch?v=g4XBIxps6Tc" target="_blank">PiPass Video Overview</a>.

If you like PiPass, please star the project on GitHub and thanks for trying out PiPass!

<strong><a href="#table-of-contents">[Back to Top]</a></strong>

## Master Branch Updates
The master branch is currently on par with PiPass 1.6.

<strong><a href="#table-of-contents">[Back to Top]</a></strong>

## What's New in Version 1.6
PiPass 1.6 builds upon on its logging system by offering relevant information for identifying a wider range of potential issues relating to WiFi chipsets and network connectivity. This new release also focuses on tightening up the dashboard to offer a better user experience.

The list of changes are as follows:

* PiPass will now accept incorrectly formatted MAC addresses that use dashes instead of colons. PiPass will internally convert dashes to colons when dealing with Nintendo Zone MAC addresses and externally make this change for authenticated MAC addresses.
* PiPass will now check network connectivity. If there is a network connectivity issue, PiPass will stop cycling and stop hostapd. Once network connectivity has been re-established, PiPass will continue cycling again.
* PiPass can now detect incompatible hostapd WiFi chipsets that are unable to change its own MAC address.
* 'PiPass Settings' uses JQuery form validation instead of HTML5 form validation.
* Added 'Time Until Next Zone' progress bar to the dashboard.
* User interface tweaks.
* HTML code cleanup.

<strong><a href="#table-of-contents">[Back to Top]</a></strong>

## Known Behaviours
PiPass sometimes does not display expected or up-to-date values. Chrome is known to be finicky with this and will NOT cause issues with PiPass. When in doubt, manually refresh your browser as this is related to browser caching.

<strong><a href="#table-of-contents">[Back to Top]</a></strong>

## Helpful Information
##### RTL8188CUS Chipset
Many people have been trying to get the RTL8188CUS chipset to work with PiPass and with other Homepass solutions as well. There is a <a href="https://github.com/Matthew-Hsu/PiPass/issues/20" target="_blank">thread</a> found in my issue list that has a discussion where someone was able to get the RTL8188CUS working with PiPass. It will require a bit of Linux knowledge to follow and so far many others have not been able to reproduce the workaround. Due to this, it is still recommended to purchase a compatible WiFi dongle that is known to work.

##### Receiving StreetPasses
When using PiPass or any other Homepass solution, you may notice that StreetPasses only occur when your Nintendo 3DS is in sleep mode. To get StreetPasses while your Nintendo 3DS is 'awake', you must ensure that your Nintendo 3DS is not connected to a network.

<strong><a href="#table-of-contents">[Back to Top]</a></strong>

## Testing Environment
Development and testing was done using all the components from the Canakit Raspberry Pi 2 Complete Starter Kit with WiFi. A -=new=- Nintendo 3DS XL with the 9.9.0-26U firmware was used to verify functionality of 'Homepass'.

The PiPass pre-made image has drivers pre-installed for Ralink, ZyDAS ZD1211/1211B, Atheros AR5007UG, and Realtek chipsets. The WiFi chipset that I tested on was the Ralink RT5370.

<strong><a href="#table-of-contents">[Back to Top]</a></strong>

## Installation
PiPass can be installed in three ways:

1. Downloading and installing a pre-made image for your Raspberry Pi 2.

2. Downloading and using a automatic installer for all Raspbian / Debian distributions. This will include the original Raspberry Pi Model B and Raspberry Pi Model B+.

3. Downloading the source code and installing PiPass manually. Others have used the manual install to fit certain Raspberry Pi customization that they have and others have successfully installed PiPass on their router running custom firmware (e.g., Tomato). Manual setup will be more work, but it has the advantage of being used on many Linux based devices that support Python.

Before moving onto your chosen installation method, please ensure that your Raspberry Pi is connected to your router via a Ethernet cable and that your WiFi USB dongle is plugged into your Raspberry Pi as well.

<strong><a href="#table-of-contents">[Back to Top]</a></strong>

##### PiPass Pre-made Image
Currently, the pre-made image can only be used for the Raspberry Pi 2. PiPass can be downloaded through these mirrors:

* <a href="https://drive.google.com/open?id=0B8bbfqFbkJvVfnE0amxxcXYyd0lMQVFwTjhnNUFRaXpnVi1YWnd2MDVUYW5tUkR6bVk3c2s&authuser=0" target="_blank">Mirror 1 @ Google Drive</a>.
* <a href="https://www.dropbox.com/sh/aflyu5ncey33fqs/AAC2AKM-udIwXSnqZuxGT4XJa?dl=0" target="_blank">Mirror 2 @ Dropbox</a>.

The PiPass image was built using <a href="https://minibianpi.wordpress.com/" target="_blank">Minibian</a>, a light weight image based on the Raspbian operating system. The smallest SD card at my availability was 4GB, so a 4GB SD card will be required at minimum. The actual "real" size of everything is just a little over 500MB.

If you are not sure on how to install an image onto your SD card, the following guide here does an excellent job in explaining how to do this for all three major platforms:
* <a href="http://www.raspberrypi.org/documentation/installation/installing-images/" target="_blank">Installing Images</a>.

Once you have the PiPass image onto your SD card, you can now load PiPass into your Raspberry Pi. Though this is not necessary, if you need to log into your Raspberry Pi, the following guide is good if you will be accessing remotely through another computer:
* <a href="http://www.raspberrypi.org/documentation/remote-access/ssh/README.md" target="_blank">Using SSH</a>.
* <a href="http://www.raspberrypi.org/documentation/troubleshooting/hardware/networking/ip-address.md" target="_blank">Finding Your IP Address</a>.

Root access is only configured and the username and password is:

    +   Username:   root
    +   Password:   PiPass

For security sake, PiPass will only work on the Nintendo 3DS systems that you authorize. Access the PiPass Dashboard by opening up a web browser on a device of your choice and enter your Raspberry Pi's IP address into the address bar. The PiPass Dashboard should be displayed. Go to your Nintendo 3DS and open up your connection settings to find out your 3DS' MAC address. Once you have your MAC address, you can add it to the authenticated list by doing the following:

    +   Click "PiPass".
    +   Click "Settings".
    +   Enter your 3DS' MAC address on a separate line and in the format of XX:XX:XX:XX:XX:XX.
    +   Click "Save".

With your 3DS' MAC address saved, you will want to start PiPass:

    +   Click "PiPass".
    +   Click "Start".
    +   Click "Start PiPass".

Wait a few seconds for the PiPass services to fully startup. At this point, you may have StreetPasses waiting for you already. If not, you may want to check the PiPass Logs for detailed information:

    +   Click "Dashboard".
    +   Click "PiPass Logs".

Generally speaking, if hostapd services are running, you should be OK. The PiPass logging system will send a warning message if a driver issue or invalid MAC address is suspected to be a problem.

If the PiPass logging system is sending a warning message regarding invalid MAC addresses, then you should make a note of the offending MAC addresses and double check if you have entered them correctly. PiPass will automatically skip invalid MAC addresses and move to the next valid Nintendo Zone in the list. Please note that some MAC addresses appear to be valid, but they are actually invalid according to hostapd. In these cases, it is best to edit PiPass DB. More information about editing PiPass DB can be found in the sections below.

For WiFi driver issues, the PiPass pre-made image has drivers pre-installed for Ralink, ZyDAS ZD1211/1211B, Atheros AR5007UG, and Realtek chipsets. Check to see if your WiFi adapter is based on one of these chipsets and make sure that it can function as an "Access Point". There might be some changes that you will need to do. I've tried to make these changes easy, so if it is a driver issue, you may want to use the PiPass Dashboard to configure the correct driver:

    +   Navigate to the PiPass Dashboard with your web browser.
    +   Click "PiPass".
    +   Click "Settings".
    +   Enter the correct driver name for "Hostapd Driver".
    +   Click "Save".

If problems persist, refer to the manual guide for some extra help.

<strong><a href="#table-of-contents">[Back to Top]</a></strong>

##### Automatic Installer
<b>NOTE: </b>The automatic installer is considered BETA at the moment. It works for me on a clean and configured image of Minibian and it should work just the same on a clean and configured image of Raspbian. If there are some issues with the installer, please let me know.

The PiPass automatic installer is meant to help those install PiPass on all models of the Raspberry Pi. Depending on the operating system, the automatic installer will work on all Raspbian / Debian distributions. Before you begin, the automatic installer assumes that you have a operating system already installed and configured on your Raspberry Pi.

The installer can be downloaded through <a href="https://drive.google.com/open?id=0B8bbfqFbkJvVflpDNWhndW5ZNVV5VkpVWWNGZUhWdjJ4bVNreGI0NXlteVBEX3NYZkRZLU0&authuser=0" target="_blank">Google Drive</a> or through <a href="https://www.dropbox.com/sh/pe2v63t476pmg9n/AADfRQVSMloUKkOhmEkGcjdwa?dl=0" target="_blank">Dropbox</a>. After downloading, simply copy install_pipass.sh to your Raspberry Pi and execute it through the terminal. There may be some permission issues, so run this command in the same directory in where you copied install_pipass.sh:

    ->    sudo chmod 755 install_pipass.sh

While in the same directory as install_pipass.sh, run this command to begin the installation:

    ->    ./install_pipass.sh

Once the installation is completed, your Raspberry Pi will restart. On another device, open up the web browser and enter the IP address of your Raspberry Pi to access the PiPass Dashboard.

For security sake, PiPass will only work on the Nintendo 3DS systems that you authorize. Go to your Nintendo 3DS and open up your connection settings to find out your 3DS' MAC address. Once you have your MAC address, you can add it to the authenticated list by doing the following:

    +   Click "PiPass".
    +   Click "Settings".
    +   Enter your 3DS' MAC address on a separate line and in the format of XX:XX:XX:XX:XX:XX.
    +   Click "Save".

With your 3DS' MAC address saved, you will want to start PiPass:

    +   Click "PiPass".
    +   Click "Start".
    +   Click "Start PiPass".

Wait a few seconds for the PiPass services to fully startup. At this point, you may have StreetPasses waiting for you already. If not, you may want to check the PiPass Logs for detailed information:

    +   Click "Dashboard".
    +   Click "PiPass Logs".

Generally speaking, if hostapd services are running, you should be OK. The PiPass logging system will send a warning message if a driver issue or invalid MAC address is suspected to be a problem.

If the PiPass logging system is sending a warning message regarding invalid MAC addresses, then you should make a note of the offending MAC addresses and double check if you have entered them correctly. PiPass will automatically skip invalid MAC addresses and move to the next valid Nintendo Zone in the list. Please note that some MAC addresses appear to be valid, but they are actually invalid according to hostapd. In these cases, it is best to edit PiPass DB. More information about editing PiPass DB can be found in the sections below.

For WiFi driver issues, the PiPass automatic installer installs drivers for Ralink, ZyDAS ZD1211/1211B, Atheros AR5007UG, and Realtek chipsets. Check to see if your WiFi adapter is based on one of these chipsets and make sure that it can function as an "Access Point". There might be some changes that you will need to do. I've tried to make these changes easy, so if it is a driver issue, you may want to use the PiPass Dashboard to configure the correct driver:

    +   Navigate to the PiPass Dashboard with your web browser.
    +   Click "PiPass".
    +   Click "Settings".
    +   Enter the correct driver name for "Hostapd Driver".
    +   Click "Save".

If problems persist, refer to the manual guide for some extra help.

<strong><a href="#table-of-contents">[Back to Top]</a></strong>

##### Manually Installing PiPass
Before you begin, there is a great guide that explains in detail on how to setup a Homepass Relay Station. It is a good read and I encourage everyone to take a look at it. It is especially helpful to those who are having WiFi driver issues. The guide, written by Semperverus, can be found <a href="https://docs.google.com/document/d/1EvmIwTIjPva5MHSFEIN0qsHtRmdRRiX3WNHu_ThxnOs/edit" target="_blank">here</a>. The following instructions will assume you are familiar with Linux and will briefly explain the installation process.

Here is a list of dependencies needed for PiPass, so install the following packages through these commands:

    ->  sudo apt-get install apache2 -y
    ->  sudo apt-get install bridge-utils -y
    ->  sudo apt-get install hostapd -y
    ->  sudo apt-get install iputils-ping -y
    ->  sudo apt-get install p7zip-full -y
    ->  sudo apt-get install php5 -y
    ->  sudo apt-get install php5-common -y
    ->  sudo apt-get install php5-cli -y
    ->  sudo apt-get install libapache2-mod-php5 -y
    ->  sudo apt-get install python -y
    ->  sudo apt-get install sudo -y

This would also be a good point where you would install the correct WiFi driver for your WiFi USB dongle. As a reference, these are the WiFi drivers that the PiPass pre-made image uses:

    ->  sudo apt-get install firmware-ralink -y
    ->  sudo apt-get install firmware-realtek -y
    ->  sudo apt-get install zd1211-firmware -y

You may want to install the following in addition to the correct WiFi driver:

    ->  sudo apt-get install firmware-linux-nonfree -y
    ->  sudo apt-get install wireless-tools -y

Now download PiPass from the 1.6 branch as a zip file and extract the contents on your local machine. You will notice three directories inside PiPass: etc, opt, and var. These three directories are the locations where you want to install PiPass (e.g., Linux root locations would be /etc/, /opt/, and /var/). Go ahead and merge the directories and it will be safe to overwrite the files with PiPass' configuration files.

Most of the features controlled by PiPass can actually be ran through the PiPass Dashboard. Since your Raspberry Pi will act as a web server as well, you will need to make sure it has the permissions to do so. The following commands can grant execution:

    ->  sudo chmod -R 755 /opt/PiPass/
    ->  sudo chmod -R 755 /var/www/

Now this part is a little more involved as we will need to grant the Dashboard some rights for execution. Typically, you would not want to do this on a public webpage, but since PiPass is ran locally and that we have some security measures in place, it should be fine. We'll need root access, so run the following commands:

    ->  su
    ->  visudo -f /etc/sudoers

Now add the following line at the end of the file:

    +   www-data ALL=(ALL:ALL) NOPASSWD: ALL

For security sake, PiPass will only work on the Nintendo 3DS systems that you authorize. Access the PiPass Dashboard by opening up a web browser on a device of your choice and enter your Raspberry Pi's IP address into the address bar. The PiPass Dashboard should be displayed. Go to your Nintendo 3DS and open up your connection settings to find out your 3DS' MAC address. Once you have your MAC address, you can add it to the authenticated list by doing the following:

    +   Click "PiPass".
    +   Click "Settings".
    +   Enter your 3DS' MAC address on a separate line and in the format of XX:XX:XX:XX:XX:XX.
    +   Click "Save".

Likewise, you can add the MAC address of your Nintendo 3DS by entering the following command:

    ->  sudo nano /etc/hostapd/mac_accept

Like the dashboard, each MAC address should be on a new line.

With the previous steps completed, you will want to start PiPass. In the PiPass Dashboard:

    +   Click "PiPass".
    +   Click "Start".
    +   Click "Start PiPass".

Wait a few seconds for the PiPass services to fully startup. At this point, you may have StreetPasses waiting for you already. If not, you may want to check the PiPass Logs for detailed information:

    +   Click "Dashboard".
    +   Click "PiPass Logs".

Generally speaking, if hostapd services are running, you should be OK. The PiPass logging system will send a warning message if a driver issue or invalid MAC address is suspected to be a problem.

If the PiPass logging system is sending a warning message regarding invalid MAC addresses, then you should make a note of the offending MAC addresses and double check if you have entered them correctly. PiPass will automatically skip invalid MAC addresses and move to the next valid Nintendo Zone in the list. Please note that some MAC addresses appear to be valid, but they are actually invalid according to hostapd. In these cases, it is best to edit PiPass DB. More information about editing PiPass DB can be found in the sections below.

For WiFi driver issues, check to see if your WiFi driver is correctly installed and working. There might be some changes that you will need to do. I've tried to make these changes easy, so if it is a driver issue, you may want to use the PiPass Dashboard to configure the correct driver:

    +   Navigate to the PiPass Dashboard with your web browser.
    +   Click "PiPass".
    +   Click "Settings".
    +   Enter the correct driver name for "Hostapd Driver".
    +   Click "Save".

If problems persist, Semperverus' guide is an excellent resource for troubleshooting. With luck, you should have PiPass working manually.

<strong><a href="#table-of-contents">[Back to Top]</a></strong>

## Using PiPass
##### The PiPass Dashboard

The PiPass Dashboard can be accessed on a device on your network by typing in your Raspberry Pi's IP address on your computer's or mobile device's browser. Most of what you need can be accessed through the Dashboard, including the ability to configure PiPass.

<strong><a href="#table-of-contents">[Back to Top]</a></strong>

## PiPass Customization
##### StreetPass Cycle Time
By default, PiPass will be a particular Nintendo Zone for 30 minutes, before moving onto the next one. This should give you enough time to play all the mini-games before you get your next batch. If this time is too long or too short for you, you can edit this setting through the PiPass Dashboard.

##### Shuffle Zones
Like most of the settings, this feature can be enabled or disabled through the PiPass Dashboard. Enabling shuffling will visit Nintendo Zones in your current list in random order, ensuring that each pass-through is different.

##### Database Source Customization
The baseline database will use the Nintendo Zones worksheet found on FatMagic's database. This section will show you how to set up a custom source where you can easily define multiple custom configurations and load them on demand.

    +   Use your own or create a Google account to store your database.

Now, make a copy of this <a href="https://drive.google.com/open?id=1OfgyryUHeCPth76ziFT985XNLS-O5EXtjQDa0kA1L6M&authuser=0" target="_blank">spreadsheet</a> and save it on Google Drive.

    +   You can copy the spreadsheet easily by clicking "File" -> "Make a copy...".

Publish your spreadsheet to the Web by clicking:

    +   "File" -> "Publish to the web..."
    +   "Publish"

Also, make sure to copy the URL link of that spreadsheet. Now, open up the PiPass Dashboard:

    +   Navigate to the PiPass Dashboard with your web browser.
    +   Click "PiPass".
    +   Click "Settings".

"PiPass DB Key" will be of interest. Take your spreadsheet's KEY and replace the previous KEY value. For example, the URL you just copied would look something like this:

    +   https://docs.google.com/spreadsheets/d/1OfgyryUHeCPth76ziFT985XNLS-O5EXtjQDa0kA1L6M/pubhtml

The KEY would be the value 1OfgyryUHeCPth76ziFT985XNLS-O5EXtjQDa0kA1L6M between /d/ and /pubhtml. So copy that KEY value and replace it with the previous KEY value.

Now you will need to enter the worksheet you want to use. "PiPass DB Worksheet" controls which worksheet to use. The default value of 1 selects the very first worksheet and the value of 2 selects the second worksheet. For example, setting PiPass DB Worksheet to the value of 2 would use the "nintendo_zones" worksheet in the templated spreadsheet that you just copied.

<b>NOTE: </b>When creating your own PiPass DB, please keep the formatting of the Google Spreadsheet consistent with the default PiPass DB. You may add / remove worksheets and change the content, but do not introduce new formatting (e.g., colouring of cells) as Google may return incorrect identifiers that PiPass will not understand.

##### Hostapd Security
This feature can be enabled or disabled through the PiPass Dashboard. Enabling security will make PiPass use the 3DS MAC addresses that are inputted in '3DS Authentication'. Disabling security will allow anyone access to your network. When disabling security, discretion is advised.

##### 3DS Authentication
The authenticated list of 3DS systems that are allowed to connect to PiPass. Enter the 3DS MAC addresses on a separate line and in the format of XX:XX:XX:XX:XX:XX. This option can be found through the dashboard.

##### Hostapd Driver
In most cases, the default hostapd driver will work. However, the driver is configurable through the dashboard if need be.

##### Dashboard Path
There are some users who use a different Linux configuration when manually installing. Configuring the dashboard install path through the PiPass Dashboard allows one the flexibility in choosing which web server is best for their purpose. However, PiPass will assume that the main program is installed in /opt/PiPass/. The PiPass Dashboard is configurable in that you may choose to install it somewhere else.

<strong><a href="#table-of-contents">[Back to Top]</a></strong>

## PiPass Maintenance
##### Updating PiPass
PiPass can be updated through the dashboard. This will pull updates from the master branch and provide PiPass with 'bleeding edge' updates. This is especially useful for those who are unfamiliar with Linux. Updating can be done by:

    +  Click 'PiPass' in the dashboard.
    +  Click 'Update'.

Please allow for 30 seconds for all the updates to complete.

##### Reset Network
This will force your Raspberry Pi to re-detect and reconfigure all Ethernet and Wifi devices. PiPass uses your very first installed WiFi dongle, so if you want PiPass to use another one instead, please remove all WiFi dongles connected to your Raspberry Pi and ensure that the one you want to use is connected before you reset the network.

<strong><a href="#table-of-contents">[Back to Top]</a></strong>

## Hardware
I have listed some kits that are quite good if you will be purchasing a Raspberry Pi for the first time. I'm not asking for any donations, but if you will be purchasing any hardware, these Amazon referral links would be helpful. The pricing on these items are exactly the same as a non-referral.

Please let me know if any other hardware is compatible and I will add them to this list.

##### Canadian Links
<a href="http://www.amazon.ca/gp/product/B00T2U7R7I/ref=as_li_ss_tl?ie=UTF8&camp=15121&creative=390961&creativeASIN=B00T2U7R7I&linkCode=as2&tag=matthew084-20">Raspberry Pi 2 Model B 1GB</a><img src="http://ir-ca.amazon-adsystem.com/e/ir?t=matthew084-20&l=as2&o=15&a=B00T2U7R7I" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />

<a href="http://www.amazon.ca/gp/product/B0096M7IJY/ref=as_li_ss_tl?ie=UTF8&camp=15121&creative=390961&creativeASIN=B0096M7IJY&linkCode=as2&tag=matthew084-20">CanaKit Raspberry Pi 2 Complete Starter Kit (Raspberry Pi 2 + WiFi + 8GB SD Card + Case + Power Supply + HDMI Cable)</a><img src="http://ir-ca.amazon-adsystem.com/e/ir?t=matthew084-20&l=as2&o=15&a=B0096M7IJY" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />

<a href="http://www.amazon.ca/gp/product/B00GWTNYJW/ref=as_li_ss_tl?ie=UTF8&camp=15121&creative=390961&creativeASIN=B00GWTNYJW&linkCode=as2&tag=matthew084-20">CanaKit Raspberry Pi 2 (1GB) Ultimate Starter Kit (Over 40 Components: New Raspberry Pi 2 + WiFi Dongle + 8GB SD Card + Case + Power Supply and many more)</a><img src="http://ir-ca.amazon-adsystem.com/e/ir?t=matthew084-20&l=as2&o=15&a=B00GWTNYJW" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />

<a href="http://www.amazon.ca/gp/product/B00OL8JSIM/ref=as_li_ss_tl?ie=UTF8&camp=15121&creative=390961&creativeASIN=B00OL8JSIM&linkCode=as2&tag=matthew084-20">Mini RT5370 150Mbps USB Wifi Wireless LAN Card 802.11 N/g/b Adapter with Antenna</a><img src="http://ir-ca.amazon-adsystem.com/e/ir?t=matthew084-20&l=as2&o=15&a=B00OL8JSIM" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />

<strong><a href="#table-of-contents">[Back to Top]</a></strong>

##### United States of America Links
<a href="http://www.amazon.com/gp/product/B00T2U7R7I/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B00T2U7R7I&linkCode=as2&tag=matthew08b-20&linkId=W2HA4PU55DSRWDWA">Raspberry Pi 2 Model B Project Board - 1GB RAM - 900 MHz Quad-Core CPU</a><img src="http://ir-na.amazon-adsystem.com/e/ir?t=matthew08b-20&l=as2&o=1&a=B00T2U7R7I" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />

<a href="http://www.amazon.com/gp/product/B008XVAVAW/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B008XVAVAW&linkCode=as2&tag=matthew08b-20&linkId=IN557BBG3PJEAU7M">CanaKit Raspberry Pi 2 Complete Starter Kit with WiFi (Latest Version Raspberry Pi 2 + WiFi + Original Preloaded 8GB SD Card + Case + Power Supply + HDMI Cable)</a><img src="http://ir-na.amazon-adsystem.com/e/ir?t=matthew08b-20&l=as2&o=1&a=B008XVAVAW" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />

<a href="http://www.amazon.com/gp/product/B00G1PNG54/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B00G1PNG54&linkCode=as2&tag=matthew08b-20&linkId=WF5DSXG3FDINKT63">CanaKit Raspberry Pi 2 (1GB) Ultimate Starter Kit (Over 40 Components: New Raspberry Pi 2 + WiFi Dongle + 8GB SD Card + Case + Power Supply and many more)</a><img src="http://ir-na.amazon-adsystem.com/e/ir?t=matthew08b-20&l=as2&o=1&a=B00G1PNG54" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />

<a href="http://www.amazon.com/gp/product/B00V39HVY0/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B00V39HVY0&linkCode=as2&tag=matthew08b-20&linkId=D5PCSSC5K4XNMGXS">SunFounder RT5370 USB Wireless Network Wifi Adapter for Raspberry Pi with 2dBi Antenna - Plug and Play</a><img src="http://ir-na.amazon-adsystem.com/e/ir?t=matthew08b-20&l=as2&o=1&a=B00V39HVY0" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />

<a href="http://www.amazon.com/gp/product/B0067NFSE2/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B0067NFSE2&linkCode=as2&tag=matthew08b-20&linkId=K7P7YF4R4Z3DFFQO">Protronix 150Mbps USB Wireless Network WIFI Adapter for Laptop Notebook 802.11N/G</a><img src="http://ir-na.amazon-adsystem.com/e/ir?t=matthew08b-20&l=as2&o=1&a=B0067NFSE2" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />

<a href="http://www.amazon.com/gp/product/B00H95C0A2/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B00H95C0A2&linkCode=as2&tag=matthew08b-20&linkId=W6TR3BCW32NGSPW7">Wifi With Antenna For Raspberry Pi - Instructions Included - PLUG and PLAY</a><img src="http://ir-na.amazon-adsystem.com/e/ir?t=matthew08b-20&l=as2&o=1&a=B00H95C0A2" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />

<strong><a href="#table-of-contents">[Back to Top]</a></strong>

## Future Features
I want to expand the functionality of PiPass by adding the following:

* Borrowing a Raspberry Pi Model B and Raspberry Pi Model B+ for an expanded list of pre-made images.
* I am always looking for suggestions, but I cannot guarantee that I will implement a requested feature. I will try my best though!

<strong><a href="#table-of-contents">[Back to Top]</a></strong>

## Support
If you have any problems with PiPass, please let me know through my GitHub. I will do my best to help you out.

<strong><a href="#table-of-contents">[Back to Top]</a></strong>
