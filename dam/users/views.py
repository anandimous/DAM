from django.contrib.auth.views import LoginView as BaseLogInView, LogoutView as BaseLogOutView

from .forms import AuthenticationForm


class LogInView(BaseLogInView):
    template_name = 'users/log_in.html'
    form_class = AuthenticationForm


class LogOutView(BaseLogOutView):
    next_page = 'inventory:index'
