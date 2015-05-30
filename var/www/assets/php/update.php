<?php
// Safety check to see if piPass.py has corrupted settings.
if (!file_exists('/opt/PiPass/config/pipass_dashboard.json'))
{
  echo "
    <!DOCTYPE html>
    <html lang='en'>
      <head>
        <meta charset='utf-8'>
        <meta name='theme-color' content='#ffd777'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <meta name='description' content='PiPass Dashboard for the Raspberry Pi'>
        <meta name='author' content='Matthew Hsu'>
        <meta name='keyword' content='Nintendo, 3DS, Homepass, Raspberry, Pi, PiPass'>

        <title>PiPass Dashboard</title>
        <link rel='icon' type='image/png' href='../../assets/img/favicon.png'>

        <!-- BOOTSTRAP CORE CSS -->
        <link href='../../assets/css/bootstrap.css' rel='stylesheet'>

        <!-- EXTERNAL CSS -->
        <link href='../../assets/font-awesome/css/font-awesome.css' rel='stylesheet'/>

        <!-- CUSTOM STYLES FOR THIS TEMPLATE -->
        <link href='../../assets/css/style.css' rel='stylesheet'>
        <link href='../../assets/css/style-responsive.css' rel='stylesheet'>
      </head>

      <body>

      <section id='container' >
          <!-- HEADER START -->
          <header class='header black-bg'>
            <!-- LOGO START -->
              <a class='logo'><b>PiPass Dashboard</b></a>
            <!-- LOGO END -->
          </header>
          <!-- HEADER END -->

          <!-- MAIN CONTENT START -->
          <section id='main-content' style='margin-left: 0px;'>
            <section class='wrapper site-min-height'>
              <h3><i class='fa fa-angle-right'></i> PiPass Update</h3>
              <div class='row mt'>
                <div class='col-lg-12'>
                  <div class='showback'>
                    <p>
                      PiPass is not configured correctly. Please re-check your settings in PiPass Settings and ensure PiPass has a valid dashboard path.
                    </p>
                    <p>
                      Redirecting back to PiPass Update in 5 seconds...
                    </p>
                  </div>
                </div>
              </div>
            </section>
          </section>
          <!-- MAIN CONTENT END -->

          <!--FOOTER START-->
          <footer class='site-footer'>
              <div class='text-center'>
                  <b>'It's a me, Mario!'</b>
                  <a href='update.php#' class='go-top'>
                      <i class='fa fa-angle-up'></i>
                  </a>
              </div>
          </footer>
          <!--FOOTER END-->
      </section>

      <!-- JS PLACED AT THE END OF THE DOCUMENT SO THE PAGES LOAD FASTER -->
      <script src='../../assets/js/jquery.js'></script>
      <script src='../../assets/js/bootstrap.min.js'></script>
      <script src='../../assets/js/jquery-ui-1.9.2.custom.min.js'></script>
      <script src='../../assets/js/jquery.ui.touch-punch.min.js'></script>
      <script class='include' type='text/javascript' src='../../assets/js/jquery.dcjqaccordion.2.7.js'></script>
      <script src='../../assets/js/jquery.scrollTo.min.js'></script>
      <script src='../../assets/js/jquery.nicescroll.js' type='text/javascript'></script>

      <!--COMMON SCRIPT FOR ALL PAGES-->
      <script src='../../assets/js/common-scripts.js'></script>

      </body>
    </html>
  ";

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

  echo "
    <!DOCTYPE html>
    <html lang='en'>
      <head>
        <meta charset='utf-8'>
        <meta name='theme-color' content='#ffd777'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <meta name='description' content='PiPass Dashboard for the Raspberry Pi'>
        <meta name='author' content='Matthew Hsu'>
        <meta name='keyword' content='Nintendo, 3DS, Homepass, Raspberry, Pi, PiPass'>

        <title>PiPass Dashboard</title>
        <link rel='icon' type='image/png' href='../../assets/img/favicon.png'>

        <!-- BOOTSTRAP CORE CSS -->
        <link href='../../assets/css/bootstrap.css' rel='stylesheet'>

        <!-- EXTERNAL CSS -->
        <link href='../../assets/font-awesome/css/font-awesome.css' rel='stylesheet'/>

        <!-- CUSTOM STYLES FOR THIS TEMPLATE -->
        <link href='../../assets/css/style.css' rel='stylesheet'>
        <link href='../../assets/css/style-responsive.css' rel='stylesheet'>
      </head>

      <body>

      <section id='container' >
          <!-- HEADER START -->
          <header class='header black-bg'>
            <!-- LOGO START -->
              <a class='logo'><b>PiPass Dashboard</b></a>
            <!-- LOGO END -->
          </header>
          <!-- HEADER END -->

          <!-- MAIN CONTENT START -->
          <section id='main-content' style='margin-left: 0px;'>
            <section class='wrapper site-min-height'>
              <h3><i class='fa fa-angle-right'></i> PiPass Update</h3>
              <div class='row mt'>
                <div class='col-lg-12'>
                  <div class='showback'>
                    <p>
                      PiPass has been upgraded successfully!
                    </p>
                    <p>
                      Redirecting back to PiPass Update in 3 seconds...
                    </p>
                  </div>
                </div>
              </div>
            </section>
          </section>
          <!-- MAIN CONTENT END -->

          <!--FOOTER START-->
          <footer class='site-footer'>
              <div class='text-center'>
                  <b>'It's a me, Mario!'</b>
                  <a href='update.php#' class='go-top'>
                      <i class='fa fa-angle-up'></i>
                  </a>
              </div>
          </footer>
          <!--FOOTER END-->
      </section>

      <!-- JS PLACED AT THE END OF THE DOCUMENT SO THE PAGES LOAD FASTER -->
      <script src='../../assets/js/jquery.js'></script>
      <script src='../../assets/js/bootstrap.min.js'></script>
      <script src='../../assets/js/jquery-ui-1.9.2.custom.min.js'></script>
      <script src='../../assets/js/jquery.ui.touch-punch.min.js'></script>
      <script class='include' type='text/javascript' src='../../assets/js/jquery.dcjqaccordion.2.7.js'></script>
      <script src='../../assets/js/jquery.scrollTo.min.js'></script>
      <script src='../../assets/js/jquery.nicescroll.js' type='text/javascript'></script>

      <!--COMMON SCRIPT FOR ALL PAGES-->
      <script src='../../assets/js/common-scripts.js'></script>

      </body>
    </html>
  ";

  header("refresh:3;url=../../update_pi_pass.html");

  exit(0);
}

echo "
  <!DOCTYPE html>
  <html lang='en'>
    <head>
      <meta charset='utf-8'>
      <meta name='theme-color' content='#ffd777'>
      <meta name='viewport' content='width=device-width, initial-scale=1.0'>
      <meta name='description' content='PiPass Dashboard for the Raspberry Pi'>
      <meta name='author' content='Matthew Hsu'>
      <meta name='keyword' content='Nintendo, 3DS, Homepass, Raspberry, Pi, PiPass'>

      <title>PiPass Dashboard</title>
      <link rel='icon' type='image/png' href='../../assets/img/favicon.png'>

      <!-- BOOTSTRAP CORE CSS -->
      <link href='../../assets/css/bootstrap.css' rel='stylesheet'>

      <!-- EXTERNAL CSS -->
      <link href='../../assets/font-awesome/css/font-awesome.css' rel='stylesheet'/>

      <!-- CUSTOM STYLES FOR THIS TEMPLATE -->
      <link href='../../assets/css/style.css' rel='stylesheet'>
      <link href='../../assets/css/style-responsive.css' rel='stylesheet'>
    </head>

    <body>

    <section id='container' >
        <!-- HEADER START -->
        <header class='header black-bg'>
          <!-- LOGO START -->
            <a class='logo'><b>PiPass Dashboard</b></a>
          <!-- LOGO END -->
        </header>
        <!-- HEADER END -->

        <!-- MAIN CONTENT START -->
        <section id='main-content' style='margin-left: 0px;'>
          <section class='wrapper site-min-height'>
            <h3><i class='fa fa-angle-right'></i> PiPass Update</h3>
            <div class='row mt'>
              <div class='col-lg-12'>
                <div class='showback'>
                  <p>
                    The PiPass Dashboard could not download updates. Please check your internet connection or try again later.
                  </p>
                  <p>
                    Redirecting back to PiPass Update in 5 seconds...
                  </p>
                </div>
              </div>
            </div>
          </section>
        </section>
        <!-- MAIN CONTENT END -->

        <!--FOOTER START-->
        <footer class='site-footer'>
            <div class='text-center'>
                <b>'It's a me, Mario!'</b>
                <a href='update.php#' class='go-top'>
                    <i class='fa fa-angle-up'></i>
                </a>
            </div>
        </footer>
        <!--FOOTER END-->
    </section>

    <!-- JS PLACED AT THE END OF THE DOCUMENT SO THE PAGES LOAD FASTER -->
    <script src='../../assets/js/jquery.js'></script>
    <script src='../../assets/js/bootstrap.min.js'></script>
    <script src='../../assets/js/jquery-ui-1.9.2.custom.min.js'></script>
    <script src='../../assets/js/jquery.ui.touch-punch.min.js'></script>
    <script class='include' type='text/javascript' src='../../assets/js/jquery.dcjqaccordion.2.7.js'></script>
    <script src='../../assets/js/jquery.scrollTo.min.js'></script>
    <script src='../../assets/js/jquery.nicescroll.js' type='text/javascript'></script>

    <!--COMMON SCRIPT FOR ALL PAGES-->
    <script src='../../assets/js/common-scripts.js'></script>

    </body>
  </html>
";

header("refresh:5;url=../../update_pi_pass.html");

exit(1);
?>
