<?php
// Send a signal to piPass.py to refresh its settings.
exec('sudo pkill --signal SIGUSR1 -f piPass.py');

exit(0);
?>
