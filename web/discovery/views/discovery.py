from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from discovery.models import Discovery


class ListView(LoginRequiredMixin, generic.edit.CreateView, generic.list.ListView):
    template_name = 'discovery/discovery/index.html'
    model = Discovery
    fields = ['ip_address', 'netmask']

    def get_success_url(self) -> str:
        return reverse('discovery:discovery-details', args=[str(self.object.pk)])

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Discovery
    fields = ['ip_address', 'netmask']

    def get_success_url(self) -> str:
        return reverse('discovery:discovery-details', args=[str(self.object.pk)])


class DetailView(LoginRequiredMixin, generic.detail.DetailView):
    template_name = 'discovery/discovery/detail.html'
    model = Discovery
