from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class HomePageView(LoginRequiredMixin , TemplateView):
    template_name = "core/home_page.html"

class CustomUserPassesTestMixin(UserPassesTestMixin):
    def test_func(self):
        """
        Para la verificacion de Administrador
        """
        return self.request.user.is_staff

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        else:
            context = {}
            return render(self.request, 'users/denied_permission.html', context)
