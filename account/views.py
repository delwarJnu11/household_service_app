from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.views.generic import FormView,View,DetailView
from django.contrib.auth.views import LoginView,PasswordChangeView
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from account.forms import UserRegistrationForm,UserUpdateForm,AdminForm,DepositForm
from account.models import UserAccount
from service.views import send_email

# Create your views here.
class UserRegistrationView(FormView):
    template_name = 'account/form.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')
        
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'user registered successfully done')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'There was an server error try again later!!')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Register'
        return context
    
class UserLoginView(LoginView):
    template_name = 'account/form.html'
    form_class = AuthenticationForm

    def form_invalid(self, form):
        messages.error(self.request, 'please provide valid user credentials.')
        return super().form_invalid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'user logged in successful')
        return reverse_lazy('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Login"
        return context
    
class UserLogoutView(View):
    def get(self,request):
        if request.user.is_authenticated:
            logout(request)
            messages.success(self.request, 'user logged out successful.')
            return redirect('account:login')

class UserProfileView(LoginRequiredMixin,DetailView):
    template_name = 'account/profile.html'
    model = UserAccount
    context_object_name = 'profile'


class UserUpdateView(LoginRequiredMixin,FormView):
    template_name = 'account/form.html'
    form_class = UserUpdateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form, 'title': 'Update Profile'})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully done')
            return redirect('account:profile', pk=request.user.id) 
        return render(request, self.template_name, {'form': form, 'title': 'Update Profile'})

class UserChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'account/form.html'
    form_class = PasswordChangeForm

    def get_success_url(self):
        return reverse_lazy('account:profile', kwargs={'pk': self.request.user.id})

    def form_valid(self, form):
        send_email(self.request.user, 'password_change', 'You have been changed your password confirmation message', 'service/email.html')
        messages.success(self.request, 'Password changed successfully done')
        return super().form_valid(form)

@login_required
def make_admin(request):
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = UserAccount.objects.filter(email=email).first()
            if user:
                user.is_admin = True
                user.is_staff = True
                user.save()
                send_email(user, 'admin', 'You have been made admin confirmation message', 'service/email.html')
                messages.success(request, 'Admin made successfull')
                return render(request, 'account/make_admin.html', {'user': user})
    else:
        form = AdminForm()

    return render(request, 'account/make_admin.html', {'form': form})  

@login_required
def deposit(request):
    if(request.method == 'POST'):
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user = UserAccount.objects.get(email=request.user.email)
            print(user)
            if(user):
                user.balance += amount
                user.save()
                messages.success(request, f'You have deposited {amount}tk successfully done.')
                send_email(user, 'deposit', 'You have been Deposited in your Housebrush account', 'service/email.html')
                return redirect('home')
    else:
        form = DepositForm() 
    return render(request, 'account/deposit.html', {'form': form})