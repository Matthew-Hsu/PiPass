<?php

if ($_POST)
{
  $json = json_encode($_POST);

  file_put_contents('/tmp/pipass_config.json', $json);
  exec('sudo cp /tmp/pipass_config.json /var/www/assets/json/');

  header('Location: ../../settings.html');
}

?>
