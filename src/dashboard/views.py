from flask import request

from main.baseview import BaseView


class DashboardView(BaseView):
    _template: str = 'dashboard.html'
    
    def  get(self):
        self._context["errors"] = {}
        return self.render()