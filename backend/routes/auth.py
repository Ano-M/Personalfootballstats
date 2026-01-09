"""
Authentication routes for user signup, login, and profile
Handles JWT token generation and user management
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt
from user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    Register a new user

    Expected JSON body:
    {
        "first_name": "string",
        "last_name": "string",
        "email": "string",
        "age": int,
        "gender": "string",
        "password": "string",
        "confirm_password": "string"
    }

    Returns:
        201: User created successfully
        400: Validation error or duplicate email
        500: Server error
    """
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email', 'age', 'gender', 'password', 'confirm_password']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return jsonify({
                'error': 'Missing required fields',
                'missing_fields': missing_fields
            }), 400

        # Extract data
        first_name = data['first_name'].strip()
        last_name = data['last_name'].strip()
        email = data['email'].strip().lower()
        age = data['age']
        gender = data['gender'].strip()
        password = data['password']
        confirm_password = data['confirm_password']

        # Validate fields
        if not first_name or not last_name:
            return jsonify({'error': 'First name and last name cannot be empty'}), 400

        if not email or '@' not in email:
            return jsonify({'error': 'Invalid email address'}), 400

        try:
            age = int(age)
            if age < 1 or age > 120:
                return jsonify({'error': 'Age must be between 1 and 120'}), 400
        except (ValueError, TypeError):
            return jsonify({'error': 'Age must be a valid number'}), 400

        if gender not in ['M', 'F', 'Other']:
            return jsonify({'error': 'Gender must be M, F, or Other'}), 400

        # Check password match
        if password != confirm_password:
            return jsonify({'error': 'Passwords do not match'}), 400

        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters long'}), 400

        # Check for existing email
        users = User.load_users()
        if any(user['email'] == email for user in users):
            return jsonify({'error': 'Email already exists'}), 400

        # Hash password using bcrypt
        password_hash = User.hash_password(password)

        # Create new user
        new_user = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'age': age,
            'gender': gender,
            'password_hash': password_hash
        }

        users.append(new_user)
        User.save_users(users)

        # Return user data (without password hash)
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'age': age,
                'gender': gender
            }
        }), 201

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate user and return JWT token

    Expected JSON body:
    {
        "email": "string",
        "password": "string"
    }

    Returns:
        200: Login successful with access token
        400: Missing fields
        401: Invalid credentials
        500: Server error
    """
    try:
        data = request.get_json()

        # Validate required fields
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Email and password are required'}), 400

        email = data['email'].strip().lower()
        password = data['password']

        # Load users
        users = User.load_users()

        # Find user by email
        user = next((u for u in users if u['email'] == email), None)

        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401

        # Verify password using bcrypt
        stored_hash = user['password_hash'].encode('utf-8')
        if not bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            return jsonify({'error': 'Invalid email or password'}), 401

        # Create JWT token with user email as identity
        access_token = create_access_token(identity=email)

        # Return token and user data
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'email': user['email'],
                'age': user['age'],
                'gender': user['gender']
            }
        }), 200

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current user profile (protected route)

    Headers:
        Authorization: Bearer <access_token>

    Returns:
        200: User profile data
        401: Unauthorized (invalid or missing token)
        404: User not found
        500: Server error
    """
    try:
        # Get user email from JWT token
        current_user_email = get_jwt_identity()

        # Load users
        users = User.load_users()

        # Find user
        user = next((u for u in users if u['email'] == current_user_email), None)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Return user data (without password hash)
        return jsonify({
            'user': {
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'email': user['email'],
                'age': user['age'],
                'gender': user['gender']
            }
        }), 200

    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500
