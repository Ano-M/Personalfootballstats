"""
Configuration settings for Flask REST API
Environment-based configuration for development and production
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration with common settings"""

    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

    # JWT settings
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)  # Token expires in 24 hours
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # Refresh token expires in 30 days

    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:3000').split(',')
    CORS_SUPPORTS_CREDENTIALS = True

    # File paths
    USERS_FILE = os.path.join(os.path.dirname(__file__), 'users.json')
    STATS_FILE = os.path.join(os.path.dirname(__file__), 'stats.json')

    # API settings
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing environment configuration"""
    DEBUG = True
    TESTING = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get configuration based on FLASK_ENV environment variable"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
