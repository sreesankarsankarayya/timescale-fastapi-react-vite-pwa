import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, TimeScale, LinearScale, PointElement, LineElement, Tooltip, Legend } from 'chart.js';
import 'chartjs-adapter-date-fns';

ChartJS.register(TimeScale, LinearScale, PointElement, LineElement, Tooltip, Legend);

interface DataPoint {
  x: Date;
  y: number;
}

function App() {
  const [dataPoints, setDataPoints] = useState<DataPoint[]>([]);

  useEffect(() => {
    const ws = new WebSocket(`ws://${window.location.host}/ws/timeseries`);
    ws.onmessage = (event) => {
      // Expected data format: "timestamp,value"
      const [ts, value] = event.data.split(",");
      const date = new Date(ts);
      const num = parseFloat(value);
      console.log("Parsed point:", { date, num });
      setDataPoints((prev) => [...prev, { x: date, y: num }]);
    };
    ws.onerror = (error) => console.error("WebSocket error:", error);
    return () => ws.close();
  }, []);

  const data = {
    datasets: [
      {
        label: "Random Timeseries",
        data: dataPoints,
        fill: false,
        borderColor: "rgb(75, 192, 192)",
      }
    ]
  };

  const options = {
    scales: {
      x: {
        type: 'time',
        time: {
          unit: 'second'
        }
      },
      y: {
        beginAtZero: true
      }
    }
  };

  async function startGeneration() {
    await fetch("/start", { method: "POST" });
  }

  async function stopGeneration() {
    await fetch("/stop", { method: "POST" });
  }

  return (
    <div className="container mx-auto p-4 text-center">
      <h1 className="text-3xl font-bold mb-4">Real-time Timeseries Data</h1>
      <div className="mb-4">
        <Line data={data} options={options} />
      </div>
      <div>
        <button
          onClick={startGeneration}
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mr-2"
        >
          Start Data Generation
        </button>
        <button
          onClick={stopGeneration}
          className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
        >
          Stop Data Generation
        </button>
      </div>
    </div>
  );
}

export default App;
