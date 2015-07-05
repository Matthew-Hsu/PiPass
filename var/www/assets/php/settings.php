<?php
// Double check to see if we actually got the form data from settings.html.
if ($_POST)
{
  // Trim leading/trailing whitespaces to help guard against dashboard path errors.
  $_POST['DASHBOARD'] = trim($_POST['DASHBOARD']);

  // Ensure that the dashboard path ends with the appropriate ' / '.
  if (strcmp(substr($_POST['DASHBOARD'], -1), "/") != 0)
  {
    $_POST['DASHBOARD'] .= "/";
  }

  // Determine if the specified installation path is valid.
  if (!file_exists($_POST['DASHBOARD']))
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
                <h3><i class='fa fa-angle-right'></i> PiPass Settings</h3>
                <div class='row mt'>
                  <div class='col-lg-12'>
                    <div class='showback'>
                      <p>
                        The entered dashboard path could not be found. Please verify that the PiPass Dashboard is installed there.
                      </p>
                      <p>
                        Redirecting back to PiPass Settings in 5 seconds...
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
                    <a href='settings.php#' class='go-top'>
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

  // Convert the list of authenticated Nintendo 3DS MAC addresses to uppercase.
  $_POST['AUTHENTICATION'] = strtoupper($_POST['AUTHENTICATION']);

  // Replace all dashes with colons to help guard against hostapd errors.
  $_POST['AUTHENTICATION'] = str_replace('-', ':', $_POST['AUTHENTICATION']);

  // Trim leading/trailing whitespaces to help guard against hostapd errors.
  $_POST['AUTHENTICATION'] = implode("\n", array_filter(array_map('trim', explode("\n", $_POST['AUTHENTICATION']))));

  // Save the list of authenticated Nintendo 3DS systems to /etc/hostapd/mac_accept.
  file_put_contents('/tmp/mac_accept', $_POST['AUTHENTICATION']);
  exec('sudo cp /tmp/mac_accept /etc/hostapd/mac_accept');

  // Trim leading/trailing whitespaces to help guard against PiPass DB URL errors.
  $_POST['GSX_KEY'] = trim($_POST['GSX_KEY']);

  // Trim leading/trailing whitespaces to help guard against hostapd errors.
  $_POST['HOSTAPD_DRIVER'] = trim($_POST['HOSTAPD_DRIVER']);

  // Convert the form data into a JSON format.
  $json = json_encode($_POST);

  // Save the JSON formatted settings to PiPass.
  file_put_contents('/tmp/pipass_config.json', $json);
  exec('sudo cp /tmp/pipass_config.json ' . $_POST['DASHBOARD'] . 'assets/json/');

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
              <h3><i class='fa fa-angle-right'></i> PiPass Settings</h3>
              <div class='row mt'>
                <div class='col-lg-12'>
                  <div class='showback'>
                    <p>
                      The PiPass settings have been saved successfully!
                    </p>
                    <p>
                      Redirecting back to PiPass Settings in 3 seconds...
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
                  <a href='settings.php#' class='go-top'>
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

  // Redirect to settings.html.
  $date = date_create();
  $timestamp = date_timestamp_get($date);
  $settingsURL = "refresh:3;url=../../settings.html?time=";
  $settingsURL .= $timestamp;

  header('Cache-Control: no-cache, no-store, must-revalidate');
  header('Pragma: no-cache');
  header('Expires: 0');
  header($settingsURL);

  exit(0);
}

exit(1);
?>
