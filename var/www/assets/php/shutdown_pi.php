<?php
exec('sudo pkill --signal SIGQUIT -f piPass.py');

exec('sudo /sbin/shutdown -h now');
?>
