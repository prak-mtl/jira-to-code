/**
 * Pull Request Metrics Bar Chart Component
 * Displays PR size distribution and metrics
 */

import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import type { PRMetrics } from '../../types';

interface PRMetricsChartProps {
  metrics: PRMetrics;
  loading?: boolean;
  error?: string;
}

const COLORS = {
  small: '#10b981',
  medium: '#3b82f6',
  large: '#f59e0b',
  xlarge: '#ef4444',
};

export const PRMetricsChart: React.FC<PRMetricsChartProps> = ({
  metrics,
  loading,
  error,
}) => {
  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-red-600">
          <p className="font-semibold">Error loading data</p>
          <p className="text-sm">{error}</p>
        </div>
      </div>
    );
  }

  if (!metrics) {
    return (
      <div className="flex items-center justify-center h-64">
        <p className="text-gray-500">No PR metrics available</p>
      </div>
    );
  }

  // Prepare data for PR size distribution
  const sizeData = [
    { name: 'Small (<100 lines)', value: metrics.pr_size_distribution.small, color: COLORS.small },
    { name: 'Medium (100-500)', value: metrics.pr_size_distribution.medium, color: COLORS.medium },
    { name: 'Large (500-1000)', value: metrics.pr_size_distribution.large, color: COLORS.large },
    { name: 'X-Large (>1000)', value: metrics.pr_size_distribution.xlarge, color: COLORS.xlarge },
  ];

  return (
    <div className="space-y-6">
      {/* Key Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <p className="text-sm text-gray-600 mb-1">Avg Time to Merge</p>
          <p className="text-2xl font-bold text-gray-900">
            {metrics.average_time_to_merge.toFixed(1)}h
          </p>
        </div>
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <p className="text-sm text-gray-600 mb-1">Avg Review Time</p>
          <p className="text-2xl font-bold text-gray-900">
            {metrics.average_review_time.toFixed(1)}h
          </p>
        </div>
        <div className="bg-white p-4 rounded-lg border border-gray-200">
          <p className="text-sm text-gray-600 mb-1">Approval Rate</p>
          <p className="text-2xl font-bold text-gray-900">
            {metrics.approval_rate.toFixed(0)}%
          </p>
        </div>
      </div>

      {/* PR Size Distribution Chart */}
      <div className="bg-white p-6 rounded-lg border border-gray-200">
        <h3 className="text-lg font-semibold mb-4">PR Size Distribution</h3>
        <div className="w-full h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={sizeData}
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis
                dataKey="name"
                stroke="#6b7280"
                style={{ fontSize: '12px' }}
              />
              <YAxis
                stroke="#6b7280"
                style={{ fontSize: '12px' }}
                label={{ value: 'Number of PRs', angle: -90, position: 'insideLeft' }}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#ffffff',
                  border: '1px solid #e5e7eb',
                  borderRadius: '8px',
                  padding: '12px',
                }}
              />
              <Legend />
              <Bar dataKey="value" name="Pull Requests" radius={[8, 8, 0, 0]}>
                {sizeData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default PRMetricsChart;

