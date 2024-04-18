from auth import auth
from auth.views import (
    AuthLoginView,
    AuthLogOutView,
    AuthSignUpView,
)


routes = [
    (
        (auth),
            ('/login', 'login_api', AuthLoginView),
            ('/logout', 'logout_api', AuthLogOutView),
            ('/signup', 'signup_api', AuthSignUpView),
    )
]