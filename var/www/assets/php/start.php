<?php
exec('sudo pkill --signal SIGQUIT -f piPass.py');

exec('sudo python /opt/PiPass/piPass.py');
?>
