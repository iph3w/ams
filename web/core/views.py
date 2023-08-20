from django.apps import apps
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as _LoginView
from django.views import generic
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _


class GenericView(LoginRequiredMixin):
    def get_menu(self):
        menu = {}
        for app, info in settings.AMS_MENU.items():
            if app in settings.INSTALLED_APPS and self.request.user.has_module_perms(app):
                menu[app] = {
                    'title': apps.get_app_config(app).verbose_name,
                    'icon': info['icon'],
                    'menu_items': {}
                }
                for model in info['models']:
                    if self.request.user.has_perm(f'{app}.view_{model}'):
                        verbose_name_plural = ''
                        for m in apps.get_app_config(app).get_models():
                            if m._meta.model_name == model:
                                verbose_name_plural = m._meta.verbose_name_plural
                                break
                        menu[app]['menu_items'].update({
                            model: {
                                'title': verbose_name_plural,
                                'link': f'{app}:{model}-index'
                            }
                        })
        return menu


class GenericListView(GenericView, generic.edit.CreateView, generic.list.ListView):
    paginate_by = 20
    modal_template = ''

    def get_modal_template(self):
        return self.modal_template

    def get_context_data(self, **kwargs):
        if "title" not in kwargs:
            kwargs["title"] = self.model._meta.verbose_name
        kwargs["model_name"] = self.model._meta.model_name
        kwargs["app_name"] = self.model._meta.app_label
        kwargs['modal_template'] = self.get_modal_template()
        kwargs['menu'] = self.get_menu()
        return super(GenericListView, self).get_context_data(**kwargs)


class GenericDetailView(GenericView, generic.detail.DetailView):
    def get_context_data(self, **kwargs):
        if "title" not in kwargs:
            kwargs["title"] = self.model._meta.verbose_name
        kwargs["model_name"] = self.model._meta.model_name
        kwargs["app_name"] = self.model._meta.app_label
        kwargs['menu'] = self.get_menu()
        return super(GenericDetailView, self).get_context_data(**kwargs)


class IndexView(GenericView, TemplateView):
    template_name = '../templates/index.html'

    def get_context_data(self, **kwargs):
        kwargs["title"] = _("Dashboard")
        kwargs['menu'] = self.get_menu()
        return super(IndexView, self).get_context_data(**kwargs)


class LoginView(_LoginView):
    template_name = '../templates/login.html'

    def get_context_data(self, **kwargs):
        kwargs["title"] = _("Login")
        return super(LoginView, self).get_context_data(**kwargs)
