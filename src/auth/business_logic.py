from pydantic import ValidationError
from typing import Union

from auth.exceptions import IncorrectCredentialsException, UserNotFoundException
from auth.models import User
from auth.data_validator import UserSignUpValidator, ChangePasswordRequestValidator, ResetPasswordValidator
from auth.utils import Utils, TokenSerializer
from utils.flask_utils import get_external_url
from utils.response_handler import Response
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
            
            if user.check_password(password):
                print(f"{user.first_name} logged in successfully")
            else:
                raise IncorrectCredentialsException
            # To Do: Update last login date 
            Utils.login_user(email)
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
            new_user = BusinessLogic.get_new_user_model(form_data)
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
            print(f"An exception occured while requesting password reset {str(e)}")
            response.message = "An internal error occured"
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
    def get_new_user_model(form_data: dict) -> User:
        new_user = User()
        new_user.email = form_data.get("email")
        new_user.first_name = form_data.get("first_name")
        new_user.last_name = form_data.get("last_name")
        new_user.mobile_no = form_data.get("mobile_no")
        new_user.password = Utils.generate_hashed_password(form_data.get("password", ''))
        new_user.username = Utils.generate_username(form_data.get("first_name", ''), form_data.get("last_name", ''))
        return new_user