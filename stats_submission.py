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
    def save_stats(StatsSubmission):
        with open("stats.json", "w") as f:
            json.dump(StatsSubmission, f, indent=4)

    def get_stats(self):
        goals = input("Enter goals scored: ")
        assists = input("Enter assists given: ")
        date = input("Enter match date: ")

        stats = StatsSubmission.load_stats()
        stats.append({
            "user_email": self.user_email,
            "goals": goals,
            "assists": assists,
            "date": date,
        })
        StatsSubmission.save_stats(stats)
        return goals, assists, date

if __name__ == "__main__":
    user = User("", "", "", "", "")
    logged_in_user = user.login()

    if logged_in_user:
        sub = StatsSubmission(logged_in_user["email"], "", "", "")
        goals, assists, date = sub.get_stats()
        print(f"Stats entered: Goals={goals}, Assists={assists}, Date={date}")
