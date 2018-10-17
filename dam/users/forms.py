from django import forms
from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm


class AuthenticationForm(BaseAuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput({'class': 'validate'}),
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput({'class': 'validate'}),
    )

    def add_prefix(self, field_name):
        # Change 'username' to 'email' to help browsers to provide
        # appropriate auto-completion based on the field name.
        if field_name == 'username':
            field_name = 'email'
        return super().add_prefix(field_name)
