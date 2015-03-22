# PiPass - Nintendo 3DS Homepass for the Raspberry Pi
PiPass turns your Raspberry Pi into a Nintendo 3DS Homepass Relay Station. The PiPass Dashboard can manage most of the features without the need of opening up any files manually. The dashboard is adaptive, so you will be able to control most of the features of PiPass using your Web browser and even your mobile phone. Though there are some setting up to do that will require getting your hands 'dirty'.

Given you have a compatible WiFi adapter that can be used as an Access Point, PiPass should be able to run on any version of the Raspberry Pi and even on a Linux computer.

# Testing Environment
I have developed and tested PiPass using all the components from the Canakit Raspberry Pi 2 Complete Starter Kit with WiFi. My wireless network is managed by an Apple Airport Extreme.

# Installation
Ideally, I don't want to have many hardware requirements and have PiPass be bounded by strict constraints. In the end, PiPass is just a local webpage that is powered by some Python scripts. PiPass should work on any Linux based machine.

For those that are interested, I can host an image of PiPass that can be readidly imaged onto a SD card.

There is actually a great guide already written by Semperverus that can be found <a href="https://docs.google.com/document/d/1EvmIwTIjPva5MHSFEIN0qsHtRmdRRiX3WNHu_ThxnOs/edit" target="_blank">here</a>. He does a great job in explaining how to use Linux and how to setup a Homepass Relay Station. I encourage everyone to check it out.

From here on, I will assume you are running the Raspbian operating system on your Raspberry Pi. You will have to run some terminal commands and upload PiPass as well.

<b>Hardware Setup</b>

Make sure you have your Raspberry Pi plugged into your router via an Ethernet cable. Also, make sure you have a compatible WiFi USB dongle plugged into your Raspberry Pi.

<b>Installing Dependencies</b>

Log into your Raspberry Pi and launch a terminal window. You will want to type in the following commands:

    ->  sudo apt-get -y update
    ->  sudo apt-get -y upgrade
    ->  sudo apt-get -y autoremove
    ->  sudo apt-get -y install apache2
    ->  sudo apt-get -y install php5
    ->  sudo apt-get -y install hostapd isc-dhcp-server bridge-utils

These commands will update your operating system and install additional software needed by PiPass.
    
<b>Installing PiPass</b>

Download PiPass from this main page as a zip file and extract the contents on your local machine. You will notice three directories inside PiPass-master: etc, opt, and var. These three directories are the locations where you want to install PiPass (e.g., Linux root locations would be /etc/, /opt/, and /var/). Go ahead and merge the directories and it will be safe to overwrite the files with PiPass' configuration files.

<b>PiPass Dashboard Permissions</b>

Most of the features controlled by PiPass can actually be ran through the PiPass Dashboard. Since your Raspberry Pi will act as a web server as well, you will need to make sure it has the permissions to do so. The following commands can grant execution:

    ->  sudo chmod -R 755 /var/www/
    ->  sudo chmod -R 755 /opt/PiPass/
    
Now this part is a little more involved as we will need to grant the Dashboard some rights for execution. Typically, you would not want to do this on a public webpage, but since PiPass is ran locally and that we have some security mesaures in place, it should be fine.

    ->  sudo passwd root
    
We'll need root access, so assign a password to root. Be careful of what you do as root, you'll want to make sure to do the work neccessary here and log back out. Only use root when you need to.

    ->  su
    ->  visudo -f /etc/sudoers
    
Now add the following line at the end of the file:

    ->  www-data ALL=(ALL) NOPASSWD: ALL

Press CTRL-X and save the changes at the exit prompt. Now you will want to exit root:

    ->  exit
    
If you need to login as root again, the command 'su' can be used.

<b>Configuring Network</b>

We'll need to setup your Raspberry Pi to act as a Access Point now:

    ->  ifconfig

A bunch of text will now appear on your screen. Look for 'eth0' and write down the following values for 'inet addr:' and 'Bcast:'. From here, you should notice if your IP address starts with the common 192.168.X.XXX or 10.0.X.XXX. If your IP address is 192.168.X.XXX, you'll probably want to refer to the values in this README. However, if your IP is 10.0.X.XXX, you can refer to the values in /etc/network/interfaces.

I'm using common values here, so hopefully one or the other can be used as is. Type in the following command and make any changes, if neccessary:

    ->  sudo nano /etc/network/interfaces
    - - - - - - - - - - - - - - - - - - - - - - - - - -
    auto lo
    iface lo inet loopback
    #iface eth0 inet dhcp
    auto br0
    iface br0 inet static
        address 192.168.1.155
        netmask 255.255.255.0
        network 192.168.1.0
        gateway 192.168.1.1
        broadcast 192.168.1.255
        bridge-ports eth0 wlan0
    allow-hotplug wlan0
    iface wlan0 inet static
        address 192.168.0.1
        netmask 255.255.255.0
        pre-up ifconfig wlan0 192.168.0.1
    #wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
    #iface default inet dhcp
    
The IP address of your Raspberry Pi will now be the value defined here:

    ->  iface br0 inet static
            address 192.168.1.155

So, if you are unable to connect to your Raspberry Pi, try the above IP address. Similarly, the IP address of your Access Point is defined here:

    ->  iface wlan0 inet static
            address 192.168.0.1



# Hardware
I have listed some kits that are quite good if you will be purchasing a Raspberry Pi for the first time. I'm not asking for any donations, but if you will be purchasing any hardware, these Amazon referal links should be helpful. The pricing on these items are exactly the same as a non-referal. As for WiFi adapters, any Ralink RT5370 based chipset should be compatible.

Please let me know if any other hardware is compatible and I will add them to this list.

<b>Canadian Links</b>

<a href="http://www.amazon.ca/gp/product/B00GWTNYJW/ref=as_li_ss_tl?ie=UTF8&camp=15121&creative=390961&creativeASIN=B00GWTNYJW&linkCode=as2&tag=matthew084-20">CanaKit Raspberry Pi 2 (1GB) Ultimate Starter Kit (Over 40 Components: New Raspberry Pi 2 + WiFi Dongle + 8GB SD Card + Case + Power Supply and many more)</a><img src="http://ir-ca.amazon-adsystem.com/e/ir?t=matthew084-20&l=as2&o=15&a=B00GWTNYJW" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />

<b>United States of America Links</b>

<a href="http://www.amazon.com/gp/product/B008XVAVAW/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B008XVAVAW&linkCode=as2&tag=matthew08b-20&linkId=IN557BBG3PJEAU7M">CanaKit Raspberry Pi 2 Complete Starter Kit with WiFi (Latest Version Raspberry Pi 2 + WiFi + Original Preloaded 8GB SD Card + Case + Power Supply + HDMI Cable)</a><img src="http://ir-na.amazon-adsystem.com/e/ir?t=matthew08b-20&l=as2&o=1&a=B008XVAVAW" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />

<a href="http://www.amazon.com/gp/product/B008OF9Z54/ref=as_li_tl?ie=UTF8&camp=1789&creative=390957&creativeASIN=B008OF9Z54&linkCode=as2&tag=matthew08b-20&linkId=B56OIMZL6L43DVYE">Mini USB 2.0 WiFi Wireless Adapter with Antenna, 802.11 n/g/b, 150M LAN Adapter</a><img src="http://ir-na.amazon-adsystem.com/e/ir?t=matthew08b-20&l=as2&o=1&a=B008OF9Z54" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
