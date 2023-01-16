from django.urls import path
from .views import UserRegistration, UserLogin, UserProifile, ChangePassword, SendPasswordResetEmail, PasswordResetEmailLink
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('registration/', UserRegistration.as_view(), name='userRegistration'),
    path('login/', UserLogin.as_view(), name='userLogin'),
    path('profile/', UserProifile.as_view(), name='userProfile'),
    path('changepassword/', ChangePassword.as_view(), name='changePassword'),
    path('password-reset-email/', SendPasswordResetEmail.as_view(),
         name='passwordResetEmail'),
    path('password-reset-link/<userid>/<token>', PasswordResetEmailLink.as_view(),
         name='passwordResetLink')
]
