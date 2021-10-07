let ctx = document.getElementById('myChart').getContext('2d');
let labels = ['pizza', 'burger', 'hotdog', 'sushi'];
let colorHex = ['#FB3640', '#EFCA08', '#43AA8B', '#253D5B'];

let myChart = new Chart(ctx, {
   type: 'pie',
   data: {
      datasets: [{
         data: [30, 10, 40, 20],
         backgroundColor: colorHex
      }],
      labels: labels


   },
   options: {
      responsive: true
   }
})

