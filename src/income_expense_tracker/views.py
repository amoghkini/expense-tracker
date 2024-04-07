from flask import request

from main.baseview import BaseView
from income_expense_tracker.business_logic import BusinessLogic
from income_expense_tracker.constants import ModeOfPayment, ReasonOfExpense
from income_expense_tracker.utils import Utils
from utils.response_handler import Response


class TransactionsTracker(BaseView):
    _template: str = 'transactions.html'
    
    def get(self):
        self._context["errors"] = {}
        return self.render()
    
    
class TrackerAddExpense(BaseView):
    _template: str = 'expense_add.html'
    
    def  get(self):
        self._context["errors"] = {}
        self._context['mode_of_payment_options'] = ModeOfPayment.allowed_values()
        self._context['reason_of_expense_options'] = ReasonOfExpense.allowed_values()
        self._context['categories_dict'] = Utils.get_categories()
        return self.render()
    
    def post(self):
        self._context["errors"] = {}
        self._context['mode_of_payment_options'] = ModeOfPayment.allowed_values()
        self._context['reason_of_expense_options'] = ReasonOfExpense.allowed_values()
        self._context['categories_dict'] = Utils.get_categories()
        import pdb;pdb.set_trace()
        form_data: dict = request.form.to_dict()
        response_handler: Response = BusinessLogic.add_new_expense(form_data)
        
        if response_handler.success:
            if response_handler.message:
                self.success(response_handler.message)
            self._context["errors"] = {}
            return self.redirect('core.index_api')
        else:
            if response_handler.message:
                self.warning(response_handler.message)
            self._context["errors"] = response_handler.errors
            self._context["form_data"] = request.form
            return self.render()
        
        
class TrackerAddIncome(BaseView):
    _template: str = 'income_add.html'
    
    def  get(self):
        self._context["errors"] = {}
        return self.render()