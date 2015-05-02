<?php
// Send a signal to piPass.py to advance to the next Nintendo Zone.
exec('sudo pkill --signal SIGUSR2 -f piPass.py');

exit(0);
?>
