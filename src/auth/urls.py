from auth import auth
from auth.views import (
    AuthManageTwoFactorAuth,
    AuthLoginView,
    AuthLogOutView,
    AuthProfileView,
    AuthProfileSecurity,
    AuthProfileSettingsView,
    AuthProfileNotificationsSettings,
    AuthProfileForgotPasswordRequest,
    AuthProfileForgotPasswordConfirmation,
    AuthProfileResetPassword,
    AuthProfileChangePassword,
    AuthSignUpView,
)


routes = [
    (
        (auth),
            ('/change-password', 'change_password_api', AuthProfileChangePassword),
            ('/manage-2fa', 'manage_2fa_api', AuthManageTwoFactorAuth),
            ('/forgot-password-confirmation', 'forgot_password_confirmation_api', AuthProfileForgotPasswordConfirmation),
            ('/forgot-password-request', 'forgot_password_request_api', AuthProfileForgotPasswordRequest),
            ('/login', 'login_api', AuthLoginView),
            ('/logout', 'logout_api', AuthLogOutView),
            ('/profile', 'profile_api', AuthProfileView),
            ('/profile-settings', 'profile_settings_api', AuthProfileSettingsView),
            ('/profile-security', 'profile_security_api', AuthProfileSecurity),
            ('/profile-notifications-settings', 'profile_notifications_settings_api', AuthProfileNotificationsSettings),
            ('/reset-password', 'reset_password_api', AuthProfileResetPassword),
            ('/signup', 'signup_api', AuthSignUpView),
    )
]