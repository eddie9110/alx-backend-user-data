#!/usr/bin/env python3
"""Hashing a password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """password hashing function"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """function verifies password"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
