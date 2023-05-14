from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as _LoginView


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'


class LoginView(_LoginView):
    template_name = 'login.html'
