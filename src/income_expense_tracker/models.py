
from database import (
    BigInteger,
    Column,
    DateTime,
    Integer,
    Model,
    String
)
class Transactions(Model):
    title = Column(String(500), nullable=False)
    amount = Column(BigInteger, nullable=False)
    type_of_transaction = Column(String(10), nullable=False)
    category = Column(String(50), nullable=False)
    mode_of_payment = Column(String(50), nullable=False)
    date = Column(BigInteger, nullable=True)  
    hidden_expense = Column(Integer, nullable=True)
    reason_of_expense = Column(String(50), nullable=False)
    description = Column(String, nullable=True)