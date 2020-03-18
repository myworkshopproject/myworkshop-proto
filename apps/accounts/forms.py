from allauth.account.forms import LoginForm, SignupForm
from django import forms
from django.utils.translation import gettext, gettext_lazy as _


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label=_("first name").capitalize())
    last_name = forms.CharField(max_length=150, label=_("last name").capitalize())

    def signup(self, request, user):
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user


class CustomLoginForm(LoginForm):
    def login(self, *args, **kwargs):
        return super(CustomLoginForm, self).login(*args, **kwargs)
