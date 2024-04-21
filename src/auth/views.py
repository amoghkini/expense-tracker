from flask import request

from auth.business_logic import BusinessLogic
from main.baseview import BaseView
from utils.flask_utils import login_required
from utils.response_handler import Response


class AuthLoginView(BaseView):
    _template = 'login.html'
    
    def get(self):
        self._context["errors"] = {}
        self._context["form_data"] = request.form
        return self.render()
    
    def post(self):
        self._context["errors"] = {}
        
        form_data: dict = request.form.to_dict()
        response_handler: Response = BusinessLogic.process_login(form_data)
        
        if response_handler.success:
            if response_handler.message:
                self.success(response_handler.message)
            self._context["errors"] = {}
            next_page = request.args.get('next_page')
            if next_page:
                from flask import redirect, url_for
                return redirect(url_for(next_page))
            return self.redirect('core.index_api')
        else:
            if response_handler.message:
                self.warning(response_handler.message)
            self._context["errors"] = response_handler.errors
            self._context["form_data"] = request.form
            return self.render()
    

class AuthLogOutView(BaseView):
    
    @login_required
    def get(self):
        BusinessLogic.process_logout()
        return self.redirect('core.index_api')

        
class AuthSignUpView(BaseView):
    _template = 'signup.html'
    
    def get(self):
        self._context["errors"] = {}
        self._context["form_data"] = request.form
        return self.render()
    
    def post(self):
        form_data: dict = request.form.to_dict()
        response_handler: Response = BusinessLogic.process_signup(form_data)

        if response_handler.success:
            if response_handler.message:
                self.success(response_handler.message)
            self._context["errors"] = {}
            return self.redirect('auth.login_api')
        else:
            if response_handler.message:
                self.warning(response_handler.message)
            self._context["errors"] = response_handler.errors
            self._context["form_data"] = request.form
            return self.render()

class AuthProfileView(BaseView):
    _template = 'profile.html'
    
    @login_required
    def get(self):
        self._context["errors"] = {}
        self._context["form_data"] = request.form
        return self.render()