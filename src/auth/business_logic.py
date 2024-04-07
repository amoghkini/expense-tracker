from pydantic import ValidationError

from auth.exceptions import IncorrectCredentialsException, UserNotFoundException
from auth.models import User
from auth.data_validator import UserSignUpValidator
from auth.utils import Utils
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
    def process_signup(
        form_data: dict
    ) -> Response:
        
        response = Response()
        try:
            user = UserSignUpValidator(**form_data)
            print(f"Registering new user: {user.to_dict()}")
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
    def get_new_user_model(form_data: dict) -> User:
        new_user = User()
        new_user.email = form_data.get("email")
        new_user.first_name = form_data.get("first_name")
        new_user.last_name = form_data.get("last_name")
        new_user.mobile_no = form_data.get("mobile_no")
        new_user.password = Utils.generate_hashed_password(form_data.get("password", ''))
        new_user.username = Utils.generate_username(form_data.get("first_name", ''), form_data.get("last_name", ''))
        return new_user