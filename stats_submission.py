import json
import os

class StatsSubmission:
    def __init__(self, playerId, date, goals, assists):
        self.playerId = playerId
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
        playerId = input("Player ID: ")
        goals = input("Enter goals scored: ")
        assists = input("Enter assists given: ")
        date = input("Enter match date: ")

        stats = StatsSubmission.load_stats()
        stats.append({
            "playerId": playerId,
            "goals": goals,
            "assists": assists,
            "date": date,
        })
        StatsSubmission.save_stats(stats)
        return playerId, goals, assists, date

if __name__ == "__main__":
    sub = StatsSubmission("", "", "", "")
    playerId, goals, assists, date = sub.get_stats()
    print(f"Stats entered: Goals={goals}, Assists={assists}, Date={date}")
