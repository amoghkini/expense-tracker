from auth import auth
from auth.views import (
    AuthLoginView,
    AuthLogOutView,
    AuthProfileView,
    AuthProfileSecurity,
    AuthProfileSettingsView,
    AuthProfileNotificationsSettings,
    AuthProfileForgotPasswordRequest,
    AuthProfileForgotPasswordConfirmation,
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
            ('/forgot-password-request', 'forgot_password_request_api', AuthProfileForgotPasswordRequest),
            ('/forgot-password-confirmation', 'forgot_password_confirmation_api', AuthProfileForgotPasswordConfirmation),
            ('/signup', 'signup_api', AuthSignUpView),
    )
]