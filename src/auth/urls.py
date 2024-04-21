from auth import auth
from auth.views import (
    AuthLoginView,
    AuthLogOutView,
    AuthProfileView,
    AuthProfileSettingsView,
    AuthSignUpView,
)


routes = [
    (
        (auth),
            ('/login', 'login_api', AuthLoginView),
            ('/logout', 'logout_api', AuthLogOutView),
            ('/profile', 'profile_api', AuthProfileView),
            ('/profile-settings', 'profile_settings_api', AuthProfileSettingsView),
            ('/signup', 'signup_api', AuthSignUpView),
    )
]