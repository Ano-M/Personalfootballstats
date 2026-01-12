"""
Statistics routes for match data submission and leaderboard
Handles stats submission, retrieval, and leaderboard generation
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from controller.stats_controller import StatsController
from validation import StatsValidator, ValidationError
from leaderboard import Leaderboard

stats_bp = Blueprint('stats', __name__, url_prefix='/api/stats')


@stats_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_stats():
    """
    Submit match statistics (protected route)

    Headers:
        Authorization: Bearer <access_token>

    Expected JSON body (17 fields):
    {
        "date": "YYYY-MM-DD",
        "home_team": "string",
        "away_team": "string",
        "match_score": "X-Y",
        "minutes_played": 1-120,
        "goals": 0-15,
        "shots": 0-30,
        "disallowed_goals": 0-5,
        "assists": 0-15,
        "passes": 0-200,
        "successful_passes": 0-200,
        "dribbles": 0-50,
        "successful_dribbles": 0-50,
        "tackles": 0-30,
        "missed_tackles": 0-30,
        "interceptions": 0-30,
        "touches": 0-300,
        "unsuccessful_touches": 0-300
    }
    
    Note: goal_involvements is calculated automatically as goals + assists

    Returns:
        201: Stats submitted successfully
        400: Validation error
        401: Unauthorized
        500: Server error
    """
    try:
        # Get user email from JWT token
        user_email = get_jwt_identity()

        data = request.get_json()

        # Define required fields (17 stats fields - goal_involvements calculated automatically)
        required_fields = [
            'date', 'home_team', 'away_team', 'match_score',
            'minutes_played', 'goals', 'shots', 'disallowed_goals',
            'assists', 'passes', 'successful_passes',
            'dribbles', 'successful_dribbles', 'tackles', 'missed_tackles',
            'interceptions', 'touches', 'unsuccessful_touches'
        ]

        # Check for missing fields
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': missing_fields
            }), 400

        # Validate each field using the validation module
        try:
            # Validate date
            date = StatsValidator.validate_date(data['date'])

            # Validate team names
            home_team = StatsValidator.validate_team_name(data['home_team'], 'Home team')
            away_team = StatsValidator.validate_team_name(data['away_team'], 'Away team')

            # Validate match score
            match_score = StatsValidator.validate_match_score(data['match_score'])

            # Validate numeric fields
            minutes_played = StatsValidator.validate_stat_field(str(data['minutes_played']), 'minutes_played')
            goals = StatsValidator.validate_stat_field(str(data['goals']), 'goals')
            shots = StatsValidator.validate_stat_field(str(data['shots']), 'shots')
            disallowed_goals = StatsValidator.validate_stat_field(str(data['disallowed_goals']), 'disallowed_goals')
            assists = StatsValidator.validate_stat_field(str(data['assists']), 'assists')
            passes = StatsValidator.validate_stat_field(str(data['passes']), 'passes')
            successful_passes = StatsValidator.validate_stat_field(str(data['successful_passes']), 'successful_passes')
            dribbles = StatsValidator.validate_stat_field(str(data['dribbles']), 'dribbles')
            successful_dribbles = StatsValidator.validate_stat_field(str(data['successful_dribbles']), 'successful_dribbles')
            tackles = StatsValidator.validate_stat_field(str(data['tackles']), 'tackles')
            missed_tackles = StatsValidator.validate_stat_field(str(data['missed_tackles']), 'missed_tackles')
            interceptions = StatsValidator.validate_stat_field(str(data['interceptions']), 'interceptions')
            touches = StatsValidator.validate_stat_field(str(data['touches']), 'touches')
            unsuccessful_touches = StatsValidator.validate_stat_field(str(data['unsuccessful_touches']), 'unsuccessful_touches')

            # Calculate goal_involvements automatically as goals + assists
            goal_involvements = goals + assists

            # Create stats dictionary for cross-field validation
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

            # Validate cross-field constraints
            StatsValidator.validate_cross_field_constraints(stats_dict)

        except ValidationError as e:
            return jsonify({'error': str(e)}), 400

        # Load existing stats and generate match_id
        stats = StatsController.load_stats()
        existing_ids = [s.get("match_id") for s in stats if s.get("match_id") is not None]
        match_id = max(existing_ids, default=0) + 1

        # Create complete stats entry
        complete_stats = {
            "match_id": match_id,
            "user_email": user_email,
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

        # Compute rating
        rating = StatsController.compute_rating(complete_stats)

        # Save stats
        stats.append(complete_stats)
        StatsController.save_stats(stats)

        return jsonify({
            'message': 'Statistics submitted successfully',
            'match_id': match_id,
            'rating': rating,
            'stats': complete_stats
        }), 201

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@stats_bp.route('/leaderboard', methods=['GET'])
@jwt_required()
def get_leaderboard():
    """
    Get user's personal leaderboard (protected route)

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        200: Leaderboard data
        401: Unauthorized
        500: Server error
    """
    try:
        # Get user email from JWT token
        user_email = get_jwt_identity()

        # Get leaderboard using existing Leaderboard class
        leaderboard_data = Leaderboard.compute_leaderboard(user_email)

        if not leaderboard_data:
            return jsonify({
                'message': 'No matches found',
                'leaderboard': [],
                'summary': {
                    'total_matches': 0,
                    'average_rating': 0,
                    'total_goals': 0,
                    'total_assists': 0,
                    'best_performance': None
                }
            }), 200

        # Calculate summary statistics
        total_matches = len(leaderboard_data)
        avg_rating = sum(e['rating'] for e in leaderboard_data) / total_matches
        total_goals = sum(e['goals'] for e in leaderboard_data)
        total_assists = sum(e['assists'] for e in leaderboard_data)
        best_performance = {
            'match_id': leaderboard_data[0]['match_id'],
            'rating': leaderboard_data[0]['rating'],
            'date': leaderboard_data[0]['date']
        }

        return jsonify({
            'leaderboard': leaderboard_data,
            'summary': {
                'total_matches': total_matches,
                'average_rating': round(avg_rating, 2),
                'total_goals': total_goals,
                'total_assists': total_assists,
                'best_performance': best_performance
            }
        }), 200

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@stats_bp.route('/match/<int:match_id>', methods=['GET'])
@jwt_required()
def get_match_details(match_id):
    """
    Get detailed statistics for a specific match (protected route)

    Headers:
        Authorization: Bearer <access_token>

    Args:
        match_id: ID of the match to retrieve

    Returns:
        200: Match details
        401: Unauthorized
        404: Match not found
        500: Server error
    """
    try:
        # Get user email from JWT token
        user_email = get_jwt_identity()

        # Load stats
        stats = StatsController.load_stats()

        # Find the specific match for this user
        match = next(
            (s for s in stats if s.get('match_id') == match_id and s.get('user_email') == user_email),
            None
        )

        if not match:
            return jsonify({'error': f'Match ID {match_id} not found'}), 404

        # Compute rating
        rating = StatsController.compute_rating(match)

        # Calculate percentages
        pass_accuracy = 0
        if match.get('passes', 0) > 0:
            pass_accuracy = round((match['successful_passes'] / match['passes']) * 100, 1)

        dribble_success = 0
        if match.get('dribbles', 0) > 0:
            dribble_success = round((match['successful_dribbles'] / match['dribbles']) * 100, 1)

        touch_success = 0
        if match.get('touches', 0) > 0:
            touch_success = round(((match['touches'] - match['unsuccessful_touches']) / match['touches']) * 100, 1)

        # Return detailed match data
        return jsonify({
            'match': {
                'match_id': match['match_id'],
                'date': match['date'],
                'home_team': match['home_team'],
                'away_team': match['away_team'],
                'match_score': match['match_score'],
                'minutes_played': match['minutes_played'],
                'rating': rating
            },
            'attacking': {
                'goals': match['goals'],
                'shots': match['shots'],
                'disallowed_goals': match['disallowed_goals'],
                'assists': match['assists'],
                'goal_involvements': match.get('goal_involvements', match['goals'] + match['assists'])
            },
            'passing': {
                'passes': match['passes'],
                'successful_passes': match['successful_passes'],
                'accuracy': pass_accuracy
            },
            'dribbling': {
                'dribbles': match['dribbles'],
                'successful_dribbles': match['successful_dribbles'],
                'success_rate': dribble_success
            },
            'defensive': {
                'tackles': match['tackles'],
                'missed_tackles': match['missed_tackles'],
                'interceptions': match['interceptions']
            },
            'ball_control': {
                'touches': match['touches'],
                'unsuccessful_touches': match['unsuccessful_touches'],
                'success_rate': touch_success
            }
        }), 200

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@stats_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_matches():
    """
    Get all matches for the current user (protected route)

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        200: List of all matches
        401: Unauthorized
        500: Server error
    """
    try:
        # Get user email from JWT token
        user_email = get_jwt_identity()

        # Get all user stats
        user_stats = Leaderboard.get_user_stats(user_email)

        if not user_stats:
            return jsonify({
                'message': 'No matches found',
                'matches': []
            }), 200

        # Add ratings to each match
        matches = []
        for stat in user_stats:
            rating = StatsController.compute_rating(stat)
            matches.append({
                'match_id': stat['match_id'],
                'date': stat['date'],
                'home_team': stat['home_team'],
                'away_team': stat['away_team'],
                'match_score': stat['match_score'],
                'minutes_played': stat['minutes_played'],
                'goals': stat['goals'],
                'assists': stat['assists'],
                'rating': rating
            })

        # Sort by date (most recent first)
        matches.sort(key=lambda x: x['date'], reverse=True)

        return jsonify({
            'matches': matches,
            'total_count': len(matches)
        }), 200

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500
