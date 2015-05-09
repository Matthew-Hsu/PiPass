<?php
// Safety check to see if piPass.py has corrupted settings.
if (!file_exists('/opt/PiPass/config/pipass_dashboard.json'))
{
  echo "Error! - PiPass is not configured correctly. Please re-check your settings in PiPass Settings and ensure PiPass has a valid 'Dashboard Path'.";
  echo "<br /><br />";
  echo "Redirecting back to PiPass Update in 5 seconds...";

  header("refresh:5;url=../../update_pi_pass.html");

  exit(1);
}

// Exit out of PiPass.
exec('sudo pkill --signal SIGQUIT -f piPass.py');

// Stop Hostapd services.
exec('sudo service hostapd stop');
exec('sudo killall hostapd');

// Download the latest version of PiPass from the master branch.
exec('sudo wget -P /tmp/PiPass/ https://github.com/Matthew-Hsu/PiPass/archive/master.zip');

// Safety is not guranteed. Ensure that master.zip has been downloaded.
if (file_exists('/tmp/PiPass/master.zip'))
{
  // 7z is a required component for the upgrade process, enforce that dependency.
  if (!file_exists('/usr/bin/7z'))
  {
    exec('sudo apt-get install p7zip-full -y');
  }

  // Get the installation path of the PiPass Dashboard.
  $json = file_get_contents('/opt/PiPass/config/pipass_dashboard.json');
  $dashboard = json_decode($json, true);

  // Prepare for the upgrade process.
  exec('sudo 7z x /tmp/PiPass/master.zip -o/tmp/PiPass/ -y');

  // Backup the PiPass settings.
  exec('sudo cp /opt/PiPass/config/pipass_dashboard.json /tmp/PiPass/');
  exec('sudo cp ' . $dashboard['DASHBOARD'] . 'assets/json/pipass_config.json /tmp/PiPass/');

  // Ensure permissions are correct before the upgrading process.
  exec('sudo chmod -R 755 /tmp/PiPass/');

  // Delete the old version of PiPass.
  exec('sudo rm -rf /opt/PiPass/*');
  exec('sudo rm -rf ' . $dashboard['DASHBOARD'] . '*');

  // Upgrade PiPass to the latest version.
  exec('sudo cp -r /tmp/PiPass/PiPass-master/opt/PiPass/* /opt/PiPass/');
  exec('sudo cp -r /tmp/PiPass/PiPass-master/var/www/* ' . $dashboard['DASHBOARD']);
  exec('sudo cp /tmp/PiPass/pipass_dashboard.json /opt/PiPass/config/');
  exec('sudo cp /tmp/PiPass/pipass_config.json ' . $dashboard['DASHBOARD'] . 'assets/json/');

  // Ensure permissions are correct for after the upgrading process.
  exec('sudo chmod -R 755 /opt/PiPass/');
  exec('sudo chmod -R 755 ' . $dashboard['DASHBOARD']);

  // Cleanup the temporary files used in upgrading PiPass.
  exec('sudo rm -rf /tmp/PiPass/');

  echo "Success! - PiPass has been upgraded successfully!";
  echo "<br /><br />";
  echo "Redirecting back to PiPass Update in 5 seconds...";

  header("refresh:5;url=../../update_pi_pass.html");

  exit(0);
}

echo "Error! - The PiPass Dashboard could not download updates. Please check your internet connection or try again later.";
echo "<br /><br />";
echo "Redirecting back to PiPass Update in 5 seconds...";

header("refresh:5;url=../../update_pi_pass.html");

exit(1);
?>
