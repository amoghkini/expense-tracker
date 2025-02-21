from flask import request, g, session, make_response, redirect, url_for
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
            session['email'] = form_data.get('email')
            next_page = request.args.get('next_page')
            if next_page:
                return self.redirect(response_handler.next_page, next_page=next_page)
            # return self.redirect(response_handler.next_page)

            response = make_response(redirect(url_for(response_handler.next_page)))
            response.set_cookie('authorization', response_handler.data, secure=True, httponly=True)
            return response
        else:
            if response_handler.message:
                self.warning(response_handler.message)
            self._context["errors"] = response_handler.errors
            self._context["form_data"] = request.form
            return self.render()
    

class AuthLoginWithOTPView(BaseView):
    _template = 'login_with_otp.html'
    
    def get(self):
        self._context["errors"] = {}
        self._context["form_data"] = request.form
        return self.render()
    
    def post(self):
        form_data: dict = request.form.to_dict()
        response_handler: Response = BusinessLogic.login_with_otp(form_data)
        if response_handler.success:
            if response_handler.message:
                self.success(response_handler.message)
            session['email'] = form_data.get('email')
            self._context["errors"] = {}
            next_page = request.args.get('next_page')
            if next_page:
                return self.redirect('auth.verify_otp_api', next_page=next_page)
            return self.redirect('auth.verify_otp_api')
        else:
            if response_handler.message:
                self.warning(response_handler.message)
            self._context["errors"] = response_handler.errors
            self._context["form_data"] = request.form
            return self.render()
      
    
class AuthResendOTPView(BaseView):
    _template = 'verify_otp.html'
    
    def post(self):
        form_data: dict = request.form.to_dict()
        response_handler: Response = BusinessLogic.resend_otp(form_data)
        if response_handler.success:
            if response_handler.message:
                self.success(response_handler.message)
            self._context["errors"] = {}
            self._context["form_data"] = request.form
        else:
            if response_handler.message:
                self.warning(response_handler.message)
            self._context["errors"] = response_handler.errors
            self._context["form_data"] = request.form
        self._context["no_of_attempts"]  = response_handler.data.get('no_of_attempts')
        self._context["max_attempts"]  = response_handler.data.get('max_attempts')
        return self.render()
    
    
class AuthVerifyOTP(BaseView):
    _template: str = 'verify_otp.html'
    
    def get(self):
        self._context["errors"] = {}
        self._context["form_data"] = request.form
        email: str = session.pop('email', None)
        self._context["email"]  = email
        
        if not email:
            return self.redirect('auth.login_api')
        response_handler: Response = BusinessLogic.pre_verify_otp_checks(email)
        self._context["no_of_attempts"]  = response_handler.data.get('no_of_attempts')
        self._context["max_attempts"]  = response_handler.data.get('max_attempts')
        return self.render()
    
    def post(self):

        self._context["errors"] = {}
        form_data: dict = request.form.to_dict()
        self._context["email"]  = form_data.get('email')
        response_handler: Response = BusinessLogic.verify_otp(form_data)
        
        if response_handler.success:
            if response_handler.message:
                self.success(response_handler.message)
            self._context["errors"] = {}
            next_page = request.args.get('next_page')
            if next_page:
                return self.redirect(next_page)
            return self.redirect('core.index_api')
        else:
            self._context["no_of_attempts"]  = response_handler.data.get('no_of_attempts')
            self._context["max_attempts"]  = response_handler.data.get('max_attempts')
            if response_handler.message:
                self.warning(response_handler.message)
            self._context["errors"] = response_handler.errors
            self._context["form_data"] = request.form
            return self.render()
   
    
class AuthLogOutView(BaseView):
    
    @login_required
    def get(self):
        # TODO: We need to mark jwt in sessions table as invalidate.
        token: str = request.cookies.get('authorization', '')
        BusinessLogic.process_logout(token)
        # return self.redirect('core.index_api')
        response = make_response(redirect(url_for('core.index_api')))
        response.delete_cookie('authorization')
        return response
        

class AuthLogOutDeviceView(BaseView):
    
    # TODO: The logout devices page should send the valid redirect url. We can achieve this using response_handler.next_page variable.
    # TODO: If we are logging out all the devices then we should mark all the devices as invalidate and delete cookies from current and remaining devices.
    # TODO: If we are logging out single device then we should just invalidate the device and redirect user to the security page. But if only one device is loggedin and user logs it out from table then we should delete cookies and redirect user to login page instead of security page.                                                                                                                                                                                                                                                                                                                                                                                                            
    def get(self):
        action: str = request.args.get('action', '').lower()
        if action == 'all':
            response_handler = BusinessLogic.logout_device(g.email)
            return self.redirect(response_handler.next_page)
        elif action == 'single':
            device_id = request.args.get('id', '')
            response_handler = BusinessLogic.logout_device(g.email, device_id)
            return self.redirect(response_handler.next_page)
        else:
            self.warning(f"Please provide valid action to logout the device")
            return self.redirect('auth.profile_security_api')
            

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
            self._context["profile_data"] = response_handler.data['profile_data']
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
            self._context["profile_data"] = response_handler.data['profile_data']
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
        token = request.cookies.get('authorization', '')
        response_handler: Response = BusinessLogic.fetch_security_page_data(g.email, token)
        if response_handler.success:
            if response_handler.message:
                self.success(response_handler.message)
            self._context["errors"] = {}
            self._context["profile_data"] = response_handler.data['profile_data']
            self._context["sessions"] = response_handler.data['sessions']
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
            return self.redirect('auth.login_api')
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