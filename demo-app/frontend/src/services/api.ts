/**
 * API client for communicating with the backend
 */

import axios, { AxiosInstance, AxiosError } from 'axios';
import type {
  User,
  AuthResponse,
  MetricData,
  PullRequest,
  PRMetrics,
  Sprint,
  SprintVelocity,
  AIInsight,
  Contributor,
  CommitActivity,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

class APIClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          // Token expired or invalid
          localStorage.removeItem('access_token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Authentication
  async getAuthorizationUrl(provider: 'github' | 'gitlab', redirectUri: string) {
    const response = await this.client.get(`/auth/${provider}/authorize`, {
      params: { redirect_uri: redirectUri },
    });
    return response.data;
  }

  async handleOAuthCallback(code: string, state: string, provider: string): Promise<AuthResponse> {
    const response = await this.client.post('/auth/callback', {
      code,
      state,
      provider,
    });
    return response.data;
  }

  async getCurrentUser(): Promise<User> {
    const response = await this.client.get('/auth/me');
    return response.data;
  }

  async logout(): Promise<void> {
    await this.client.post('/auth/logout');
    localStorage.removeItem('access_token');
  }

  async refreshToken(): Promise<AuthResponse> {
    const response = await this.client.post('/auth/refresh');
    return response.data;
  }

  // Metrics
  async getCommitFrequency(
    teamId: string,
    startDate: string,
    endDate: string
  ): Promise<CommitActivity[]> {
    const response = await this.client.get('/metrics/commit_frequency', {
      params: { team_id: teamId, start_date: startDate, end_date: endDate },
    });
    return response.data;
  }

  async getPRVelocity(
    teamId: string,
    startDate: string,
    endDate: string
  ): Promise<MetricData> {
    const response = await this.client.get('/metrics/pr_velocity', {
      params: { team_id: teamId, start_date: startDate, end_date: endDate },
    });
    return response.data;
  }

  async getPRMetrics(teamId: string): Promise<PRMetrics> {
    const response = await this.client.get('/metrics/pr_analytics', {
      params: { team_id: teamId },
    });
    return response.data;
  }

  async getPullRequests(
    teamId: string,
    state?: string,
    limit?: number
  ): Promise<PullRequest[]> {
    const response = await this.client.get('/pull_requests', {
      params: { team_id: teamId, state, limit },
    });
    return response.data;
  }

  // Sprints
  async getSprints(teamId: string): Promise<Sprint[]> {
    const response = await this.client.get('/sprints', {
      params: { team_id: teamId },
    });
    return response.data;
  }

  async getSprintVelocity(teamId: string, limit: number = 6): Promise<SprintVelocity[]> {
    const response = await this.client.get('/sprints/velocity', {
      params: { team_id: teamId, limit },
    });
    return response.data;
  }

  async createSprint(sprint: Omit<Sprint, 'sprint_id'>): Promise<Sprint> {
    const response = await this.client.post('/sprints', sprint);
    return response.data;
  }

  async updateSprint(sprintId: string, updates: Partial<Sprint>): Promise<Sprint> {
    const response = await this.client.put(`/sprints/${sprintId}`, updates);
    return response.data;
  }

  // AI Insights
  async getAIInsights(teamId: string, category?: string): Promise<AIInsight[]> {
    const response = await this.client.get('/insights', {
      params: { team_id: teamId, category },
    });
    return response.data;
  }

  async generateInsights(teamId: string): Promise<AIInsight[]> {
    const response = await this.client.post('/insights/generate', { team_id: teamId });
    return response.data;
  }

  // Contributors
  async getContributors(teamId: string, limit?: number): Promise<Contributor[]> {
    const response = await this.client.get('/contributors', {
      params: { team_id: teamId, limit },
    });
    return response.data;
  }
}

export const apiClient = new APIClient();
export default apiClient;

