<?php

if ($_POST)
{
  $json = json_encode($_POST);

  file_put_contents('/tmp/pipass_config.json', $json);
  exec('sudo cp /tmp/pipass_config.json /var/www/assets/json/');

  header('Cache-Control: no-cache, no-store, must-revalidate');
  header('Pragma: no-cache');
  header('Expires: 0');
  header('Location: ../../settings.html');
}

?>
