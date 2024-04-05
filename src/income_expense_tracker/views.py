from main.baseview import BaseView


class TransactionsTracker(BaseView):
    _template: str = 'transactions.html'
    
    def get(self):
        self._context["errors"] = {}
        return self.render()
    
    
class TrackerAddExpense(BaseView):
    _template: str = 'expense_add.html'
    
    def  get(self):
        self._context["errors"] = {}
        return self.render()
    

class TrackerAddIncome(BaseView):
    _template: str = 'income_add.html'
    
    def  get(self):
        self._context["errors"] = {}
        return self.render()