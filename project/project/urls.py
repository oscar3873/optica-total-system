from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

#path("", include("applicacions.nombre_app.urls")),

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("applications.core.urls")),
    path("users/", include("applications.users.urls")),
    path("dashboard/", include("applications.dashboard.urls")),
    path("employees/", include("applications.employes.urls")),
    path("customers/", include("applications.clients.urls")),
    path("branches/", include("applications.branches.urls")),
    path("notes/", include("applications.notes.urls")),
    path("products/", include("applications.products.urls")),
    path("suppliers/", include("applications.suppliers.urls")),
    path("cashregister/", include("applications.cashregister.urls")),
    path("notifications/", include("applications.notifications.urls")),
    path("sales/", include("applications.sales.urls")),    
    path("promotions/", include("applications.promotions.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
