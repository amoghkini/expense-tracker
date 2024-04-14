import re
from werkzeug.security import generate_password_hash, check_password_hash

from flask import session

class Utils:
    
    @staticmethod
    def generate_username(
        first_name: str,
        last_name: str
    ) -> str:
        return f"{first_name.lower()}_{last_name.lower()}"
    
    @staticmethod
    def generate_hashed_password(
        password: str
    ) -> str:         
        return generate_password_hash(password)
    
    @staticmethod
    def check_password_hash(
        hashed_password: str, 
        plain_text_password: str
    ) -> bool:
        """
        :param hashed_password: a hashed string like returned by
                            :func:`generate_password_hash`.
        :param plain_text_password: the plaintext password to compare against the hash.
        """
        return check_password_hash(hashed_password, plain_text_password)
    
    @staticmethod
    def login_user(email: str) -> None:
        session['logged_in'] = True
        session['email'] = email
    
    @staticmethod
    def validate(data: str, regex: str) -> bool:
        """Custom Validator"""
        return True if re.match(regex, data) else False
    
    def __str__(self) -> str:
        return "This is utility function for auth blueprint"