from auth import auth
from auth.views import (
    AuthLoginView,
    AuthLogOutView,
    AuthProfileView,
    AuthProfileSecurity,
    AuthProfileSettingsView,
    AuthProfileNotificationsSettings,
    AuthSignUpView,
)


routes = [
    (
        (auth),
            ('/login', 'login_api', AuthLoginView),
            ('/logout', 'logout_api', AuthLogOutView),
            ('/profile', 'profile_api', AuthProfileView),
            ('/profile-settings', 'profile_settings_api', AuthProfileSettingsView),
            ('/profile-security', 'profile_security_api', AuthProfileSecurity),
            ('/profile-notifications-settings', 'profile_notifications_settings_api', AuthProfileNotificationsSettings),
            ('/signup', 'signup_api', AuthSignUpView),
    )
]