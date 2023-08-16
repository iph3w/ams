from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as _LoginView
from django.utils.translation import gettext_lazy as _


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = '../templates/index.html'

    def get_context_data(self, **kwargs):
        kwargs["title"] = _("Dashboard")
        return super(IndexView, self).get_context_data(**kwargs)


class LoginView(_LoginView):
    template_name = '../templates/login.html'

    def get_context_data(self, **kwargs):
        kwargs["title"] = _("Login")
        return super(LoginView, self).get_context_data(**kwargs)
