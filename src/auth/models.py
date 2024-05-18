from auth.constants import UserStatus
from database import (
    Boolean,
    BigInteger,
    Column, 
    DateTime,
    Integer,
    Model,
    String
)
from auth.utils import Utils
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


class User(Model):
    email = Column(String(50), unique=True, index=True)
    first_name = Column(String(50))
    middle_name = Column(String(50), nullable=True)
    last_name = Column(String(50))
    username = Column(String, nullable=True)
    password = Column(String, nullable=True)
    mobile_no = Column(String(50), unique=True, nullable=False)
    status =  Column(String(50), default=UserStatus.CREATED)
    last_login_time = Column(DateTime(), nullable=True)  
    profile_pic = Column(String, nullable=True)
    date_of_birth = Column(DateTime(), nullable=True)
    address_line1 = Column(String, nullable=True)
    address_line2 = Column(String, nullable=True)
    state = Column(String, nullable=True)
    zip_code = Column(String, nullable=True)
    last_password_change_date = Column(DateTime(), nullable=True)  
    two_factor_auth = Column(Boolean, default=False)
    otp_secret = Column(String, nullable=True)
    incorrect_password_attempts = Column(Integer, nullable=True, default=0)
    incorrect_otp_attempts = Column(Integer, nullable=True, default=0)
    otps = relationship('auth.models.UserOTP', backref='user', lazy=True)
    # transactions = relationship('income_expense_tracker.models.Transactions', backref='email', lazy=True)
    
    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def get_by_mobile_no(cls, mobile_no):
        return cls.query.filter_by(mobile_no=mobile_no).first()
    
    def check_password(
        self, 
        password: str
    ) -> bool:
        return Utils.check_password_hash(self.password, password)
    
    @property
    def name(self) -> str:
        return str(self.first_name)
        
    @property
    def full_name(self) -> str:
        return f'{self.first_name.title()} {self.last_name.title()}'
    
    def __str__(self) -> str:
        if self.first_name != "":
            rtn = self.full_name
        else:
            rtn = self.email
        return rtn

    def __repr__(self) -> str:
        return f'User<{self.email} {self.first_name}>'
    

class UserOTP(Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    hashed_otp = Column(String(60), nullable=False)
    otp_timestamp = Column(BigInteger, nullable=False)
