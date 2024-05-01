from datetime import datetime, date
from pydantic import BaseModel, validator
from typing import Union

from auth.constants import RegularExpressions
from auth.models import User
from auth.utils import Utils
from utils.time_utils import TimeUtils


class UserSignUpValidator(BaseModel):
    email: str
    first_name: str
    last_name: str
    username: Union[str, None] = None
    password: str
    confirm_password: str
    mobile_no: str
    date_of_birth: str
    account_creation_date: int = TimeUtils.get_epoch()
    
    def __post_init__(self):
        pass

    
    @validator('email')    
    def email_validator(cls, email):
        result = Utils.validate(email, RegularExpressions.EMAIL_REGEX)
        if not result:
            raise ValueError("Please enter a valid email address")
        
        user: User = User.get_by_email(email)
        if user:
            raise ValueError("The user with this email address is already exist")
        return email
    
    @validator('mobile_no')    
    def mobile_no_validator(cls, mobile_no):
        if len(mobile_no) != 10:
            raise ValueError("Please enter valid phone number")
        
        user: User = User.get_by_mobile_no(mobile_no)
        if user:
            raise ValueError("The user with this mobile number is already exist")
        return mobile_no
    
    @validator('confirm_password')
    def password_match(cls, confirm_password , values, **kwargs):
        if 'password'in values and confirm_password != values['password']:
            raise ValueError("The password and confirm password should be same")
        return confirm_password
    
    @validator('password')
    def password_requirements(cls, password):
        result = Utils.validate(password, RegularExpressions.PASSWORD_REGEX)
        if not result:
            raise ValueError("To create a password, you have to meet all of the requirement")
        return password
    
    @validator("date_of_birth")
    def date_of_birth_validator(cls, date_of_birth):
        # Convert string DOB to datetime object
        dob_date = datetime.strptime(date_of_birth, "%m/%d/%Y").date()
        
        # Get today's date
        todays_date: date = TimeUtils.get_today_date()
        
        # Check if date_of_birth is todays date
        if dob_date == todays_date:
            raise ValueError("Please enter a valid date of birth")
        return date_of_birth
    
    def to_dict(self):
        return self.dict()
    
    def __str__(self) -> str:
        return f"{self.email}"
    

class ChangePasswordRequestValidator(BaseModel):
    new_password: str
    confirm_password: str
    old_password: str
    
    @validator('new_password')
    def password_requirements(cls, new_password):
        result = Utils.validate(new_password, RegularExpressions.PASSWORD_REGEX)
        if not result:
            raise ValueError("To create a password, you have to meet all of the requirement")
        return new_password
    
    @validator('confirm_password')
    def password_match(cls, confirm_password , values, **kwargs):
        if 'new_password'in values and confirm_password != values.get('new_password'):
            raise ValueError("The new password and confirm password should be same")
        return confirm_password
    
    @validator('old_password')
    def old_password_match(cls, old_password , values, **kwargs):
        if 'new_password'in values and old_password == values.get('new_password'):
            raise ValueError("The old and new password should be different")
        return old_password