#!/usr/bin/env python3
"""Session Authentication module"""
from api.v1.auth.auth import Auth
from models.user import User
from flask import request
import uuid


class SessionAuth(Auth):
    """Session Authentication class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session"""
        if user_id is None or not type(user_id) == str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session Id"""
        if session_id and type(session_id) == str:
            return self.user_id_by_session_id.get(session_id)
        return None

    def current_user(self, request=None):
        """overload that returns a User instance based on a cookie value"""
        session_cookie_ = self.session_cookie(request)
        session_id_ = self.user_id_for_session_id(session_cookie_)
        return User.get(session_id_)

    def destroy_session(self, request=None):
        """method destroys a user's session"""
        if request is None:
            return False
        
        session_cookie_ = self.session_cookie(request)
        if not session_cookie_:
            return False
        
        user_id = self.user_id_for_session_id(session_cookie_)
        if not user_id:
            return False

        self.user_id_by_session_id.pop(session_cookie_)
        return True