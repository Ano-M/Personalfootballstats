# Football Stats Leaderboard - REST API Documentation

## 🚀 Overview

A complete Flask REST API backend for the football stats leaderboard system. The API connects the React frontend to the existing backend logic with JWT authentication, comprehensive validation, and full CRUD operations for match statistics.

## 📁 Project Structure

```
backend/
├── app.py                    # Main Flask application
├── config.py                 # Configuration management
├── .env.example              # Environment variables template
├── .env                      # Actual environment variables (not committed)
├── .gitignore                # Git ignore file
├── routes/
│   ├── __init__.py
│   ├── auth.py               # Authentication endpoints
│   └── stats.py              # Stats management endpoints
├── user.py                   # User class (existing)
├── controller/
│   └── stats_controller.py   # Stats controller (existing)
├── validation.py             # Input validation (existing)
├── leaderboard.py            # Leaderboard logic (existing)
├── users.json                # User data storage
└── stats.json                # Match stats storage
```

## 🔧 Setup and Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `flask==3.0.0` - Web framework
- `flask-cors==4.0.0` - CORS support
- `flask-jwt-extended==4.6.0` - JWT authentication
- `python-dotenv==1.0.0` - Environment variables
- `bcrypt==4.1.2` - Password hashing

### 2. Configure Environment

Copy `.env.example` to `.env` and update values:

```bash
cp backend/.env.example backend/.env
```

Edit `.env`:
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
CORS_ORIGINS=http://localhost:3000
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

### 3. Start the Server

```bash
cd backend
python app.py
```

The server will start on `http://localhost:5000`

## 📚 API Endpoints

### Base URL
```
http://localhost:5000
```

### Health Check

**GET** `/health`

Check if the API is running.

```bash
curl http://localhost:5000/health
```

Response:
```json
{
  "status": "healthy"
}
```

---

## 🔐 Authentication Endpoints

### 1. User Signup

**POST** `/api/auth/signup`

Register a new user account.

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "age": 25,
  "gender": "M",
  "password": "password123",
  "confirm_password": "password123"
}
```

**Response (201):**
```json
{
  "message": "User registered successfully",
  "user": {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "age": 25,
    "gender": "M"
  }
}
```

**Curl Example:**
```bash
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "age": 25,
    "gender": "M",
    "password": "password123",
    "confirm_password": "password123"
  }'
```

**Validation Rules:**
- `first_name`, `last_name`: Non-empty strings
- `email`: Valid email format
- `age`: Integer between 1-120
- `gender`: "M", "F", or "Other"
- `password`: Minimum 6 characters
- `confirm_password`: Must match password

---

### 2. User Login

**POST** `/api/auth/login`

Authenticate user and receive JWT token.

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

**Response (200):**
```json
{
  "message": "Login successful",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "age": 25,
    "gender": "M"
  }
}
```

**Curl Example:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

**Save Token for Later Use:**
```bash
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"password123"}' \
  | python -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
```

---

### 3. Get Current User Profile

**GET** `/api/auth/me` 🔒 Protected

Get the currently authenticated user's profile.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "user": {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "age": 25,
    "gender": "M"
  }
}
```

**Curl Example:**
```bash
curl -X GET http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

---

## ⚽ Stats Endpoints

### 1. Submit Match Statistics

**POST** `/api/stats/submit` 🔒 Protected

Submit statistics for a match. All 18 fields are validated.

**Headers:**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**Request Body (All 18 Fields):**
```json
{
  "date": "2025-12-30",
  "home_team": "Manchester United",
  "away_team": "Liverpool",
  "match_score": "3-2",
  "minutes_played": 90,
  "goals": 2,
  "shots": 8,
  "disallowed_goals": 0,
  "goal_involvements": 3,
  "assists": 1,
  "passes": 45,
  "successful_passes": 38,
  "dribbles": 10,
  "successful_dribbles": 7,
  "tackles": 5,
  "missed_tackles": 2,
  "interceptions": 3,
  "touches": 65,
  "unsuccessful_touches": 8
}
```

**Response (201):**
```json
{
  "message": "Statistics submitted successfully",
  "match_id": 1,
  "rating": 86.16,
  "stats": {
    "match_id": 1,
    "user_email": "john@example.com",
    "date": "2025-12-30",
    "home_team": "Manchester United",
    "away_team": "Liverpool",
    "match_score": "3-2",
    "minutes_played": 90,
    "goals": 2,
    "shots": 8,
    ...
  }
}
```

**Curl Example:**
```bash
curl -X POST http://localhost:5000/api/stats/submit \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-12-30",
    "home_team": "Manchester United",
    "away_team": "Liverpool",
    "match_score": "3-2",
    "minutes_played": 90,
    "goals": 2,
    "shots": 8,
    "disallowed_goals": 0,
    "goal_involvements": 3,
    "assists": 1,
    "passes": 45,
    "successful_passes": 38,
    "dribbles": 10,
    "successful_dribbles": 7,
    "tackles": 5,
    "missed_tackles": 2,
    "interceptions": 3,
    "touches": 65,
    "unsuccessful_touches": 8
  }'
```

**Field Validation Rules:**

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `date` | String | YYYY-MM-DD | Match date |
| `home_team` | String | 1-50 chars | Home team name |
| `away_team` | String | 1-50 chars | Away team name |
| `match_score` | String | X-Y | Match score (e.g., "2-1") |
| `minutes_played` | Integer | 1-120 | Minutes played |
| `goals` | Integer | 0-15 | Goals scored |
| `shots` | Integer | 0-30 | Total shots |
| `disallowed_goals` | Integer | 0-5 | Disallowed goals |
| `goal_involvements` | Integer | 0-20 | Total goal involvements |
| `assists` | Integer | 0-15 | Assists given |
| `passes` | Integer | 0-200 | Total passes |
| `successful_passes` | Integer | 0-200 | Successful passes |
| `dribbles` | Integer | 0-50 | Total dribbles |
| `successful_dribbles` | Integer | 0-50 | Successful dribbles |
| `tackles` | Integer | 0-30 | Tackles made |
| `missed_tackles` | Integer | 0-30 | Missed tackles |
| `interceptions` | Integer | 0-30 | Interceptions |
| `touches` | Integer | 0-300 | Total touches |
| `unsuccessful_touches` | Integer | 0-300 | Unsuccessful touches |

**Cross-Field Validation:**
- `successful_passes` ≤ `passes`
- `successful_dribbles` ≤ `dribbles`
- `unsuccessful_touches` ≤ `touches`
- `goals` ≤ `shots`
- `goal_involvements` ≥ `goals + assists`

---

### 2. Get Personal Leaderboard

**GET** `/api/stats/leaderboard` 🔒 Protected

Get user's personal leaderboard with all matches ranked by rating.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "leaderboard": [
    {
      "match_id": 1,
      "date": "2025-12-30",
      "match": "Manchester United vs Liverpool",
      "score": "3-2",
      "goals": 2,
      "assists": 1,
      "minutes": 90,
      "rating": 86.16,
      "full_stats": { ... }
    }
  ],
  "summary": {
    "total_matches": 1,
    "average_rating": 86.16,
    "total_goals": 2,
    "total_assists": 1,
    "best_performance": {
      "match_id": 1,
      "rating": 86.16,
      "date": "2025-12-30"
    }
  }
}
```

**Curl Example:**
```bash
curl -X GET http://localhost:5000/api/stats/leaderboard \
  -H "Authorization: Bearer $TOKEN"
```

---

### 3. Get Match Details

**GET** `/api/stats/match/<match_id>` 🔒 Protected

Get detailed statistics for a specific match.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "match": {
    "match_id": 1,
    "date": "2025-12-30",
    "home_team": "Manchester United",
    "away_team": "Liverpool",
    "match_score": "3-2",
    "minutes_played": 90,
    "rating": 86.16
  },
  "attacking": {
    "goals": 2,
    "shots": 8,
    "disallowed_goals": 0,
    "assists": 1,
    "goal_involvements": 3
  },
  "passing": {
    "passes": 45,
    "successful_passes": 38,
    "accuracy": 84.4
  },
  "dribbling": {
    "dribbles": 10,
    "successful_dribbles": 7,
    "success_rate": 70.0
  },
  "defensive": {
    "tackles": 5,
    "missed_tackles": 2,
    "interceptions": 3
  },
  "ball_control": {
    "touches": 65,
    "unsuccessful_touches": 8,
    "success_rate": 87.7
  }
}
```

**Curl Example:**
```bash
curl -X GET http://localhost:5000/api/stats/match/1 \
  -H "Authorization: Bearer $TOKEN"
```

---

### 4. Get All Matches

**GET** `/api/stats/all` 🔒 Protected

Get all matches for the current user (sorted by date, most recent first).

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "matches": [
    {
      "match_id": 1,
      "date": "2025-12-30",
      "home_team": "Manchester United",
      "away_team": "Liverpool",
      "match_score": "3-2",
      "minutes_played": 90,
      "goals": 2,
      "assists": 1,
      "rating": 86.16
    }
  ],
  "total_count": 1
}
```

**Curl Example:**
```bash
curl -X GET http://localhost:5000/api/stats/all \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🔒 Authentication & Security

### JWT Token Authentication

All protected endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### Token Expiration

- Access tokens expire after **24 hours**
- Users must login again to get a new token

### Error Responses

**401 Unauthorized - Missing Token:**
```json
{
  "msg": "Missing Authorization Header"
}
```

**401 Unauthorized - Invalid Credentials:**
```json
{
  "error": "Invalid email or password"
}
```

**422 Unprocessable Entity - Invalid Token:**
```json
{
  "msg": "Not enough segments"
}
```

**400 Bad Request - Validation Error:**
```json
{
  "error": "Goals (5) cannot exceed shots (3)"
}
```

**404 Not Found:**
```json
{
  "error": "Match ID 999 not found"
}
```

---

## 🧪 Testing

### Complete Test Script

Save this as `test_api.sh`:

```bash
#!/bin/bash

BASE_URL="http://localhost:5000"

# 1. Signup
echo "1. Testing signup..."
curl -X POST "$BASE_URL/api/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Test",
    "last_name": "User",
    "email": "test@example.com",
    "age": 25,
    "gender": "M",
    "password": "password123",
    "confirm_password": "password123"
  }'

# 2. Login and get token
echo -e "\n\n2. Testing login..."
TOKEN=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' \
  | python -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

echo "Token: ${TOKEN:0:50}..."

# 3. Get profile
echo -e "\n\n3. Testing /api/auth/me..."
curl -X GET "$BASE_URL/api/auth/me" \
  -H "Authorization: Bearer $TOKEN"

# 4. Submit stats
echo -e "\n\n4. Testing stats submission..."
curl -X POST "$BASE_URL/api/stats/submit" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-12-30",
    "home_team": "Team A",
    "away_team": "Team B",
    "match_score": "2-1",
    "minutes_played": 90,
    "goals": 1,
    "shots": 5,
    "disallowed_goals": 0,
    "goal_involvements": 1,
    "assists": 0,
    "passes": 40,
    "successful_passes": 35,
    "dribbles": 8,
    "successful_dribbles": 6,
    "tackles": 4,
    "missed_tackles": 1,
    "interceptions": 2,
    "touches": 50,
    "unsuccessful_touches": 5
  }'

# 5. Get leaderboard
echo -e "\n\n5. Testing leaderboard..."
curl -X GET "$BASE_URL/api/stats/leaderboard" \
  -H "Authorization: Bearer $TOKEN"
```

Run with:
```bash
chmod +x test_api.sh
./test_api.sh
```

---

## 📊 Rating System

The performance rating (0-100 scale) is calculated based on:

### Components (Maximum Points)

1. **Attacking (40 points)**
   - Goals: 10 points each
   - Assists: 5 points each
   - Goal involvements: 2 points each
   - Non-goal shots: 0.5 points each

2. **Passing (20 points)**
   - Pass completion rate × 20

3. **Dribbling (15 points)**
   - Success rate × 10
   - Successful dribbles × 0.5

4. **Defensive (15 points)**
   - Tackles: 2 points each
   - Interceptions: 2 points each

5. **Ball Control (10 points)**
   - Touch success rate × 10

### Normalization

All ratings are normalized to 90 minutes and capped at 100.

---

## 🎯 Frontend Integration

### React Example

```javascript
const API_BASE_URL = 'http://localhost:5000';

// Login
const login = async (email, password) => {
  const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  const data = await response.json();
  localStorage.setItem('token', data.access_token);
  return data;
};

// Get leaderboard
const getLeaderboard = async () => {
  const token = localStorage.getItem('token');
  const response = await fetch(`${API_BASE_URL}/api/stats/leaderboard`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  return await response.json();
};

// Submit stats
const submitStats = async (statsData) => {
  const token = localStorage.getItem('token');
  const response = await fetch(`${API_BASE_URL}/api/stats/submit`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(statsData)
  });
  return await response.json();
};
```

---

## 📝 Data Preservation

✅ **Original data preserved:**
- `backend/users.json` - Existing user with bcrypt hash intact
- `backend/stats.json` - All existing match data preserved

---

## ✅ Success Criteria - All Met!

- ✅ Flask API runs without errors on port 5000
- ✅ All 6 endpoints respond correctly
- ✅ JWT authentication works (login returns token)
- ✅ Protected routes reject requests without token
- ✅ Stats validation works (rejects invalid data)
- ✅ Can test with curl: signup, login, submit stats, get leaderboard
- ✅ Original data preserved (users.json & stats.json)
- ✅ All 18 stats fields supported and validated
- ✅ Cross-field validation working
- ✅ Rating calculation using existing StatsController
- ✅ CORS configured for React frontend

---

## 🚀 Next Steps

1. **Frontend Integration**
   - Update React app to use these API endpoints
   - Implement token storage (localStorage/sessionStorage)
   - Add authentication state management

2. **Production Deployment**
   - Use production WSGI server (gunicorn/uWSGI)
   - Set strong SECRET_KEY and JWT_SECRET_KEY
   - Configure CORS for production domain
   - Use HTTPS

3. **Enhancements**
   - Add refresh token functionality
   - Implement password reset
   - Add user profile update endpoint
   - Add match deletion endpoint
   - Implement pagination for large datasets

---

## 📞 Support

For issues or questions, refer to the codebase or create an issue in the repository.

**API Version:** 1.0.0
**Last Updated:** 2025-01-09
