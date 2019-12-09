function calculatePoint(i, intervalSize, colorRangeInfo) {
  var { colorStart, colorEnd, useEndAsStart } = colorRangeInfo;
  return (useEndAsStart
    ? (colorEnd - (i * intervalSize))
    : (colorStart + (i * intervalSize)));
}

/* Must use an interpolated color scale, which has a range of [0, 1] */
function interpolateColors(dataLength, colorScale, colorRangeInfo) {
  var { colorStart, colorEnd } = colorRangeInfo;
  var colorRange = colorEnd - colorStart;
  var intervalSize = colorRange / dataLength;
  var i, colorPoint;
  var colorArray = [];

  for (i = 0; i < dataLength; i++) {
    colorPoint = calculatePoint(i, intervalSize, colorRangeInfo);
    colorArray.push(colorScale(colorPoint));
  }

  return colorArray;
}

/* Set up Chart.js Pie Chart */
function createChart(chartId, chartData, colorScale, colorRangeInfo) {
  /* Grab chart element by id */
  const chartElement = document.getElementById(chartId).getContext('2d');
  const dataLength = chartData.data.length;

  /* Create color array */
  var COLORS = interpolateColors(dataLength, colorScale, colorRangeInfo);

  /* Create chart */
  var myChart = new Chart(chartElement, {
    type: 'pie',
    data: {
      labels: chartData.labels,
      datasets: [{
          data: chartData.data,
          backgroundColor: COLORS
        }],
    },
  });

  return myChart;
}
