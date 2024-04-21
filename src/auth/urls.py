from auth import auth
from auth.views import (
    AuthLoginView,
    AuthLogOutView,
    AuthProfileView,
    AuthSignUpView,
)


routes = [
    (
        (auth),
            ('/login', 'login_api', AuthLoginView),
            ('/logout', 'logout_api', AuthLogOutView),
            ('/profile', 'profile_api', AuthProfileView),
            ('/signup', 'signup_api', AuthSignUpView),
    )
]