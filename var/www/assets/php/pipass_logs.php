<?php
$LOG_FILENAME = '/opt/PiPass/logs/piPass.log';

// Check for the case where no logging has been generated yet.
if (!file_exists($LOG_FILENAME))
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
              <h3><i class='fa fa-angle-right'></i> PiPass Logs</h3>
              <div class='row mt'>
                <div class='col-lg-12'>
                  <div class='showback'>
                    <p>
                      No PiPass logging has been found. Please try again by starting PiPass.
                    </p>
                    <p>
                      Redirecting back to the PiPass Dashboard in 5 seconds...
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
                  <a href='pipass_logs.php#' class='go-top'>
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

  header("refresh:5;url=../../index.html");

  exit(1);
}

header("Content-Type:text/plain; charset=UTF-8");
header("refresh:10;url=pipass_logs.php");

echo file_get_contents($LOG_FILENAME);

exit(0);
?>
