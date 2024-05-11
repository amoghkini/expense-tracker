from pydantic import ValidationError
from typing import Union

from auth.exceptions import IncorrectCredentialsException, IncorrectOTPException, OTPTimeoutException, UserNotFoundException
from auth.models import User
from auth.data_validator import UserSignUpValidator, ChangePasswordRequestValidator, ResetPasswordValidator
from auth.utils import Utils, TokenSerializer, OTPUtils
from utils.flask_utils import get_external_url
from utils.response_handler import Response
from utils.time_utils import TimeUtils
from utils.utils import Utils as CommonUtils


class BusinessLogic:
    
    @staticmethod
    def process_login(
        form_data: dict
    ) -> Response:
        response = Response()
        try:
            email: str = form_data.get('email', '')
            password: str = form_data.get('password', '')
            
            user: User = User.get_by_email(email)
            if not user:
                raise UserNotFoundException
            
            if not user.check_password(password):
                raise IncorrectCredentialsException
            
            # To Do: Update last login date 
            if user.two_factor_auth:
                new_otp = OTPUtils.get_otp_object(user).now()
                print(f"New OTP {new_otp}")       
                user.otp_sent_time = TimeUtils.get_epoch()
                response.next_page = 'auth.verify_otp_api'
            else:
                Utils.login_user(email)
                response.next_page = 'core.index_api'
                response.message = "User logged in successfully"
        except (IncorrectCredentialsException, UserNotFoundException) as e:
            print(f"The entered email id or password may be incorrect")
            response.errors['email'] = "The entered email id or password may be incorrect"
            response.success = False
        except Exception as e:
            print(f"An exception occured while login {str(e)}")
            response.message = "An internal error occured"
            response.success = False
        return response
    
    @staticmethod
    def login_with_otp(form_data: dict) -> Response:
        response = Response()
        try:
            email: str = form_data.get('email', '')
            
            user: User = User.get_by_email(email)
            if not user:
                print("The user is not registered in the system")    
            
            new_otp = OTPUtils.get_otp_object(user).now()
            print(f"New OTP {new_otp}")       
            user.otp_sent_time = TimeUtils.get_epoch()
            response.message = "The OTP is sent on registered email address"
            
        except UserNotFoundException as e:
            print(f"The entered email id or password may be incorrect")
            response.errors['email'] = "The entered email id or password may be incorrect"
            response.success = False
        except Exception as e:
            print(f"An exception occured while requesting password reset {str(e)}")
            response.message = "An internal error occured"
            response.success = False
        return response     
   
    @staticmethod
    def verify_otp(form_data: dict) -> Response:
        OTP_VALID_DURATION = 3   # This should be from environment variables
        response = Response()
        try:
            email: str = form_data.get('email', '')
            otp: str = form_data.get('otp', '')
            user: User = User.get_by_email(email)
            if not user:
                raise UserNotFoundException
            
            current_time: int = TimeUtils.get_epoch()
            if user.otp_sent_time and (current_time - user.otp_sent_time) > OTP_VALID_DURATION:
                raise OTPTimeoutException(f"The user must enter the OTP within {OTP_VALID_DURATION} seconds")
            
            if OTPUtils.is_otp_valid(user, otp):
                print("OTP verified successfully")
                Utils.login_user(email)
                response.message = "User logged in successfully"
            else:
                raise IncorrectOTPException("The entered OTP is incorrect")
            
        except (OTPTimeoutException, IncorrectOTPException) as e:
            print(f"The entered OTP is incorrect")
            response.errors['otp'] = e
            response.success = False
        except UserNotFoundException as e:
            print(f"The entered email id is incorrect")
            response.errors['email'] = "The entered email id is not valid"
            response.success = False
        except Exception as e:
            print(f"An exception occured while login {str(e)}")
            response.message = "An internal error occured"
            response.success = False
        return response
    
    @staticmethod
    def process_logout():
        try:
            Utils.logout_user()
        except Exception as e:
            print(f"An exception occured while registering the user {str(e)}")
            
    @staticmethod
    def process_signup(
        form_data: dict
    ) -> Response:

        response = Response()
        try:
            user = UserSignUpValidator(**form_data)
            print(f"Registering new user: {user.email}")
            new_user = BusinessLogic.form_to_model(form_data)
            new_user.save(commit=True)
            
            response.message = "User created successfully"
        except ValidationError as e:
            response.errors = {error['loc'][0]: f"Please provide a valid {CommonUtils.title_case(error['loc'][0])}" if error['type'] == 'value_error.missing' else error['msg']  for error in e.errors()}
            response.message = "Validation Error: Please correct the errors below"
            response.success = False
        except Exception as e:
            print(f"An exception occured while registering the user {str(e)}")
            response.message = f"An internal error occurred"
            response.success = False
        return response
    
    @staticmethod
    def fetch_profile_data(email: str) -> Response:
        response = Response()
        try:            
            user: User = User.get_by_email(email)
            
            if not user:
                raise UserNotFoundException
            response.data = user.to_dict()
            print(response.data)
        except UserNotFoundException as e:
            print(f"The user is invalid")
            response.errors['email'] = "The entered email invalid"
            response.success = False
        except Exception as e:
            print(f"An exception occured while fetching the profile data {str(e)}")
            response.message = "An internal error occured"
            response.success = False
        return response
    
    @staticmethod
    def update_profile(
        form_data: dict,
        email: str
    ) -> Response:
        response = Response()
        try:
            user = User.query.filter_by(email=email).first()
            if not user:
                raise UserNotFoundException("The user is not registered in system")
            
            user.first_name = form_data.get('first_name')
            user.last_name = form_data.get('last_name')
            user.address_line1 = form_data.get('address_line1')
            user.address_line2 = form_data.get('address_line2')
            user.state = form_data.get('state')
            user.zip_code = form_data.get('zip_code')
            user.commit()
            response.message = "Data updated successfully" 
       
        except UserNotFoundException as e:
            print(f"Error encountered {e}")
            response.success = False
            
        except Exception as e:
            print(f"An exception occured while changing the user password {str(e)}")
            response.message = f"An internal error occurred"
            response.success = False
        return response
    
    @staticmethod
    def change_password(
        form_data: dict,
        email: str
    ) -> Response:
        
        response = Response()
        try:
            user_data = ChangePasswordRequestValidator(**form_data)

            # Retrieve the user from the database
            user = User.query.filter_by(email=email).first()
            if not user:
                raise UserNotFoundException("The user is not registered in system")
            
            if Utils.check_password_hash(user.password, user_data.old_password):
                user.password = Utils.generate_hashed_password(user_data.new_password)
                user.commit()
                response.message = "Password changed successfully"
            else:
                raise IncorrectCredentialsException("Please enter the correct old password!")    
        except ValidationError as e:
            response.errors = {error['loc'][0]: f"Please provide a valid {CommonUtils.title_case(error['loc'][0])}" if error['type'] == 'value_error.missing' else error['msg']  for error in e.errors()}
            response.message = "Validation Error: Please correct the errors below"
            response.success = False
        except (IncorrectCredentialsException, UserNotFoundException) as e:
            print(f"Error encountered {e}")
            response.errors['old_password'] = e
            response.success = False
            
        except Exception as e:
            print(f"An exception occured while changing the user password {str(e)}")
            response.message = f"An internal error occurred"
            response.success = False
        return response
    
    @staticmethod
    def request_password_reset(form_data: dict) -> Response:
        response = Response()
        try:
            email: str = form_data.get('email', '')
            
            user: User = User.get_by_email(email)
            if not user:
                raise UserNotFoundException
            
            token_serializer = TokenSerializer('amogh')
            verify_token: Union[str, bytes] = token_serializer.generate_token(email)
            password_reset_url: str = get_external_url('auth.reset_password_api',{"token":verify_token})
            print("Password reset link", password_reset_url)
            
            response.message = "The password reset link has been sent successfully on registered email address"
            
        except UserNotFoundException as e:
            print(f"The entered email id or password may be incorrect")
            response.errors['email'] = "The entered email id or password may be incorrect"
            response.success = False
        except Exception as e:
            print(f"An exception occured while requesting password reset {str(e)}")
            response.message = "An internal error occured"
            response.success = False
        return response
        
    @staticmethod
    def reset_password_token_verification(form_data: dict) -> Response:
        response = Response()
        try:
            token: str = form_data.get('token', '')
            
            token_serializer = TokenSerializer('amogh')
            email = token_serializer.verify_token(token, max_age=3600)  
            
            user: User = User.get_by_email(email)
            
            if not user:
                raise UserNotFoundException
            response.data = {'email': email}
            # response.message = "Password reset successfully"
            
        except UserNotFoundException as e:
            print(f"The user is invalid or token is expired")
            response.errors['email'] = "The entered email id or password may be incorrect"
            response.success = False
        except Exception as e:
            print(f"An exception occured while requesting password reset {str(e)}")
            response.message = "An internal error occured"
            response.success = False
        return response
         
    @staticmethod
    def reset_password(form_data: dict) -> Response:
        
        response = Response()
        try:
            user_data = ResetPasswordValidator(**form_data)
            
            # Retrieve the user from the database
            user = User.query.filter_by(email=form_data.get('email')).first()
            if not user:
                raise UserNotFoundException("The user is not registered in system")
            
            if Utils.check_password_hash(user.password, user_data.new_password):
                raise IncorrectCredentialsException("New password should not be same as old password!")   
            else:
                user.password = Utils.generate_hashed_password(user_data.new_password)
                user.commit()
            response.message = "Password reset successfully"
            
        except ValidationError as e:
            response.errors = {error['loc'][0]: f"Please provide a valid {CommonUtils.title_case(error['loc'][0])}" if error['type'] == 'value_error.missing' else error['msg']  for error in e.errors()}
            response.message = "Validation Error: Please correct the errors below"
            response.success = False
        except (IncorrectCredentialsException, UserNotFoundException) as e:
            print(f"Error encountered {e}")
            response.message = str(e)
            response.success = False
        except Exception as e:
            print(f"An exception occured while changing the user password {str(e)}")
            response.message = f"An internal error occurred"
            response.success = False
        return response
    
    @staticmethod
    def manage_2fa(
        form_data: dict,
        email: str
    ) -> Response:
        response = Response()
        try:
            action: str = form_data.get('action', '')            
            
            user: User = User.get_by_email(email)
            if not user:
                raise UserNotFoundException
            
            if action.lower() == 'enable':
                user.two_factor_auth = True    
            else:    
                user.two_factor_auth = False
            
        except Exception as e:
            print(f"An exception occured while changing 2fa status {str(e)}")
            response.message = "An internal error occured"
            response.success = False
        return response
    
    @staticmethod
    def form_to_model(form_data: dict) -> User:
        new_user = User()
        new_user.email = form_data.get("email")
        new_user.first_name = form_data.get("first_name")
        new_user.last_name = form_data.get("last_name")
        new_user.mobile_no = form_data.get("mobile_no")
        new_user.password = Utils.generate_hashed_password(form_data.get("password", ''))
        new_user.username = Utils.generate_username(form_data.get("first_name", ''), form_data.get("last_name", ''))
        new_user.otp_secret = OTPUtils.generate_otp_secret()
        return new_user