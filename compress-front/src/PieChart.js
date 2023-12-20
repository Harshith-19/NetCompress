import React from 'react'
import { Line } from 'react-chartjs-2'
import Chart from 'chart.js/auto';
 

function PieChart({chartData}) {
  return <Line data={chartData} />
}

export default PieChart