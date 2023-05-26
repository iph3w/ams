"""
URL configuration for web_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.urls import path, include


urlpatterns = [
    path('__admin__/', admin.site.urls),
    path('', include(('web_app.apps.core.urls', 'web_app.apps.core'), namespace='core')),
]

admin.site.site_header = _("Assets Management System Administration")
admin.site.site_title = _("Assets Management System")
admin.site.index_title = _("A.M.S")
