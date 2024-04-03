from auth import auth
from auth.views import (
    AuthLoginView,
    AuthSignUpView,
)


routes = [
    (
        (auth),
            ('/login', 'login_api', AuthLoginView),
            ('/signup', 'signup_api', AuthSignUpView),
    )
]