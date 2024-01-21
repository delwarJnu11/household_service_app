from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import View,DetailView,ListView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from service.models import Service,Cart,Review
from service.forms import ReviewForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

####### email send #######
def send_email(user,email_type,mail_subject,template):
    message = render_to_string(template, {
        'user': user,
        'type': email_type,
    })
    from_email = "HOUSEHOLD <delwarjnu24@gmail.com>"
    send_email = EmailMultiAlternatives(mail_subject, '', to=[user.email], from_email=from_email, reply_to=[from_email])
    send_email.attach_alternative(message, 'text/html')
    send_email.send()

# Create your views here.
class ServiceDetailsView(LoginRequiredMixin,DetailView):
    template_name = 'service/service_details.html'
    context_object_name = 'service'
    model = Service
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = self.get_object()
        reviews = service.reviews.all()
        context['reviews'] = reviews
        context['form'] = ReviewForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        service = self.object
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.service = service
            review.save()
            messages.success(request, 'Review added successfully!')
            return redirect('details', id=service.id)

        return self.render_to_response(self.get_context_data(form=form))
    
@login_required
def add_to_cart(request, id):
    service = get_object_or_404(Service, id=id)
    user = request.user
    if user:
        cart, created = Cart.objects.get_or_create(service = service, customer=user, is_order_confirm=False)

    if not created:
        messages.warning(request, 'Service is already in the Cart')
    else:
        cart.save()
        send_email(user, 'add_to_cart', 'You ordered a service', 'service/email.html')
        messages.success(request, 'Service added in the Cart')

    return redirect('cart')

class Cartview(LoginRequiredMixin, ListView):
    model = Cart
    template_name = 'service/cart.html'
    context_object_name= 'items'

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Cart.objects.filter(customer = user_id)
        return queryset
    
class CartAllItemsView(LoginRequiredMixin, ListView):
    model = Cart
    template_name = 'service/admin_cart.html'
    context_object_name= 'items'

class CancelServiceView(LoginRequiredMixin,DeleteView):
    model = Cart
    template_name = 'service/cancel.html'
    success_url = reverse_lazy('cart')

    def form_valid(self, form):
        messages.success(self.request, 'Your service deleted successfully done!!!')
        return super().form_valid(form)
    
class AdminCancelServiceView(LoginRequiredMixin,DeleteView):
    model = Cart
    template_name = 'service/cancel.html'
    success_url = reverse_lazy('cart_items')

    def form_valid(self, form):
        messages.success(self.request, 'Your service deleted successfully done!!!')
        return super().form_valid(form)
    
def confirm_oder(request, id):
    cart = get_object_or_404(Cart, id=id)
    cart.is_order_confirm = True
    cart.save()
    send_email(request.user, 'confirm', 'You order confirmed message', 'service/email.html')
    messages.success(request, 'Order Confirm successfull')
    return redirect('cart_items')
