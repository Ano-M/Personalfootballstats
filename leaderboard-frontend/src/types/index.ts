// API Response Types for Football Stats Leaderboard

export interface User {
  first_name: string;
  last_name: string;
  email: string;
  age: number;
  gender: string;
}

export interface LoginResponse {
  access_token: string;
  user: User;
}

export interface SignupData {
  first_name: string;
  last_name: string;
  email: string;
  age: number;
  gender: string;
  password: string;
  confirm_password: string;
}

export interface MatchStats {
  match_id?: number;
  user_email?: string;
  date: string;
  home_team: string;
  away_team: string;
  match_score: string;
  minutes_played: number;
  goals: number;
  shots: number;
  disallowed_goals: number;
  goal_involvements?: number; // Calculated automatically on backend (goals + assists)
  assists: number;
  passes: number;
  successful_passes: number;
  dribbles: number;
  successful_dribbles: number;
  tackles: number;
  missed_tackles: number;
  interceptions: number;
  touches: number;
  unsuccessful_touches: number;
}

export interface LeaderboardEntry {
  match_id: number;
  date: string;
  match: string;
  score: string;
  goals: number;
  assists: number;
  minutes: number;
  rating: number;
  full_stats: MatchStats;
}

export interface MatchDetail {
  match_id: number;
  date: string;
  home_team: string;
  away_team: string;
  match_score: string;
  minutes_played: number;
  rating: number;
  goals: number;
  shots: number;
  disallowed_goals: number;
  goal_involvements: number;
  assists: number;
  passes: number;
  successful_passes: number;
  dribbles: number;
  successful_dribbles: number;
  tackles: number;
  missed_tackles: number;
  interceptions: number;
  touches: number;
  unsuccessful_touches: number;
}

export interface ApiError {
  message: string;
  status?: number;
}
