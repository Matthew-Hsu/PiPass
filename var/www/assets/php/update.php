<?php
// Exit out of PiPass.
exec('sudo pkill --signal SIGQUIT -f piPass.py');

// Stop Hostapd services.
exec('sudo service hostapd stop');
exec('sudo killall hostapd');

// Download the latest version of PiPass from the master branch and extract master.zip for updating preparation.
exec('sudo wget -P /tmp/PiPass/ https://github.com/Matthew-Hsu/PiPass/archive/master.zip');
exec('sudo 7z x /tmp/PiPass/master.zip -o/tmp/PiPass/ -y');

// Backup the PiPass settings.
exec('sudo cp /var/www/assets/json/pipass_config.json /tmp/PiPass/');

// Delete the old version of PiPass.
exec('sudo rm -rf /opt/PiPass/');
exec('sudo rm -rf /var/www/');

// Upgrade PiPass to the latest version.
exec('sudo cp -ar /tmp/PiPass/PiPass-master/opt/PiPass/ /opt/');
exec('sudo cp -ar /tmp/PiPass/PiPass-master/var/www/ /var/');
exec('sudo cp /tmp/PiPass/pipass_config.json /var/www/assets/json/');

// Ensure permissions are correct.
exec('sudo chmod -R 755 /opt/PiPass/');
exec('sudo chmod -R 755 /var/www/');

// Cleanup the temporary files used in upgrading PiPass.
exec('sudo rm -rf /tmp/PiPass/');

exit(0);
?>
