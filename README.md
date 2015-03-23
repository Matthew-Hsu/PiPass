# PiPass - Nintendo 3DS Homepass for the Raspberry Pi
PiPass turns your Raspberry Pi into a Nintendo 3DS Homepass Relay Station. The PiPass Dashboard can manage most of the features without the need of opening up any files manually. The dashboard is adaptive, so you will be able to control most of the features of PiPass using your Web browser and even your mobile device. Though there is some setting up to do that will require getting your hands 'dirty'.

# Testing Environment
Development and testing was done using all the components from the Canakit Raspberry Pi 2 Complete Starter Kit with WiFi. A *new* Nintendo 3DS XL with the 9.5.0-22 U firmware was used to verify functionality of 'Homepass'.

# Installation
PiPass can be installed by downloading a pre-made image for your Raspberry Pi or by downloading the source files here on GitHub and setting it up manually. Manual setup will be more work, but it has the advantage of being able to use PiPass on most Linux based operating systems that are not just limited to the Raspberry Pi.

<b>PiPass Premade Image</b>

PiPass can be downloaded through these mirrors:

* <a href="https://drive.google.com/folderview?id=0B8bbfqFbkJvVfk55dzhwWUZNUkNpQ2lXMHk3bnZXOUl5V2FlOTZqX2RmZE9OQWZQOEJZYjA&usp=sharing" target="_blank">Mirror 1 @ Google Drive</a>.
* <a href="https://www.dropbox.com/sh/91rdhi212d1vqnj/AADKzZCSQg89t68nU5R_quu9a?dl=0" target="_blank">Mirror 2 @ Dropbox</a>.

The PiPass image was built using <a href="https://minibianpi.wordpress.com/" target="_blank">Minibian</a>, a light weight image based on the Raspbian operating system. The smallest SD card at my availability was 4GB, so a 4GB SD card will be required at minimum. The actual "real" size of everything is just a little over 500MB.

If you are not sure on how to install an image onto your SD card, the following guide here does an excellent job in explaining how to do this for all three major platforms:
* <a href="http://www.raspberrypi.org/documentation/installation/installing-images/" target="_blank">Installing Images</a>.

Once you have the PiPass image onto your SD card, you can now load PiPass into your Raspberry Pi. Depending on how you will be operating your Raspberry Pi, the following guide is good if you will be accessing your Raspberry Pi remotely through another computer:
* <a href="http://www.raspberrypi.org/documentation/remote-access/ssh/README.md" target="_blank">Using SSH</a>.
* <a href="http://www.raspberrypi.org/documentation/troubleshooting/hardware/networking/ip-address.md" target="_blank">Finding Your IP Address</a>.

Root access is only configured and the password for root is:

    +   PiPass

I've used common configurations, so the installation of PiPass could be finished here. For security sake, PiPass will only work on the Nintendo 3DS that you authorize. Type in the following command:

    ->  nano /etc/hostapd/mac_accept

This file will contain the list of all devices that are authorized to work with PiPass. Go to your Nintendo 3DS and open up your connection settings to find out your 3DS' MAC address. Once you have your MAC address, you can either replace the MAC address in the file or add yours right underneath it. Each MAC address should be on its own seperate line.

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

    +   apt-get install python -y
    +   apt-get install apache2 -y
    +   apt-get install php5 -y
    +   apt-get install hostapd -y
    +   apt-get install bridge-utils -y

Download PiPass from this main page as a zip file and extract the contents on your local machine. You will notice three directories inside PiPass-master: etc, opt, and var. These three directories are the locations where you want to install PiPass (e.g., Linux root locations would be /etc/, /opt/, and /var/). Go ahead and merge the directories and it will be safe to overwrite the files with PiPass' configuration files.

As a security measure, add the MAC address of your Nintendo 3DS by entering the following command:

    ->  sudo nano /etc/hostapd/mac_accept
    
Each MAC address should be on a new line. You can either delete and replace the MAC address currently in that file or add a new one right below it.

Most of the features controlled by PiPass can actually be ran through the PiPass Dashboard. Since your Raspberry Pi will act as a web server as well, you will need to make sure it has the permissions to do so. The following commands can grant execution:

    ->  sudo chmod -R 755 /var/www/
    ->  sudo chmod -R 755 /opt/PiPass/

Now this part is a little more involved as we will need to grant the Dashboard some rights for execution. Typically, you would not want to do this on a public webpage, but since PiPass is ran locally and that we have some security measures in place, it should be fine. We'll need root access, so run the following commands:

    ->  su
    ->  visudo -f /etc/sudoers
    
Now add the following line at the end of the file:

    ->  www-data ALL=(ALL:ALL) NOPASSWD: ALL
    
If you are experiencing WiFi driver problems, there might be some changes that you will need to do. I've tried to make these changes easy, so if it is a driver issue, you may want to change the value of "driver=" in these two files down below:

    +   /etc/hostapd/hostapd.conf
    +   /opt/PiPass/piPass.py

Semperverus' guide is a excellent resource for troubleshooting. With luck, you should have PiPass working manually.

# Using PiPass
The PiPass Dashboard can be accessed by typing in your Raspberry Pi's IP address in your browser window or mobile device. Most of what you need can be accessed through the Dashboard. However, if you want to customize PiPass, you'll have to edit some files manually.

I've added a good chunk of Nintendo Zones from <a href="https://docs.google.com/spreadsheet/ccc?key=0AvvH5W4E2lIwdEFCUkxrM085ZGp0UkZlenp6SkJablE#gid=0" target="_blank">FatMagic's list</a>. If you want to add more Nintendo Zones or remove some, you can edit the XML file by entering the following command:

    ->  sudo nano /var/www/assets/xml/current_zones.xml
    
By default, PiPass will be a particular Nintendo Zone for 15 minutes, before moving onto the next one. This should give you enough time to play all the mini-games before you get your next batch. If this time is too long or too short for you, you can edit the Python script here:

    -> sudo nano /opt/PiPass/piPass.py
    
Be careful though and try to limit your changes to the STREETPASS_CYCLE_MINUTES variable.

# Hardware
I have listed some kits that are quite good if you will be purchasing a Raspberry Pi for the first time. I'm not asking for any donations, but if you will be purchasing any hardware, these Amazon referal links should be helpful. The pricing on these items are exactly the same as a non-referal. As for WiFi adapters, any Ralink RT5370 based chipset should be compatible.

Please let me know if any other hardware is compatible and I will add them to this list.

<b>Canadian Links</b>

<a href="http://www.amazon.ca/gp/product/B00GWTNYJW/ref=as_li_ss_tl?ie=UTF8&camp=15121&creative=390961&creativeASIN=B00GWTNYJW&linkCode=as2&tag=matthew084-20">CanaKit Raspberry Pi 2 (1GB) Ultimate Starter Kit (Over 40 Components: New Raspberry Pi 2 + WiFi Dongle + 8GB SD Card + Case + Power Supply and many more)</a><img src="http://ir-ca.amazon-adsystem.com/e/ir?t=matthew084-20&l=as2&o=15&a=B00GWTNYJW" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />

<b>United States of America Links</b>

<a href="http://www.amazon.com/gp/product/B008XVAVAW/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B008XVAVAW&linkCode=as2&tag=matthew08b-20&linkId=IN557BBG3PJEAU7M">CanaKit Raspberry Pi 2 Complete Starter Kit with WiFi (Latest Version Raspberry Pi 2 + WiFi + Original Preloaded 8GB SD Card + Case + Power Supply + HDMI Cable)</a><img src="http://ir-na.amazon-adsystem.com/e/ir?t=matthew08b-20&l=as2&o=1&a=B008XVAVAW" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />

<a href="http://www.amazon.com/gp/product/B008OF9Z54/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B008OF9Z54&linkCode=as2&tag=matthew08b-20&linkId=B56OIMZL6L43DVYE">Mini USB 2.0 WiFi Wireless Adapter with Antenna, 802.11 n/g/b, 150M LAN Adapter</a><img src="http://ir-na.amazon-adsystem.com/e/ir?t=matthew08b-20&l=as2&o=1&a=B008OF9Z54" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />

# Future Features
I want to expand the functionality of PiPass by adding the following:

    +   Adding/Removing Nintendo Zones through the Dashboard.
    +   Adding/Removing Accepted MAC Addresses through the Dashboard.
    +   Configuration for piPass.py and piPassCommands.py and control of those settings through the Dashboard.
    +   Randomized Visiting of Nintendo Zones.

# Support
If you have any problems with PiPass, please let me know through my GitHub. I will do my best to help you out. Thanks for trying out PiPass!
