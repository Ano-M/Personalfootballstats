"""
Flask REST API Backend for Football Stats Leaderboard System
Main application entry point with JWT authentication and CORS support
"""
import os
import sys
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import get_config

# Add backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import blueprints
from routes.auth import auth_bp
from routes.stats import stats_bp


def create_app(config_name=None):
    """
    Application factory pattern for creating Flask app

    Args:
        config_name: Configuration environment (development, production, testing)

    Returns:
        Configured Flask application
    """
    app = Flask(__name__)

    # Load configuration
    if config_name:
        from config import config
        app.config.from_object(config[config_name])
    else:
        app.config.from_object(get_config())

    # Initialize extensions
    JWTManager(app)
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=app.config['CORS_SUPPORTS_CREDENTIALS'])

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(stats_bp)

    # Root endpoint
    @app.route('/')
    def index():
        """API information endpoint"""
        return jsonify({
            'name': 'Football Stats Leaderboard API',
            'version': '1.0.0',
            'endpoints': {
                'auth': {
                    'signup': 'POST /api/auth/signup',
                    'login': 'POST /api/auth/login',
                    'me': 'GET /api/auth/me (protected)'
                },
                'stats': {
                    'submit': 'POST /api/stats/submit (protected)',
                    'leaderboard': 'GET /api/stats/leaderboard (protected)',
                    'match_detail': 'GET /api/stats/match/<match_id> (protected)',
                    'all_matches': 'GET /api/stats/all (protected)'
                }
            },
            'status': 'running'
        }), 200

    # Health check endpoint
    @app.route('/health')
    def health():
        """Health check endpoint"""
        return jsonify({'status': 'healthy'}), 200

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({'error': 'Endpoint not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        return jsonify({'error': 'Internal server error'}), 500

    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 errors"""
        return jsonify({'error': 'Bad request'}), 400

    # JWT error handlers
    @app.errorhandler(401)
    def unauthorized(error):
        """Handle 401 errors"""
        return jsonify({'error': 'Unauthorized - Invalid or missing token'}), 401

    @app.errorhandler(422)
    def unprocessable_entity(error):
        """Handle 422 errors (JWT validation)"""
        return jsonify({'error': 'Unprocessable entity - Invalid token format'}), 422

    return app


if __name__ == '__main__':
    # Create and run the app
    app = create_app()

    # Get host and port from environment or use defaults
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'

    print("\n" + "="*60)
    print("🚀 Football Stats Leaderboard API")
    print("="*60)
    print(f"🌐 Running on: http://{host}:{port}")
    print(f"📝 Environment: {os.getenv('FLASK_ENV', 'development')}")
    print(f"🔧 Debug mode: {debug}")
    print("="*60)
    print("\n📚 Available endpoints:")
    print("  Auth:")
    print("    POST   /api/auth/signup")
    print("    POST   /api/auth/login")
    print("    GET    /api/auth/me (protected)")
    print("\n  Stats:")
    print("    POST   /api/stats/submit (protected)")
    print("    GET    /api/stats/leaderboard (protected)")
    print("    GET    /api/stats/match/<match_id> (protected)")
    print("    GET    /api/stats/all (protected)")
    print("\n  Other:")
    print("    GET    / (API info)")
    print("    GET    /health (Health check)")
    print("="*60 + "\n")

    app.run(host=host, port=port, debug=debug)
