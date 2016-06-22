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
       $('#boat_name').val(result.boat_name);

       if (result.valid) {
          $('#hour').css({"color":"blue"});
          $('#battery_voltage').val(result.battery_voltage);
          $('#output_current').val(result.output_current);
          $('#input_current').val(result.input_current);
          $('#battery_current').val(result.battery_current);
          $('#latitude_begin').val(result.latitude_begin);
          $('#latitude_end').val(result.latitude_end);
          $('#longitude_begin').val(result.longitude_begin);
          $('#longitude_end').val(result.longitude_end);
          $('#box_temperature').val(result.box_temperature);
          $('#output_voltage').val(result.output_voltage);
          $('#last_msg').val(result.last_msg);
          $('#boat_timestamp').val(result.boat_timestamp);
          $('#engine_rpm').val(result.engine_rpm);
          $('#speed').val(result.speed);
          $('#distance_travelled').val(result.distance_travelled);


        var greenIcon = L.icon({
            iconUrl: '/static/marker-icon-green.png'
        });

        var redIcon = L.icon({
            iconUrl: '/static/marker-icon-red.png'
        });

        var marker_from = L.marker([result.latitude_begin, result.longitude_begin], {icon: redIcon} ).addTo(map);

        var marker_low = L.marker([result.latitude_end, result.longitude_end], {icon: greenIcon} ).addTo(map);

        map.setView([result.latitude_end, result.longitude_end], 18)

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
