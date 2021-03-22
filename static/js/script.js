// Tooltip
$(document).ready(() => {
    $('[data-toggle="tooltip"]').tooltip();   
});

// login form 
$(".input-field input").on("focus",function(){
    $(this).addClass("focus");
});
$(".input-field input").on("blur",function(){
    if($(this).val() == "")
    $(this).removeClass("focus");
});

// temperature gauge
$(function () {
    (function () {
        const points = 43;
        const radius = 257;
        const max = 60;
        const peaks = [0, 10, 20, 30, 40, 50, 60];
        const step = (max + 1) / points;
        const realPeaks = peaks.map(peak => Math.floor(peak * (1 / step)));
        const hueStep = 120 / points;
        const gaugeDigits = $('.gauge-digits');
        const digit = $('.gauge').data('digit');
        gaugeDigits.prepend(`<span class="digit current-digit count">0</span>`);
        for (let i = 0; i < points; i++) {
            const degree = i * (radius / (points - 1)) - radius / 2;
            const isPeak = realPeaks.indexOf(i) > -1;
            const gaugeInner = $('.gauge-inner').append(`<i class="bar${isPeak ? ' peak' : ''}" style="transform: rotate(${degree}deg)"></i>`);
            const intStep = Math.ceil(step * i);
            const intNextStep = Math.ceil(step * (i + 1));
            let styles = `transition-delay: ${ (i / digit) * (i / digit) + 1 }s;`;
            if (intStep <= digit) {
                styles += `background-color: hsl(${240 - 2 * i * hueStep}, 92%, 64%);`;
            }
            if (intStep > digit || (intStep <= digit && intNextStep <= digit)) {
                styles += `
            -webkit-transform: rotate(${degree}deg);
            -moz-transform: rotate(${degree}deg);
            -ms-transform: rotate(${degree}deg);
            -o-transform: rotate(${degree}deg);
            transform: rotate(${degree}deg);`;
            } else {
                if (intNextStep > digit)
                    styles += `
                -webkit-transform: rotate(${degree}deg) translateY(-.3em);
                -moz-transform: rotate(${degree}deg) translateY(-.3em);
                -ms-transform: rotate(${degree}deg) translateY(-.3em);
                -o-transform: rotate(${degree}deg) translateY(-.3em);
                transform: rotate(${degree}deg) translateY(-.3em);
                height: 1em;`;
            }
            $('.gauge-outer').append(`<i class="bar" style="${styles}"></i>`);
            if (isPeak) {
                const digit = $(`<span class="digit">${peaks[realPeaks.indexOf(i)]}</span>`);
                const peakOffset = gaugeInner.find('.peak').last().offset();
                gaugeDigits.append(digit);
                if (degree > -5 && degree < 5)
                    digit.offset({left: peakOffset.left - 5, top: peakOffset});
                else
                    digit.offset(peakOffset);
                setTimeout(function () {
                    gaugeDigits.addClass('scale');
                }, 1)
            }
        }
        counterify();
    }());
    setTimeout(() => {
        const gauge = $('.gauge');
        const digit = gauge.data('digit');
        gauge.addClass('load');
        setTimeout(()=>{
            gauge.find('.current-digit').text(digit).trigger('count');
        }, 1000)
    }, 500);
    function counterify() {
        $('.count').each(function () {
            $(this).on('count', function () {
                let fixed = $(this).text().toString().split('.')[1];
                const thousand = $(this).hasClass('thousandify');
                fixed = fixed ? (fixed.length > 2 ? 2 : fixed.length) : 0;
                $(this).prop('Counter', 0).animate({
                    Counter: $(this).text()
                }, {
                    duration: 600,
                    easing: 'swing',
                    step: function (now) {
                        if (thousand)
                            $(this).text((thousandify(now.toFixed(fixed))));
                        else
                            $(this).text((now.toFixed(fixed)));
                    }
                });
            });
        });
    }
});

// temerature gauge 2
anychart.onDocumentReady(function () {
    // Create and return simple linear gauge
    function drawLinearGauge(value) {
      var gauge = anychart.gauges.linear();
      gauge.data([value]).padding(10, 0, 30, 0);
      gauge
        .tooltip()
        .useHtml(true)
        .format(function () {
          switch (this.pointer.id()) {
            case '0':
              return this.value + '°C';
            case '1':
              return (
                this.value +
                '°C' +
                ' (' +
                (this.value * 1.8 + 32).toFixed(1) +
                '°F)'
              );
            default:
          }
        });

      // Set scale settings
      var scale = gauge.scale();
      scale.minimum(-25).maximum(25).ticks({ interval: 5 });

      // Set axis and axis settings
      var axis = gauge.axis();
      axis.scale(scale).width('0.5%').offset('-1%');

      // Set text formatter for axis labels
      axis.labels().useHtml(true).format('{%Value}°');

      return gauge;
    }

    // Create simple gauge
    var simpleGauge = drawLinearGauge(12);
    var simpleThermometer = simpleGauge.thermometer(0);

    // Set simple thermometer settings
    simpleThermometer
      .name('Thermometer')
      .id('0')
      .fill('#64b5f6')
      .stroke('#64b5f6');

    // Create gauge with extra axis
    var multiAxisGauge = drawLinearGauge(12);
    var multiAxisThermometer = multiAxisGauge.thermometer(0);
    multiAxisThermometer.name('Thermometer').id('1');

    // Add left axis with custom labels
    var axisLeft = multiAxisGauge.axis(0);
    axisLeft.minorTicks(true);
    axisLeft
      .labels()
      .useHtml(true)
      .format(function () {
        if (this.value > 0) {
          return (
            '<span style="color:#dd2c00;">' + this.value + '°</span>'
          );
        }
        return (
          '<span style="color: #1976d2;">' + this.value + '°</span>'
        );
      });

    // Add custom right axis with custom labels
    var axisRight = multiAxisGauge.axis(1);
    axisRight.minorTicks(true);
    axisRight
      .labels()
      .useHtml(true)
      .format(function () {
        if (this.value > 32) {
          return '<span style="color:#dd2c00;">' + this.value + 'F</span>';
        }
        return '<span style="color: #1976d2;">' + this.value + 'F</span>';
      });
    axisRight.orientation('right').offset('3.5%');

    // Set scale Fahrenheit for right axis
    var Fscale = anychart.scales.linear();
    Fscale.minimum(-13).maximum(77).ticks({ interval: 5 });
    axisRight.scale(Fscale);

    // Create table to place thermometers
    var layoutTable = anychart.standalones.table();
    layoutTable
      .hAlign('center')
      .vAlign('middle')
      .useHtml(true)
      .fontSize(16)
      .cellBorder(null);

    // Put thermometers into the layout table
    layoutTable.contents([
      ['Thermometer Samples', null],
      [
        'Simple Thermometer',
        'Thermometer with Custom<br/>Celsius and Fahrenheit Scales'
      ],
      [simpleGauge, multiAxisGauge]
    ]);

    // Set height for first row in layout table
    layoutTable.getRow(0).height(40).fontSize(18);
    layoutTable.getRow(1).height(80).fontSize(14);

    // Merge cells in layout table where needed
    layoutTable.getCell(0, 0).colSpan(3);

    // Set container id and initiate drawing
    layoutTable.container('container');
    layoutTable.draw();
  });

