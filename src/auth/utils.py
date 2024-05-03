import re
from flask import session
from itsdangerous import URLSafeTimedSerializer
from typing import Optional, Union
from werkzeug.security import generate_password_hash, check_password_hash

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
    def logout_user() -> None:
        session.pop('logged_in',None)
        session.pop('email',None)
        
    @staticmethod
    def validate(data: str, regex: str) -> bool:
        """Custom Validator"""
        return True if re.match(regex, data) else False
    
    def __str__(self) -> str:
        return "This is utility function for auth blueprint"


class TokenSerializer:
    """
    Utility class for serializing and deserializing tokens using itsdangerous library.

    Args:
        secret_key (str): The secret key used for token serialization and deserialization.

    Attributes:
        serializer (URLSafeTimedSerializer): An instance of URLSafeTimedSerializer for token operations.
    """

    def __init__(self, secret_key: str) -> None:
        """
        Initializes the TokenSerializer instance.

        Args:
            secret_key (str): The secret key used for token serialization and deserialization.
        """
        self.serializer: URLSafeTimedSerializer = URLSafeTimedSerializer(secret_key)

    def generate_token(self, data: str) -> Union[str, bytes]:
        """
        Generates a token for the given data.

        Args:
            data (str): The data to be serialized into the token.

        Returns:
            str: The generated token.
        """
        return self.serializer.dumps(data)

    def verify_token(self, token: str, max_age: int) -> Optional[str]:
        """
        Verifies and deserializes a token, returning the original data if valid.

        Args:
            token (str): The token to be verified and deserialized.
            max_age (int): The maximum allowed age (in seconds) for the token.

        Returns:
            str: The deserialized data if the token is valid, None otherwise.
        """
        try:
            data: str = self.serializer.loads(token, max_age=max_age)
            return data
        except Exception as e:
            return None