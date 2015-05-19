<?php
// Send a signal to piPass.py to terminate.
exec('sudo pkill --signal SIGQUIT -f piPass.py');

// Delete /etc/udev/rules.d/70-persistent-net.rules.
exec('sudo rm /etc/udev/rules.d/70-persistent-net.rules');

// Restart the Raspberry Pi.
exec('sudo /sbin/shutdown -r now');

exit(0);
?>
