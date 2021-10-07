var data;
var chart;

  load('current', {
  callback: drawChart,
  packages:['corechart']
});

function drawChart() {
  var results = [{"sender":"Facebook <notification@facebookmail.com>","Count":3},{"sender":"Indeed <alert@indeed.com>","Count":3},{"sender":"Twitter <info@twitter.com>","Count":1}];

//   data = new google.visualization.DataTable();
  data.addColumn('string', 'VoteName');
  data.addColumn('number', 'VoteCount');

  // iterate "vt" keys
  Object.keys(results[0]).forEach(function (key) {
    if (key.indexOf("vt") > -1) {
      data.addRow([
        key,
        parseFloat(results[0][key])
      ]);
    }
  });

  var options = {
    title: 'My Pie Chart',
    width: 600,
    height: 600
  };

  chart = new.PieChart(document.getElementById('chart_div'));
  events.addListener(chart, 'select', selectHandler);
  chart.draw(data, options);
}

function selectHandler() {
  // be sure something is selected
  if (chart.getSelection().length) {
    var selectedItem = chart.getSelection()[0];
    var value = data.getValue(selectedItem.row, 0);
    alert('The user selected ' + value);
  }
}