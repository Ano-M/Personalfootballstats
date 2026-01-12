# Quick Start Guide - Flask API

## 🚀 Start the API Server

```bash
cd backend
python app.py
```

Server will run on: **http://localhost:5000**

## 📋 Quick Test (Copy & Paste)

```bash
# 1. Create a new user
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

# 2. Login and get token
TOKEN=$(curl -s -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"password123"}' \
  | python -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

echo "Token: ${TOKEN:0:50}..."

# 3. Submit match stats
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

# 4. Get leaderboard
curl -X GET http://localhost:5000/api/stats/leaderboard \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool
```

## 📚 Available Endpoints

### Authentication (No token needed)
- `POST /api/auth/signup` - Register
- `POST /api/auth/login` - Login & get token

### Protected (Token required)
- `GET /api/auth/me` - Get profile
- `POST /api/stats/submit` - Submit stats
- `GET /api/stats/leaderboard` - Get leaderboard
- `GET /api/stats/match/<id>` - Match details
- `GET /api/stats/all` - All matches

## 📖 Full Documentation

See `API_DOCUMENTATION.md` for complete details.

## 🔑 Existing Test User

```
Email: anomaphosa@gmail.com
Password: (use your original password)
```

## ✅ What's Working

✅ JWT authentication
✅ All 6 endpoints tested
✅ Input validation (17 fields - goal_involvements calculated automatically)
✅ Protected routes
✅ Rating calculation (0-10 scale)
✅ CORS for React frontend
✅ Original data preserved
