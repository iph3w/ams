from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListView.as_view(), name='index'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('<pk>', views.DetailView.as_view(), name='details'),
]
