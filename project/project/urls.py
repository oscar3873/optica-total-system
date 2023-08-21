"""
URL configuration for project project.

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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

#path("", include("applicacions.nombre_app.urls")),

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("applications.users.urls")),
    path("home/", include("applications.core.urls")),
    path("staff/", include("applications.employes.urls")),
    path("customers/", include("applications.clients.urls")),
    path("branch/", include("applications.branches.urls")),
    path("notes/", include("applications.notes.urls")),
    path("items/", include("applications.products.urls")),
    path("suppliers/", include("applications.suppliers.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)