from django.urls import path
from account.views import UserRegistrationView,UserLoginView,UserLogoutView, UserProfileView, UserUpdateView, UserChangePasswordView, make_admin

app_name = 'account'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('user/<int:pk>/profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update_profile/', UserUpdateView.as_view(), name='edit_profile'),
    path('profile/change_password/', UserChangePasswordView.as_view(), name='change_password'),
    path('make_admin/', make_admin, name='make_admin'),
]
