export interface FieldConfig {
  name: string;
  type: string;
  unique?: boolean;
  constraints?: {
    min?: number;
    max?: number;
    min_length?: number;
    max_length?: number;
    regex?: string;
    null_pct?: number;
    precision?: number;
  };
  distribution?: {
    type?: string;
    start?: string;
    end?: string;
    mu?: number;
    sigma?: number;
  };
  values?: string[];
  weights?: number[];
}

export interface DatasetSchema {
  fields: FieldConfig[];
}

export interface ExportRequest {
  fields: FieldConfig[];
  count: number;
  format: 'csv' | 'json' | 'ndjson';
}

export interface ExportResponse {
  id: string;
  status: string;
  format: string;
  size: number;
  count: number;
}

export interface GenerateRequest {
  fields: FieldConfig[];
  count: number;
  preview?: boolean;
}

export interface GenerateResponse {
  data: any[];
  total: number;
  preview: boolean;
}
