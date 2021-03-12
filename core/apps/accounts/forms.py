from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from allauth.account import app_settings
from allauth.account.forms import SignupForm


class CustomSignupForm(SignupForm):

    first_name = forms.CharField(
        max_length=30,
        label=_("first name").capitalize(),
        widget=forms.TextInput(attrs={"placeholder": _("first name").capitalize()}),
    )

    last_name = forms.CharField(
        max_length=150,
        label=_("last name").capitalize(),
        widget=forms.TextInput(attrs={"placeholder": _("last name").capitalize()}),
    )

    username = forms.CharField(
        label=_("Username"),
        min_length=app_settings.USERNAME_MIN_LENGTH,
        widget=forms.TextInput(
            attrs={"placeholder": _("Username"), "autocomplete": "username"}
        ),
        help_text=_("Required. 20 characters or fewer. Letters, digits and _ only."),
    )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "type": "email",
                "placeholder": _("E-mail address"),
                "autocomplete": "email",
            }
        )
    )

    field_order = [
        "first_name",
        "last_name",
        "username",
        "email",
        "email2",  # ignored when not present
        "password1",
        "password2",  # ignored when not present
    ]

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user
