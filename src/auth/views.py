from flask import request

from auth.business_logic import BusinessLogic, Response
from main.baseview import BaseView


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
            return self.redirect('core.index_api')
        else:
            if response_handler.message:
                self.warning(response_handler.message)
            self._context["errors"] = response_handler.errors
            self._context["form_data"] = request.form
            return self.render()
    
    
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
