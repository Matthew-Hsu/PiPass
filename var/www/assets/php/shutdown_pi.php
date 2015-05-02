<?php
// Send a signal to piPass.py to terminate.
exec('sudo pkill --signal SIGQUIT -f piPass.py');

// Shutdown the Raspberry Pi.
exec('sudo /sbin/shutdown -h now');

exit(0);
?>
