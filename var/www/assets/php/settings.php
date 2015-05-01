<?php

if ($_POST)
{
  $json = json_encode($_POST);
  $date = date_create();
  $timestamp = date_timestamp_get($date);
  $settingsURL = "Location: ../../settings.html?time=";
  $settingsURL .= $timestamp;

  file_put_contents('/tmp/pipass_config.json', $json);
  exec('sudo cp /tmp/pipass_config.json /var/www/assets/json/');

  header($settingsURL);
}

?>
