import React, { useState } from 'react';
import { Card, InputNumber, Button, Space, message, Spin, Table } from 'antd';
import { FieldEditor } from '../components/FieldEditor';
import { api } from '../services/api';
import type { FieldConfig } from '../types';

export const TemplateEditor: React.FC = () => {
    const [fields, setFields] = useState<FieldConfig[]>([]);
    const [count, setCount] = useState(100);
    const [loading, setLoading] = useState(false);
    const [previewData, setPreviewData] = useState<any[]>([]);

    const handlePreview = async () => {
        if (fields.length === 0) {
            message.warning('请至少添加一个字段');
            return;
        }

        setLoading(true);
        try {
            const response = await api.generateData({
                fields,
                count: Math.min(count, 100),
                preview: true,
            });
            setPreviewData(response.data);
            message.success(`预览生成成功，共 ${response.total} 条数据`);
        } catch (error: any) {
            message.error(`预览失败: ${error.response?.data?.error || error.message}`);
        } finally {
            setLoading(false);
        }
    };

    // 根据字段动态生成表格列
    const columns = fields.map((field) => ({
        title: field.name,
        dataIndex: field.name,
        key: field.name,
        ellipsis: true,
    }));

    return (
        <div style={{ padding: 24 }}>
            <Card title="模板编辑器" style={{ marginBottom: 24 }}>
                <FieldEditor value={fields} onChange={setFields} />
            </Card>

            <Card title="预览设置" style={{ marginBottom: 24 }}>
                <Space>
                    <span>生成数量:</span>
                    <InputNumber
                        min={1}
                        max={1000}
                        value={count}
                        onChange={(val) => setCount(val || 100)}
                    />
                    <Button type="primary" onClick={handlePreview} loading={loading}>
                        生成预览
                    </Button>
                </Space>
            </Card>

            {previewData.length > 0 && (
                <Card title="数据预览">
                    <Spin spinning={loading}>
                        <Table
                            dataSource={previewData}
                            columns={columns}
                            rowKey={(_, index) => index?.toString() || '0'}
                            pagination={{ pageSize: 10 }}
                            scroll={{ x: 'max-content' }}
                        />
                    </Spin>
                </Card>
            )}
        </div>
    );
};
