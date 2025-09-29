import json
import os
from user import User


class StatsSubmission:
    def __init__(self, user_email, date, goals, assists):
        self.user_email = user_email
        self.date = date
        self.goals = goals
        self.assists = assists

    @staticmethod
    def load_stats():
        try:
            if not os.path.exists("stats.json") or os.stat("stats.json").st_size == 0:
                return []  # empty file → return empty list
            with open("stats.json", "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod


    def get_stats(self):
        goals = int(input("Enter goals scored: "))
        assists = int(input("Enter assists given: "))
        date = input("Enter match date: ")

        stats = StatsSubmission.load_stats()

        existing_ids = [s.get("match_id") for s in stats]
        existing_ids = [mid for mid in existing_ids if mid is not None]
        match_id = max(existing_ids, default=0) + 1
        while any(s.get("match_id") == match_id for s in stats):
            match_id += 1

        stats.append({
            "match_id": match_id,
            "user_email": self.user_email,
            "goals": goals,
            "assists": assists,
            "date": date,
        })
        StatsSubmission.save_stats(stats)
        return match_id, goals, assists, date

    @staticmethod
    def compute_rating(stat):
        goals = int(stat.get("goals", 0))
        assists = int(stat.get("assists", 0))
        return goals * 10 + assists * 5