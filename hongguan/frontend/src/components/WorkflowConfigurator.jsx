import React, { useState } from 'react';
import axios from 'axios';
import { Button, Input, Card, message } from 'antd';

function WorkflowConfigurator() {
  const [taskConfig, setTaskConfig] = useState('');

  const handleSubmit = () => {
    if (!taskConfig) {
      message.warning('请输入任务配置');
      return;
    }
    try {
      const config = JSON.parse(taskConfig);
      axios
        .post('/api/workflow', { task_config: config })
        .then((response) => {
          message.success('工作流执行成功');
        })
        .catch((error) => {
          console.error('工作流执行失败:', error);
          message.error('工作流执行失败，请稍后重试');
        });
    } catch (e) {
      message.error('任务配置格式错误，请输入合法的 JSON');
    }
  };

  return (
    <div style={{ marginBottom: '24px' }}>
      <h2>工作流配置</h2>
      <Card>
        <Input.TextArea
          value={taskConfig}
          onChange={(e) => setTaskConfig(e.target.value)}
          placeholder="请输入任务配置的 JSON 字符串"
          rows={6}
        />
        <Button
          type="primary"
          onClick={handleSubmit}
          style={{ marginTop: '16px' }}
        >
          执行工作流
        </Button>
      </Card>
    </div>
  );
}

export default WorkflowConfigurator;
