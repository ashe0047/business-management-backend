from django.urls import path
from auth_core.views import *

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('users/', GetUserView.as_view(), name='get_user_list'),
    path('remove/<int:pk>', DeleteUserView.as_view(), name='user_remove'),
    path('user/', RetrieveUpdateUserView.as_view(), name='get_or_update_user_detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
