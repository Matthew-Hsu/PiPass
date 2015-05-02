<?php
// Double check to see if we actually got the form data from settings.html.
if ($_POST)
{
  // Convert the form data into a JSON format.
  $json = json_encode($_POST);

  // Browser caching is annoying. Generate a timestamp and append that to settings.html redirection to help aid in showing the most
  // up-to-date settings.
  $date = date_create();
  $timestamp = date_timestamp_get($date);
  $settingsURL = "Location: ../../settings.html?time=";
  $settingsURL .= $timestamp;

  // Save the JSON formatted settings to PiPass.
  file_put_contents('/tmp/pipass_config.json', $json);
  exec('sudo cp /tmp/pipass_config.json /var/www/assets/json/');

  // Redirect to settings.html.
  header('Cache-Control: no-cache, no-store, must-revalidate');
  header('Pragma: no-cache');
  header('Expires: 0');
  header($settingsURL);
}

exit(0);
?>
