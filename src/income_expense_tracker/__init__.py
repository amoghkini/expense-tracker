from flask import Blueprint

income_expense_tracker = Blueprint(
    'income_expense_tracker',
    __name__,
    template_folder='templates',
    url_prefix='/tracker'
)