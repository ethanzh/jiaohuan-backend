from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'phone_number', 'company', 'location', 'email', 'first_name', 'last_name',
                  'website', 'title', 'address', 'info']


