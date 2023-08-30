from django.shortcuts import render
from django.views.generic import CreateView, ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import NotificationsForm
from .models import Notifications
# Create your views here.

class NotificationsCreateView(LoginRequiredMixin, CreateView):
    model = Notifications
    form_class = NotificationsForm
    template_name = 'notifications/noti_form.html'