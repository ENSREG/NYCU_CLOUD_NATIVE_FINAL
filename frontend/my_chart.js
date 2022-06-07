am5.ready(function() {
    // Create root element
    // https://www.amcharts.com/docs/v5/getting-started/#Root_element 
    var root = am5.Root.new("chartdiv");
    
    // readTextFile('sample.csv')
    // Set themes
    // https://www.amcharts.com/docs/v5/concepts/themes/ 
    root.setThemes([
      am5themes_Animated.new(root)
    ]);
    
    
    // Create chart
    // https://www.amcharts.com/docs/v5/charts/xy-chart/
    var chart = root.container.children.push(am5xy.XYChart.new(root, {
      panX: true,
      panY: true,
      wheelX: "panX",
      wheelY: "zoomX",
      maxTooltipDistance: 0,
      pinchZoomX: true
    }));
    
    var date = new Date();
    date.setHours(0, 0, 0, 0);
    var value = 100;
  
    // Create axes
    // https://www.amcharts.com/docs/v5/charts/xy-chart/axes/
    var xAxis = chart.xAxes.push(am5xy.DateAxis.new(root, {
      maxDeviation: 0.2,
      baseInterval: {
        timeUnit: "day",
        count: 1
      },
      renderer: am5xy.AxisRendererX.new(root, {}),
      tooltip: am5.Tooltip.new(root, {})
    }));
    
    var yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
      renderer: am5xy.AxisRendererY.new(root, {})
    }));
    
    
    // Add series
    // https://www.amcharts.com/docs/v5/charts/xy-chart/series/
    var brands = ['TSMC', 'ASML', 'AM', 'SUMCO']
    var predict_labels = []
    for (i in brands) predict_labels.push(brands[i] + '-predict');
    var line_colors = ['#70bbf7','#ef8179', '#f6c940', '#69a86b']
    for (i in line_colors) line_colors.push(line_colors[i]);

    function convertData(response, keys) {
      var data = {};
      response = JSON.parse(response);
      // const date2 = new Date('2021-01-01');
      // const date1 = new Date();
      for (var i = 0; i < keys.length; ++i) {
        data[keys[i]] = [];
        // console.log(Object.keys(response).length);
        for (var j = 0; j < Object.keys(response).length; j++){
          // console.log(response[j]);
          var day = new Date(response[j]["date"])
          data[keys[i]].push({
            date: day.getTime(),
            value: parseInt(response[j][keys[i]])
          });
        }
      }
      return data;
    }

    function draw_chart(crawler_data, predict_data) {
      // var data = convertData(response);
      // console.log(response);
      // var all_data = convertData(response);
      for (var i = 0; i < 8; i++) {
        if (i < 4) {
          data = crawler_data[brands[i]];
          label = brands[i];
        }
        else {
          data = predict_data[brands[i-4]];
          label = predict_labels[i-4];
        }
        var series = chart.series.push(am5xy.LineSeries.new(root, {
          name: label,
          stroke: line_colors[i],
          xAxis: xAxis,
          yAxis: yAxis,
          valueYField: "value",
          valueXField: "date",
          legendValueText: "{valueY}",
          tooltip: am5.Tooltip.new(root, {
            pointerOrientation: "vertical",
            labelText: "{valueY}"
          })
        }));
        series.set("fill", am5.color(line_colors[i]));
  
        if(i < 4) date = new Date("2021-01-01");
        else {
          date = new Date();
          series.strokes.template.setAll({
            strokeDasharray: [3, 3],
            strokeWidth: 2
          });
        }

        date.setHours(0, 0, 0, 0);
        value = 0;
      
        series.data.setAll(data);
      
        // Make stuff animate on load
        // https://www.amcharts.com/docs/v5/concepts/animations/
        series.appear();
      }
      // Add cursor
      // https://www.amcharts.com/docs/v5/charts/xy-chart/cursor/
      var cursor = chart.set("cursor", am5xy.XYCursor.new(root, {
        behavior: "none"
      }));
      cursor.lineY.set("visible", false);
      
      
      // Add scrollbar
      // https://www.amcharts.com/docs/v5/charts/xy-chart/scrollbars/
      chart.set("scrollbarX", am5.Scrollbar.new(root, {
        orientation: "horizontal"
      }));
      
      chart.set("scrollbarY", am5.Scrollbar.new(root, {
        orientation: "vertical"
      }));
      
      
      // Add legend
      // https://www.amcharts.com/docs/v5/charts/xy-chart/legend-xy-series/
      var legend = chart.rightAxesContainer.children.push(am5.Legend.new(root, {
        width: 200,
        paddingLeft: 15,
        height: am5.percent(100),
      }));
      
      // When legend item container is hovered, dim all the series except the hovered one
      legend.itemContainers.template.events.on("pointerover", function(e) {
        var itemContainer = e.target;
      
        // As series list is data of a legend, dataContext is series
        var series = itemContainer.dataItem.dataContext;
      
        chart.series.each(function(chartSeries) {
          if (chartSeries != series) {
            chartSeries.strokes.template.setAll({
              strokeOpacity: 0.15,
              stroke: am5.color(0x000000)
            });
          } else {
            chartSeries.strokes.template.setAll({
              strokeWidth: 3
            });
          }
        })
      })
      
      // When legend item container is unhovered, make all series as they are
      legend.itemContainers.template.events.on("pointerout", function(e) {
        var itemContainer = e.target;
        var series = itemContainer.dataItem.dataContext;
      
        chart.series.each(function(chartSeries) {
          chartSeries.strokes.template.setAll({
            strokeOpacity: 1,
            strokeWidth: 1,
            stroke: chartSeries.get("fill")
          });
        });
      })
      
      legend.itemContainers.template.set("width", am5.p100);
      legend.valueLabels.template.setAll({
        width: am5.p100,
        textAlign: "right"
      });
      
      // It's is important to set legend data after all the events are set on template, otherwise events won't be copied
      legend.data.setAll(chart.series.values);
      
      // Make stuff animate on load
      // https://www.amcharts.com/docs/v5/concepts/animations/
      chart.appear(1000, 100);
    };

    // send request to backend, receive response and pass to draw_chart function
    function data_load(draw_chart) {
      let crawler_url = "http://127.0.0.1:8080/GetAll/G";
      let predict_url = "http://127.0.0.1:8080/GetAll/P";
      var crawler_data;
      let craw_xhr = new XMLHttpRequest();
      craw_xhr.open('get', crawler_url, true);
      craw_xhr.send();
      craw_xhr.onload = function () {
        if (craw_xhr.status == 200) {
          // console.log(craw_xhr.responseText);
          crawler_data = convertData(craw_xhr.responseText, brands);
        }
        else {
          console.log("Fail to receive crawler data from backend API.");
        }
      };

      let pre_xhr = new XMLHttpRequest();
      pre_xhr.open('get', predict_url, true);
      pre_xhr.send();
      pre_xhr.onload = function () {
        if (pre_xhr.status == 200) {
          // console.log(pre_xhr.responseText);
          var predict_data = convertData(pre_xhr.responseText, brands);
          draw_chart(crawler_data, predict_data);
        }
        else {
          console.log("Fail to receive predict data from backend API.");
        }
      };
    };

    data_load(draw_chart);
    
}); // end am5.ready()