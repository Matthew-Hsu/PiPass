<?php
// Send a signal to piPass.py to terminate.
exec('sudo pkill --signal SIGQUIT -f piPass.py');

// Start PiPass.
exec('sudo python /opt/PiPass/piPass.py');

exit(0);
?>
