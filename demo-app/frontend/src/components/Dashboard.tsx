/**
 * Main Dashboard Component
 * Displays overview of team productivity metrics
 */

import React, { useEffect, useState } from 'react';
import { Activity, GitPullRequest, TrendingUp, Users } from 'lucide-react';
import { CommitActivityChart } from './charts/CommitActivityChart';
import { PRMetricsChart } from './charts/PRMetricsChart';
import { apiClient } from '../services/api';
import type { CommitActivity, PRMetrics } from '../types';

export const Dashboard: React.FC = () => {
  const [commitData, setCommitData] = useState<CommitActivity[]>([]);
  const [prMetrics, setPRMetrics] = useState<PRMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const teamId = 'default-team'; // TODO: Get from user context

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Calculate date range (last 30 days)
      const endDate = new Date();
      const startDate = new Date();
      startDate.setDate(startDate.getDate() - 30);

      // Fetch data in parallel
      const [commits, metrics] = await Promise.all([
        apiClient.getCommitFrequency(
          teamId,
          startDate.toISOString(),
          endDate.toISOString()
        ),
        apiClient.getPRMetrics(teamId),
      ]);

      setCommitData(commits);
      setPRMetrics(metrics);
    } catch (err) {
      console.error('Error loading dashboard data:', err);
      setError('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">
            Developer Productivity Dashboard
          </h1>
          <p className="mt-2 text-sm text-gray-600">
            Real-time insights into your team's development metrics
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <SummaryCard
            icon={<Activity className="w-6 h-6" />}
            title="Total Commits"
            value={commitData.reduce((sum, item) => sum + item.count, 0)}
            subtitle="Last 30 days"
            color="blue"
          />
          <SummaryCard
            icon={<GitPullRequest className="w-6 h-6" />}
            title="Avg Merge Time"
            value={prMetrics ? `${prMetrics.average_time_to_merge.toFixed(1)}h` : '-'}
            subtitle="Pull requests"
            color="green"
          />
          <SummaryCard
            icon={<TrendingUp className="w-6 h-6" />}
            title="Approval Rate"
            value={prMetrics ? `${prMetrics.approval_rate.toFixed(0)}%` : '-'}
            subtitle="Pull requests"
            color="purple"
          />
          <SummaryCard
            icon={<Users className="w-6 h-6" />}
            title="Active Contributors"
            value={new Set(commitData.flatMap(item => item.authors)).size}
            subtitle="Last 30 days"
            color="orange"
          />
        </div>

        {/* Charts */}
        <div className="space-y-8">
          {/* Commit Activity */}
          <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
            <h2 className="text-xl font-semibold mb-4">Commit Activity</h2>
            <CommitActivityChart
              data={commitData}
              loading={loading}
              error={error || undefined}
            />
          </div>

          {/* PR Metrics */}
          <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
            <h2 className="text-xl font-semibold mb-4">Pull Request Analytics</h2>
            {prMetrics && (
              <PRMetricsChart
                metrics={prMetrics}
                loading={loading}
                error={error || undefined}
              />
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

// Summary Card Component
interface SummaryCardProps {
  icon: React.ReactNode;
  title: string;
  value: string | number;
  subtitle: string;
  color: 'blue' | 'green' | 'purple' | 'orange';
}

const SummaryCard: React.FC<SummaryCardProps> = ({
  icon,
  title,
  value,
  subtitle,
  color,
}) => {
  const colorClasses = {
    blue: 'bg-blue-100 text-blue-600',
    green: 'bg-green-100 text-green-600',
    purple: 'bg-purple-100 text-purple-600',
    orange: 'bg-orange-100 text-orange-600',
  };

  return (
    <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <div className={`p-3 rounded-lg ${colorClasses[color]}`}>
          {icon}
        </div>
      </div>
      <h3 className="text-sm font-medium text-gray-600 mb-1">{title}</h3>
      <p className="text-2xl font-bold text-gray-900">{value}</p>
      <p className="text-xs text-gray-500 mt-1">{subtitle}</p>
    </div>
  );
};

export default Dashboard;

