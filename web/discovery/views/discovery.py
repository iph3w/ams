from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from discovery.models import Discovery


class ListView(LoginRequiredMixin, generic.edit.CreateView, generic.list.ListView):
    template_name = 'discovery/discovery/index.html'
    model = Discovery
    fields = ['ip_address', 'netmask']

    def get_queryset(self):
        queryset = super(ListView, self).get_queryset()
        if self.request.user.is_superuser is True:
            return queryset.filter(start_automatically=True)
        return queryset.filter(
            start_automatically=True,
            created_by_id=self.request.user.pk
        )

    def get_success_url(self) -> str:
        return reverse('discovery:discovery-details', args=[str(self.object.pk)])

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.start_automatically = True
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        if "title" not in kwargs:
            kwargs["title"] = self.model._meta.verbose_name
        kwargs['modal_template'] = 'discovery/discovery/add.html'
        return super(ListView, self).get_context_data(**kwargs)


class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Discovery
    fields = ['ip_address', 'netmask']

    def get_success_url(self) -> str:
        return reverse('discovery:discovery-details', args=[str(self.object.pk)])


class DetailView(LoginRequiredMixin, generic.detail.DetailView):
    template_name = 'discovery/discovery/detail.html'
    model = Discovery

    def get_context_data(self, **kwargs):
        if "title" not in kwargs:
            kwargs["title"] = self.model._meta.verbose_name
        return super(DetailView, self).get_context_data(**kwargs)

    def get_queryset(self):
        if self.request.user.is_superuser is True:
            return Discovery.objects.filter(start_automatically=True)
        return Discovery.objects.filter(
            created_by_id=self.request.user.pk,
            start_automatically=True
        )
