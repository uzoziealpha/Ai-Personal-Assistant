import React from 'react';
import { ResponsivePie } from '@nivo/pie';
import { ResponsiveLine } from '@nivo/line';

const pieData = [
  { id: 'Tokens Received', value: 500 },
  { id: 'Tokens Answered', value: 450 },
  { id: 'Unanswered Queries', value: 50 },
];

const lineData = [
  {
    id: 'Tokens',
    data: [
      { x: 'Jan', y: 100 },
      { x: 'Feb', y: 200 },
      { x: 'Mar', y: 300 },
    ],
  },
];

const Charts = () => {
  return (
    <div>
      <h2>Pie Chart</h2>
      <div style={{ height: '400px' }}>
        <ResponsivePie data={pieData} />
      </div>
      <h2>Line Chart</h2>
      <div style={{ height: '400px' }}>
        <ResponsiveLine data={lineData} />
      </div>
    </div>
  );
};

export default Charts;