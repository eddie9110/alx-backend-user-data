#!/usr/bin/env python3
"""Flask app"""
from flask import Flask, jsonify, request, redirect, abort
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def message():
    """home route"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """create new user"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login() -> str:
    """logging in a user."""
    email = request.form.get("email")
    password = request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", AUTH.create_session(email))
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
