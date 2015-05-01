<?php
exec('sudo pkill --signal SIGQUIT -f piPass.py');

exec('sudo service hostapd stop');
exec('sudo killall hostapd');

exec('sudo /sbin/shutdown -r now');
?>
