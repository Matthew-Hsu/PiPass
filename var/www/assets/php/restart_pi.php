<?php
// Send a signal to piPass.py to terminate.
exec('sudo pkill --signal SIGQUIT -f piPass.py');

// Restart the Raspberry Pi.
exec('sudo /sbin/shutdown -r now');

exit(0);
?>
