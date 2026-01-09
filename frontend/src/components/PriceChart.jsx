import React, { useRef } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const PriceChart = ({ data, symbol }) => {
  const chartRef = useRef(null);

  const chartData = {
    labels: data.map(d => new Date(d.timestamp).toLocaleTimeString()),
    datasets: [
      {
        label: `${symbol} Price`,
        data: data.map(d => d.price),
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.2)',
        tension: 0.4,
        fill: true,
        pointRadius: 0,
        pointHoverRadius: 6,
        pointHoverBackgroundColor: 'rgb(59, 130, 246)',
        pointHoverBorderColor: '#fff',
        pointHoverBorderWidth: 2,
        borderWidth: 3,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'top',
        labels: {
          color: '#ffffff',
          font: {
            size: 13,
            weight: '600',
          },
          padding: 15,
          usePointStyle: true,
          pointStyle: 'circle',
        }
      },
      title: {
        display: true,
        text: `${symbol} Price History (24h)`,
        color: '#ffffff',
        font: {
          size: 18,
          weight: '700',
        },
        padding: {
          top: 10,
          bottom: 20
        }
      },
      tooltip: {
        backgroundColor: 'rgba(21, 25, 50, 0.95)',
        titleColor: '#ffffff',
        bodyColor: '#a0aec0',
        borderColor: 'rgba(255, 255, 255, 0.1)',
        borderWidth: 1,
        padding: 12,
        cornerRadius: 8,
        displayColors: true,
        mode: 'index',
        intersect: false,
        callbacks: {
          label: function(context) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            if (context.parsed.y !== null) {
              label += '$' + context.parsed.y.toFixed(2);
            }
            return label;
          }
        }
      },
    },
    scales: {
      x: {
        display: true,
        grid: {
          display: true,
          color: 'rgba(255, 255, 255, 0.05)',
          drawBorder: false,
        },
        title: {
          display: true,
          text: 'Time',
          color: '#a0aec0',
          font: {
            size: 12,
            weight: '600',
          }
        },
        ticks: {
          color: '#a0aec0',
          maxRotation: 45,
          minRotation: 45,
          font: {
            size: 11,
          }
        },
      },
      y: {
        display: true,
        grid: {
          display: true,
          color: 'rgba(255, 255, 255, 0.05)',
          drawBorder: false,
        },
        title: {
          display: true,
          text: 'Price (USD)',
          color: '#a0aec0',
          font: {
            size: 12,
            weight: '600',
          }
        },
        ticks: {
          color: '#a0aec0',
          font: {
            size: 11,
          },
          callback: function(value) {
            return '$' + value.toFixed(2);
          }
        }
      },
    },
    interaction: {
      mode: 'nearest',
      axis: 'x',
      intersect: false,
    },
  };

  return (
    <div className="card chart-card">
      <div style={{ height: '400px' }}>
        <Line ref={chartRef} data={chartData} options={options} />
      </div>
    </div>
  );
};

export default PriceChart;
