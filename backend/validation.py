"""
Input validation for football statistics.
Provides validation for numeric stats, dates, and text fields.
"""
import re
from datetime import datetime
from typing import Tuple, Optional


class ValidationError(Exception):
    """Custom exception for validation failures"""
    pass


class StatsValidator:
    """Validates football statistics input"""

    # Field constraints (min, max)
    NUMERIC_CONSTRAINTS = {
        'goals': (0, 15),
        'shots': (0, 30),
        'disallowed_goals': (0, 5),
        'goal_involvements': (0, 20),
        'assists': (0, 15),
        'passes': (0, 200),
        'successful_passes': (0, 200),
        'dribbles': (0, 50),
        'successful_dribbles': (0, 50),
        'tackles': (0, 30),
        'missed_tackles': (0, 30),
        'interceptions': (0, 30),
        'touches': (0, 300),
        'unsuccessful_touches': (0, 300),
        'minutes_played': (1, 120),
    }

    @staticmethod
    def validate_integer(value: str, field_name: str, min_val: int, max_val: int) -> int:
        """
        Validate integer input with bounds checking.

        Args:
            value: String input from user
            field_name: Name of field for error messages
            min_val: Minimum allowed value
            max_val: Maximum allowed value

        Returns:
            Validated integer

        Raises:
            ValidationError: If validation fails
        """
        try:
            num = int(value)
        except ValueError:
            raise ValidationError(f"{field_name} must be a number. You entered: '{value}'")

        if num < min_val or num > max_val:
            raise ValidationError(
                f"{field_name} must be between {min_val} and {max_val}. You entered: {num}"
            )

        return num

    @staticmethod
    def validate_stat_field(value: str, field_name: str) -> int:
        """
        Validate a statistics field using predefined constraints.

        Args:
            value: String input from user
            field_name: Name of the stat field

        Returns:
            Validated integer

        Raises:
            ValidationError: If field not found or validation fails
        """
        if field_name not in StatsValidator.NUMERIC_CONSTRAINTS:
            raise ValidationError(f"Unknown field: {field_name}")

        min_val, max_val = StatsValidator.NUMERIC_CONSTRAINTS[field_name]
        return StatsValidator.validate_integer(value, field_name, min_val, max_val)

    @staticmethod
    def validate_date(date_str: str) -> str:
        """
        Validate date format (YYYY-MM-DD).

        Args:
            date_str: Date string from user

        Returns:
            Validated date string

        Raises:
            ValidationError: If date format invalid
        """
        if not date_str or not date_str.strip():
            raise ValidationError("Date cannot be empty")

        # Check format with regex
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            raise ValidationError(
                f"Date must be in format YYYY-MM-DD. You entered: '{date_str}'"
            )

        # Validate actual date
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            raise ValidationError(
                f"Invalid date: '{date_str}'. Please check day/month values."
            )

        return date_str

    @staticmethod
    def validate_team_name(team_name: str, field_name: str) -> str:
        """
        Validate team name (non-empty, max 50 chars).

        Args:
            team_name: Team name from user
            field_name: Field name for error messages

        Returns:
            Validated team name

        Raises:
            ValidationError: If validation fails
        """
        if not team_name or not team_name.strip():
            raise ValidationError(f"{field_name} cannot be empty")

        team_name = team_name.strip()

        if len(team_name) > 50:
            raise ValidationError(
                f"{field_name} too long (max 50 characters). You entered {len(team_name)} characters."
            )

        return team_name

    @staticmethod
    def validate_match_score(score: str) -> str:
        """
        Validate match score format (e.g., "2-1", "0-0").

        Args:
            score: Score string from user

        Returns:
            Validated score string

        Raises:
            ValidationError: If format invalid
        """
        if not score or not score.strip():
            raise ValidationError("Match score cannot be empty")

        score = score.strip()

        # Format: digit(s)-digit(s)
        if not re.match(r'^\d{1,2}-\d{1,2}$', score):
            raise ValidationError(
                f"Match score must be in format 'X-Y' (e.g., '2-1'). You entered: '{score}'"
            )

        # Validate reasonable score values (0-99)
        home, away = score.split('-')
        home_score = int(home)
        away_score = int(away)

        if home_score < 0 or home_score > 99 or away_score < 0 or away_score > 99:
            raise ValidationError(
                f"Each score must be between 0 and 99. You entered: '{score}'"
            )

        return score

    @staticmethod
    def validate_cross_field_constraints(stats: dict) -> None:
        """
        Validate logical relationships between fields.

        Args:
            stats: Dictionary of all stats

        Raises:
            ValidationError: If cross-field validation fails
        """
        # Successful passes can't exceed total passes
        if stats['successful_passes'] > stats['passes']:
            raise ValidationError(
                f"Successful passes ({stats['successful_passes']}) cannot exceed "
                f"total passes ({stats['passes']})"
            )

        # Successful dribbles can't exceed total dribbles
        if stats['successful_dribbles'] > stats['dribbles']:
            raise ValidationError(
                f"Successful dribbles ({stats['successful_dribbles']}) cannot exceed "
                f"total dribbles ({stats['dribbles']})"
            )

        # Unsuccessful touches can't exceed total touches
        if stats['unsuccessful_touches'] > stats['touches']:
            raise ValidationError(
                f"Unsuccessful touches ({stats['unsuccessful_touches']}) cannot exceed "
                f"total touches ({stats['touches']})"
            )

        # Goals can't exceed shots
        if stats['goals'] > stats['shots']:
            raise ValidationError(
                f"Goals ({stats['goals']}) cannot exceed shots ({stats['shots']})"
            )

        # Note: goal_involvements is now calculated automatically as goals + assists
        # No validation needed since it's always correct


def get_validated_input(prompt: str, validator_func, *args, max_attempts: int = 3):
    """
    Get validated input from user with retry logic.

    Args:
        prompt: Input prompt for user
        validator_func: Validation function to call
        *args: Additional arguments for validator
        max_attempts: Maximum retry attempts

    Returns:
        Validated value

    Raises:
        ValidationError: If max attempts exceeded
    """
    for attempt in range(max_attempts):
        try:
            value = input(prompt)
            return validator_func(value, *args)
        except ValidationError as e:
            print(f"Validation Error: {e}")
            if attempt < max_attempts - 1:
                print(f"Please try again ({max_attempts - attempt - 1} attempts remaining).\n")
            else:
                raise ValidationError(f"Max validation attempts exceeded for: {prompt}")

    # Should never reach here
    raise ValidationError("Unexpected validation error")
