import React, { useState } from 'react';
import { Form, Input, Button } from 'antd';
import axios from 'axios';

function Auth() {
  const [loading, setLoading] = useState(false);

  const onFinish = (values) => {
    setLoading(true);
    axios.post('/api/auth/login', values)
      .then(response => {
        // 保存令牌，跳转到主页
        localStorage.setItem('token', response.data.token);
        window.location.href = '/';
      })
      .catch(error => {
        console.error('登录失败:', error);
      })
      .finally(() => setLoading(false));
  };

  return (
    <Form onFinish={onFinish}>
      <Form.Item name="username" rules={[{ required: true, message: '请输入用户名' }]}>
        <Input placeholder="用户名" />
      </Form.Item>
      <Form.Item name="password" rules={[{ required: true, message: '请输入密码' }]}>
        <Input.Password placeholder="密码" />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit" loading={loading}>
          登录
        </Button>
      </Form.Item>
    </Form>
  );
}

export default Auth;
