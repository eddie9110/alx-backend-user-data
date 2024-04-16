#!/usr/bin/env python3
"""
module for basic authentication
"""

from typing import TypeVar
import base64
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """
    Auth Class
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """extracts base64 authorization header"""
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        if authorization_header.startswith("Basic "):
            return "".join(authorization_header.split(" ")[1:])
        else:
            return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """decodes base64 authorization header"""
        base_header = base64_authorization_header
        if base_header and type(base_header) == str:
            try:
                base = base64.b64decode(base_header.encode('utf-8'))
                return base.decode('utf-8')
            except Exception:
                return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """extracts user credentials"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) != str:
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        users_email = decoded_base64_authorization_header.split(':')[0]
        users_password = "".join(c.split(':', 1)[1:])
        return(users_email, users_password)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """user object from credentials"""
        if type(user_email) != str or user_email is None:
            return None
        if type(user_pwd) != str or user_pwd is None:
            return None
        if user_pwd and user_pwd:
            users = User.search({"email": user_email})
            for user in users:
                if user.password == user_pwd:
                    return user

    def current_user(self, request=None) -> TypeVar('User'):
        """method overloads Auth and retrieves the
        User instance for a request"""
        if request:
            auth_h = self.authorization_header(request)
            extract_h = self.extract_base64_authorization_header(auth_h)
            decode_h = self.decode_base64_authorization_header(extract_h)
            email, password = self.extract_user_credentials(decode_h)
            return self.user_object_from_credentials(email, password)
