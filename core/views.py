from django.shortcuts import render
from django.views.generic import ListView
from service.models import Service

# Create your views here.
class HomeView(ListView):
    template_name = 'home.html'
    model = Service
    context_object_name = 'services'
