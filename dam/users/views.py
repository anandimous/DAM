from django.contrib.auth.views import LoginView as BaseLogInView, LogoutView as BaseLogOutView

from .forms import AuthenticationForm


class FormErrorsContextMixin:
    def get_context_data(self, **kwargs):
        form = kwargs.get('form')
        form_errors = []
        if form is not None:
            for error_list in form.errors.as_data().values():
                for error in error_list:
                    form_errors.extend(error.messages)
        form_errors_str = ' '.join(form_errors)
        return super().get_context_data(**kwargs, form_errors=form_errors_str)


class LogInView(FormErrorsContextMixin, BaseLogInView):
    template_name = 'users/log_in.html'
    form_class = AuthenticationForm


class LogOutView(BaseLogOutView):
    next_page = 'inventory:index'
