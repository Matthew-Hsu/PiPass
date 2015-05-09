<?php
// Double check to see if we actually got the form data from settings.html.
if ($_POST)
{
  // Ensure that the dashboard path ends with the approperiate ' / '.
  if (strcmp(substr($_POST['DASHBOARD'], -1), "/") != 0) 
  {
    $_POST['DASHBOARD'] .= "/";
  }

  // Determine if the specified installation path is valid.
  if (!file_exists($_POST['DASHBOARD'])) 
  {
    echo "Error! - The dashboard path of [ " . $_POST['DASHBOARD'] . " ] could not be found. Please verify that the PiPass Dashboard is installed there.";
    echo "<br /><br />";
    echo "Redirecting back to PiPass Settings in 5 seconds...";

    header("refresh:5;url=../../settings.html");

    exit(1);
  }

  // Prepare the dashboard path to be encoded into JSON.
  $dashboard = array('DASHBOARD' => $_POST['DASHBOARD']);

  // Enforce PiPass directory structure in case of corruption of configuration files.
  if (!file_exists('/opt/PiPass/config/'))
  {
    exec('sudo mkdir /opt/PiPass/config/');
  }

  // Save the JSON formatted setting that tells PiPass where the dashboard is installed.
  file_put_contents('/tmp/pipass_dashboard.json', json_encode($dashboard));
  exec('sudo cp /tmp/pipass_dashboard.json /opt/PiPass/config/');

  // Convert the form data into a JSON format.
  $json = json_encode($_POST);

  // Save the JSON formatted settings to PiPass.
  file_put_contents('/tmp/pipass_config.json', $json);
  exec('sudo cp /tmp/pipass_config.json ' . $_POST['DASHBOARD'] . 'assets/json/');

  // Redirect to settings.html.
  header('Cache-Control: no-cache, no-store, must-revalidate');
  header('Pragma: no-cache');
  header('Expires: 0');
  header('refresh:0;url=../../settings.html');

  exit(0);
}

exit(1);
?>
