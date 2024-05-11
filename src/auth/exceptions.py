class UserNotFoundException(Exception):
    pass


class IncorrectCredentialsException(Exception):
    pass


class IncorrectOTPException(Exception):
    pass


class OTPTimeoutException(Exception):
    pass