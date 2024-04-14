from flask import  g

from core.utils import Utils
from main.baseview import BaseView


class IndexView(BaseView):
    
    def get(self):
        if Utils.get_current_user_from_session():
            return self.redirect('dashboard.dashboard_api')
        else:
            return self.redirect('auth.login_api')
    
    
class AboutView(BaseView):
    _template = 'about.html'

    def get(self):
        return self.render()