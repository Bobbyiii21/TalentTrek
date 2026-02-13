from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django import forms
from .models import TTUser
class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=31)
    last_name = forms.CharField(max_length=31)

    field_order = ['email', 'first_name', 'last_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = 'Email'
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].label = 'First Name'
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].label = 'Last Name'
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].label = 'Password'
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].label = 'Password Confirmation'
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        for field in ['email', 'first_name', 'last_name', 'password1', 'password2']:
            self.fields[field].help_text = None
\
    class Meta:
        model = TTUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')