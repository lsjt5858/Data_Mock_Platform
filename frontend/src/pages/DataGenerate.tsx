import React, { useState } from 'react';
import { Card, InputNumber, Button, Space, message, Select, Spin } from 'antd';
import { DownloadOutlined } from '@ant-design/icons';
import { FieldEditor } from '../components/FieldEditor';
import { api } from '../services/api';
import type { FieldConfig } from '../types';

const { Option } = Select;

export const DataGenerate: React.FC = () => {
    const [fields, setFields] = useState<FieldConfig[]>([]);
    const [count, setCount] = useState(1000);
    const [format, setFormat] = useState<'csv' | 'json' | 'ndjson'>('csv');
    const [loading, setLoading] = useState(false);

    const handleExport = async () => {
        if (fields.length === 0) {
            message.warning('请至少添加一个字段');
            return;
        }

        if (count <= 0 || count > 1000000) {
            message.warning('数量必须在1到1000000之间');
            return;
        }

        setLoading(true);
        try {
            const response = await api.createExport({
                fields,
                count,
                format,
            });

            message.success(`导出任务创建成功！正在下载...`);

            // 自动下载文件
            const downloadUrl = api.downloadExport(response.id);
            window.open(downloadUrl, '_blank');
        } catch (error: any) {
            message.error(`导出失败: ${error.response?.data?.error || error.message}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ padding: 24 }}>
            <Card title="数据生成与导出" style={{ marginBottom: 24 }}>
                <FieldEditor value={fields} onChange={setFields} />
            </Card>

            <Card title="生成配置">
                <Space direction="vertical" style={{ width: '100%' }}>
                    <Space>
                        <span>生成数量:</span>
                        <InputNumber
                            min={1}
                            max={1000000}
                            value={count}
                            onChange={(val) => setCount(val || 1000)}
                            style={{ width: 150 }}
                        />
                        <span>(最大 1,000,000)</span>
                    </Space>

                    <Space>
                        <span>导出格式:</span>
                        <Select value={format} onChange={setFormat} style={{ width: 150 }}>
                            <Option value="csv">CSV</Option>
                            <Option value="json">JSON</Option>
                            <Option value="ndjson">NDJSON</Option>
                        </Select>
                    </Space>

                    <Button
                        type="primary"
                        size="large"
                        icon={<DownloadOutlined />}
                        onClick={handleExport}
                        loading={loading}
                        style={{ marginTop: 16 }}
                    >
                        {loading ? '生成并导出中...' : '生成并导出'}
                    </Button>
                </Space>

                {loading && (
                    <div style={{ marginTop: 24, textAlign: 'center' }}>
                        <Spin tip="正在生成数据，请稍候..." />
                    </div>
                )}
            </Card>
        </div>
    );
};
