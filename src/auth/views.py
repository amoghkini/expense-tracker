from flask import request, g

from auth.business_logic import BusinessLogic
from auth.constants import IndianStatesAndUTs
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
                return self.redirect(next_page)
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
        response_handler: Response = BusinessLogic.fetch_profile_data(g.email)
        if response_handler.success:
            if response_handler.message:
                self.success(response_handler.message)
            self._context["errors"] = {}
            self._context["profile_data"] = response_handler.data
        else:
            if response_handler.message:
                self.warning(response_handler.message)
        return self.render()
        
    
class AuthProfileSettingsView(BaseView):
    _template = 'profile_settings.html'
    
    @login_required
    def get(self):
        self._context["errors"] = {}
        response_handler: Response = BusinessLogic.fetch_profile_data(g.email)
        if response_handler.success:
            if response_handler.message:
                self.success(response_handler.message)
            self._context["errors"] = {}
            self._context['states'] = IndianStatesAndUTs.allowed_values()
            self._context["profile_data"] = response_handler.data
        else:
            if response_handler.message:
                self.warning(response_handler.message)
            self._context["errors"] = {}
            self._context['states'] = IndianStatesAndUTs.allowed_values()
            self._context["profile_data"] = {}
        return self.render()
    
    @login_required
    def post(self):
        form_data: dict = request.form.to_dict()
        response_handler: Response = BusinessLogic.update_profile(form_data, g.email)

        if response_handler.success:
            if response_handler.message:
                self.success(response_handler.message)
            self._context["errors"] = {}
            return self.redirect('auth.profile_settings_api')
        else:
            if response_handler.message:
                self.warning(response_handler.message)
            self._context["errors"] = response_handler.errors
            self._context["form_data"] = request.form
            return self.render()
        

class AuthProfileSecurity(BaseView):
    _template = 'security.html'
    
    @login_required
    def get(self):
        self._context["errors"] = {}
        response_handler: Response = BusinessLogic.fetch_profile_data(g.email)
        if response_handler.success:
            if response_handler.message:
                self.success(response_handler.message)
            self._context["errors"] = {}
            self._context["profile_data"] = response_handler.data
        else:
            if response_handler.message:
                self.warning(response_handler.message)
        return self.render()

class AuthProfileNotificationsSettings(BaseView):
    _template = 'notifications_settings.html'
    
    @login_required
    def get(self):
        self._context["errors"] = {}
        self._context["form_data"] = request.form
        return self.render()
    

class AuthProfileForgotPasswordRequest(BaseView):
    _template = 'forgot_password_request.html'
    
    def get(self):
        self._context["errors"] = {}
        self._context["form_data"] = request.form
        return self.render()
            
    def post(self):
        form_data: dict = request.form.to_dict()
        response_handler: Response = BusinessLogic.request_password_reset(form_data)
        if response_handler.success:
            if response_handler.message:
                self.success(response_handler.message)
            self._context["errors"] = {}
            return self.redirect('auth.forgot_password_confirmation_api')
        else:
            if response_handler.message:
                self.warning(response_handler.message)
            self._context["errors"] = response_handler.errors
            self._context["form_data"] = request.form
            return self.render()
        

class AuthProfileForgotPasswordConfirmation(BaseView):
    _template = 'forgot_password_request_confirmation.html'
    
    def get(self):
        self._context["errors"] = {}
        self._context["form_data"] = request.form
        return self.render()
    

class AuthProfileResetPassword(BaseView):
    _template = 'reset_password.html'
    
    def get(self):
        form_data: dict = request.args.to_dict()
        response_handler: Response = BusinessLogic.reset_password_token_verification(form_data)
        if response_handler.success:
            if response_handler.message:
                self.success(response_handler.message)
            self._context["errors"] = {}
            self._context["form_data"] = response_handler.data
            return self.render()
        else:
            if response_handler.message:
                self.warning(response_handler.message)
            return self.redirect('core.index_api')
    
    def post(self):
        form_data: dict = request.form.to_dict()
        response_handler: Response = BusinessLogic.reset_password(form_data)
        if response_handler.success:
            if response_handler.message:
                self.success(response_handler.message)
            self._context["errors"] = {}
            return self.redirect('core.index_api')
        else:
            if response_handler.message:
                print(response_handler.message)
                self.warning(response_handler.message)
            self._context["errors"] = response_handler.errors
            self._context["form_data"] = request.form
            return self.render()
        
        
class AuthProfileChangePassword(BaseView):
    _template = 'change_password.html'
    
    def get(self):
        self._context["errors"] = {}
        self._context["form_data"] = request.form
        return self.render()
    
    def post(self):
        form_data: dict = request.form.to_dict()
        response_handler: Response = BusinessLogic.change_password(form_data, g.email)

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
        
class AuthManageTwoFactorAuth(BaseView):
    
    _template = 'security.html'
        
    def get(self):
        form_data: dict = request.args.to_dict()
        response_handler: Response = BusinessLogic.manage_2fa(form_data, g.email)
        if response_handler.success:
            if response_handler.message:
                self.success(response_handler.message)
            self._context["errors"] = {}
            self._context["form_data"] = response_handler.data
            return self.redirect('auth.profile_security_api')
        else:
            if response_handler.message:
                self.warning(response_handler.message)
            return self.redirect('core.index_api')