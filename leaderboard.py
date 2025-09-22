import stats_submission
from stats_submission import StatsSubmission

class Leaderboard:
    @staticmethod
    def get_user_stats(user_email):
        stats = StatsSubmission.load_stats()
        # Filter stats for the logged-in user
        return [s for s in stats if s["user_email"] == user_email]

    @staticmethod
    def compute_leaderboard(user_email):
        user_stats = Leaderboard.get_user_stats(user_email)

        leaderboard = []
        for stat in user_stats:
            rating = StatsSubmission.compute_rating(stat)
            leaderboard.append({
                "match_id": stat["match_id"],
                "date": stat["date"],
                "goals": stat["goals"],
                "assists": stat["assists"],
                "rating": rating,
            })

        # Sort matches by rating (highest first)
        leaderboard.sort(key=lambda x: x["rating"], reverse=True)
        return leaderboard

    @staticmethod
    def show_personal_leaderboard(user_email):
        leaderboard = Leaderboard.compute_leaderboard(user_email)
        print(f"\n--- Leaderboard for {user_email} ---")
        print("MatchID | Date       | Goals | Assists | Rating")
        print("-----------------------------------------------")
        for entry in leaderboard:
            print(f"{entry['match_id']:7} | {entry['date']:<10} | {entry['goals']:5} | {entry['assists']:7} | {entry['rating']:6}")
