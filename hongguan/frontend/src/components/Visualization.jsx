import React from 'react';
import { Card } from 'antd';
import ReactECharts from 'echarts-for-react';

function Visualization({ data }) {
  const option = {
    title: {
      text: '数据可视化',
    },
    tooltip: {},
    xAxis: {
      data: ['类别1', '类别2', '类别3', '类别4', '类别5'],
    },
    yAxis: {},
    series: [
      {
        name: '数量',
        type: 'bar',
        data: [5, 20, 36, 10, 10],
      },
    ],
  };

  return (
    <div style={{ marginBottom: '24px' }}>
      <h2>分析结果</h2>
      <Card>
        <ReactECharts option={option} style={{ height: '400px' }} />
      </Card>
    </div>
  );
}

export default Visualization;
