from flask import  g

from main.baseview import BaseView


class IndexView(BaseView):
    
    def get(self):
        g.user = 'amogh'
        if not g.user:
            return self.redirect('auth.login_api')
        else:
            return self.redirect('dashboard.dashboard_api')
    
    
class AboutView(BaseView):
    _template = 'about.html'

    def get(self):
        return self.render()