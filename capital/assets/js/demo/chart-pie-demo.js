// Set new default font family and font color to mimic Bootstrap's default styling
import {rgb as jsonResponse} from "../../vendor/chart.js/Chart";

Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
var ctx = document.getElementById("myPieChart");
var myPieChart = new Chart(ctx, {
  type: 'doughnut',
  options: {
    maintainAspectRatio: false,
    tooltips: {
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
    },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});
$(document).ready(function (){
      $.ajax({
      url: "/pie_chart",
      type: "GET",
      dataType: "json",
      success: (jsonResponse) => {
        console.log(jsonResponse)
        const title = jsonResponse.title;
        const labels = jsonResponse.data.labels;
        const datasets = jsonResponse.data.datasets;
        // Reset the current chart
        myPieChart.data.datasets = [];
        myPieChart.data.labels = [];
        // Load new data into the chart
        myPieChart.options.title.text = title;
        myPieChart.options.title.display = true;
        myPieChart.data.labels = labels;
        datasets.forEach(dataset => {
          myPieChart.data.datasets.push(dataset);
        });
        myPieChart.update();
      },
       error: () => console.log("Failed to fetch chart filter options!")
     });
});
