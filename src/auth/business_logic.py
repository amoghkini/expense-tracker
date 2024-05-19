from pydantic import ValidationError
from typing import Union

from auth.constants import UserStatus
from auth.exceptions import (
    AccountLockedException,
    IncorrectCredentialsException, 
    IncorrectOTPException, 
    InvalidOTPSecretKeyException,
    OTPTimeoutException, 
    MaxLoginAttemptsReachedException, 
    MaxResendOTPLimitReached,
    UserNotFoundException
)
from auth.models import (
    User, 
    UserOTP
)
from auth.data_validator import (
    ChangePasswordRequestValidator, 
    ResetPasswordValidator,
    UserSignUpValidator
)
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
        MAX_LOGIN_ATTEMPTS = 5
        response = Response()
        try:
            email: str = form_data.get('email', '')
            password: str = form_data.get('password', '')
            
            user: User = User.get_by_email(email)
            if not user:
                raise UserNotFoundException("The entered email id or password may be incorrect")
            
            if user.status == UserStatus.LOCKED:
                raise AccountLockedException("The account is locked. Please reset the password to proceed by clicking on forgot password link.")
            else:
                if not user.check_password(password):
                    Utils.increment_incorrect_password_attempts(user)
                    if user.incorrect_password_attempts >= MAX_LOGIN_ATTEMPTS:
                        user.status = UserStatus.LOCKED
                        raise MaxLoginAttemptsReachedException("Maxed login attempts reached. Account is locked")
                    user.commit()
                    raise IncorrectCredentialsException("The entered email id or password may be incorrect")

                # Update last login date 
                user.last_login_time = TimeUtils.get_epoch()
                
                if user.two_factor_auth:
                    if user.otp_secret:
                        hashed_otp = OTPUtils.get_otp_object(user)
                        otp = UserOTP(user_id=user.id, hashed_otp=hashed_otp, otp_timestamp=TimeUtils.get_epoch())
                        otp.save(commit=True)
                        response.next_page = 'auth.verify_otp_api'
                    else:
                        raise InvalidOTPSecretKeyException("Something went wrong while generating OTP.")
                else:
                    Utils.reset_incorrect_password_attempts(user)
                    Utils.login_user(email)
                    response.next_page = 'core.index_api'
                    response.message = "User logged in successfully"
                user.commit()
        except (IncorrectCredentialsException, UserNotFoundException, MaxLoginAttemptsReachedException, AccountLockedException, InvalidOTPSecretKeyException) as e:
            print(f"Excption occured in login method {str(e)}")
            response.errors['email'] = e
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
            else:
                if user.status == UserStatus.LOCKED:
                    raise AccountLockedException("The account is locked. Please reset the password to proceed by clicking on forgot password link.")
                else:
                    if user.otp_secret:
                        hashed_otp = OTPUtils.get_otp_object(user)
                        
                        otp = UserOTP(user_id=user.id, hashed_otp=hashed_otp, otp_timestamp=TimeUtils.get_epoch())
                        otp.save(commit=True)
                    else:
                        raise InvalidOTPSecretKeyException("Something went wrong while generating OTP.")
            response.message = "The OTP is sent on registered email address"
        except (AccountLockedException, InvalidOTPSecretKeyException) as e:
            print(e)
            response.errors['email'] = e
            response.success = False
        except Exception as e:
            print(f"An exception occured while requesting password reset {str(e)}")
            response.message = "An internal error occured"
            response.success = False
        return response     
   
    @staticmethod
    def pre_verify_otp_checks(email: str) -> Response:
        MAX_OTP_ATTEMPTS = 5   # This should be from environment variables

        response = Response(data = {}, errors={})
        try:
           
            user: User = User.get_by_email(email)
            if not user:
                print("The user is not registered in the system")
                response.data['no_of_attempts'] = -1
                response.data['max_attempts'] = MAX_OTP_ATTEMPTS
            else:
                if user.status == UserStatus.LOCKED:
                    raise AccountLockedException("The account is locked. Please reset the password to proceed by clicking on forgot password link.")
                else:
                    response.data['no_of_attempts'] = user.incorrect_otp_attempts
                    response.data['max_attempts'] = MAX_OTP_ATTEMPTS
        except (OTPTimeoutException, IncorrectOTPException, MaxLoginAttemptsReachedException, AccountLockedException) as e:
            print(f"The entered OTP is incorrect")
            response.errors['otp'] = e
            response.success = False
        except UserNotFoundException as e:
            print(f"The entered email id is incorrect")
            response.errors['email'] = e
            response.success = False
        except Exception as e:
            print(f"An exception occured while login {str(e)}")
            response.message = "An internal error occured"
            response.success = False
        return response
        
    @staticmethod
    def verify_otp(form_data: dict) -> Response:
        MAX_OTP_ATTEMPTS = 5       # This should be from environment variables
        OTP_VALID_DURATION = 300   # This should be from environment variables

        response = Response(data = {}, errors={})
        try:
            response.data['no_of_attempts'] = -1
            response.data['max_attempts'] = MAX_OTP_ATTEMPTS
                
            email: str = form_data.get('email', '')
            otp: str = form_data.get('otp', '')
            user: User = User.get_by_email(email)
            if not user:
                # Even thoght the user is not found, we don't want to throw this error message on screen to avoid hackers to find the registered usrs. Hence passing incorrect otp here.
                raise IncorrectOTPException("The entered OTP is incorrect.")

            if user.status == UserStatus.LOCKED:
                raise AccountLockedException("The account is locked. Please reset the password to proceed by clicking on forgot password link.")
            else:
                
                if user.incorrect_otp_attempts >= MAX_OTP_ATTEMPTS:
                    raise MaxLoginAttemptsReachedException("Maxed login attempts reached. Account is locked")
                
                otp_entry: UserOTP = UserOTP.query.filter_by(user_id=user.id).order_by(UserOTP.id.desc()).first()
                if not otp_entry:
                    print("The valid OTP entry is not found")
                    raise IncorrectOTPException("The entered OTP is incorrect.")
                
                current_time: int = TimeUtils.get_epoch()
                if otp_entry.otp_timestamp and (current_time - otp_entry.otp_timestamp) > OTP_VALID_DURATION:
                    raise OTPTimeoutException(f"The user must enter the OTP within {OTP_VALID_DURATION} seconds")
                
                if OTPUtils.is_otp_valid(otp_entry, otp):
                    print("OTP verified successfully")
                    # Reset incorect OTP count
                    user = Utils.reset_incorrect_otp_attempts(user)
                    user.commit()
                    
                    # Delete OTP entry from database
                    otp_entry.delete(commit=True)
                    
                    # Add data to session
                    Utils.login_user(email)
                    response.message = "User logged in successfully"
                else:
                    user = Utils.increment_incorrect_otp_attempts(user)
                    response.data['no_of_attempts'] = user.incorrect_otp_attempts
                    response.data['max_attempts'] = MAX_OTP_ATTEMPTS
                    if user.incorrect_otp_attempts >= MAX_OTP_ATTEMPTS:
                        user.status = UserStatus.LOCKED
                        raise MaxLoginAttemptsReachedException("Maxed login attempts reached. Account is locked.")
                    user.commit()
                    raise IncorrectOTPException("The entered OTP is incorrect.")
            
        except (OTPTimeoutException, IncorrectOTPException, MaxLoginAttemptsReachedException, AccountLockedException) as e:
            print(f"The entered OTP is incorrect")
            response.errors['otp'] = e
            response.success = False
        except Exception as e:
            print(f"An exception occured while login {str(e)}")
            response.message = "An internal error occured"
            response.success = False
        return response
    
    @staticmethod
    def resend_otp(form_data: dict) -> Response:
        MAX_OTP_ATTEMPTS = 5       # This should be from environment variables
        COOLDOWN_TIME_IN_SECONDS = 1800
        MAX_NO_OF_OTPS_BEFORE_COOLDOWN_PERIOD = 3
        INTERVAL_BETWEEN_TWO_OTP_GENERATION = 30
        response = Response(data = {}, errors={})
        try:
            email: str = form_data.get('email', '')
            
            user: User = User.get_by_email(email)
            if not user:
                print("The user is not registered in the system")    
                response.data['no_of_attempts'] = -1
                response.data['max_attempts'] = MAX_OTP_ATTEMPTS
                response.message = "The OTP is sent on registered email address"
                return response
            
            response.data['no_of_attempts'] = user.incorrect_otp_attempts
            response.data['max_attempts'] = MAX_OTP_ATTEMPTS
            if user.status == UserStatus.LOCKED:
                raise AccountLockedException("The account is locked. Please reset the password to proceed by clicking on forgot password link.")
        
            if not user.otp_secret:
                raise InvalidOTPSecretKeyException("Something went wrong while generating OTP.")
            
            # Check if max resend otp limit is breached.
            current_time: int = TimeUtils.get_epoch()
            thirty_minutes_ago = current_time - COOLDOWN_TIME_IN_SECONDS
            
            otp_records = UserOTP.query.filter(
                UserOTP.user_id == user.id,
                UserOTP.otp_timestamp >= thirty_minutes_ago
            ).order_by(UserOTP.otp_timestamp).all()

            if len(otp_records) >= MAX_NO_OF_OTPS_BEFORE_COOLDOWN_PERIOD:
                next_allowed_time = otp_records[0].otp_timestamp + COOLDOWN_TIME_IN_SECONDS 
                next_allowed_time_str = TimeUtils.get_datetime_from_epoch(next_allowed_time, TimeUtils.DATE_TIME_FORMAT_UI)
                raise MaxResendOTPLimitReached(f"You have reached the maximum limit of {MAX_NO_OF_OTPS_BEFORE_COOLDOWN_PERIOD} OTP requests within {COOLDOWN_TIME_IN_SECONDS//60} minutes. You can request a new OTP after {next_allowed_time_str}.")

            if otp_records and (current_time - otp_records[-1].otp_timestamp) < INTERVAL_BETWEEN_TWO_OTP_GENERATION:
                next_allowed_time = INTERVAL_BETWEEN_TWO_OTP_GENERATION - (current_time - otp_records[-1].otp_timestamp)
                raise OTPTimeoutException(f"You must wait {next_allowed_time} seconds before resending OTP.")
            
            # Generate the otp
            hashed_otp = OTPUtils.get_otp_object(user)
                        
            otp = UserOTP(user_id=user.id, hashed_otp=hashed_otp, otp_timestamp=TimeUtils.get_epoch())
            otp.save(commit=True)
                
            response.message = "The OTP is sent on registered email address"
        except (AccountLockedException, InvalidOTPSecretKeyException, MaxResendOTPLimitReached, OTPTimeoutException) as e:
            print(e)
            response.errors['otp'] = e
            response.success = False
        except Exception as e:
            print(f"An exception occured while resending OTP {str(e)}")
            response.message = "An internal error occured"
            response.success = False
        return response
        
    @staticmethod
    def process_logout() -> None:
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
                raise UserNotFoundException("The entered email id or password may be incorrect")
            
            token_serializer = TokenSerializer('amogh')
            verify_token: Union[str, bytes] = token_serializer.generate_token(email)
            password_reset_url: str = get_external_url('auth.reset_password_api',{"token":verify_token})
            print("Password reset link", password_reset_url)
            
            response.message = "The password reset link has been sent successfully on registered email address"
            
        except UserNotFoundException as e:
            print(f"The entered email id or password may be incorrect")
            response.errors['email'] = e
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
                user.status = UserStatus.CREATED
                user = Utils.reset_incorrect_password_attempts(user)
                user = Utils.reset_incorrect_otp_attempts(user)
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