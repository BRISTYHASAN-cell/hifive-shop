
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, initial='buyer')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone', 'address', 'role')
