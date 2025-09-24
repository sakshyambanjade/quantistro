import React from "react";
import { ResponsiveContainer, ComposedChart, XAxis, YAxis, Tooltip, Bar, Line } from "recharts";

// data points expect format:
// { date, open, high, low, close }

const CandlestickChart = ({ data }) => {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <ComposedChart data={data}>
        <XAxis dataKey="date" />
        <YAxis domain={["auto", "auto"]} />
        <Tooltip />
        {/* High-Low line */}
        <Line 
          type="monotone"
          dataKey={(d) => [d.low, d.high]}
          stroke="#000" 
          strokeWidth={1} 
          dot={false} 
          activeDot={{ r: 5 }} 
          isRange 
        />
        {/* Open-Close bars */}
        <Bar 
          dataKey="close" 
          fill="#8884d8" 
          stroke="#000" 
          shape={(props) => {
            const { x, y, width, height, payload } = props;
            const open = payload.open;
            const close = payload.close;
            const fill = close > open ? "green" : "red";
            return (
              <rect
                x={x}
                y={Math.min(y, y + height)}
                width={width}
                height={Math.abs(height)}
                fill={fill}
                stroke="black"
              />
            );
          }}
        />
      </ComposedChart>
    </ResponsiveContainer>
  );
};

export default CandlestickChart;
