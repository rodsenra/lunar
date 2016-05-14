/**
Author: Rod Senra <rodsenra@gmail.com>
 */

$(function() {

    function handleError(jqXHR, textStatus, errorThrown) {
        switch (textStatus) {
            case "error":
                break;
            case "timeout":
                break;
            case "abort":
                break;
            case "parsererror":
                break;
        }
        $("#error").html(textStatus + '<br/>'+ jqXHR.responseText);
    }

    var STATUS_POLLING_MS = 2000;

    next_telemetry();

    function next_telemetry() {

        $.ajax({
          type: "GET",
          url: '/telemetry',
          success: function (result) { successful_telemetry(result); } ,
          error: function(jqXHR, textStatus, errorThrown) { handleError(jqXHR, textStatus, errorThrown); }
        });
        setTimeout(function () { next_telemetry();}, STATUS_POLLING_MS);
    }

    function successful_telemetry(result) {
       $('#hour').val(result.hour);
       if (result.valid) {
          $('#hour').css({"color":"blue"});
          $('#timestamp').val(result.timestamp);
          $('#voltage').val(result.battery_voltage);
          $('#input_current').val(result.input_current);
          $('#current').val(result.output_current);
          $('#voltage').val(result.battery_voltage);
          $('#msg').val(result.msg);

       } else {
          $('#hour').css({"color":"red"});
       }
    }

});
