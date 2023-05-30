from django.urls import path

from . import views

urlpatterns = [
    path('discovery/', views.DiscoveryListView.as_view(), name='discovery-index'),
    path('discovery/create/', views.DiscoveryCreateView.as_view(), name='discovery-create'),
    path('discovery/<pk>', views.DiscoveryDetailView.as_view(), name='discovery-details'),
    path('scanner/', views.ScannerListView.as_view(), name='scanner-index'),
    path('scanner/create/', views.ScannerCreateView.as_view(), name='scanner-create'),
    path('scanner/<pk>', views.ScannerDetailView.as_view(), name='scanner-details'),
]
