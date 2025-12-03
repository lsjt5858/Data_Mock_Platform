import React, { useState } from 'react';
import { Form, Input, Select, InputNumber, Button, Space, Card, Row, Col } from 'antd';
import { PlusOutlined, MinusCircleOutlined } from '@ant-design/icons';
import type { FieldConfig } from '../types';

const { Option } = Select;

interface FieldEditorProps {
    value?: FieldConfig[];
    onChange?: (fields: FieldConfig[]) => void;
}

const FIELD_TYPES = [
    { value: 'int', label: '整数' },
    { value: 'float', label: '浮点数' },
    { value: 'string', label: '字符串' },
    { value: 'boolean', label: '布尔值' },
    { value: 'datetime', label: '日期时间' },
    { value: 'uuid', label: 'UUID' },
    { value: 'email', label: '邮箱' },
    { value: 'phone', label: '电话号码' },
    { value: 'name', label: '姓名' },
    { value: 'address', label: '地址' },
    { value: 'company', label: '公司名' },
    { value: 'city', label: '城市' },
    { value: 'url', label: 'URL' },
    { value: 'ipv4', label: 'IPv4地址' },
];

export const FieldEditor: React.FC<FieldEditorProps> = ({ value = [], onChange }) => {
    const [fields, setFields] = useState<FieldConfig[]>(value);

    const handleAddField = () => {
        const newField: FieldConfig = {
            name: `field_${fields.length + 1}`,
            type: 'string',
        };
        const newFields = [...fields, newField];
        setFields(newFields);
        onChange?.(newFields);
    };

    const handleRemoveField = (index: number) => {
        const newFields = fields.filter((_, i) => i !== index);
        setFields(newFields);
        onChange?.(newFields);
    };

    const handleFieldChange = (index: number, key: keyof FieldConfig, val: any) => {
        const newFields = [...fields];
        newFields[index] = { ...newFields[index], [key]: val };
        setFields(newFields);
        onChange?.(newFields);
    };

    const handleConstraintChange = (index: number, key: string, val: any) => {
        const newFields = [...fields];
        newFields[index] = {
            ...newFields[index],
            constraints: {
                ...newFields[index].constraints,
                [key]: val,
            },
        };
        setFields(newFields);
        onChange?.(newFields);
    };

    return (
        <div>
            <Space direction="vertical" style={{ width: '100%' }} size="middle">
                {fields.map((field, index) => (
                    <Card
                        key={index}
                        size="small"
                        title={`字段 ${index + 1}`}
                        extra={
                            <MinusCircleOutlined
                                onClick={() => handleRemoveField(index)}
                                style={{ color: 'red', cursor: 'pointer' }}
                            />
                        }
                    >
                        <Row gutter={16}>
                            <Col span={8}>
                                <Form.Item label="字段名">
                                    <Input
                                        value={field.name}
                                        onChange={(e) => handleFieldChange(index, 'name', e.target.value)}
                                        placeholder="字段名称"
                                    />
                                </Form.Item>
                            </Col>
                            <Col span={8}>
                                <Form.Item label="类型">
                                    <Select
                                        value={field.type}
                                        onChange={(val) => handleFieldChange(index, 'type', val)}
                                    >
                                        {FIELD_TYPES.map((type) => (
                                            <Option key={type.value} value={type.value}>
                                                {type.label}
                                            </Option>
                                        ))}
                                    </Select>
                                </Form.Item>
                            </Col>
                            <Col span={8}>
                                <Form.Item label="唯一性">
                                    <Select
                                        value={field.unique ? 'true' : 'false'}
                                        onChange={(val) => handleFieldChange(index, 'unique', val === 'true')}
                                    >
                                        <Option value="false">否</Option>
                                        <Option value="true">是</Option>
                                    </Select>
                                </Form.Item>
                            </Col>
                        </Row>

                        {/* 约束配置 - 仅对数值类型显示 */}
                        {(field.type === 'int' || field.type === 'float') && (
                            <Row gutter={16}>
                                <Col span={12}>
                                    <Form.Item label="最小值">
                                        <InputNumber
                                            value={field.constraints?.min}
                                            onChange={(val) => handleConstraintChange(index, 'min', val)}
                                            style={{ width: '100%' }}
                                        />
                                    </Form.Item>
                                </Col>
                                <Col span={12}>
                                    <Form.Item label="最大值">
                                        <InputNumber
                                            value={field.constraints?.max}
                                            onChange={(val) => handleConstraintChange(index, 'max', val)}
                                            style={{ width: '100%' }}
                                        />
                                    </Form.Item>
                                </Col>
                            </Row>
                        )}

                        {/* 字符串长度约束 */}
                        {field.type === 'string' && (
                            <Row gutter={16}>
                                <Col span={12}>
                                    <Form.Item label="最小长度">
                                        <InputNumber
                                            value={field.constraints?.min_length}
                                            onChange={(val) => handleConstraintChange(index, 'min_length', val)}
                                            style={{ width: '100%' }}
                                        />
                                    </Form.Item>
                                </Col>
                                <Col span={12}>
                                    <Form.Item label="最大长度">
                                        <InputNumber
                                            value={field.constraints?.max_length}
                                            onChange={(val) => handleConstraintChange(index, 'max_length', val)}
                                            style={{ width: '100%' }}
                                        />
                                    </Form.Item>
                                </Col>
                            </Row>
                        )}
                    </Card>
                ))}
            </Space>

            <Button
                type="dashed"
                onClick={handleAddField}
                icon={<PlusOutlined />}
                style={{ width: '100%', marginTop: 16 }}
            >
                添加字段
            </Button>
        </div>
    );
};
