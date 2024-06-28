import bcrypt
import pyotp
import re
import jwt
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer
from typing import Optional, Union
from werkzeug.security import generate_password_hash, check_password_hash

from utils.time_utils import TimeUtils
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
    def logout_user() -> None:
        session.pop('logged_in',None)
        session.pop('email',None)
        
    @staticmethod
    def validate(data: str, regex: str) -> bool:
        """Custom Validator"""
        return True if re.match(regex, data) else False
    
    @staticmethod
    def increment_incorrect_password_attempts(user):
        user.incorrect_password_attempts += 1
        return user
    
    @staticmethod
    def increment_incorrect_otp_attempts(user):
        user.incorrect_otp_attempts += 1
        return user
    
    @staticmethod 
    def reset_incorrect_password_attempts(user):
        user.incorrect_password_attempts = 0
        return user
    
    @staticmethod 
    def reset_incorrect_otp_attempts(user):
        user.incorrect_otp_attempts = 0
        return user
    
    @staticmethod
    def invalidate_session(session, deactivation_reason) -> None:
        session.is_active = False
        session.deactivation_time = TimeUtils.get_epoch()
        session.deactivation_reason = deactivation_reason
        session.commit()
        
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
      
        
class OTPUtils:
    """
    Utility class for generating and verifying OTPs (One-Time Passwords).
    """
    
    @staticmethod
    def generate_otp_secret() -> str:
        """
        Get a TOTP (Time-based One-Time Password) object for the specified user.

        Args:
            user (User): The user for whom the OTP object is retrieved.

        Returns:
            pyotp.TOTP: A TOTP object initialized with the user's OTP secret.

        Raises:
            ValueError: If the user does not have an OTP secret.
        """
        return pyotp.random_base32()
    
    @staticmethod
    def get_otp_object(user) -> bytes:
        secret: str = user.otp_secret  
        otp: str = pyotp.TOTP(secret).now()
        print(f"New OTP {otp}")
        hashed_otp: bytes = bcrypt.hashpw(otp.encode('utf-8'), bcrypt.gensalt())
        return hashed_otp
    
    @staticmethod
    def is_otp_valid(otp_entry, otp: str) -> bool:
        """
        Verify if the provided OTP is valid for the specified user.

        Args:
            user (User): The user for whom the OTP is verified.
            otp (str): The OTP entered by the user.

        Returns:
            bool: True if the OTP is valid, False otherwise.

        Raises:
            ValueError: If the user does not have an OTP secret.
        """
        
        is_valid = bcrypt.checkpw(otp.encode('utf-8'), otp_entry.hashed_otp)
        return is_valid
    
    
class JWTUtils:
    """
    Utility class for generating and decoding JWT tokens.
    """
    
    @staticmethod
    def generate_jwt(
        user_id: Union[str, int], 
        secret_key: str = "SomeRandomSecretKey"
    ) -> str:
        """
        Generates a JWT token for a given user ID.

        Args:
            user_id (Union[str, int]): The ID of the user for whom the token is generated.
            secret_key (str): The secret key used to sign the JWT token. Defaults to "SomeRandomSecretKey".

        Returns:
            str: The encoded JWT token.
        """
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(hours=6)
        }
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token

    @staticmethod
    def decode_jwt(
        token: str, 
        secret_key: str = "SomeRandomSecretKey"
    ) -> Optional[dict[str, Union[str, int]]]:
        """
        Decodes a given JWT token.

        Args:
            token (str): The JWT token to be decoded.
            secret_key (str): The secret key used to decode the JWT token. Defaults to "SomeRandomSecretKey".

        Returns:
            Optional[Dict[str, Union[str, int]]]: The decoded payload if the token is valid, otherwise None.
        """
        try:
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None