import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from validation import StatsValidator, ValidationError, get_validated_input


class StatsController:
    """
    Manages football match statistics with comprehensive field support.
    Source of truth for stats model.
    """

    def __init__(self, user_email):
        """
        Initialize stats controller.

        Args:
            user_email: Email of logged-in user
        """
        self.user_email = user_email

    @staticmethod
    def load_stats():
        """Load statistics from JSON file"""
        try:
            if not os.path.exists("stats.json") or os.stat("stats.json").st_size == 0:
                return []
            with open("stats.json", "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def save_stats(stats):
        """Save statistics to JSON file"""
        with open("stats.json", "w") as f:
            json.dump(stats, f, indent=4)

    def get_stats(self):
        """
        Collect all statistics from user with validation.
        Prompts for all 18 fields with grouped logical sections.

        Returns:
            Tuple of (match_id, stats_dict)
        """
        print("\n" + "="*60)
        print("MATCH STATISTICS ENTRY")
        print("="*60)
        print("Please enter statistics for your match.")
        print("All numeric fields will be validated.\n")

        try:
            # === SECTION 1: Match Information ===
            print("--- MATCH INFORMATION ---")
            date = get_validated_input(
                "Enter match date (YYYY-MM-DD): ",
                StatsValidator.validate_date
            )

            home_team = get_validated_input(
                "Enter home team name: ",
                StatsValidator.validate_team_name,
                "Home team"
            )

            away_team = get_validated_input(
                "Enter away team name: ",
                StatsValidator.validate_team_name,
                "Away team"
            )

            match_score = get_validated_input(
                "Enter match score (format: X-Y, e.g., '2-1'): ",
                StatsValidator.validate_match_score
            )

            minutes_played = get_validated_input(
                "Enter minutes played (1-120): ",
                StatsValidator.validate_stat_field,
                'minutes_played'
            )

            # === SECTION 2: Attacking Statistics ===
            print("\n--- ATTACKING STATISTICS ---")
            goals = get_validated_input(
                "Enter goals scored (0-15): ",
                StatsValidator.validate_stat_field,
                'goals'
            )

            shots = get_validated_input(
                "Enter shots taken (0-30): ",
                StatsValidator.validate_stat_field,
                'shots'
            )

            disallowed_goals = get_validated_input(
                "Enter disallowed goals (0-5): ",
                StatsValidator.validate_stat_field,
                'disallowed_goals'
            )

            assists = get_validated_input(
                "Enter assists given (0-15): ",
                StatsValidator.validate_stat_field,
                'assists'
            )

            # Calculate goal_involvements automatically as goals + assists
            goal_involvements = goals + assists
            print(f"Goal Involvements: {goal_involvements} (calculated: goals + assists)")

            # === SECTION 3: Passing Statistics ===
            print("\n--- PASSING STATISTICS ---")
            passes = get_validated_input(
                "Enter total passes (0-200): ",
                StatsValidator.validate_stat_field,
                'passes'
            )

            successful_passes = get_validated_input(
                "Enter successful passes (0-200): ",
                StatsValidator.validate_stat_field,
                'successful_passes'
            )

            # === SECTION 4: Dribbling Statistics ===
            print("\n--- DRIBBLING STATISTICS ---")
            dribbles = get_validated_input(
                "Enter total dribbles (0-50): ",
                StatsValidator.validate_stat_field,
                'dribbles'
            )

            successful_dribbles = get_validated_input(
                "Enter successful dribbles (0-50): ",
                StatsValidator.validate_stat_field,
                'successful_dribbles'
            )

            # === SECTION 5: Defensive Statistics ===
            print("\n--- DEFENSIVE STATISTICS ---")
            tackles = get_validated_input(
                "Enter tackles made (0-30): ",
                StatsValidator.validate_stat_field,
                'tackles'
            )

            missed_tackles = get_validated_input(
                "Enter missed tackles (0-30): ",
                StatsValidator.validate_stat_field,
                'missed_tackles'
            )

            interceptions = get_validated_input(
                "Enter interceptions (0-30): ",
                StatsValidator.validate_stat_field,
                'interceptions'
            )

            # === SECTION 6: General Play Statistics ===
            print("\n--- GENERAL PLAY ---")
            touches = get_validated_input(
                "Enter total touches (0-300): ",
                StatsValidator.validate_stat_field,
                'touches'
            )

            unsuccessful_touches = get_validated_input(
                "Enter unsuccessful touches (0-300): ",
                StatsValidator.validate_stat_field,
                'unsuccessful_touches'
            )

            # === Cross-field validation ===
            stats_dict = {
                'goals': goals,
                'shots': shots,
                'disallowed_goals': disallowed_goals,
                'goal_involvements': goal_involvements,
                'assists': assists,
                'passes': passes,
                'successful_passes': successful_passes,
                'dribbles': dribbles,
                'successful_dribbles': successful_dribbles,
                'tackles': tackles,
                'missed_tackles': missed_tackles,
                'interceptions': interceptions,
                'touches': touches,
                'unsuccessful_touches': unsuccessful_touches,
                'minutes_played': minutes_played,
            }

            StatsValidator.validate_cross_field_constraints(stats_dict)

            # === Generate match_id and save ===
            stats = StatsController.load_stats()

            existing_ids = [s.get("match_id") for s in stats]
            existing_ids = [mid for mid in existing_ids if mid is not None]
            match_id = max(existing_ids, default=0) + 1

            # Create complete stats entry
            complete_stats = {
                "match_id": match_id,
                "user_email": self.user_email,
                "date": date,
                "home_team": home_team,
                "away_team": away_team,
                "match_score": match_score,
                "minutes_played": minutes_played,
                "goals": goals,
                "shots": shots,
                "disallowed_goals": disallowed_goals,
                "goal_involvements": goal_involvements,
                "assists": assists,
                "passes": passes,
                "successful_passes": successful_passes,
                "dribbles": dribbles,
                "successful_dribbles": successful_dribbles,
                "tackles": tackles,
                "missed_tackles": missed_tackles,
                "interceptions": interceptions,
                "touches": touches,
                "unsuccessful_touches": unsuccessful_touches,
            }

            stats.append(complete_stats)
            StatsController.save_stats(stats)

            print("\n" + "="*60)
            print("Statistics saved successfully!")
            print(f"Match ID: {match_id}")
            print("="*60 + "\n")

            return match_id, complete_stats

        except ValidationError as e:
            print(f"\n[ERROR] Failed to save statistics: {e}")
            print("Please try submitting your stats again.\n")
            return None, None
        except KeyboardInterrupt:
            print("\n\nStats entry cancelled by user.\n")
            return None, None

    @staticmethod
    def compute_rating(stat):
        """
        Compute comprehensive performance rating.

        Enhanced algorithm that considers:
        - Attacking: goals, assists, shots
        - Passing: pass completion rate
        - Dribbling: dribble success rate
        - Defending: tackles, interceptions
        - Ball control: touch success rate
        - Minutes played: normalized performance

        Args:
            stat: Statistics dictionary

        Returns:
            Performance rating (0-10 scale, 1 decimal place)
        """
        # Extract values with defaults
        goals = int(stat.get("goals", 0))
        assists = int(stat.get("assists", 0))
        shots = int(stat.get("shots", 0))

        passes = int(stat.get("passes", 0))
        successful_passes = int(stat.get("successful_passes", 0))

        dribbles = int(stat.get("dribbles", 0))
        successful_dribbles = int(stat.get("successful_dribbles", 0))

        tackles = int(stat.get("tackles", 0))
        interceptions = int(stat.get("interceptions", 0))

        touches = int(stat.get("touches", 0))
        unsuccessful_touches = int(stat.get("unsuccessful_touches", 0))

        minutes_played = int(stat.get("minutes_played", 90))

        # === Attacking Score (40 points max) ===
        attacking_score = (
            goals * 10 +                    # Goals: 10 points each
            assists * 5 +                   # Assists: 5 points each
            (shots - goals) * 0.5           # Non-goal shots: 0.5 points each
        )

        # === Passing Score (20 points max) ===
        if passes > 0:
            pass_completion_rate = successful_passes / passes
            passing_score = pass_completion_rate * 20
        else:
            passing_score = 0

        # === Dribbling Score (15 points max) ===
        if dribbles > 0:
            dribble_success_rate = successful_dribbles / dribbles
            dribbling_score = (
                dribble_success_rate * 10 +      # Success rate: 10 points
                successful_dribbles * 0.5        # Absolute success: 0.5 per dribble
            )
        else:
            dribbling_score = 0

        # === Defensive Score (15 points max) ===
        defensive_score = (
            tackles * 2 +                   # Tackles: 2 points each
            interceptions * 2               # Interceptions: 2 points each
        )

        # === Ball Control Score (10 points max) ===
        if touches > 0:
            touch_success_rate = (touches - unsuccessful_touches) / touches
            ball_control_score = touch_success_rate * 10
        else:
            ball_control_score = 0

        # === Total Raw Score ===
        raw_score = (
            attacking_score +
            passing_score +
            dribbling_score +
            defensive_score +
            ball_control_score
        )

        # === Minutes Normalization ===
        # Normalize to 90 minutes (full match)
        if minutes_played > 0:
            normalized_score = (raw_score / minutes_played) * 90
        else:
            normalized_score = raw_score

        # Cap at 100, then convert to 0-10 scale
        capped_score = min(normalized_score, 100)
        final_rating = capped_score / 10.0

        return round(final_rating, 1)
