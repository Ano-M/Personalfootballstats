import axios, { type AxiosInstance, AxiosError } from 'axios';
import type { User, LoginResponse, SignupData, MatchStats, LeaderboardEntry, MatchDetail } from '../types';

// Get base URL from environment variable or use default
const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000';

// Create axios instance with default config
const apiClient: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 second timeout
});

// Request interceptor to add JWT token to headers
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    // Handle 401 unauthorized - only redirect if user was logged in (has token)
    // Don't redirect on login/signup failures
    if (error.response?.status === 401) {
      const token = localStorage.getItem('auth_token');
      if (token) {
        // User was logged in but token expired/invalid - clear and redirect
        localStorage.removeItem('auth_token');
        window.location.href = '/';
      }
    }
    return Promise.reject(error);
  }
);

// Helper function to handle API errors
const handleApiError = (error: unknown): string => {
  if (axios.isAxiosError(error)) {
    if (error.response?.data?.message) {
      return error.response.data.message;
    }
    if (error.response?.data?.error) {
      return error.response.data.error;
    }
    if (error.message) {
      return error.message;
    }
  }
  return 'An unexpected error occurred';
};

// API Service object with all endpoints
export const api = {
  // Authentication endpoints
  auth: {
    signup: async (data: SignupData): Promise<{ message: string; user: User }> => {
      try {
        const response = await apiClient.post('/api/auth/signup', data);
        return response.data;
      } catch (error) {
        throw new Error(handleApiError(error));
      }
    },

    login: async (email: string, password: string): Promise<LoginResponse> => {
      try {
        const response = await apiClient.post('/api/auth/login', { email, password });
        const { access_token } = response.data;

        // Store token in localStorage
        localStorage.setItem('auth_token', access_token);

        return response.data;
      } catch (error) {
        throw new Error(handleApiError(error));
      }
    },

    getProfile: async (): Promise<User> => {
      try {
        const response = await apiClient.get('/api/auth/me');
        return response.data;
      } catch (error) {
        throw new Error(handleApiError(error));
      }
    },

    logout: () => {
      localStorage.removeItem('auth_token');
    },

    isAuthenticated: (): boolean => {
      return !!localStorage.getItem('auth_token');
    },

    getToken: (): string | null => {
      return localStorage.getItem('auth_token');
    },
  },

  // Stats endpoints
  stats: {
    submit: async (stats: MatchStats): Promise<{ message: string; match_id: number }> => {
      try {
        const response = await apiClient.post('/api/stats/submit', stats);
        return response.data;
      } catch (error) {
        throw new Error(handleApiError(error));
      }
    },

    getLeaderboard: async (): Promise<LeaderboardEntry[]> => {
      try {
        const response = await apiClient.get('/api/stats/leaderboard');
        return response.data.leaderboard || [];
      } catch (error) {
        throw new Error(handleApiError(error));
      }
    },

    getMatch: async (matchId: number): Promise<MatchDetail> => {
      try {
        const response = await apiClient.get(`/api/stats/match/${matchId}`);
        // Flatten the nested response into MatchDetail format
        const data = response.data;
        return {
          match_id: data.match.match_id,
          date: data.match.date,
          home_team: data.match.home_team,
          away_team: data.match.away_team,
          match_score: data.match.match_score,
          minutes_played: data.match.minutes_played,
          rating: data.match.rating,
          goals: data.attacking.goals,
          shots: data.attacking.shots,
          disallowed_goals: data.attacking.disallowed_goals,
          goal_involvements: data.attacking.goal_involvements,
          assists: data.attacking.assists,
          passes: data.passing.passes,
          successful_passes: data.passing.successful_passes,
          dribbles: data.dribbling.dribbles,
          successful_dribbles: data.dribbling.successful_dribbles,
          tackles: data.defensive.tackles,
          missed_tackles: data.defensive.missed_tackles,
          interceptions: data.defensive.interceptions,
          touches: data.ball_control.touches,
          unsuccessful_touches: data.ball_control.unsuccessful_touches,
        };
      } catch (error) {
        throw new Error(handleApiError(error));
      }
    },

    getAllMatches: async (): Promise<MatchStats[]> => {
      try {
        const response = await apiClient.get('/api/stats/all');
        return response.data;
      } catch (error) {
        throw new Error(handleApiError(error));
      }
    },
  },
};

export default api;
