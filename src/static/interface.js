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

    var STATUS_POLLING_MS = 5000;

    setMap();
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
          $('#msg').val(result.msg);

        var greenIcon = L.icon({
            iconUrl: '/static/marker-icon-green.png'
        });

        var redIcon = L.icon({
            iconUrl: '/static/marker-icon-red.png'
        });

        var marker_low = L.marker([result.latitude, result.longitude], {icon: greenIcon} ).addTo(map);
        map.setView([result.latitude, result.longitude], 18)
       } else {
          $('#hour').css({"color":"red"});
       }
    }

    function setMap() {
        map = L.map('map').setView([51.505, -0.09], 18);

        // add an OpenStreetMap tile layer
          L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
            maxZoom: 18,
            id: 'rodsenra.5a0dfce3',
            accessToken: 'pk.eyJ1Ijoicm9kc2VucmEiLCJhIjoiY2lvN28ybDkxMDJyNXZwa2phNjcwdnRqdyJ9.gpLxHX7iHkytgeSmJXQ9xg'
          }).addTo(map);

        var popup = L.popup();

            function onMapClick(e) {
                popup
                    .setLatLng(e.latlng)
                    .setContent("@" + e.latlng.toString())
                    .openOn(map);
            }

            map.on('click', onMapClick);
    }

});
