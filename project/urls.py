from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

#path("", include("applicacions.nombre_app.urls")),

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("users/", include("users.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("employees/", include("employes.urls")),
    path("customers/", include("clients.urls")),
    path("branches/", include("branches.urls")),
    path("notes/", include("notes.urls")),
    path("products/", include("products.urls")),
    path("suppliers/", include("suppliers.urls")),
    path("cashregister/", include("cashregister.urls")),
    path("notifications/", include("notifications.urls")),
    path("sales/", include("sales.urls")),    
    path("promotions/", include("promotions.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)