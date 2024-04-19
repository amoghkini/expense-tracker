from sqlalchemy import ForeignKey
from database import (
    BigInteger,
    Column,
    DateTime,
    Integer,
    Model,
    String
)
from utils.time_utils import TimeUtils


class Transactions(Model):
    title = Column(String(500), nullable=False)
    amount = Column(BigInteger, nullable=False)
    type_of_transaction = Column(String(10), nullable=False)
    category = Column(String(50), nullable=False)
    mode_of_payment = Column(String(50), nullable=False)
    date = Column(BigInteger, nullable=True)  
    hidden_expense = Column(Integer, nullable=True)
    reason_of_expense = Column(String(50), nullable=True)
    description = Column(String, nullable=True)
    user_email = Column(Integer,ForeignKey('user.email'))
    
    
    def to_dict(self, columns=None):
        data = super().to_dict(columns)
        if 'date' in data and data.get('date') is not None:
            data['date'] = TimeUtils.get_datetime_from_epoch(data.get('date',0), TimeUtils.DATE_TIME_FORMAT_UI)
        return data