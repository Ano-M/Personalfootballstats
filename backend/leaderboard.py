from controller.stats_controller import StatsController


class Leaderboard:
    """Display and compute personal leaderboard for user statistics"""

    @staticmethod
    def get_user_stats(user_email):
        """
        Get all statistics for a specific user.

        Args:
            user_email: Email of the user

        Returns:
            List of stat dictionaries for the user
        """
        stats = StatsController.load_stats()
        return [s for s in stats if s["user_email"] == user_email]

    @staticmethod
    def compute_leaderboard(user_email):
        """
        Compute leaderboard with ratings for user's matches.

        Args:
            user_email: Email of the user

        Returns:
            List of match entries with ratings, sorted by rating
        """
        user_stats = Leaderboard.get_user_stats(user_email)

        leaderboard = []
        for stat in user_stats:
            rating = StatsController.compute_rating(stat)
            leaderboard.append({
                "match_id": stat["match_id"],
                "date": stat["date"],
                "match": f"{stat.get('home_team', 'N/A')} vs {stat.get('away_team', 'N/A')}",
                "score": stat.get("match_score", "N/A"),
                "goals": stat["goals"],
                "assists": stat["assists"],
                "minutes": stat.get("minutes_played", "N/A"),
                "rating": rating,
                # Include additional stats for detailed view
                "full_stats": stat
            })

        # Sort by rating (highest first)
        leaderboard.sort(key=lambda x: x["rating"], reverse=True)
        return leaderboard

    @staticmethod
    def show_personal_leaderboard(user_email):
        """
        Display formatted leaderboard for user.

        Args:
            user_email: Email of the user
        """
        leaderboard = Leaderboard.compute_leaderboard(user_email)

        if not leaderboard:
            print(f"\n--- Leaderboard for {user_email} ---")
            print("No matches recorded yet. Submit your first match stats!\n")
            return

        print(f"\n{'='*90}")
        print(f"PERSONAL LEADERBOARD: {user_email}")
        print(f"{'='*90}")
        print(f"{'ID':<5} | {'Date':<12} | {'Match':<25} | {'Score':<7} | {'G':<2} | {'A':<2} | {'Min':<4} | {'Rating':<6}")
        print(f"{'-'*90}")

        for entry in leaderboard:
            print(
                f"{entry['match_id']:<5} | "
                f"{entry['date']:<12} | "
                f"{entry['match'][:25]:<25} | "
                f"{entry['score']:<7} | "
                f"{entry['goals']:<2} | "
                f"{entry['assists']:<2} | "
                f"{entry['minutes']:<4} | "
                f"{entry['rating']:<6.2f}"
            )

        print(f"{'='*90}\n")

        # Show summary statistics
        avg_rating = sum(e['rating'] for e in leaderboard) / len(leaderboard)
        total_goals = sum(e['goals'] for e in leaderboard)
        total_assists = sum(e['assists'] for e in leaderboard)

        print("SUMMARY STATISTICS:")
        print(f"  Total Matches: {len(leaderboard)}")
        print(f"  Average Rating: {avg_rating:.2f}")
        print(f"  Total Goals: {total_goals}")
        print(f"  Total Assists: {total_assists}")
        print(f"  Best Performance: {leaderboard[0]['rating']:.2f} (Match ID: {leaderboard[0]['match_id']})")
        print()

    @staticmethod
    def show_detailed_match(user_email, match_id):
        """
        Display detailed statistics for a specific match.

        Args:
            user_email: Email of the user
            match_id: ID of the match to display
        """
        leaderboard = Leaderboard.compute_leaderboard(user_email)
        match = next((m for m in leaderboard if m['match_id'] == match_id), None)

        if not match:
            print(f"Match ID {match_id} not found for user {user_email}\n")
            return

        stats = match['full_stats']

        print(f"\n{'='*60}")
        print(f"DETAILED MATCH STATISTICS - Match ID: {match_id}")
        print(f"{'='*60}")
        print(f"Date: {stats['date']}")
        print(f"Match: {stats.get('home_team', 'N/A')} vs {stats.get('away_team', 'N/A')}")
        print(f"Score: {stats.get('match_score', 'N/A')}")
        print(f"Minutes Played: {stats.get('minutes_played', 'N/A')}")
        print(f"Performance Rating: {match['rating']:.2f}/100")
        print(f"{'-'*60}")

        print("\nATTACKING:")
        print(f"  Goals: {stats['goals']}")
        print(f"  Shots: {stats.get('shots', 'N/A')}")
        print(f"  Disallowed Goals: {stats.get('disallowed_goals', 'N/A')}")
        print(f"  Assists: {stats['assists']}")
        print(f"  Goal Involvements: {stats.get('goal_involvements', 'N/A')}")

        print("\nPASSING:")
        passes = stats.get('passes', 0)
        successful_passes = stats.get('successful_passes', 0)
        pass_rate = (successful_passes / passes * 100) if passes > 0 else 0
        print(f"  Passes: {successful_passes}/{passes} ({pass_rate:.1f}% accuracy)")

        print("\nDRIBBLING:")
        dribbles = stats.get('dribbles', 0)
        successful_dribbles = stats.get('successful_dribbles', 0)
        dribble_rate = (successful_dribbles / dribbles * 100) if dribbles > 0 else 0
        print(f"  Dribbles: {successful_dribbles}/{dribbles} ({dribble_rate:.1f}% success)")

        print("\nDEFENSIVE:")
        print(f"  Tackles: {stats.get('tackles', 'N/A')}")
        print(f"  Missed Tackles: {stats.get('missed_tackles', 'N/A')}")
        print(f"  Interceptions: {stats.get('interceptions', 'N/A')}")

        print("\nBALL CONTROL:")
        touches = stats.get('touches', 0)
        unsuccessful_touches = stats.get('unsuccessful_touches', 0)
        touch_rate = ((touches - unsuccessful_touches) / touches * 100) if touches > 0 else 0
        print(f"  Touches: {touches - unsuccessful_touches}/{touches} ({touch_rate:.1f}% successful)")

        print(f"{'='*60}\n")
