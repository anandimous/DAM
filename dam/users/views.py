from django.contrib.auth.views import LoginView as BaseLogInView

from .forms import AuthenticationForm


class LogInView(BaseLogInView):
    template_name = 'users/log_in.html'
    form_class = AuthenticationForm
