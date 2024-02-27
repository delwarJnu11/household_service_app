from django import forms 
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from . models import UserAccount,Admin
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = UserAccount
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'address', 'image']

class UserUpdateForm(UserChangeForm):
    password = None
    class Meta:
        model = UserAccount
        fields = ['username', 'first_name', 'last_name', 'email','address', 'image']

class AdminForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = Admin
        fields = ['email', 'is_admin']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return email
    
class DepositForm(forms.Form):
    amount = forms.DecimalField(max_digits=12)

    