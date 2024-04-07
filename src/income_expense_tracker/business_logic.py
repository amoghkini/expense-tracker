from pydantic import ValidationError
from typing import Union

from income_expense_tracker.constants import TransactionType
from income_expense_tracker.data_validator import NewExpenseValidator
from income_expense_tracker.exceptions import InvalidTransactionTypeException
from income_expense_tracker.models import Transactions
from utils.response_handler import Response
from utils.time_utils import TimeUtils
from utils.utils import Utils as CommonUtils


class BusinessLogic:
    
    @staticmethod
    def add_new_expense(
        form_data: dict
    ) -> Response:
        response = Response()
        try:
            expense = NewExpenseValidator(**form_data)
            print(f"Adding new expense")
            # new_expense = BusinessLogic.get_new_transaction_model(form_data, "DEBIT")
            new_expense = BusinessLogic.get_new_transaction_model(form_data, TransactionType.DEBIT)
            new_expense.save(commit=True)
            response.message = "Expense added successfully"
        except ValidationError as e:
            response.errors = {error['loc'][0]: f"Please provide a valid {CommonUtils.title_case(error['loc'][0])}" if error['type'] == 'value_error.missing' else error['msg']  for error in e.errors()}
            response.message = "Validation Error: Please correct the errors below"
            response.success = False
        except Exception as e:
            print(f"An exception occured while adding new expense {str(e)}")
            response.message = f"An internal error occurred"
            response.success = False
        return response
            
    @staticmethod
    def get_new_transaction_model(
        form_data: dict,
        transction_type: Union[str, TransactionType]
    ) -> Transactions:
        # Check if transaction_type is valid
        if not transction_type in TransactionType.allowed_values():
            raise InvalidTransactionTypeException("Invalid transaction type provided")
        
        new_transaction: Transactions = Transactions()
        new_transaction.type_of_transaction = transction_type
        new_transaction.title = form_data.get('title')
        new_transaction.amount = form_data.get('amount')
        new_transaction.category = form_data.get('category')
        new_transaction.mode_of_payment = form_data.get('mode_of_payment')
        new_transaction.date = TimeUtils.get_epoch(TimeUtils.combine_date_time(form_data.get('date', ''), TimeUtils.DATE_FORMAT_US, form_data.get('time', ''), TimeUtils.TIME_FORMAT_WITHOUT_SEC))
        new_transaction.hidden_expense = 0
        new_transaction.reason_of_expense = form_data.get('reason_of_expense')
        new_transaction.description = form_data.get('description')
        
        return new_transaction