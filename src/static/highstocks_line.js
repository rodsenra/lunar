$(function () {
 /**
     * Sand-Signika theme for Highcharts JS
     * @author Torstein Honsi
     */

    /**
    // Load the fonts
    Highcharts.createElement('link', {
       href: 'https://fonts.googleapis.com/css?family=Signika:400,700',
       rel: 'stylesheet',
       type: 'text/css'
    }, null, document.getElementsByTagName('head')[0]);
    */

    // Add the background image to the container
    Highcharts.wrap(Highcharts.Chart.prototype, 'getContainer', function (proceed) {
       proceed.call(this);
       this.container.style.background = 'url(http://www.highcharts.com/samples/graphics/sand.png)';
    });


    Highcharts.theme = {
       colors: ["#f45b5b", "#8085e9", "#8d4654", "#7798BF", "#aaeeee", "#ff0066", "#eeaaee",
          "#55BF3B", "#DF5353", "#7798BF", "#aaeeee"],
       chart: {
          backgroundColor: null,
          style: {
             fontFamily: "Orbitron"
          }
       },
       title: {
          style: {
             color: 'black',
             fontSize: '12px',
             fontWeight: 'bold'
          }
       },
       subtitle: {
          style: {
             color: 'black'
          }
       },
       tooltip: {
          borderWidth: 0
       },
       legend: {
          itemStyle: {
             fontWeight: 'bold',
             fontSize: '10px'
          }
       },
       xAxis: {
          labels: {
             style: {
                color: '#6e6e70'
             }
          }
       },
       yAxis: {
          labels: {
             style: {
                color: '#6e6e70'
             }
          }
       },
       plotOptions: {
          series: {
             shadow: true
          },
          candlestick: {
             lineColor: '#404048'
          },
          map: {
             shadow: false
          }
       },

       // Highstock specific
       navigator: {
          xAxis: {
             gridLineColor: '#D0D0D8'
          }
       },
       rangeSelector: {
          buttonTheme: {
             fill: 'white',
             stroke: '#C0C0C8',
             'stroke-width': 1,
             states: {
                select: {
                   fill: '#D0D0D8'
                }
             }
          }
       },
       scrollbar: {
          trackBorderColor: '#C0C0C8'
       },

       // General
       background2: '#E0E0E8'

    };

    // Apply the theme
    Highcharts.setOptions(Highcharts.theme);

    Highcharts.setOptions({
        global : {
            useUTC : false
        }
    });

    // Create the chart
    $('#highstocks').highcharts('StockChart', {
        chart : {
            events : {
                load : function () {

                    // set up the updating of the chart each second
                    var series = this.series[0];
                    setInterval(function () {
                        var x = (new Date()).getTime(), // current time
                            y = Math.round(Math.random() * 100);
                        series.addPoint([x, y], true, true);
                    }, 1000);
                }
            }
        },

        rangeSelector: {
            buttons: [{
                count: 1,
                type: 'minute',
                text: '1M'
            }, {
                count: 5,
                type: 'minute',
                text: '5M'
            }, {
                type: 'all',
                text: 'All'
            }],
            inputEnabled: false,
            selected: 0
        },

        title : {
            text : 'Live random data'
        },

        exporting: {
            enabled: false
        },

        series : [{
            name : 'Random data',
            data : (function () {
                // generate an array of random data
                var data = [], time = (new Date()).getTime(), i;

                for (i = -999; i <= 0; i += 1) {
                    data.push([
                        time + i * 1000,
                        Math.round(Math.random() * 100)
                    ]);
                }
                return data;
            }())
        }]
    });



});
