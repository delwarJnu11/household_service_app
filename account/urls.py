from django.urls import path
from account.views import UserRegistrationView,UserLoginView,UserLogoutView,UserUpdateView,make_admin

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/update_profile/', UserUpdateView.as_view(), name='profile'),
    path('make_admin/', make_admin, name='admin'),
]
