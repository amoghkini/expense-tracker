from flask import request

from main.baseview import BaseView
from utils.flask_utils import login_required


class DashboardView(BaseView):
    _template: str = 'dashboard.html'
    
    @login_required
    def  get(self):
        self._context["errors"] = {}
        return self.render()