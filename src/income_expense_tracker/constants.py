from enum import StrEnum, auto


class TransactionType(StrEnum):
    CREDIT = auto()
    DEBIT = auto()
    
    @staticmethod
    def allowed_transaction_types():
        return [member.value for member in TransactionType]
    
    
class ModeOfPayment(StrEnum):
    CASH = auto()
    UPI = auto()
    
    @staticmethod
    def allowed_mode_of_payment_types():
        return [member.value for member in ModeOfPayment]


class ReasonOfExpense(StrEnum):
    INVESTMENT = auto()
    NEED = auto()
    WANT = auto()
    OTHER = auto()
    
    @staticmethod
    def allowed_reason_of_expense_types():
        return [member.value for member in ReasonOfExpense]