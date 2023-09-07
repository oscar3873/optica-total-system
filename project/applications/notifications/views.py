from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import NotificationsForm
from .models import Notifications
from applications.notes.consumers import send_notifications
# Create your views here.

class NotificationsCreateView(LoginRequiredMixin, CreateView):
    model = Notifications
    form_class = NotificationsForm
    template_name = 'notifications/noti_form.html'
    success_url = reverse_lazy('notifications_app:list')

    def form_valid(self, form):
        notification = form.save(commit=False)
        notification.user_made = self.request.user
        notification.save()
        send_notifications(f"{notification.user_made}: Nuevo {notification.content_object._meta.verbose_name}: {notification.details}")

        return super().form_valid(form)


class NotificationsListView(LoginRequiredMixin, ListView):
    model = Notifications
    template_name = 'notifications/noti_list.html'
    
    
class DynamicDetail(LoginRequiredMixin, View):
    def get(self, request, model_name, pk):
        content_type = ContentType.objects.get(model=model_name)
        model_class = content_type.model_class()
        obj = model_class.objects.get(pk=pk)
        return redirect(obj.objects.get_absolute_url())
    

class LoadNotificationsView(View): # NOTIFICACIONES SOLO SON VISIBLES PARA LOS ADMINS
    def get(self, request, *args, **kwargs):
        notifications = list(Notifications.objects.all().order_by('-created_at')[:5].values())
        return JsonResponse({'notifications': notifications}, safe=False)
    

