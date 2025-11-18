/**
 * TypeScript type definitions for the Developer Productivity Dashboard
 */

// Time Series Data
export interface TimeSeriesMetric {
  timestamp: string; // ISO 8601 string
  value: number;
  unit?: string;
}

export interface MetricData {
  metric_type: string;
  team_id: string;
  data: TimeSeriesMetric[];
}

// User Types
export interface User {
  user_id: string;
  username: string;
  email?: string;
  name?: string;
  avatar_url?: string;
  provider: 'github' | 'gitlab';
  team_id?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: User;
}

// Commit Data
export interface Commit {
  sha: string;
  message: string;
  author: {
    name: string;
    email: string;
    date: string;
  };
  url: string;
  repository: string;
}

export interface CommitActivity {
  date: string;
  count: number;
  authors: string[];
}

// Pull Request / Merge Request Data
export interface PullRequest {
  id: string;
  number: number;
  title: string;
  state: 'open' | 'closed' | 'merged';
  author: string;
  created_at: string;
  updated_at: string;
  merged_at?: string;
  closed_at?: string;
  url: string;
  repository: string;
  additions: number;
  deletions: number;
  changed_files: number;
  review_comments: number;
  reviews: Review[];
}

export interface Review {
  id: string;
  user: string;
  state: 'approved' | 'changes_requested' | 'commented';
  submitted_at: string;
}

// PR Metrics
export interface PRMetrics {
  average_time_to_merge: number; // in hours
  average_review_time: number; // in hours
  approval_rate: number; // percentage
  pr_size_distribution: {
    small: number;
    medium: number;
    large: number;
    xlarge: number;
  };
}

// Sprint Data
export interface Sprint {
  sprint_id: string;
  name: string;
  team_id: string;
  start_date: string;
  end_date: string;
  capacity: number; // story points
  completed_points: number;
  status: 'planned' | 'active' | 'completed';
}

export interface SprintVelocity {
  sprint_name: string;
  planned_points: number;
  completed_points: number;
  velocity: number;
}

export interface BurndownData {
  date: string;
  ideal: number;
  actual: number;
}

// AI Insights
export interface AIInsight {
  insight_id: string;
  category: 'productivity_pattern' | 'bottleneck_detection' | 'team_health';
  title: string;
  description: string;
  severity: 'info' | 'warning' | 'critical';
  recommendations: string[];
  generated_at: string;
  team_id: string;
}

// Contributor Data
export interface Contributor {
  username: string;
  name?: string;
  avatar_url?: string;
  commits: number;
  pull_requests: number;
  reviews: number;
  score: number;
}

// Code Review Heatmap
export interface HeatmapData {
  day: string; // 'Monday', 'Tuesday', etc.
  hour: number; // 0-23
  count: number;
}

// Chart Props
export interface ChartProps {
  title: string;
  data: any[];
  loading?: boolean;
  error?: string;
}

// Filter Options
export interface DateRange {
  start: Date;
  end: Date;
}

export interface FilterOptions {
  dateRange: DateRange;
  repositories: string[];
  teamMembers: string[];
}

// API Response Types
export interface APIResponse<T> {
  data: T;
  message?: string;
  error?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  has_more: boolean;
}

