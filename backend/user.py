import bcrypt
import json
import os

from typing_extensions import reveal_type


class User:
    def __init__(self, first_name, last_name, email, age, gender):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.age = age
        self.gender = gender

    @staticmethod
    def hash_password(password):
        """Hash password using bcrypt with 12 rounds"""
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')  # Store as string in JSON

    @staticmethod
    def load_users():
        try:
            if not os.path.exists("users.json") or os.stat("users.json").st_size == 0:
                return []
            with open("users.json", "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    @staticmethod
    def save_users(users):
        with open("users.json", "w") as f:
            json.dump(users, f, indent=4)

    def signup(self):
        email = input("Enter email address: ")
        password = input("Enter password: ")
        conf_password = input("Confirm password: ")

        if conf_password != password:
            print("Password is not same as above!\n")
            return

        users = User.load_users()
        # Check for existing email
        if any(user['email'] == email for user in users):
            print("Email already exists!\n")
            return

        hash1 = User.hash_password(password)
        users.append({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": email,
            "age": self.age,
            "gender": self.gender,
            "password_hash": hash1,
        })
        User.save_users(users)
        print("You have registered successfully!")

    def login(self):
        email = input("Enter email address: ")
        password = input("Enter password: ")

        users = User.load_users()

        for user in users:
            if user["email"] == email:
                # Use bcrypt to verify password
                stored_hash = user["password_hash"].encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
                    print("Logged in Successfully!")
                    return user

        print("Login failed!\n")
        return None
