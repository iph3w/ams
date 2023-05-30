from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from discovery.models import Scanner


class ListView(LoginRequiredMixin, generic.edit.CreateView, generic.list.ListView):
    template_name = 'discovery/scanner/index.html'
    model = Scanner
    fields = ['ip_address', 'netmask', 'tcp_ports', 'udp_ports']

    def get_success_url(self) -> str:
        return reverse('discovery:scanner-details', args=[str(self.object.pk)])

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Scanner
    fields = ['ip_address', 'netmask', 'tcp_ports', 'udp_ports']

    def get_success_url(self) -> str:
        return reverse('discovery:scanner-details', args=[str(self.object.pk)])


class DetailView(LoginRequiredMixin, generic.detail.DetailView):
    template_name = 'discovery/scanner/detail.html'
    model = Scanner
