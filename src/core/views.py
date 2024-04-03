from flask import  g

from config.settings import BaseConfig
from core.forms import ColumnForm
from main.baseview import BaseView
from core.test_jinja import row, col

class IndexView(BaseView):
    _template = 'index.html'
    
    def get(self):
        g.user = 'amogh'
        if not g.user:
            return self.redirect('auth.login_api')
        return self.render()
    
    
class AboutView(BaseView):
    _template = 'about.html'

    def get(self):
        return self.render()