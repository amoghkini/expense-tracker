from income_expense_tracker import income_expense_tracker
from income_expense_tracker.views import (
    TrackerAddExpense,
    TrackerAddIncome,
    TransactionsTracker,
)


routes = [
    (
        (income_expense_tracker),
            ('/add-expense', 'add_expense_api', TrackerAddExpense),
            ('/add-income', 'add_income_api', TrackerAddIncome),
            ('/transactions', 'transactions_api', TransactionsTracker),
    )
]