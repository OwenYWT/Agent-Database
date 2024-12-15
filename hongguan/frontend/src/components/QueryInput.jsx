import React, { useState } from 'react';
import axios from 'axios';
import { Input, Button, Card, message } from 'antd';

function QueryInput() {
  const [query, setQuery] = useState('');
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = () => {
    if (!query) {
      message.warning('请输入查询内容');
      return;
    }
    setLoading(true);
    axios
      .post('/api/query', { query })
      .then((response) => {
        setInsights(response.data);
      })
      .catch((error) => {
        console.error('查询失败:', error);
        message.error('查询失败，请稍后重试');
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <div style={{ marginBottom: '24px' }}>
      <h2>查询分析</h2>
      <Input.TextArea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="请输入您的查询"
        rows={4}
      />
      <Button type="primary" onClick={handleSubmit} loading={loading} style={{ marginTop: '16px' }}>
        查询
      </Button>
      {insights && (
        <Card title="查询结果" style={{ marginTop: '24px' }}>
          <pre>{JSON.stringify(insights, null, 2)}</pre>
        </Card>
      )}
    </div>
  );
}

export default QueryInput;
