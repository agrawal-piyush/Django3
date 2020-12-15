from django import forms
from django.contrib.auth.models import User
from .models import Search1
class LoginForm(forms.Form):
    username = forms.CharField(max_length=256)
    password=forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    password2=forms.CharField(label="Confirm Pass",widget=forms.PasswordInput)

    class Meta:
        model = User
        fields=('username','first_name','email')

    def clean_password2(self):
        cd= self.cleaned_data
        if cd['password']!=cd['password2']:
            raise forms.ValidationError('Passwords Don\'t Match')
        return cd['password2']

class SearchForm(forms.ModelForm):
    class Meta:
        model=Search1
        fields='__all__'
