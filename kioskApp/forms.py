from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    registration_code = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'registration_code']

    def clean_registration_code(self):
        code = self.cleaned_data.get('registration_code')
        if code != 'HLSITS':
            raise forms.ValidationError('Invalid registration code.')
        return code
