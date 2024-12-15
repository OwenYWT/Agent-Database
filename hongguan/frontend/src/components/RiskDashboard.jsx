import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Card, List } from 'antd';

function RiskDashboard() {
  const [risks, setRisks] = useState(null);

  useEffect(() => {
    axios
      .get('/api/risks')
      .then((response) => {
        setRisks(response.data);
      })
      .catch((error) => {
        console.error('获取风险数据失败:', error);
      });
  }, []);

  return (
    <div style={{ marginBottom: '24px' }}>
      <h2>风险评估</h2>
      <Card>
        {risks ? (
          <List
            itemLayout="horizontal"
            dataSource={risks}
            renderItem={(item) => (
              <List.Item>
                <List.Item.Meta
                  title={item.riskType}
                  description={`风险等级：${item.level}`}
                />
              </List.Item>
            )}
          />
        ) : (
          '加载中...'
        )}
      </Card>
    </div>
  );
}

export default RiskDashboard;
