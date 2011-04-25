var chart;
$(document).ready(function() {
   chart = new Highcharts.Chart({
      chart: {
         renderTo: 'container',
         defaultSeriesType: 'line'
      },
      title: {
         text: 'The LCD Offset Of F3C-H...Cl H-Bond'
      },
      subtitle: {
         text: 'MP2/accq'
      },
      xAxis: {
         categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
      },
      yAxis: {
         title: {
            text: 'The Offset Value'
         }
      },
      tooltip: {
         enabled: true,
         formatter: function() {
            return '<b>'+ this.series.name +'</b><br/>'+
               this.x +': '+ (this.y * 1000).toFixed(3) ;
         }
      },
      plotOptions: {
          value: 0,
          width: 1,
          color: '#808080'
          //line: {
          //   dataLabels: {
          //      enabled: true
          //   },
          //   enableMouseTracking: true
          //}
      },
      //legend: {
      //    layout: 'vertical',
      //    align: 'right',
      //    verticalAlign: 'top',
      //    x: -10,
      //    y: 100,
      //    borderWidth: 0
      //},
