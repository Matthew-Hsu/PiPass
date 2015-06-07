var Script = function() {

  $.validator.setDefaults({
    focusInvalid: false,
    invalidHandler: function(form, validator) {

        if (!validator.numberOfInvalids())
            return;

        $('html, body').animate({
            scrollTop: $(validator.errorList[0].element).offset().top - 250
        }, 500);

    },
    errorElement: "span",
    errorClass: "help-block",
    highlight: function(element) {
      $(element).parent().is('.has-success, .has-error') ? $(element).parent().removeClass(
        'has-success').addClass('has-error') : $(element).wrap(
        '<span class="has-error"></span>');
    },
    unhighlight: function(element) {
      $(element).parent().is('.has-success, .has-error') ? $(element).parent().removeClass(
        'has-error').addClass('has-success') : $(element).wrap(
        '<span class="has-success"></span>');
    },
    errorPlacement: function(error, element) {
      if (element.prop('type') === 'checkbox' || element.prop('type') === 'radio') {
        error.insertAfter(element.parent());
      } else {
        error.insertAfter(element);
      }
    },
  });

  $().ready(function() {

    $('#submit').click(function(){
        $('#settings').modal('hide');
    });

    $('#settingsForm').validate({
      rules: {
        STREETPASS_CYCLE_MINUTES: {
          min: 1,
          digits: true,
          required: true
        },
        GSX_KEY: {
          required: true
        },
        GSX_WORKSHEET: {
          min: 1,
          digits: true,
          required: true
        },
        HOSTAPD_DRIVER: {
          required: true
        },
        DASHBOARD: {
          required: true
        }
      },
    });
  });

}();
