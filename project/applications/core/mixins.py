from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render


class CustomUserPassesTestMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Clase mixin para requerir autenticacion del usuario administrador
    """
    def test_func(self):
        """
        Para la verificacion de Administrador
        """
        return self.request.user.is_staff

    def handle_no_permission(self):
        """
        Renderiza un template con el acceso denegado a quien quiera acceder a una pestaña sin permiso
        """
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        else:
            context = {}
            return render(self.request, 'users/denied_permission.html', context) 