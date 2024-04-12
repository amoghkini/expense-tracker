from pydantic import BaseModel, validator

from income_expense_tracker.constants import ModeOfPayment, ReasonOfExpense


class NewExpenseValidator(BaseModel):
    title: str
    amount: int
    category: str
    mode_of_payment: str
    date: str
    time: str
    reason_of_expense: str
    description: str
    
    @validator('amount')
    def amount_validator(cls, amount):
        if amount <=0:
            raise ValueError("Please provide amount greater than 0")
        return amount
        
    @validator('mode_of_payment')
    def mode_of_payment_validator(cls, mode_of_payment):
        if mode_of_payment not in ModeOfPayment.allowed_values():
            raise ValueError('Please provide valid mode of payment')
        return mode_of_payment
        
    @validator('reason_of_expense')
    def reason_of_expense_validator(cls, reason_of_expense):
        if reason_of_expense not in ReasonOfExpense.allowed_values():
            raise ValueError('Please provide valid reason of expense')
        return reason_of_expense

    def to_dict(self):
        return self.dict()
    
    def __str__(self) -> str:
        return f"{self.title}: {self.amount}"
    

class NewIncomeValidator(BaseModel):
    title: str
    amount: int
    category: str
    mode_of_payment: str
    date: str
    time: str
    description: str
    
    @validator('amount')
    def amount_validator(cls, amount):
        if amount <=0:
            raise ValueError("Please provide amount greater than 0")
        return amount
        
    @validator('mode_of_payment')
    def mode_of_payment_validator(cls, mode_of_payment):
        if mode_of_payment not in ModeOfPayment.allowed_values():
            raise ValueError('Please provide valid mode of payment')
        return mode_of_payment
        
    def to_dict(self):
        return self.dict()
    
    def __str__(self) -> str:
        return f"{self.title}: {self.amount}"