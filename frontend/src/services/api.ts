import axios from 'axios';
import type { GenerateRequest, GenerateResponse, ExportRequest, ExportResponse } from '../types';

const API_BASE_URL = 'http://localhost:5001';

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: 60000,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const api = {
    // 生成数据
    generateData: async (request: GenerateRequest): Promise<GenerateResponse> => {
        const response = await apiClient.post('/api/generate', request);
        return response.data;
    },

    // 创建导出
    createExport: async (request: ExportRequest): Promise<ExportResponse> => {
        const response = await apiClient.post('/api/exports', request);
        return response.data;
    },

    // 下载导出
    downloadExport: (exportId: string): string => {
        return `${API_BASE_URL}/api/exports/${exportId}/download`;
    },

    // 健康检查
    healthCheck: async (): Promise<any> => {
        const response = await apiClient.get('/api/health');
        return response.data;
    },
};
