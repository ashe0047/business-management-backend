from django.urls import path
from auth_core.views import *

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('users/', GetUserView.as_view(), name='get_user_list'),
    path('user/<int:pk>/', DeleteUserView.as_view(), name='user_remove'),
    path('user/', UserView.as_view(), name='get_or_update_user_detail'),
    path('passwordreset/', PasswordResetView.as_view(), name='password_reset_request'),
    path('reset/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
