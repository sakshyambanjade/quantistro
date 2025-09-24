import React, { useState } from "react";
import { getStockRaw, getLstmForecast } from "./api";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

interface RawDataPoint {
  date: string;
  close: number;
}

interface ForecastDataPoint {
  name: string;
  Forecast: number;
}

export default function App() {
  const [symbol, setSymbol] = useState<string>("NVDA");
  const [rawData, setRawData] = useState<RawDataPoint[] | null>(null);
  const [forecastData, setForecastData] = useState<number[] | null>(null);

  async function fetchData() {
    try {
      const raw = await getStockRaw(symbol);
      setRawData(raw.sample);

      const forecastRes = await getLstmForecast(symbol, 5);
      setForecastData(forecastRes.lstm_forecast);
    } catch (error) {
      console.error("Error fetching data", error);
      alert("Failed to fetch data");
    }
  }

  // Convert forecast array to object array for plotting
  const forecastChartData: ForecastDataPoint[] | undefined = forecastData?.map(
    (value, index) => ({
      name: `Day ${index + 1}`,
      Forecast: value,
    })
  );

  return (
    <div style={{ padding: 20 }}>
      <h1>Stock Data Viewer</h1>
      <input
        value={symbol}
        onChange={(e) => setSymbol(e.target.value.toUpperCase())}
        placeholder="Enter stock symbol"
      />
      <button onClick={fetchData}>Load Data</button>

      {rawData && (
        <>
          <h2>Historical Close Prices</h2>
          <LineChart
            width={700}
            height={300}
            data={rawData}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis dataKey="close" />
            <Tooltip />
            <Legend />
            <Line
              type="monotone"
              dataKey="close"
              stroke="#8884d8"
              activeDot={{ r: 8 }}
            />
          </LineChart>
        </>
      )}

      {forecastChartData && (
        <>
          <h2>LSTM Forecast</h2>
          <LineChart
            width={700}
            height={300}
            data={forecastChartData}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line
              type="monotone"
              dataKey="Forecast"
              stroke="#82ca9d"
            />
          </LineChart>
        </>
      )}
    </div>
  );
}
