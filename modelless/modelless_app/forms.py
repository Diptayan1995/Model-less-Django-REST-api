from django import forms
from django.core.exceptions import ValidationError

class userRegistration(forms.Form):
    user_name = forms.CharField(label='User name', max_length=100)
    password1 = forms.CharField(label='Password', max_length=100)
    password2 = forms.CharField(label='Confirm Password', max_length=100)
    email = forms.CharField(label='Email id', max_length=100)

    '''def clean_user_name(self):
        if self.cleaned_data['user_name'] exists:
            raise ValidationError('User Name exists')

        return user_name'''
    def clean_password2(self):
        if self.cleaned_data['password1']!=self.cleaned_data['password2']:
            raise ValidationError('Passwords does not match')
        return self.cleaned_data['password2']

class userLogin(forms.Form):
    user_name = forms.CharField(label='User name', max_length=100)
    password = forms.CharField(label='Password', max_length=100)



