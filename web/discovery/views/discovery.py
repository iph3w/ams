from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from discovery.models import Discovery


class ListView(LoginRequiredMixin, generic.edit.CreateView, generic.list.ListView):
    template_name = 'discovery/discovery/index.html'
    model = Discovery
    fields = ['ip_address', 'netmask']

    def get_queryset(self):
        if self.request.user.is_superuser is True:
            return Discovery.objects.filter(start_automatically=True)
        return Discovery.objects.filter(
            created_by_id=self.request.user.pk,
            start_automatically=True
        )

    def get_success_url(self) -> str:
        return reverse('discovery:discovery-details', args=[str(self.object.pk)])

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.start_automatically = True
        return super().form_valid(form)


class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Discovery
    fields = ['ip_address', 'netmask']

    def get_success_url(self) -> str:
        return reverse('discovery:discovery-details', args=[str(self.object.pk)])


class DetailView(LoginRequiredMixin, generic.detail.DetailView):
    template_name = 'discovery/discovery/detail.html'
    model = Discovery

    def get_queryset(self):
        if self.request.user.is_superuser is True:
            return Discovery.objects.filter(start_automatically=True)
        return Discovery.objects.filter(
            created_by_id=self.request.user.pk,
            start_automatically=True
        )
