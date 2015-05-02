<?php
// Send a signal to piPass.py to terminate.
exec('sudo pkill --signal SIGQUIT -f piPass.py');

// Stop Hostapd services.
exec('sudo service hostapd stop');
exec('sudo killall hostapd');

exit(0);
?>
