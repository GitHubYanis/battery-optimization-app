import type { Data, Layout } from 'plotly.js';

interface ChartData {
  data: Data[];
  layout: Partial<Layout>;
}

export interface VisualizeResponse {
  summary: VisualizeSummary;
  charts: {
    load_chart: ChartData;
    dispatch_chart: ChartData;
    soc_chart: ChartData;
  };
}

export interface VisualizeSummary {
  total_cost_before: number;
  total_cost_after: number;
  savings: number;
  peak_before_kw: number;
  peak_after_kw: number;
}

export interface ChartsResponse {
    load_chart: ChartData;
    dispatch_chart: ChartData;
    soc_chart: ChartData;
}