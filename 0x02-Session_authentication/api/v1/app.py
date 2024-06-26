#!/usr/bin/env python3
"""
Route module for the API
"""
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS)
import os
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None

if os.getenv("AUTH_TYPE") == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()

if os.getenv("AUTH_TYPE") == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()

if os.getenv("AUTH_TYPE") == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()


@app.before_request
def request_filter():
    """
    request filter
    """
    path_list = ['/api/v1/status/', '/api/v1/unauthorized/',
                 '/api/v1/forbidden/', '/api/v1/auth_session/login/']

    if auth is None:
        return
    if not auth.require_auth(request.path, path_list):
        return
    if (auth.authorization_header(request)is None and
            auth.session_cookie(request) is None):
        return abort(401)
    if auth.current_user(request) is None:
        return abort(403)
    request.current_user = auth.current_user(request)


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    forbidden access handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    unauthorised access handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = os.getenv("API_PORT", "5000")
    app.run(host=host, port=port)
