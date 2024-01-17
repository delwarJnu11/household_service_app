from django import forms 
from service.models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['customer_name', 'email', 'text', 'rating']