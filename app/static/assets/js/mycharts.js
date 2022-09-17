function doughnutChart(array){
    var data = {
        datasets: [{
          data: array,
          borderColor: [
            'rgba(255,99,132,1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)'
          ],
          backgroundColor: [
            'rgba(255, 99, 132, 0.5)',
            'rgba(54, 162, 235, 0.5)',
            'rgba(255, 206, 86, 0.5)',
            'rgba(75, 192, 192, 0.5)',
            'rgba(153, 102, 255, 0.5)',
            'rgba(255, 159, 64, 0.5)'
          ],
        }],
    
        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: [
          'Failed',
          'Successful',
        ]
      };

      var options = {
        responsive: true,
        animation: {
          animateScale: true,
          animateRotate: true
        }
      };
    
    var doughnutChartCanvas = document.getElementById('doughnutChart').getContext("2d");
    var doughnutChart = new Chart(doughnutChartCanvas, {
        type: 'doughnut',
        data: data,
        options: options
      });
}

function multiAreaChart(array){
    var data = {
        //get last 7 days and merge with selection
        labels: array[0][0],
        datasets: [
          {
            label: 'Failed',
            data: array[0][2],
            borderColor: ['rgba(255, 99, 132, 1)'],
            backgroundColor: ['rgba(255, 99, 132, 1)'],
            borderWidth: 1,
            fill: true
          },
          {
          label: 'Total',
          data: array[0][1],
          borderColor: ['rgba(54, 162, 235, 0.5)'],
          backgroundColor: ['rgba(54, 162, 235, 0.5)'],
          borderWidth: 1,
          fill: true
        }
        ]
      };
    
      var options = {
        plugins: {
          filler: {
            propagate: true
          }
        },
        elements: {
          point: {
            radius: 5,
            backgroundColor: 'rgba(255, 255, 255, 0.8)',
            hoverRadius: 10
          }
        },
        scales: {
          xAxes: [{
            gridLines: {
              display: false
            }
          }],
          yAxes: [{
            gridLines: {
              display: true
            }
          }]
        }
      }
      
    var multiAreaCanvas = document.getElementById('areachart-multi').getContext("2d");
    var multiAreaChart = new Chart(multiAreaCanvas, {
        type: 'line',
        data: data,
        options: options
    });


}

