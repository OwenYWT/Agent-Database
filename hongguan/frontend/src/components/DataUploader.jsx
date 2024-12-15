import React from 'react';
import { Upload, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';

function DataUploader() {
  const props = {
    name: 'file',
    multiple: true,
    action: 'http://localhost:8000/api/upload',
    headers: {
      // 如果需要身份验证令牌，可以在这里添加
      // Authorization: localStorage.getItem('token') || '',
    },
    onChange(info) {
      const { status } = info.file;
      if (status === 'done') {
        message.success(`${info.file.name} 文件上传成功.`);
      } else if (status === 'error') {
        message.error(`${info.file.name} 文件上传失败.`);
      }
    },
    withCredentials: true,
  };

  return (
    <div style={{ marginBottom: '24px' }}>
      <h2>上传数据</h2>
      <Upload {...props}>
        <button type="button" className="ant-btn ant-btn-primary">
          <UploadOutlined /> 点击上传
        </button>
      </Upload>
    </div>
  );
}

export default DataUploader;
