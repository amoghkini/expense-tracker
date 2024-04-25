from auth import auth
from auth.views import (
    AuthLoginView,
    AuthLogOutView,
    AuthProfileView,
    AuthProfileSecurity,
    AuthProfileSettingsView,
    AuthProfileNotificationsSettings,
    AuthProfileResetPassword,
    AuthProfileResetPasswordConfirmation,
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
            ('/reset-password', 'reset_password_api', AuthProfileResetPassword),
            ('/reset-password-confirmation', 'reset_password_confirmation_api', AuthProfileResetPasswordConfirmation),
            ('/signup', 'signup_api', AuthSignUpView),
    )
]